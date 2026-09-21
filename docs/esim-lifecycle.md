# SIM & eSIM Subscriber Resource Lifecycle

> **From Digital Order to Active Subscriber Identity**  
> Architecture & Research by **Mohamed Salman**

---

## 1. Purpose

This document defines a vendor-neutral reference architecture for managing **SIM/eSIM-related subscriber resources** across the digital telecom product lifecycle.

It focuses on the relationships between:

**Product → Service → Subscription → MSISDN → IMSI → SIM/eSIM → Activation**

For eSIM, the architecture additionally considers the remote SIM provisioning boundary around the **eUICC and eSIM profile**.

```mermaid
flowchart LR

    PRODUCT["Digital Product"]
    SERVICE["Service"]
    SUB["Subscription"]

    NUMBER["MSISDN"]
    IMSI["IMSI"]

    PROFILE["eSIM Profile"]
    EUICC["eUICC"]

    ACT["Activation"]

    PRODUCT --> SERVICE
    SERVICE --> SUB

    SUB --> NUMBER
    SUB --> IMSI

    IMSI --> PROFILE
    PROFILE --> EUICC

    SUB --> ACT
```

The goal is not to reproduce a vendor-specific provisioning implementation.

The goal is to define clear lifecycle boundaries between **commercial products, subscriber identity resources and network activation**.

---

# 2. Terminology

The architecture distinguishes several identifiers and resources that are sometimes incorrectly treated as interchangeable.

| Concept | Architectural Meaning |
|---|---|
| **SIM** | Subscriber identity module implemented as a removable physical card |
| **eSIM** | Embedded-SIM capability based on an eUICC with remotely managed profiles |
| **eUICC** | Secure element capable of hosting remotely provisioned SIM profiles |
| **EID** | Identifier associated with an eUICC |
| **Profile** | Operator subscription profile installed on an eUICC |
| **ICCID** | Identifier associated with a SIM/profile |
| **IMSI** | Subscriber identity used by the mobile network |
| **MSISDN** | Telephone number associated with a subscriber/service |
| **Subscription** | Logical subscriber-service relationship |
| **SM-DP+** | GSMA remote SIM provisioning function used for profile preparation/delivery in the consumer architecture |

These concepts should remain distinct in the domain model.

---

# 3. Resource Relationship Model

A simplified conceptual model is:

```mermaid
flowchart TB

    CUSTOMER["Customer"]

    PRODUCT["Product"]

    SERVICE["Service"]

    SUB["Subscription"]

    NUMBER["MSISDN"]

    IMSI["IMSI"]

    PROFILE["SIM / eSIM Profile<br/>ICCID"]

    EUICC["eUICC<br/>EID"]

    CUSTOMER --> PRODUCT
    PRODUCT --> SERVICE
    SERVICE --> SUB

    SUB --> NUMBER
    SUB --> IMSI

    IMSI --> PROFILE
    PROFILE --> EUICC
```

The model intentionally separates:

- Commercial product
- Operational service
- Subscription
- Telephone number
- Network subscriber identity
- SIM/profile
- eUICC

This enables each resource to evolve according to its own lifecycle.

---

# 4. Physical SIM vs eSIM

At the commercial level, both may provide the same subscriber service.

Their fulfillment paths differ.

```mermaid
flowchart TB

    ORDER["Subscriber Order"]

    TYPE{"SIM Type"}

    PSIM["Physical SIM"]

    ESIM["eSIM"]

    ICCID1["ICCID"]

    ICCID2["Profile / ICCID"]

    EUICC["eUICC / EID"]

    IMSI1["IMSI"]
    IMSI2["IMSI"]

    ACT1["Activation"]
    ACT2["Activation"]

    ORDER --> TYPE

    TYPE -->|"Physical"| PSIM
    TYPE -->|"Embedded"| ESIM

    PSIM --> ICCID1
    ICCID1 --> IMSI1
    IMSI1 --> ACT1

    ESIM --> ICCID2
    ICCID2 --> IMSI2
    ICCID2 --> EUICC
    IMSI2 --> ACT2
```

The product layer should not need separate commercial implementations for every underlying SIM technology unless the customer proposition itself requires that distinction.

---

# 5. Architecture Domains

```mermaid
flowchart TB

    subgraph EXPERIENCE["Experience"]
        APP["Digital Channel"]
    end

    subgraph PRODUCT["Product"]
        ORDER["Product Order"]
    end

    subgraph SERVICE["Service"]
        SO["Service Orchestration"]
    end

    subgraph SUBSCRIBER["Subscriber Resource"]
        SRM["Subscriber Resource Manager"]
        MSISDN["MSISDN"]
        IMSI["IMSI"]
        SIM["SIM / eSIM"]
    end

    subgraph RSP["eSIM Provisioning Boundary"]
        ESIMADAPTER["eSIM Provisioning Adapter"]
        SMDP["SM-DP+"]
    end

    subgraph NETWORK["Network Activation"]
        ACT["Activation"]
        SUBSCRIBERDB["Subscriber / Policy Platforms"]
    end

    APP --> ORDER
    ORDER --> SO
    SO --> SRM

    SRM --> MSISDN
    SRM --> IMSI
    SRM --> SIM

    SRM --> ESIMADAPTER
    ESIMADAPTER --> SMDP

    SRM --> ACT
    ACT --> SUBSCRIBERDB
```

The **Subscriber Resource Manager** acts as an orchestration boundary.

It does not replace GSMA remote SIM provisioning components.

---

# 6. Subscriber Resource Manager

The Subscriber Resource Manager coordinates the lifecycle of subscriber-related resources.

```mermaid
flowchart LR

    REQUEST["Service Request"]

    SRM["Subscriber Resource Manager"]

    NUMBER["Number Management"]

    SIM["SIM / eSIM Resources"]

    ID["Subscriber Identity"]

    RSP["eSIM Provisioning"]

    ACT["Activation"]

    INV["Resource Inventory"]

    REQUEST --> SRM

    SRM --> NUMBER
    SRM --> SIM
    SRM --> ID
    SRM --> RSP
    SRM --> ACT

    SRM <--> INV
```

Responsibilities may include:

- MSISDN reservation
- SIM/eSIM resource allocation
- ICCID association
- IMSI association
- Subscription-resource relationships
- Resource state management
- Activation coordination
- Replacement workflows
- Release and reconciliation

> `Subscriber Resource Manager` is a project-specific architectural abstraction and is not presented as an official TM Forum component.

---

# 7. eSIM Activation Journey

A simplified digital eSIM onboarding journey:

```mermaid
sequenceDiagram

    autonumber

    actor Customer

    participant App as Digital Channel
    participant Order as Product Order
    participant Service as Service Orchestrator
    participant SRM as Subscriber Resource Manager
    participant Number as Number Management
    participant Inventory as Resource Inventory
    participant RSP as eSIM Provisioning
    participant Activation as Network Activation

    Customer->>App: Select product + eSIM

    App->>Order: Create product order

    Order->>Service: Create service order

    Service->>SRM: Request subscriber resources

    SRM->>Number: Reserve MSISDN
    Number-->>SRM: MSISDN reserved

    SRM->>Inventory: Allocate subscriber identity resources
    Inventory-->>SRM: ICCID / IMSI allocation

    SRM->>RSP: Request eSIM profile fulfillment
    RSP-->>SRM: Profile fulfillment status

    SRM->>Activation: Activate subscription resources
    Activation-->>SRM: Activation successful

    SRM-->>Service: Subscriber ready

    Service-->>Order: Service active

    Order-->>App: Order completed

    App-->>Customer: Service ready
```

The exact RSP interaction is intentionally abstracted because implementation details depend on the selected GSMA architecture, platform and integration model.

---

# 8. eSIM Profile Provisioning Boundary

The remote SIM provisioning domain should remain isolated behind an adapter/interface.

```mermaid
flowchart LR

    SRM["Subscriber Resource Manager"]

    ADAPTER["eSIM Provisioning Adapter"]

    SMDP["SM-DP+"]

    DEVICE["Device / LPA"]

    EUICC["eUICC"]

    PROFILE["Operator Profile"]

    SRM --> ADAPTER

    ADAPTER --> SMDP

    SMDP --> DEVICE

    DEVICE --> EUICC

    EUICC --> PROFILE
```

The architecture deliberately avoids embedding SM-DP+ implementation logic inside Product Order or Service Order.

---

# 9. eSIM Profile Lifecycle

At a conceptual level, an eSIM profile passes through multiple operational states.

```mermaid
stateDiagram-v2

    [*] --> Available

    Available --> Allocated: Allocate profile

    Allocated --> DownloadReady: Prepare fulfillment

    DownloadReady --> Downloaded: Profile downloaded

    Downloaded --> Enabled: Enable

    Enabled --> Disabled: Disable

    Disabled --> Enabled: Re-enable

    Disabled --> Deleted: Delete

    Enabled --> Replaced: Replacement

    Replaced --> Deleted

    Deleted --> [*]
```

> This is a project-level lifecycle abstraction for architecture discussion.  
> Authoritative eSIM profile state definitions and procedures should be taken from the applicable GSMA specifications.

---

# 10. Physical SIM Lifecycle

Physical SIM lifecycle management differs because a physical inventory asset exists.

```mermaid
stateDiagram-v2

    [*] --> Stock

    Stock --> Reserved: Reserve

    Reserved --> Assigned: Assign subscriber

    Reserved --> Stock: Reservation released

    Assigned --> Active: Activate

    Active --> Suspended: Suspend

    Suspended --> Active: Restore

    Active --> Replaced: Replace

    Replaced --> Retired

    Active --> Retired: Terminate

    Retired --> [*]
```

Typical physical SIM concerns include:

- Stock availability
- Distribution
- Reservation
- ICCID tracking
- Assignment
- Activation
- Replacement
- Retirement

---

# 11. MSISDN Lifecycle

MSISDN lifecycle management should remain independent from SIM lifecycle management.

```mermaid
stateDiagram-v2

    [*] --> Available

    Available --> Reserved: Reserve

    Reserved --> Assigned: Assign

    Reserved --> Available: Reservation timeout

    Assigned --> Active: Activate service

    Active --> Suspended: Suspend

    Suspended --> Active: Restore

    Active --> Quarantine: Release

    Quarantine --> Available: Recycling policy

    Quarantine --> Retired: Retire

    Retired --> [*]
```

This separation enables scenarios such as:

- SIM replacement without number change
- eSIM migration while retaining the number
- service suspension without releasing the number
- controlled number recycling

---

# 12. IMSI Lifecycle

```mermaid
stateDiagram-v2

    [*] --> Available

    Available --> Reserved: Reserve

    Reserved --> Assigned: Associate subscription

    Assigned --> Active: Network activation

    Active --> Suspended: Suspend

    Suspended --> Active: Restore

    Active --> Released: Terminate / replace

    Released --> Retired

    Retired --> [*]
```

The precise lifecycle depends on network architecture and operator policies.

The important architectural principle is that **IMSI lifecycle is not assumed to be identical to MSISDN or SIM lifecycle**.

---

# 13. Independent Resource Lifecycles

A subscription can bind resources that evolve independently.

```mermaid
flowchart TB

    SUB["Subscription"]

    MSISDN["MSISDN Lifecycle"]
    IMSI["IMSI Lifecycle"]
    SIM["SIM Lifecycle"]
    PROFILE["eSIM Profile Lifecycle"]

    SUB --> MSISDN
    SUB --> IMSI
    SUB --> SIM
    SUB --> PROFILE
```

This is important because:

```text
SIM change      ≠ MSISDN change

eSIM replacement ≠ Product change

MSISDN suspension ≠ SIM deletion

Product change   ≠ Subscriber identity replacement
```

The orchestration layer must preserve these distinctions.

---

# 14. SIM Replacement

A SIM replacement should preserve the higher-level subscription where appropriate.

```mermaid
sequenceDiagram

    autonumber

    actor Customer

    participant Channel
    participant SRM as Subscriber Resource Manager
    participant Inventory
    participant Activation
    participant Network

    Customer->>Channel: Request SIM replacement

    Channel->>SRM: Replace subscriber credential

    SRM->>Inventory: Allocate replacement SIM/eSIM
    Inventory-->>SRM: New ICCID / identity resources

    SRM->>Activation: Activate replacement

    Activation->>Network: Update subscriber provisioning
    Network-->>Activation: Update complete

    Activation-->>SRM: Replacement active

    SRM->>Inventory: Retire / update previous resource

    SRM-->>Channel: Replacement complete

    Channel-->>Customer: Service restored
```

The customer should not need to repurchase the commercial product simply because the underlying subscriber credential changes.

---

# 15. eSIM Device Migration

Conceptually:

```mermaid
flowchart LR

    OLD["Existing Device"]

    VERIFY["Verify Subscription"]

    NEW["New Device / eUICC"]

    PROFILE["Provision Profile"]

    ENABLE["Enable"]

    RECONCILE["Reconcile Old State"]

    COMPLETE["Migration Complete"]

    OLD --> VERIFY
    VERIFY --> NEW
    NEW --> PROFILE
    PROFILE --> ENABLE
    ENABLE --> RECONCILE
    RECONCILE --> COMPLETE
```

The exact migration mechanism depends on supported device, platform, operator and GSMA procedures.

The architecture therefore models migration as a business workflow while keeping implementation-specific RSP behavior behind the provisioning boundary.

---

# 16. Allocation vs Activation

Resource allocation must remain distinct from operational activation.

```mermaid
flowchart LR

    AVAILABLE["Available"]

    RESERVED["Reserved"]

    ASSIGNED["Assigned"]

    ACTIVATING["Activating"]

    ACTIVE["Active"]

    AVAILABLE --> RESERVED
    RESERVED --> ASSIGNED
    ASSIGNED --> ACTIVATING
    ACTIVATING --> ACTIVE
```

### Allocation answers

> Which resources belong to this subscription?

### Activation answers

> Are those resources operational?

This distinction becomes critical when provisioning fails after resources have already been assigned.

---

# 17. Activation Failure

```mermaid
flowchart TB

    REQUEST["Activation Request"]

    PROVISION["Provision"]

    VERIFY{"Successful?"}

    ACTIVE["Active"]

    FAILED["Activation Failed"]

    RETRY["Retry"]

    RECONCILE["Reconcile"]

    RELEASE["Compensate / Release"]

    REQUEST --> PROVISION
    PROVISION --> VERIFY

    VERIFY -->|"Yes"| ACTIVE
    VERIFY -->|"No"| FAILED

    FAILED --> RETRY
    FAILED --> RECONCILE

    RETRY --> PROVISION

    RECONCILE -->|"Recover"| PROVISION
    RECONCILE -->|"Cannot Recover"| RELEASE
```

A failed activation must not automatically result in uncontrolled allocation of another MSISDN, ICCID or IMSI.

Idempotency and reconciliation are therefore mandatory architectural concerns.

---

# 18. Resource Reservation

Reservation protects scarce resources during long-running order workflows.

```mermaid
sequenceDiagram

    participant Order
    participant SRM as Subscriber Resource Manager
    participant Pool as Resource Pool

    Order->>SRM: Request resources

    SRM->>Pool: Find available resource

    Pool-->>SRM: Candidate resource

    SRM->>Pool: Reserve(resource, TTL)

    Pool-->>SRM: Reservation confirmed

    alt Order succeeds
        SRM->>Pool: Assign resource
    else Order fails or expires
        SRM->>Pool: Release reservation
    end
```

Reservations should have controlled expiration policies where appropriate.

---

# 19. Resource Exhaustion

The architecture should explicitly account for resource-pool exhaustion.

```mermaid
flowchart TB

    REQUEST["Resource Request"]

    CHECK{"Available?"}

    RESERVE["Reserve"]

    EXHAUSTED["Pool Exhausted"]

    POLICY["Fallback / Business Policy"]

    ALERT["Operational Alert"]

    REQUEST --> CHECK

    CHECK -->|"Yes"| RESERVE

    CHECK -->|"No"| EXHAUSTED

    EXHAUSTED --> POLICY
    EXHAUSTED --> ALERT
```

Examples include:

- MSISDN range exhaustion
- SIM inventory exhaustion
- eSIM profile pool exhaustion
- subscriber identity capacity constraints

Resource readiness therefore becomes part of **product launch readiness**.

---

# 20. Resource Readiness Dashboard

Conceptually, product enablement should have visibility into resource readiness before launch.

```mermaid
flowchart LR

    PRODUCT["Planned Product Launch"]

    CHECK["Resource Readiness"]

    NUMBER["MSISDN Capacity"]

    SIM["SIM Capacity"]

    ESIM["eSIM Profile Capacity"]

    IMSI["Identity Capacity"]

    ACT["Activation Capacity"]

    READY{"Ready?"}

    PRODUCT --> CHECK

    CHECK --> NUMBER
    CHECK --> SIM
    CHECK --> ESIM
    CHECK --> IMSI
    CHECK --> ACT

    NUMBER --> READY
    SIM --> READY
    ESIM --> READY
    IMSI --> READY
    ACT --> READY
```

This connects subscriber-resource engineering with product planning.

---

# 21. Event Model

Subscriber-resource lifecycle changes can emit events.

```mermaid
flowchart TB

    SRM["Subscriber Resource Manager"]

    BUS[("Event Backbone")]

    INVENTORY["Inventory"]
    ASSURANCE["Assurance"]
    ANALYTICS["Analytics"]
    NOTIFY["Notifications"]
    AUDIT["Audit"]

    SRM -->|"MSISDNReserved"| BUS
    SRM -->|"SIMAllocated"| BUS
    SRM -->|"ESIMProfileAllocated"| BUS
    SRM -->|"SubscriberActivated"| BUS
    SRM -->|"SIMReplaced"| BUS
    SRM -->|"SubscriptionTerminated"| BUS

    BUS --> INVENTORY
    BUS --> ASSURANCE
    BUS --> ANALYTICS
    BUS --> NOTIFY
    BUS --> AUDIT
```

Example project-level events:

```text
MSISDNReservationRequested
MSISDNReserved
MSISDNReleased

SIMAllocated
SIMActivated
SIMReplaced
SIMRetired

ESIMProfileAllocated
ESIMProfileReady
ESIMProfileEnabled
ESIMProfileDisabled
ESIMProfileDeleted

SubscriberResourcesAllocated
SubscriberActivationRequested
SubscriberActivated
SubscriberActivationFailed

SubscriptionSuspended
SubscriptionRestored
SubscriptionTerminated
```

These are illustrative project event names unless explicitly mapped to standardized events.

---

# 22. TM Forum Alignment

The subscriber-resource architecture sits within a wider TM Forum-aligned product-to-resource flow.

```mermaid
flowchart LR

    TMF620["TMF620<br/>Product Catalog"]

    TMF622["TMF622<br/>Product Order"]

    TMF641["TMF641<br/>Service Order"]

    SRM["Subscriber Resource Manager"]

    TMF652["TMF652<br/>Resource Order"]

    TMF702["TMF702<br/>Resource Activation"]

    TMF639["TMF639<br/>Resource Inventory"]

    TMF638["TMF638<br/>Service Inventory"]

    TMF620 --> TMF622
    TMF622 --> TMF641

    TMF641 --> SRM

    SRM --> TMF652

    TMF652 --> TMF702

    TMF702 --> TMF639
    TMF702 --> TMF638
```

TM Forum APIs provide standardized capability boundaries where applicable.

They should not be interpreted as defining GSMA eSIM remote provisioning procedures.

---

# 23. TM Forum vs GSMA Boundary

This distinction is important.

```mermaid
flowchart LR

    PRODUCT["Product / Service<br/>Lifecycle"]

    TMF["TM Forum-aligned<br/>Business & Operational APIs"]

    SRM["Subscriber Resource<br/>Orchestration"]

    GSMA["GSMA eSIM<br/>Provisioning Domain"]

    NETWORK["Mobile Network<br/>Activation"]

    PRODUCT --> TMF
    TMF --> SRM
    SRM --> GSMA
    SRM --> NETWORK
```

Conceptually:

**TM Forum**

helps structure product, service and resource management capabilities.

**GSMA**

defines the relevant eSIM ecosystem architecture and remote SIM provisioning specifications.

The two standards domains are complementary rather than interchangeable.

---

# 24. Security Boundary

Subscriber identifiers and eSIM provisioning are security-sensitive domains.

```mermaid
flowchart TB

    CHANNEL["Channel"]

    IAM["Identity & Access"]

    API["API Gateway"]

    SRM["Subscriber Resource Manager"]

    POLICY["Authorization Policy"]

    AUDIT["Audit"]

    RSP["eSIM Provisioning"]

    NETWORK["Network Provisioning"]

    CHANNEL --> API
    IAM --> API

    API --> SRM

    POLICY --> SRM

    SRM --> RSP
    SRM --> NETWORK

    API --> AUDIT
    SRM --> AUDIT
```

Architecture controls should consider:

- Strong authentication
- Authorization
- Least privilege
- Service identity
- Encryption in transit
- Sensitive identifier protection
- Secrets management
- Auditability
- Replay protection
- Idempotency
- Controlled provisioning interfaces

---

# 25. Observability

The full eSIM activation journey should be traceable.

```mermaid
flowchart LR

    ORDER["Product Order"]

    SERVICE["Service Order"]

    RESERVE["Resource Reservation"]

    PROFILE["Profile Fulfillment"]

    ACT["Activation"]

    NETWORK["Network"]

    READY["Subscriber Ready"]

    ORDER --> SERVICE
    SERVICE --> RESERVE
    RESERVE --> PROFILE
    PROFILE --> ACT
    ACT --> NETWORK
    NETWORK --> READY
```

A common correlation identifier should allow operators to trace:

```text
Product Order
      ↓
Service Order
      ↓
MSISDN Reservation
      ↓
ICCID / IMSI Allocation
      ↓
eSIM Profile Fulfillment
      ↓
Network Activation
      ↓
Inventory Update
      ↓
Subscriber Ready
```

---

# 26. Operational Metrics

Useful operational measures may include:

### Resource

- Available MSISDN pool
- Reservation utilization
- SIM inventory
- eSIM profile availability
- Resource allocation failure rate

### Activation

- Activation success rate
- Activation latency
- Retry rate
- Reconciliation backlog
- Partial activation count

### Customer Journey

- eSIM onboarding completion
- Time to activate
- Profile fulfillment failures
- Replacement completion
- Digital journey drop-off

The exact KPI definitions depend on implementation and operating model.

---

# 27. Design Principles

1. **SIM, IMSI and MSISDN are different lifecycle entities**
2. **Subscription is not synonymous with SIM**
3. **Allocation and activation remain separate**
4. **Commercial products remain insulated from provisioning internals**
5. **eSIM RSP remains behind a dedicated integration boundary**
6. **Resource reservation must support expiration and compensation**
7. **Activation must be idempotent**
8. **Failed workflows must be reconcilable**
9. **Resource readiness is part of product readiness**
10. **Every subscriber activation should be observable end-to-end**

---

# 28. Architectural North Star

```mermaid
flowchart LR

    SELECT["Select Product"]

    ORDER["Order"]

    RESERVE["Reserve Identity"]

    PROFILE["Fulfill SIM/eSIM"]

    ACT["Activate"]

    VERIFY["Verify"]

    READY["Subscriber Ready"]

    OBSERVE["Observe"]

    SELECT --> ORDER
    ORDER --> RESERVE
    RESERVE --> PROFILE
    PROFILE --> ACT
    ACT --> VERIFY
    VERIFY --> READY
    READY --> OBSERVE
```

> **The goal is not merely to provision an eSIM.**
>
> **The goal is to make subscriber-resource readiness, allocation, activation, replacement and lifecycle management reusable capabilities of the digital product platform.**

---

## Standards Boundary

This repository is an independent reference architecture.

TM Forum Open APIs and ODA/SID concepts are referenced for interoperability and architecture purposes.

GSMA terminology is referenced to describe the eSIM ecosystem at an architectural level.

Official TM Forum and GSMA specifications remain the authoritative sources for their respective standards.

The lifecycle states and orchestration models in this document are project-level abstractions unless explicitly identified as standardized behavior.

---

## Related Documentation

- [Project Overview](../README.md)
- [Reference Architecture](architecture.md)
- [Product Lifecycle](product-lifecycle.md)
- [ADR-001 — Domain Separation](design-decisions/ADR-001-domain-separation.md)
- `msisdn-lifecycle.md`
- `tmf-api-mapping.md`
- `sid-domain-model.md`

---

## Author

**Mohamed Salman**

Solution & Enterprise Architecture · Digital Platforms · Telecommunications · Data & AI

---

**Digital Telco Product Activation Architecture**

*From product idea to activated subscriber.*
