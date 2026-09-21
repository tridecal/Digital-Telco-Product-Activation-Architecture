# Digital Telco Product Activation — Reference Architecture

> **Architecture & Research by Mohamed Salman**  
> Vendor-neutral · TM Forum Open API aligned · ODA-inspired · API-first · Event-driven

---

## 1. Purpose

This document defines the solution architecture for a digital telecommunications product activation platform.

The architecture connects the commercial product lifecycle with service orchestration, subscriber resource management, activation, and inventory.

The core architectural journey is:

```mermaid
flowchart LR
    A["Product"] --> B["Order"]
    B --> C["Service"]
    C --> D["Subscriber Resources"]
    D --> E["Activation"]
    E --> F["Inventory"]
    F --> G["Events & Observability"]
```

The architecture is designed around a simple principle:

> **A commercial product should evolve independently from the technical complexity required to activate it.**

---

# 2. Architecture Goals

The reference architecture aims to provide:

- Clear separation between **Product, Service and Resource domains**
- API-first interoperability
- TM Forum Open API alignment where applicable
- Independent SIM/eSIM and MSISDN lifecycle management
- Product-to-resource traceability
- Event-driven lifecycle propagation
- Idempotent activation workflows
- Failure recovery and reconciliation
- Cloud-native deployment capability
- End-to-end observability
- Vendor-neutral integration boundaries

---

# 3. System Context

At the highest level, the platform sits between digital engagement channels and existing BSS/OSS/network capabilities.

```mermaid
flowchart TB

    CUSTOMER(["Customer"])

    CHANNEL["Digital Channels<br/>Mobile · Web · Partner"]

    PLATFORM["Digital Product Activation Platform"]

    BSS["BSS<br/>Customer · Billing · Product"]

    OSS["OSS<br/>Service · Resource · Inventory"]

    NETWORK["Network & Subscriber Platforms"]

    EVENTS["Enterprise Event Platform"]

    CUSTOMER --> CHANNEL
    CHANNEL --> PLATFORM

    PLATFORM <--> BSS
    PLATFORM <--> OSS
    PLATFORM --> NETWORK

    PLATFORM <--> EVENTS
```

The platform does **not** require replacement of existing BSS or OSS capabilities.

Instead, it provides standardized domain boundaries and orchestration between commercial intent and technical execution.

---

# 4. Business-to-Technology View

The architecture translates a commercial proposition progressively into technical execution.

```mermaid
flowchart LR

    subgraph BUSINESS["Business"]
        IDEA["Product Idea"]
        OFFER["Offering"]
    end

    subgraph PRODUCT["Product Domain"]
        CATALOG["Catalog"]
        CONFIG["Configuration"]
        ORDER["Product Order"]
    end

    subgraph SERVICE["Service Domain"]
        SVCORDER["Service Order"]
        SERVICEINV["Service Inventory"]
    end

    subgraph RESOURCE["Resource Domain"]
        SRM["Subscriber Resource Manager"]
        RESORDER["Resource Order"]
        RESINV["Resource Inventory"]
    end

    subgraph EXECUTION["Execution"]
        ACT["Activation"]
        NETWORK["Network Platforms"]
    end

    IDEA --> OFFER
    OFFER --> CATALOG
    CATALOG --> CONFIG
    CONFIG --> ORDER

    ORDER --> SVCORDER
    SVCORDER --> SRM
    SRM --> RESORDER
    RESORDER --> ACT
    ACT --> NETWORK

    ACT --> RESINV
    ACT --> SERVICEINV
```

This separation allows a commercial product to change without embedding network-specific implementation logic into the product domain.

---

# 5. Domain Architecture

The solution is divided into bounded architectural domains.

```mermaid
flowchart TB

    subgraph EXPERIENCE["Experience Domain"]
        CHANNEL["Digital Channels"]
        PARTNER["Partner Channels"]
    end

    subgraph PRODUCT["Product Domain"]
        PC["Product Catalog"]
        CFG["Product Configuration"]
        PO["Product Order"]
        PI["Product Inventory"]
    end

    subgraph SERVICE["Service Domain"]
        SO["Service Order"]
        SI["Service Inventory"]
        ORCH["Service Orchestration"]
    end

    subgraph SUBSCRIBER["Subscriber Resource Domain"]
        SRM["Subscriber Resource Manager"]
        SIM["SIM / eSIM"]
        IMSI["IMSI"]
        NUMBER["MSISDN"]
        SUB["Subscription"]
    end

    subgraph RESOURCE["Resource Domain"]
        RO["Resource Order"]
        RI["Resource Inventory"]
    end

    subgraph ACTIVATION["Activation Domain"]
        ACT["Resource Activation"]
        ADAPTER["Network Adapters"]
    end

    EXPERIENCE --> PRODUCT

    PC --> CFG
    CFG --> PO
    PO --> PI

    PO --> SO
    SO --> ORCH

    ORCH --> SRM

    SRM --> SIM
    SRM --> IMSI
    SRM --> NUMBER
    SRM --> SUB

    SRM --> RO

    RO --> ACT
    ACT --> ADAPTER

    ACT --> RI
    ACT --> SI
```

---

# 6. Domain Responsibilities

| Domain | Responsibility |
|---|---|
| **Experience** | Customer and partner interaction |
| **Product** | What is commercially offered and purchased |
| **Service** | What operational service must be instantiated |
| **Subscriber Resource** | Subscriber identity and number resource coordination |
| **Resource** | Technical resource ordering and inventory |
| **Activation** | Execution against provisioning/network platforms |
| **Event** | Asynchronous lifecycle propagation |
| **Observability** | Cross-domain operational visibility |

The boundaries are intentional.

For example:

**Product Order** should not directly provision a SIM.

Instead:

```text
Product Order
     ↓
Service Order
     ↓
Subscriber Resource Manager
     ↓
Resource / Activation
```

---

# 7. TM Forum API Alignment

The reference architecture maps relevant capabilities to TM Forum Open APIs.

| Architecture Capability | TM Forum API |
|---|---|
| Product Catalog | TMF620 |
| Product Order | TMF622 |
| Product Inventory | TMF637 |
| Service Order | TMF641 |
| Service Inventory | TMF638 |
| Resource Inventory | TMF639 |
| Resource Order | TMF652 |
| Resource Activation | TMF702 |

```mermaid
flowchart LR

    TMF620["TMF620<br/>Product Catalog"]
    TMF622["TMF622<br/>Product Order"]
    TMF637["TMF637<br/>Product Inventory"]

    TMF641["TMF641<br/>Service Order"]
    TMF638["TMF638<br/>Service Inventory"]

    SRM["Subscriber Resource<br/>Manager"]

    TMF652["TMF652<br/>Resource Order"]
    TMF702["TMF702<br/>Resource Activation"]
    TMF639["TMF639<br/>Resource Inventory"]

    TMF620 --> TMF622
    TMF622 --> TMF637
    TMF622 --> TMF641

    TMF641 --> SRM

    SRM --> TMF652
    TMF652 --> TMF702

    TMF702 --> TMF638
    TMF702 --> TMF639
```

> **Standards boundary**
>
> `Subscriber Resource Manager` is a project-specific architectural abstraction.
>
> It is not presented as an official TM Forum component or API.

---

# 8. Subscriber Resource Manager

The **Subscriber Resource Manager (SRM)** isolates subscriber-resource complexity from commercial product logic.

Its conceptual responsibility includes coordination of:

- SIM
- eSIM
- ICCID
- IMSI
- MSISDN
- Subscription relationships
- Reservation
- Assignment
- Release
- Replacement
- Lifecycle state

```mermaid
flowchart TB

    SRM["Subscriber Resource Manager"]

    POLICY["Allocation Policies"]
    NUMBER["MSISDN Pool"]
    SIM["SIM / eSIM Inventory"]
    ID["IMSI Resources"]
    SUB["Subscription"]
    RESOURCE["Resource Inventory"]
    EVENT["Event Bus"]

    POLICY --> SRM

    SRM --> NUMBER
    SRM --> SIM
    SRM --> ID
    SRM --> SUB

    SRM <--> RESOURCE
    SRM --> EVENT
```

This prevents channels, product-order systems and service-order systems from directly implementing SIM/MSISDN allocation logic.

---

# 9. Subscriber Resource Model

```mermaid
classDiagram

    class Subscription {
        +subscriptionId
        +status
    }

    class MSISDN {
        +number
        +status
    }

    class SIM {
        +iccid
        +type
        +status
    }

    class IMSI {
        +imsi
        +status
    }

    class Service {
        +serviceId
        +status
    }

    Service "1" --> "0..*" Subscription
    Subscription "1" --> "0..1" MSISDN
    Subscription "1" --> "1..*" IMSI
    IMSI "1" --> "1" SIM
```

This is a **conceptual project model**, not a reproduction or replacement of the TM Forum Information Framework (SID).

---

# 10. End-to-End Activation

A typical digital subscription activation follows this sequence.

```mermaid
sequenceDiagram

    autonumber

    actor Customer

    participant Channel
    participant Catalog as Product Catalog
    participant Order as Product Order
    participant Service as Service Orchestrator
    participant SRM as Subscriber Resource Manager
    participant Inventory as Resource Inventory
    participant Activation
    participant Network

    Customer->>Channel: Select offering

    Channel->>Catalog: Retrieve offering
    Catalog-->>Channel: Product configuration

    Customer->>Channel: Confirm purchase

    Channel->>Order: Create product order

    Order->>Service: Create service order

    Service->>SRM: Request subscriber resources

    SRM->>Inventory: Reserve MSISDN
    Inventory-->>SRM: MSISDN reserved

    SRM->>Inventory: Allocate SIM/eSIM + IMSI
    Inventory-->>SRM: Resources allocated

    SRM->>Activation: Request activation

    Activation->>Network: Provision subscriber

    Network-->>Activation: Provisioning completed

    Activation-->>SRM: Resources active
    SRM-->>Service: Subscriber ready

    Service-->>Order: Service active
    Order-->>Channel: Order completed

    Channel-->>Customer: Service ready
```

---

# 11. Resource Allocation vs Activation

Allocation and activation are deliberately separated.

```mermaid
flowchart LR

    REQUEST["Resource Request"]

    CHECK["Check Availability"]

    RESERVE["Reserve"]

    ASSIGN["Assign"]

    ACTIVATE["Activate"]

    VERIFY["Verify"]

    ACTIVE["Active"]

    REQUEST --> CHECK
    CHECK --> RESERVE
    RESERVE --> ASSIGN
    ASSIGN --> ACTIVATE
    ACTIVATE --> VERIFY
    VERIFY --> ACTIVE
```

### Allocation

Answers:

> **Which resource belongs to this subscription?**

Examples:

- reserve MSISDN
- allocate ICCID
- associate IMSI
- create resource relationships

### Activation

Answers:

> **Is that resource operational?**

Examples:

- subscriber provisioning
- network activation
- policy provisioning
- service enablement

Keeping the two concerns separate improves failure handling and reconciliation.

---

# 12. Event Architecture

Lifecycle state changes are propagated asynchronously where appropriate.

```mermaid
flowchart TB

    PRODUCT["Product Domain"]
    SERVICE["Service Domain"]
    SRM["Subscriber Resource Domain"]
    RESOURCE["Resource Domain"]
    ACTIVATION["Activation Domain"]

    BUS[("Event Backbone")]

    NOTIFY["Notifications"]
    ANALYTICS["Analytics"]
    ASSURANCE["Service Assurance"]
    OBS["Observability"]
    AUDIT["Audit"]

    PRODUCT --> BUS
    SERVICE --> BUS
    SRM --> BUS
    RESOURCE --> BUS
    ACTIVATION --> BUS

    BUS --> NOTIFY
    BUS --> ANALYTICS
    BUS --> ASSURANCE
    BUS --> OBS
    BUS --> AUDIT
```

Example project-level domain events include:

```text
ProductOrderCreated
ProductOrderCompleted

ServiceOrderCreated
ServiceActivated

MSISDNReserved
MSISDNAssigned

SIMAllocated
ESIMAllocated

SubscriberResourcesAllocated

ResourceActivationRequested
ResourceActivated
ResourceActivationFailed

SubscriptionSuspended
SubscriptionTerminated
```

These names are illustrative project concepts unless explicitly mapped to standardized TM Forum events.

---

# 13. API Gateway Boundary

The API Gateway provides external API concerns but does not own domain orchestration.

```mermaid
flowchart TB

    CHANNEL["Digital / Partner Channels"]

    GW["API Gateway"]

    AUTH["Identity & Access"]
    RATE["Rate Limiting"]
    POLICY["API Policies"]
    OBS["API Observability"]

    PRODUCT["Product APIs"]
    SERVICE["Service APIs"]
    RESOURCE["Resource APIs"]
    ACTIVATION["Activation APIs"]

    CHANNEL --> GW

    AUTH --> GW
    RATE --> GW
    POLICY --> GW
    GW --> OBS

    GW --> PRODUCT
    GW --> SERVICE
    GW --> RESOURCE
    GW --> ACTIVATION
```

The gateway may provide:

- Authentication
- Authorization enforcement
- Routing
- Rate limiting
- API version routing
- Request validation
- Correlation identifiers
- API telemetry

Business workflow logic remains within domain services.

---

# 14. Orchestration Pattern

Telecom activation frequently involves long-running workflows.

A distributed ACID transaction across all systems is therefore avoided.

```mermaid
flowchart LR

    START["Create Order"]

    SERVICE["Create Service"]

    RESERVE["Reserve Resources"]

    ACTIVATE["Activate"]

    VERIFY["Verify"]

    COMPLETE["Complete"]

    COMPENSATE["Compensate"]

    RECONCILE["Reconcile"]

    START --> SERVICE
    SERVICE --> RESERVE
    RESERVE --> ACTIVATE
    ACTIVATE --> VERIFY

    VERIFY -->|Success| COMPLETE

    SERVICE -->|Failure| COMPENSATE
    RESERVE -->|Failure| COMPENSATE
    ACTIVATE -->|Failure| RECONCILE

    RECONCILE -->|Retry| ACTIVATE
    RECONCILE -->|Rollback| COMPENSATE
```

This resembles a **Saga-style orchestration approach** for long-running transactions.

---

# 15. Idempotency

Activation and ordering operations must tolerate retries.

Conceptually:

```text
Request
   │
   ▼
Idempotency Key
   │
   ├── Existing Result ──► Return Previous Result
   │
   └── New Request ──────► Execute Operation
```

Typical candidates include:

```text
POST /productOrders
POST /serviceOrders
POST /resourceReservations
POST /activations
```

A repeated network timeout must not accidentally create another subscription, number assignment, or activation.

---

# 16. Failure Architecture

Failure is treated as a normal architectural state.

```mermaid
stateDiagram-v2

    [*] --> Requested

    Requested --> Allocating
    Allocating --> Allocated

    Allocated --> Activating

    Activating --> Active
    Activating --> ActivationFailed

    ActivationFailed --> RetryPending
    RetryPending --> Activating

    ActivationFailed --> ManualResolution

    ManualResolution --> Activating
    ManualResolution --> Compensating

    Compensating --> Released

    Released --> [*]
    Active --> [*]
```

Examples of failure scenarios:

- MSISDN reservation timeout
- SIM resource unavailable
- activation platform unavailable
- downstream network timeout
- partial provisioning
- inventory update failure
- event publication failure

---

# 17. Observability Architecture

Every lifecycle transaction should carry a correlation identifier across domains.

```mermaid
flowchart LR

    CHANNEL["Channel"]

    ORDER["Product Order"]

    SERVICE["Service Order"]

    SRM["Subscriber Resources"]

    ACT["Activation"]

    NETWORK["Network"]

    TRACE["Distributed Trace"]

    CHANNEL --> ORDER
    ORDER --> SERVICE
    SERVICE --> SRM
    SRM --> ACT
    ACT --> NETWORK

    CHANNEL -.-> TRACE
    ORDER -.-> TRACE
    SERVICE -.-> TRACE
    SRM -.-> TRACE
    ACT -.-> TRACE
    NETWORK -.-> TRACE
```

A single business transaction should ideally be traceable as:

```text
Correlation ID
      │
      ├── Product Order
      ├── Service Order
      ├── Resource Reservation
      ├── Activation Request
      ├── Network Transaction
      └── Inventory Update
```

Core telemetry includes:

- logs
- metrics
- distributed traces
- lifecycle events
- API latency
- provisioning latency
- activation success/failure rate
- resource allocation failures
- reconciliation backlog

---

# 18. Security Architecture

```mermaid
flowchart TB

    USER["Customer / Partner"]

    EDGE["API Edge"]

    IDP["Identity Provider"]

    GW["API Gateway"]

    DOMAIN["Domain Services"]

    POLICY["Authorization Policy"]

    SECRET["Secrets Management"]

    AUDIT["Audit"]

    NETWORK["Provisioning Systems"]

    USER --> EDGE
    EDGE --> GW

    GW <--> IDP

    GW --> DOMAIN

    POLICY --> DOMAIN
    SECRET --> DOMAIN

    DOMAIN --> NETWORK

    GW --> AUDIT
    DOMAIN --> AUDIT
```

Security principles include:

- OAuth/OIDC where applicable
- scoped API authorization
- service-to-service identity
- least privilege
- encrypted transport
- secret isolation
- audit logging
- separation between external and internal APIs
- protection of subscriber identifiers
- controlled access to provisioning interfaces

---

# 19. Deployment Architecture

The logical architecture can be deployed using cloud-native infrastructure without coupling the design to a specific cloud provider.

```mermaid
flowchart TB

    INTERNET["Digital Channels"]

    subgraph EDGE["Edge"]
        GW["API Gateway"]
    end

    subgraph PLATFORM["Container Platform"]

        PRODUCT["Product Services"]
        SERVICE["Service Services"]
        SRM["Subscriber Resource Manager"]
        RESOURCE["Resource Services"]
        ACT["Activation Adapter"]

        EVENT[("Event Backbone")]

        CACHE[("Cache")]

        DB[("Domain Data Stores")]

        OBS["Observability"]
    end

    subgraph ENTERPRISE["Enterprise Systems"]
        CRM["Customer"]
        BILLING["Billing"]
        INVENTORY["Existing Inventory"]
    end

    subgraph NETWORK["Network Domain"]
        PROVISION["Provisioning"]
        SUBSCRIBER["Subscriber Platforms"]
    end

    INTERNET --> GW

    GW --> PRODUCT
    GW --> SERVICE
    GW --> SRM

    PRODUCT --> DB
    SERVICE --> DB
    SRM --> DB
    RESOURCE --> DB

    PRODUCT <--> EVENT
    SERVICE <--> EVENT
    SRM <--> EVENT
    RESOURCE <--> EVENT
    ACT <--> EVENT

    SRM --> CACHE

    PRODUCT <--> CRM
    PRODUCT <--> BILLING

    RESOURCE <--> INVENTORY

    SERVICE --> SRM
    SRM --> RESOURCE
    RESOURCE --> ACT

    ACT --> PROVISION
    ACT --> SUBSCRIBER

    PRODUCT --> OBS
    SERVICE --> OBS
    SRM --> OBS
    RESOURCE --> OBS
    ACT --> OBS
```

---

# 20. Logical Component Model

```mermaid
flowchart LR

    subgraph DIGITAL["Digital Layer"]
        EXPERIENCE["Experience APIs"]
    end

    subgraph COMMERCIAL["Commercial Layer"]
        CATALOG["Catalog"]
        CONFIG["Configuration"]
        ORDER["Order"]
        PINV["Product Inventory"]
    end

    subgraph OPERATIONAL["Operational Layer"]
        SORDER["Service Order"]
        SINV["Service Inventory"]
    end

    subgraph SUBSCRIBER["Subscriber Layer"]
        SRM["Subscriber Resource Manager"]
    end

    subgraph TECHNICAL["Technical Layer"]
        RORDER["Resource Order"]
        RINV["Resource Inventory"]
        ACT["Activation"]
    end

    EXPERIENCE --> CATALOG
    EXPERIENCE --> CONFIG
    CONFIG --> ORDER

    ORDER --> PINV
    ORDER --> SORDER

    SORDER --> SRM

    SRM --> RORDER

    RORDER --> ACT

    ACT --> RINV
    ACT --> SINV
```

---

# 21. Product-to-Resource Traceability

The architecture preserves relationships across layers.

```mermaid
flowchart LR

    CUSTOMER["Customer"]

    ORDER["Product Order"]

    PRODUCT["Product"]

    SERVICE["Service"]

    SUB["Subscription"]

    NUMBER["MSISDN"]

    ID["IMSI"]

    SIM["SIM / eSIM"]

    CUSTOMER --> ORDER
    ORDER --> PRODUCT
    PRODUCT --> SERVICE
    SERVICE --> SUB

    SUB --> NUMBER
    SUB --> ID
    ID --> SIM
```

This supports operational questions such as:

- Which resources support this product?
- Which subscription owns this number?
- Which service depends on this resource?
- What must be changed during SIM replacement?
- Which resources must be released after termination?

---

# 22. Architecture Principles

The architecture follows these principles:

### 1. Product is not Service

Commercial intent and operational realization are separate concerns.

### 2. Service is not Resource

A service describes operational capability; resources provide the technical realization.

### 3. Allocation is not Activation

Owning a resource does not mean it is operational.

### 4. APIs define boundaries

Domain APIs expose capabilities without leaking internal implementation.

### 5. Events communicate lifecycle change

Events reduce unnecessary synchronous coupling.

### 6. Failure is expected

Retries, compensation and reconciliation are architectural requirements.

### 7. Every transaction is observable

Product-to-network execution should be traceable end-to-end.

### 8. Standards before proprietary integration

Standard interfaces are preferred where they satisfy the required capability.

### 9. Network complexity stays behind domain boundaries

Digital channels should not understand provisioning-system internals.

### 10. Architecture remains vendor-neutral

Products and infrastructure can change without redefining the core domain model.

---

# 23. Architecture Decision Records

The following ADRs will document major design decisions:

| ADR | Decision |
|---|---|
| ADR-001 | Separate Product, Service and Resource Domains |
| ADR-002 | Introduce Subscriber Resource Manager |
| ADR-003 | Adopt API-First Domain Boundaries |
| ADR-004 | Use Event-Driven Lifecycle Propagation |
| ADR-005 | Separate Resource Allocation from Activation |
| ADR-006 | Maintain Product-to-Resource Traceability |
| ADR-007 | Keep Provisioning Behind Activation Adapters |
| ADR-008 | Design Long-Running Workflows for Idempotency and Compensation |

---

# 24. Target Evolution

```mermaid
flowchart LR

    A["Architecture"]

    B["API Contracts"]

    C["Reference Services"]

    D["Event Backbone"]

    E["Containerization"]

    F["Kubernetes"]

    G["Observability"]

    H["Conformance & Architecture Tests"]

    A --> B --> C --> D --> E --> F --> G --> H
```

The repository intentionally evolves from **architecture first** toward executable reference components.

---

# 25. Architecture Boundary

This project is:

- a reference architecture
- vendor-neutral
- standards-aware
- implementation-oriented
- designed for experimentation and architecture discussion

It is not:

- a production BSS
- an official TM Forum implementation
- a TM Forum certification claim
- a replacement for SID
- a network provisioning product

Where TM Forum APIs or concepts are referenced, the official specifications remain authoritative.

---

# 26. Architectural North Star

```mermaid
flowchart LR

    IDEA["Idea"]

    CONFIG["Configure"]

    LAUNCH["Launch"]

    ACTIVATE["Activate"]

    OBSERVE["Observe"]

    LEARN["Learn"]

    ITERATE["Iterate"]

    IDEA --> CONFIG
    CONFIG --> LAUNCH
    LAUNCH --> ACTIVATE
    ACTIVATE --> OBSERVE
    OBSERVE --> LEARN
    LEARN --> ITERATE
    ITERATE --> CONFIG
```

The architecture is ultimately designed around one objective:

> **Reduce the architectural distance between a product idea and an activated, observable subscriber service — without sacrificing domain separation, interoperability or operational control.**

---

## Author

**Mohamed Salman**

Solution & Enterprise Architecture · Digital Platforms · Telecommunications · Data & AI

---

## Related Documentation

- [Project Overview](../README.md)
- Product Lifecycle — `product-lifecycle.md`
- eSIM Lifecycle — `esim-lifecycle.md`
- MSISDN Lifecycle — `msisdn-lifecycle.md`
- TM Forum API Mapping — `tmf-api-mapping.md`
- SID Domain Model — `sid-domain-model.md`
- Architecture Decision Records — `design-decisions/`

---

**Digital Telco Product Activation Architecture**  
*From product idea to activated subscriber.*
