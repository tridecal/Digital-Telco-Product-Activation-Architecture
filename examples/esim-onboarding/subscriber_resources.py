"""
Digital Telco Product Activation Architecture
Subscriber Resource Lifecycle Management

Architecture & Reference Implementation
Mohamed Salman

Purpose
-------
Vendor-neutral reference model for managing subscriber resources such as
MSISDN, IMSI and eSIM profiles across reservation, allocation, assignment,
activation, suspension and release.

All identifiers and integrations are synthetic.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional
from uuid import uuid4


# ---------------------------------------------------------------------------
# Resource States
# ---------------------------------------------------------------------------

class ResourceState(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    ALLOCATED = "allocated"
    ASSIGNED = "assigned"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    RELEASED = "released"


# ---------------------------------------------------------------------------
# Resource Types
# ---------------------------------------------------------------------------

class ResourceType(str, Enum):
    MSISDN = "MSISDN"
    IMSI = "IMSI"
    ESIM_PROFILE = "eSIM_PROFILE"


# ---------------------------------------------------------------------------
# Domain Model
# ---------------------------------------------------------------------------

@dataclass
class SubscriberResource:
    resource_id: str
    resource_type: ResourceType
    value: str

    state: ResourceState = ResourceState.AVAILABLE

    subscription_id: Optional[str] = None
    correlation_id: Optional[str] = None

    created_at: str = field(
        default_factory=lambda:
        datetime.now(timezone.utc).isoformat()
    )

    updated_at: str = field(
        default_factory=lambda:
        datetime.now(timezone.utc).isoformat()
    )


# ---------------------------------------------------------------------------
# Lifecycle Rules
# ---------------------------------------------------------------------------

ALLOWED_TRANSITIONS = {

    ResourceState.AVAILABLE: {
        ResourceState.RESERVED,
    },

    ResourceState.RESERVED: {
        ResourceState.ALLOCATED,
        ResourceState.RELEASED,
    },

    ResourceState.ALLOCATED: {
        ResourceState.ASSIGNED,
        ResourceState.RELEASED,
    },

    ResourceState.ASSIGNED: {
        ResourceState.ACTIVE,
        ResourceState.RELEASED,
    },

    ResourceState.ACTIVE: {
        ResourceState.SUSPENDED,
        ResourceState.RELEASED,
    },

    ResourceState.SUSPENDED: {
        ResourceState.ACTIVE,
        ResourceState.RELEASED,
    },

    ResourceState.RELEASED: set(),
}


# ---------------------------------------------------------------------------
# Lifecycle Manager
# ---------------------------------------------------------------------------

class SubscriberResourceManager:

    def __init__(self):

        self.resources: Dict[
            str,
            SubscriberResource
        ] = {}

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    def create(
        self,
        resource_type: ResourceType,
        value: str,
        correlation_id: Optional[str] = None,
    ) -> SubscriberResource:

        resource = SubscriberResource(
            resource_id=self._generate_id(
                resource_type
            ),
            resource_type=resource_type,
            value=value,
            correlation_id=correlation_id,
        )

        self.resources[
            resource.resource_id
        ] = resource

        self._event(
            resource,
            "ResourceCreated",
        )

        return resource

    # ------------------------------------------------------------------
    # Reserve
    # ------------------------------------------------------------------

    def reserve(
        self,
        resource_id: str,
        subscription_id: str,
    ) -> SubscriberResource:

        resource = self.get(resource_id)

        self._transition(
            resource,
            ResourceState.RESERVED,
        )

        resource.subscription_id = (
            subscription_id
        )

        self._event(
            resource,
            "ResourceReserved",
        )

        return resource

    # ------------------------------------------------------------------
    # Allocate
    # ------------------------------------------------------------------

    def allocate(
        self,
        resource_id: str,
    ) -> SubscriberResource:

        resource = self.get(resource_id)

        self._transition(
            resource,
            ResourceState.ALLOCATED,
        )

        self._event(
            resource,
            "ResourceAllocated",
        )

        return resource

    # ------------------------------------------------------------------
    # Assign
    # ------------------------------------------------------------------

    def assign(
        self,
        resource_id: str,
    ) -> SubscriberResource:

        resource = self.get(resource_id)

        if not resource.subscription_id:
            raise ValueError(
                "Resource must belong to a "
                "subscription before assignment"
            )

        self._transition(
            resource,
            ResourceState.ASSIGNED,
        )

        self._event(
            resource,
            "ResourceAssigned",
        )

        return resource

    # ------------------------------------------------------------------
    # Activate
    # ------------------------------------------------------------------

    def activate(
        self,
        resource_id: str,
    ) -> SubscriberResource:

        resource = self.get(resource_id)

        self._transition(
            resource,
            ResourceState.ACTIVE,
        )

        self._event(
            resource,
            "ResourceActivated",
        )

        return resource

    # ------------------------------------------------------------------
    # Suspend
    # ------------------------------------------------------------------

    def suspend(
        self,
        resource_id: str,
    ) -> SubscriberResource:

        resource = self.get(resource_id)

        self._transition(
            resource,
            ResourceState.SUSPENDED,
        )

        self._event(
            resource,
            "ResourceSuspended",
        )

        return resource

    # ------------------------------------------------------------------
    # Release
    # ------------------------------------------------------------------

    def release(
        self,
        resource_id: str,
    ) -> SubscriberResource:

        resource = self.get(resource_id)

        self._transition(
            resource,
            ResourceState.RELEASED,
        )

        resource.subscription_id = None

        self._event(
            resource,
            "ResourceReleased",
        )

        return resource

    # ------------------------------------------------------------------
    # Retrieve
    # ------------------------------------------------------------------

    def get(
        self,
        resource_id: str,
    ) -> SubscriberResource:

        resource = self.resources.get(
            resource_id
        )

        if resource is None:
            raise KeyError(
                f"Resource not found: "
                f"{resource_id}"
            )

        return resource

    # ------------------------------------------------------------------
    # State Machine
    # ------------------------------------------------------------------

    def _transition(
        self,
        resource: SubscriberResource,
        target: ResourceState,
    ) -> None:

        allowed = ALLOWED_TRANSITIONS.get(
            resource.state,
            set(),
        )

        if target not in allowed:

            raise ValueError(
                "Invalid resource lifecycle "
                f"transition: "
                f"{resource.state.value} "
                f"-> {target.value}"
            )

        previous = resource.state

        resource.state = target

        resource.updated_at = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        print(
            f"LIFECYCLE: "
            f"{resource.resource_id} "
            f"{previous.value} "
            f"-> {target.value}"
        )

    # ------------------------------------------------------------------
    # Identifier Generation
    # ------------------------------------------------------------------

    def _generate_id(
        self,
        resource_type: ResourceType,
    ) -> str:

        prefixes = {
            ResourceType.MSISDN:
                "MSISDN",

            ResourceType.IMSI:
                "IMSI",

            ResourceType.ESIM_PROFILE:
                "ESIM",
        }

        return (
            f"{prefixes[resource_type]}-"
            f"{uuid4().hex[:8].upper()}"
        )

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    def _event(
        self,
        resource: SubscriberResource,
        event_type: str,
    ) -> None:

        print(
            f"EVENT: {event_type} | "
            f"resource={resource.resource_id} | "
            f"type={resource.resource_type.value} | "
            f"state={resource.state.value}"
        )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    manager = SubscriberResourceManager()

    subscription_id = "SUB-DEMO-001"
    correlation_id = str(uuid4())

    msisdn = manager.create(
        ResourceType.MSISDN,
        "9665XXXX0001",
        correlation_id,
    )

    manager.reserve(
        msisdn.resource_id,
        subscription_id,
    )

    manager.allocate(
        msisdn.resource_id
    )

    manager.assign(
        msisdn.resource_id
    )

    manager.activate(
        msisdn.resource_id
    )

    print("\nFinal resource state:")
    print(
        manager.get(
            msisdn.resource_id
        )
    )
