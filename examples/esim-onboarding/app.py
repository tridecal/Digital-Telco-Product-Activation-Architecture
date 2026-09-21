"""
Digital Telco Product Activation Architecture
Executable eSIM Onboarding Reference Implementation

Author: Mohamed Salman

This implementation is an architecture demonstrator.
All subscriber identifiers are synthetic.
"""

from datetime import datetime, timezone
from typing import Dict, Literal, Optional
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException, Response, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="Subscriber Resource Management API",
    description=(
        "Vendor-neutral reference implementation for subscriber resource "
        "orchestration across MSISDN, IMSI and eSIM activation."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class CreateSubscriberRequest(BaseModel):
    subscriptionId: str = Field(examples=["SUB-100001"])
    productOrderId: Optional[str] = Field(
        default=None,
        examples=["PO-100001"],
    )
    serviceOrderId: str = Field(examples=["SO-100001"])
    simType: Literal["SIM", "eSIM"] = "eSIM"
    numberSelectionMode: Literal[
        "automatic",
        "customer-selected",
    ] = "automatic"


class MSISDNRequest(BaseModel):
    selectionMode: Literal[
        "automatic",
        "customer-selected",
    ] = "automatic"

    requestedNumber: Optional[str] = None


class ESIMProfileRequest(BaseModel):
    profileType: Literal[
        "consumer",
        "enterprise",
    ] = "consumer"


class Resource(BaseModel):
    resourceId: str
    value: Optional[str] = None
    status: str


class ESIMProfile(BaseModel):
    resourceId: str
    iccid: str
    eid: str
    status: str


class SubscriberContext(BaseModel):
    subscriptionId: str
    productOrderId: Optional[str]
    serviceOrderId: str

    resourceOrderId: Optional[str] = None

    simType: str
    numberSelectionMode: str

    status: str = "created"

    msisdn: Optional[Resource] = None
    imsi: Optional[Resource] = None
    esimProfile: Optional[ESIMProfile] = None

    correlationId: str
    createdAt: str


class ActivationResponse(BaseModel):
    activationId: str
    subscriptionId: str
    status: str
    correlationId: str


# ---------------------------------------------------------------------------
# Demo State
# ---------------------------------------------------------------------------

subscriber_store: Dict[str, SubscriberContext] = {}

idempotency_store: Dict[str, object] = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_event(
    correlation_id: str,
    event: str,
    subscription_id: Optional[str] = None,
) -> None:

    context = (
        f" subscription={subscription_id}"
        if subscription_id
        else ""
    )

    print(
        f"[{utc_now()}] "
        f"[correlation={correlation_id}] "
        f"{event}{context}"
    )


def require_subscriber(subscription_id: str) -> SubscriberContext:

    subscriber = subscriber_store.get(subscription_id)

    if subscriber is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscriber resource context not found",
        )

    return subscriber


def idempotent_result(key: str):

    return idempotency_store.get(key)


def store_idempotent_result(key: str, result):

    idempotency_store[key] = result


# ---------------------------------------------------------------------------
# Platform
# ---------------------------------------------------------------------------

@app.get("/")
def root():

    return {
        "service": "Subscriber Resource Management API",
        "version": "1.0.0",
        "architecture": "Digital Telco Product Activation",
        "documentation": "/docs",
    }


@app.get("/health")
def health():

    return {
        "status": "UP",
        "timestamp": utc_now(),
    }


# ---------------------------------------------------------------------------
# Subscriber Resource Context
# ---------------------------------------------------------------------------

@app.post(
    "/subscriber-resources",
    response_model=SubscriberContext,
    status_code=status.HTTP_201_CREATED,
)
def create_subscriber_resources(
    request: CreateSubscriberRequest,
    response: Response,
    x_correlation_id: str = Header(
        ...,
        alias="X-Correlation-ID",
    ),
    idempotency_key: str = Header(
        ...,
        alias="Idempotency-Key",
    ),
):

    previous = idempotent_result(idempotency_key)

    if previous:
        response.status_code = status.HTTP_200_OK

        log_event(
            x_correlation_id,
            "Idempotent subscriber context replay",
            request.subscriptionId,
        )

        return previous

    if request.subscriptionId in subscriber_store:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Subscriber resource context already exists",
        )

    subscriber = SubscriberContext(
        subscriptionId=request.subscriptionId,
        productOrderId=request.productOrderId,
        serviceOrderId=request.serviceOrderId,
        simType=request.simType,
        numberSelectionMode=request.numberSelectionMode,
        correlationId=x_correlation_id,
        createdAt=utc_now(),
    )

    subscriber_store[request.subscriptionId] = subscriber

    store_idempotent_result(
        idempotency_key,
        subscriber,
    )

    log_event(
        x_correlation_id,
        "SubscriberResourceContextCreated",
        request.subscriptionId,
    )

    return subscriber


@app.get(
    "/subscriber-resources/{subscription_id}",
    response_model=SubscriberContext,
)
def get_subscriber_resources(
    subscription_id: str,
    x_correlation_id: str = Header(
        ...,
        alias="X-Correlation-ID",
    ),
):

    subscriber = require_subscriber(subscription_id)

    log_event(
        x_correlation_id,
        "SubscriberResourceContextRetrieved",
        subscription_id,
    )

    return subscriber


# ---------------------------------------------------------------------------
# MSISDN
# ---------------------------------------------------------------------------

@app.post(
    "/subscriber-resources/{subscription_id}/msisdn",
    response_model=Resource,
)
def reserve_msisdn(
    subscription_id: str,
    request: MSISDNRequest,
    x_correlation_id: str = Header(
        ...,
        alias="X-Correlation-ID",
    ),
    idempotency_key: str = Header(
        ...,
        alias="Idempotency-Key",
    ),
):

    previous = idempotent_result(idempotency_key)

    if previous:
        return previous

    subscriber = require_subscriber(subscription_id)

    if request.selectionMode == "customer-selected":

        if not request.requestedNumber:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "requestedNumber is required "
                    "for customer-selected mode"
                ),
            )

        number = request.requestedNumber

    else:
        number = "9665XXXX0001"

    resource = Resource(
        resourceId=f"MSISDN-{uuid4().hex[:8].upper()}",
        value=number,
        status="reserved",
    )

    subscriber.msisdn = resource
    subscriber.status = "allocating"

    store_idempotent_result(
        idempotency_key,
        resource,
    )

    log_event(
        x_correlation_id,
        "MSISDNReserved",
        subscription_id,
    )

    return resource


# ---------------------------------------------------------------------------
# IMSI
# ---------------------------------------------------------------------------

@app.post(
    "/subscriber-resources/{subscription_id}/imsi",
    response_model=Resource,
)
def allocate_imsi(
    subscription_id: str,
    x_correlation_id: str = Header(
        ...,
        alias="X-Correlation-ID",
    ),
    idempotency_key: str = Header(
        ...,
        alias="Idempotency-Key",
    ),
):

    previous = idempotent_result(idempotency_key)

    if previous:
        return previous

    subscriber = require_subscriber(subscription_id)

    resource = Resource(
        resourceId=f"IMSI-{uuid4().hex[:8].upper()}",
        value="42001XXXXXXXXX",
        status="allocated",
    )

    subscriber.imsi = resource
    subscriber.status = "allocating"

    store_idempotent_result(
        idempotency_key,
        resource,
    )

    log_event(
        x_correlation_id,
        "IMSIAllocated",
        subscription_id,
    )

    return resource


# ---------------------------------------------------------------------------
# eSIM
# ---------------------------------------------------------------------------

@app.post(
    "/subscriber-resources/{subscription_id}/esim-profile",
    response_model=ESIMProfile,
)
def allocate_esim_profile(
    subscription_id: str,
    request: Optional[ESIMProfileRequest] = None,
    x_correlation_id: str = Header(
        ...,
        alias="X-Correlation-ID",
    ),
    idempotency_key: str = Header(
        ...,
        alias="Idempotency-Key",
    ),
):

    previous = idempotent_result(idempotency_key)

    if previous:
        return previous

    subscriber = require_subscriber(subscription_id)

    if subscriber.simType != "eSIM":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Subscriber is not configured for eSIM",
        )

    profile = ESIMProfile(
        resourceId=f"ESIM-{uuid4().hex[:8].upper()}",
        iccid="89XXXXXXXXXXXXXXXXXX",
        eid="89XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        status="allocated",
    )

    subscriber.esimProfile = profile

    if (
        subscriber.msisdn
        and subscriber.imsi
        and subscriber.esimProfile
    ):
        subscriber.status = "allocated"

    store_idempotent_result(
        idempotency_key,
        profile,
    )

    log_event(
        x_correlation_id,
        "ESIMProfileAllocated",
        subscription_id,
    )

    return profile


# ---------------------------------------------------------------------------
# Activation
# ---------------------------------------------------------------------------

@app.post(
    "/subscriber-resources/{subscription_id}/activate",
    response_model=ActivationResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def activate_subscriber(
    subscription_id: str,
    x_correlation_id: str = Header(
        ...,
        alias="X-Correlation-ID",
    ),
    idempotency_key: str = Header(
        ...,
        alias="Idempotency-Key",
    ),
):

    previous = idempotent_result(idempotency_key)

    if previous:
        return previous

    subscriber = require_subscriber(subscription_id)

    missing = []

    if subscriber.msisdn is None:
        missing.append("MSISDN")

    if subscriber.imsi is None:
        missing.append("IMSI")

    if (
        subscriber.simType == "eSIM"
        and subscriber.esimProfile is None
    ):
        missing.append("eSIM profile")

    if missing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Subscriber resources are incomplete",
                "missingResources": missing,
            },
        )

    subscriber.status = "activating"

    log_event(
        x_correlation_id,
        "ActivationRequested",
        subscription_id,
    )

    #
    # Mock activation boundary.
    #
    # A production implementation would delegate to resource
    # activation / technology adapters here.
    #

    subscriber.status = "active"

    subscriber.msisdn.status = "assigned"
    subscriber.imsi.status = "active"

    if subscriber.esimProfile:
        subscriber.esimProfile.status = "enabled"

    activation = ActivationResponse(
        activationId=f"ACT-{uuid4().hex[:8].upper()}",
        subscriptionId=subscription_id,
        status="active",
        correlationId=x_correlation_id,
    )

    store_idempotent_result(
        idempotency_key,
        activation,
    )

    log_event(
        x_correlation_id,
        "SubscriberActivated",
        subscription_id,
    )

    return activation
