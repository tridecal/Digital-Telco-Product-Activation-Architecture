"""
Digital Telco Product Activation Architecture
eSIM Onboarding Orchestrator

Architecture & Reference Implementation
Mohamed Salman

Purpose
-------
Demonstrates a vendor-neutral orchestration pattern for moving a digital
telecom subscription from product order through service/resource readiness
to subscriber activation.

All identifiers and downstream systems are synthetic.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4


# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------

class LifecycleState(str, Enum):
    RECEIVED = "received"
    VALIDATED = "validated"
    SERVICE_ORDER_CREATED = "service-order-created"
    RESOURCE_ORDER_CREATED = "resource-order-created"
    RESOURCES_ALLOCATED = "resources-allocated"
    ACTIVATION_PENDING = "activation-pending"
    ACTIVE = "active"
    FAILED = "failed"


# ---------------------------------------------------------------------------
# Domain Models
# ---------------------------------------------------------------------------

@dataclass
class ProductOrder:
    product_order_id: str
    customer_id: str
    product_offering_id: str
    sim_type: str = "eSIM"


@dataclass
class ServiceOrder:
    service_order_id: str
    product_order_id: str
    state: str = "acknowledged"


@dataclass
class ResourceOrder:
    resource_order_id: str
    service_order_id: str
    requested_resources: List[str] = field(
        default_factory=lambda: [
            "MSISDN",
            "IMSI",
            "eSIM_PROFILE",
        ]
    )


@dataclass
class SubscriberResources:
    subscription_id: str

    msisdn: Optional[str] = None
    imsi: Optional[str] = None

    iccid: Optional[str] = None
    eid: Optional[str] = None

    status: str = "pending"


@dataclass
class ActivationResult:
    activation_id: str
    subscription_id: str
    state: str
    timestamp: str


# ---------------------------------------------------------------------------
# Synthetic Resource Managers
# ---------------------------------------------------------------------------

class MSISDNManager:
    """
    Represents the number-management capability boundary.

    A production implementation could integrate with number inventory,
    reservation and assignment capabilities.
    """

    def reserve(self) -> str:
        return "9665XXXX0001"


class IMSIManager:
    """
    Represents subscriber identity allocation.
    """

    def allocate(self) -> str:
        return "42001XXXXXXXXX"


class ESIMProfileManager:
    """
    Represents the eSIM profile-management boundary.

    No real SM-DP+ or RSP operation is performed.
    """

    def allocate(self) -> Dict[str, str]:

        return {
            "iccid": "89XXXXXXXXXXXXXXXXXX",
            "eid": "89XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        }


# ---------------------------------------------------------------------------
# Event Publisher
# ---------------------------------------------------------------------------

class EventPublisher:

    def publish(
        self,
        event_type: str,
        correlation_id: str,
        payload: Dict,
    ) -> None:

        print(
            f"\nEVENT  : {event_type}"
            f"\nTRACE  : {correlation_id}"
            f"\nPAYLOAD: {payload}"
        )


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

class ESIMOnboardingOrchestrator:

    def __init__(self):

        self.msisdn_manager = MSISDNManager()
        self.imsi_manager = IMSIManager()
        self.esim_manager = ESIMProfileManager()

        self.events = EventPublisher()

        self.state = LifecycleState.RECEIVED

    # ------------------------------------------------------------------
    # Main Flow
    # ------------------------------------------------------------------

    def execute(
        self,
        product_order: ProductOrder,
        correlation_id: Optional[str] = None,
    ) -> ActivationResult:

        correlation_id = correlation_id or str(uuid4())

        self._log(
            correlation_id,
            "Product order received",
        )

        try:

            # -----------------------------------------------------------
            # 1. Validate Product Order
            # -----------------------------------------------------------

            self._validate_product_order(product_order)

            self.state = LifecycleState.VALIDATED

            self.events.publish(
                "ProductOrderValidated",
                correlation_id,
                {
                    "productOrderId":
                        product_order.product_order_id
                },
            )

            # -----------------------------------------------------------
            # 2. Create Service Order
            # -----------------------------------------------------------

            service_order = self._create_service_order(
                product_order
            )

            self.state = LifecycleState.SERVICE_ORDER_CREATED

            self.events.publish(
                "ServiceOrderCreated",
                correlation_id,
                {
                    "serviceOrderId":
                        service_order.service_order_id,
                    "productOrderId":
                        product_order.product_order_id,
                },
            )

            # -----------------------------------------------------------
            # 3. Create Resource Order
            # -----------------------------------------------------------

            resource_order = self._create_resource_order(
                service_order
            )

            self.state = LifecycleState.RESOURCE_ORDER_CREATED

            self.events.publish(
                "ResourceOrderCreated",
                correlation_id,
                {
                    "resourceOrderId":
                        resource_order.resource_order_id,
                    "requestedResources":
                        resource_order.requested_resources,
                },
            )

            # -----------------------------------------------------------
            # 4. Create Subscriber Context
            # -----------------------------------------------------------

            resources = SubscriberResources(
                subscription_id=(
                    f"SUB-{uuid4().hex[:8].upper()}"
                )
            )

            # -----------------------------------------------------------
            # 5. Reserve MSISDN
            # -----------------------------------------------------------

            resources.msisdn = (
                self.msisdn_manager.reserve()
            )

            self.events.publish(
                "MSISDNReserved",
                correlation_id,
                {
                    "subscriptionId":
                        resources.subscription_id,
                    "msisdn":
                        resources.msisdn,
                },
            )

            # -----------------------------------------------------------
            # 6. Allocate IMSI
            # -----------------------------------------------------------

            resources.imsi = (
                self.imsi_manager.allocate()
            )

            self.events.publish(
                "IMSIAllocated",
                correlation_id,
                {
                    "subscriptionId":
                        resources.subscription_id,
                    "imsi":
                        resources.imsi,
                },
            )

            # -----------------------------------------------------------
            # 7. Allocate eSIM Profile
            # -----------------------------------------------------------

            if product_order.sim_type.lower() == "esim":

                esim_profile = (
                    self.esim_manager.allocate()
                )

                resources.iccid = esim_profile["iccid"]
                resources.eid = esim_profile["eid"]

                self.events.publish(
                    "ESIMProfileAllocated",
                    correlation_id,
                    {
                        "subscriptionId":
                            resources.subscription_id,
                        "iccid":
                            resources.iccid,
                    },
                )

            # -----------------------------------------------------------
            # 8. Resource Readiness Gate
            # -----------------------------------------------------------

            self._validate_resource_readiness(
                product_order,
                resources,
            )

            resources.status = "allocated"

            self.state = LifecycleState.RESOURCES_ALLOCATED

            self.events.publish(
                "SubscriberResourcesReady",
                correlation_id,
                {
                    "subscriptionId":
                        resources.subscription_id,
                    "resourceOrderId":
                        resource_order.resource_order_id,
                },
            )

            # -----------------------------------------------------------
            # 9. Activation
            # -----------------------------------------------------------

            self.state = LifecycleState.ACTIVATION_PENDING

            result = self._activate(resources)

            self.state = LifecycleState.ACTIVE

            self.events.publish(
                "SubscriberActivated",
                correlation_id,
                {
                    "subscriptionId":
                        resources.subscription_id,
                    "activationId":
                        result.activation_id,
                    "state":
                        result.state,
                },
            )

            return result

        except Exception as exc:

            self.state = LifecycleState.FAILED

            self.events.publish(
                "OnboardingFailed",
                correlation_id,
                {
                    "productOrderId":
                        product_order.product_order_id,
                    "reason":
                        str(exc),
                },
            )

            raise

    # ------------------------------------------------------------------
    # Domain Operations
    # ------------------------------------------------------------------

    def _validate_product_order(
        self,
        order: ProductOrder,
    ) -> None:

        if not order.product_order_id:
            raise ValueError(
                "product_order_id is required"
            )

        if not order.customer_id:
            raise ValueError(
                "customer_id is required"
            )

        if not order.product_offering_id:
            raise ValueError(
                "product_offering_id is required"
            )

        if order.sim_type.lower() not in {
            "sim",
            "esim",
        }:
            raise ValueError(
                "sim_type must be SIM or eSIM"
            )

    def _create_service_order(
        self,
        product_order: ProductOrder,
    ) -> ServiceOrder:

        return ServiceOrder(
            service_order_id=(
                f"SO-{uuid4().hex[:8].upper()}"
            ),
            product_order_id=(
                product_order.product_order_id
            ),
        )

    def _create_resource_order(
        self,
        service_order: ServiceOrder,
    ) -> ResourceOrder:

        return ResourceOrder(
            resource_order_id=(
                f"RO-{uuid4().hex[:8].upper()}"
            ),
            service_order_id=(
                service_order.service_order_id
            ),
        )

    def _validate_resource_readiness(
        self,
        order: ProductOrder,
        resources: SubscriberResources,
    ) -> None:

        missing = []

        if not resources.msisdn:
            missing.append("MSISDN")

        if not resources.imsi:
            missing.append("IMSI")

        if order.sim_type.lower() == "esim":

            if not resources.iccid:
                missing.append("ICCID")

            if not resources.eid:
                missing.append("EID")

        if missing:
            raise RuntimeError(
                "Resource readiness failed: "
                + ", ".join(missing)
            )

    def _activate(
        self,
        resources: SubscriberResources,
    ) -> ActivationResult:

        resources.status = "active"

        return ActivationResult(
            activation_id=(
                f"ACT-{uuid4().hex[:8].upper()}"
            ),
            subscription_id=(
                resources.subscription_id
            ),
            state="active",
            timestamp=(
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),
        )

    # ------------------------------------------------------------------
    # Observability
    # ------------------------------------------------------------------

    def _log(
        self,
        correlation_id: str,
        message: str,
    ) -> None:

        print(
            f"[{datetime.now(timezone.utc).isoformat()}]"
            f" [{correlation_id}] {message}"
        )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    order = ProductOrder(
        product_order_id="PO-DEMO-001",
        customer_id="CUSTOMER-DEMO-001",
        product_offering_id="DIGITAL-PLAN-001",
        sim_type="eSIM",
    )

    orchestrator = ESIMOnboardingOrchestrator()

    activation = orchestrator.execute(order)

    print("\n----------------------------------------")
    print("DIGITAL SUBSCRIBER ACTIVATION COMPLETE")
    print("----------------------------------------")
    print(
        f"Subscription : "
        f"{activation.subscription_id}"
    )
    print(
        f"Activation   : "
        f"{activation.activation_id}"
    )
    print(
        f"State        : "
        f"{activation.state}"
    )
