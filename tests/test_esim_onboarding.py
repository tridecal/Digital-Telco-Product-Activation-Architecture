"""
Digital Telco Product Activation Architecture
End-to-End eSIM Onboarding Tests

Architecture & Reference Implementation
Mohamed Salman

Validates the executable subscriber activation journey:

Subscriber Context
    -> MSISDN Reservation
    -> IMSI Allocation
    -> eSIM Profile Allocation
    -> Activation

All identifiers used by the reference implementation are synthetic.
"""

from fastapi.testclient import TestClient

from examples.esim_onboarding.app import (
    app,
    subscriber_store,
    idempotency_store,
)


client = TestClient(app)


# ---------------------------------------------------------------------------
# Test Helpers
# ---------------------------------------------------------------------------

SUBSCRIPTION_ID = "SUB-TEST-001"
CORRELATION_ID = "CORR-TEST-001"


def headers(idempotency_key: str) -> dict:
    return {
        "X-Correlation-ID": CORRELATION_ID,
        "Idempotency-Key": idempotency_key,
    }


def setup_function():
    """
    Reset in-memory demo state before every test.
    """

    subscriber_store.clear()
    idempotency_store.clear()


def create_subscriber():
    return client.post(
        "/subscriber-resources",
        headers=headers("IDEMP-CREATE-001"),
        json={
            "subscriptionId": SUBSCRIPTION_ID,
            "productOrderId": "PO-TEST-001",
            "serviceOrderId": "SO-TEST-001",
            "simType": "eSIM",
            "numberSelectionMode": "automatic",
        },
    )


# ---------------------------------------------------------------------------
# Platform Tests
# ---------------------------------------------------------------------------


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "UP"


# ---------------------------------------------------------------------------
# Subscriber Context
# ---------------------------------------------------------------------------


def test_create_subscriber_context():
    response = create_subscriber()

    assert response.status_code == 201

    body = response.json()

    assert body["subscriptionId"] == SUBSCRIPTION_ID
    assert body["productOrderId"] == "PO-TEST-001"
    assert body["serviceOrderId"] == "SO-TEST-001"
    assert body["simType"] == "eSIM"
    assert body["status"] == "created"
    assert body["correlationId"] == CORRELATION_ID


# ---------------------------------------------------------------------------
# Complete eSIM Onboarding Journey
# ---------------------------------------------------------------------------


def test_complete_esim_onboarding_flow():

    # ---------------------------------------------------------------
    # 1. Create subscriber resource context
    # ---------------------------------------------------------------

    response = create_subscriber()

    assert response.status_code == 201
    assert response.json()["status"] == "created"

    # ---------------------------------------------------------------
    # 2. Reserve MSISDN
    # ---------------------------------------------------------------

    response = client.post(
        f"/subscriber-resources/{SUBSCRIPTION_ID}/msisdn",
        headers=headers("IDEMP-MSISDN-001"),
        json={
            "selectionMode": "automatic"
        },
    )

    assert response.status_code == 200

    msisdn = response.json()

    assert msisdn["resourceId"].startswith("MSISDN-")
    assert msisdn["status"] == "reserved"
    assert msisdn["value"] == "9665XXXX0001"

    # ---------------------------------------------------------------
    # 3. Allocate IMSI
    # ---------------------------------------------------------------

    response = client.post(
        f"/subscriber-resources/{SUBSCRIPTION_ID}/imsi",
        headers=headers("IDEMP-IMSI-001"),
    )

    assert response.status_code == 200

    imsi = response.json()

    assert imsi["resourceId"].startswith("IMSI-")
    assert imsi["status"] == "allocated"
    assert imsi["value"] == "42001XXXXXXXXX"

    # ---------------------------------------------------------------
    # 4. Allocate eSIM Profile
    # ---------------------------------------------------------------

    response = client.post(
        f"/subscriber-resources/{SUBSCRIPTION_ID}/esim-profile",
        headers=headers("IDEMP-ESIM-001"),
        json={
            "profileType": "consumer"
        },
    )

    assert response.status_code == 200

    esim = response.json()

    assert esim["resourceId"].startswith("ESIM-")
    assert esim["status"] == "allocated"
    assert esim["iccid"]
    assert esim["eid"]

    # ---------------------------------------------------------------
    # 5. Validate resource readiness
    # ---------------------------------------------------------------

    response = client.get(
        f"/subscriber-resources/{SUBSCRIPTION_ID}",
        headers={
            "X-Correlation-ID": CORRELATION_ID
        },
    )

    assert response.status_code == 200

    subscriber = response.json()

    assert subscriber["status"] == "allocated"
    assert subscriber["msisdn"] is not None
    assert subscriber["imsi"] is not None
    assert subscriber["esimProfile"] is not None

    # ---------------------------------------------------------------
    # 6. Activate subscriber
    # ---------------------------------------------------------------

    response = client.post(
        f"/subscriber-resources/{SUBSCRIPTION_ID}/activate",
        headers=headers("IDEMP-ACTIVATE-001"),
    )

    assert response.status_code == 202

    activation = response.json()

    assert activation["activationId"].startswith("ACT-")
    assert activation["subscriptionId"] == SUBSCRIPTION_ID
    assert activation["status"] == "active"
    assert activation["correlationId"] == CORRELATION_ID

    # ---------------------------------------------------------------
    # 7. Validate final subscriber state
    # ---------------------------------------------------------------

    response = client.get(
        f"/subscriber-resources/{SUBSCRIPTION_ID}",
        headers={
            "X-Correlation-ID": CORRELATION_ID
        },
    )

    assert response.status_code == 200

    subscriber = response.json()

    assert subscriber["status"] == "active"
    assert subscriber["msisdn"]["status"] == "assigned"
    assert subscriber["imsi"]["status"] == "active"
    assert subscriber["esimProfile"]["status"] == "enabled"


# ---------------------------------------------------------------------------
# Resource Readiness Guard
# ---------------------------------------------------------------------------


def test_activation_rejected_when_resources_missing():

    response = create_subscriber()

    assert response.status_code == 201

    response = client.post(
        f"/subscriber-resources/{SUBSCRIPTION_ID}/activate",
        headers=headers("IDEMP-ACTIVATE-INCOMPLETE"),
    )

    assert response.status_code == 409

    detail = response.json()["detail"]

    assert detail["message"] == "Subscriber resources are incomplete"

    assert "MSISDN" in detail["missingResources"]
    assert "IMSI" in detail["missingResources"]
    assert "eSIM profile" in detail["missingResources"]


# ---------------------------------------------------------------------------
# Idempotency
# ---------------------------------------------------------------------------


def test_subscriber_creation_is_idempotent():

    first = create_subscriber()
    second = create_subscriber()

    assert first.status_code == 201
    assert second.status_code == 200

    assert (
        first.json()["subscriptionId"]
        == second.json()["subscriptionId"]
    )


# ---------------------------------------------------------------------------
# Invalid Number Selection
# ---------------------------------------------------------------------------


def test_customer_selected_number_requires_number():

    create_subscriber()

    response = client.post(
        f"/subscriber-resources/{SUBSCRIPTION_ID}/msisdn",
        headers=headers("IDEMP-MSISDN-INVALID"),
        json={
            "selectionMode": "customer-selected"
        },
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "requestedNumber is required for customer-selected mode"
    )
