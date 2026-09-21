# Digital Telco Product Lifecycle

> **From Market Opportunity to Activated & Measurable Product**  
> Architecture & Research by **Mohamed Salman**

---

## 1. Purpose

A digital telecom product lifecycle does not end when a product is designed or published to a catalog.

The complete lifecycle connects:

**Market Opportunity → Product Strategy → Design → Configure → Launch → Order → Activate → Adopt → Measure → Improve**

This document defines a vendor-neutral lifecycle connecting **commercial product management** with the technology capabilities required to launch, operate, measure, and evolve digital telecom products.

```mermaid
flowchart LR
    A["Discover"] --> B["Define"]
    B --> C["Design"]
    C --> D["Configure"]
    D --> E["Launch"]
    E --> F["Activate"]
    F --> G["Adopt"]
    G --> H["Measure"]
    H --> I["Improve"]
    I --> B
```

The objective is simple:

> **Reduce the distance between identifying a market opportunity and delivering a measurable product to an active subscriber.**

---

# 2. Product Lifecycle Model

The reference lifecycle contains nine stages.

| Stage | Primary Question | Outcome |
|---|---|---|
| **Discover** | Where is the opportunity? | Opportunity hypothesis |
| **Define** | What should we offer? | Product proposition |
| **Design** | How should it work? | Product design |
| **Configure** | Can the platform represent it? | Launchable configuration |
| **Launch** | Can customers access it? | Market availability |
| **Activate** | Can it become a working service? | Active subscriber |
| **Adopt** | Are customers using it? | Product adoption |
| **Measure** | Is it delivering value? | Performance insight |
| **Improve** | What should change next? | New product iteration |

```mermaid
flowchart TB

    DISCOVER["1. Discover<br/>Market & Customer"]

    DEFINE["2. Define<br/>Strategy & Proposition"]

    DESIGN["3. Design<br/>Experience & Product"]

    CONFIG["4. Configure<br/>Catalog & Rules"]

    LAUNCH["5. Launch<br/>Channels & GTM"]

    ACTIVATE["6. Activate<br/>Service & Resources"]

    ADOPT["7. Adopt<br/>Customer Usage"]

    MEASURE["8. Measure<br/>Product Performance"]

    IMPROVE["9. Improve<br/>Iteration"]

    DISCOVER --> DEFINE
    DEFINE --> DESIGN
    DESIGN --> CONFIG
    CONFIG --> LAUNCH
    LAUNCH --> ACTIVATE
    ACTIVATE --> ADOPT
    ADOPT --> MEASURE
    MEASURE --> IMPROVE
    IMPROVE --> DEFINE
```

---

# 3. Stage 1 — Discover

Product development begins with an opportunity, not a technical feature.

Inputs may include:

- Customer needs
- Customer behavior
- Market trends
- Competitive propositions
- Usage patterns
- Customer feedback
- Commercial performance
- Technology capabilities
- Regulatory constraints
- Partner opportunities

```mermaid
flowchart LR

    CUSTOMER["Customer Needs"]
    MARKET["Market"]
    COMP["Competition"]
    DATA["Usage & Analytics"]
    TECH["Technology"]
    PARTNER["Partners"]

    OPPORTUNITY["Product Opportunity"]

    CUSTOMER --> OPPORTUNITY
    MARKET --> OPPORTUNITY
    COMP --> OPPORTUNITY
    DATA --> OPPORTUNITY
    TECH --> OPPORTUNITY
    PARTNER --> OPPORTUNITY
```

### Output

A product opportunity should clearly identify:

```text
Customer Problem
       +
Target Segment
       +
Potential Value
       +
Strategic Fit
       =
Product Opportunity
```

---

# 4. Stage 2 — Define

The opportunity becomes a product proposition.

A useful product definition answers:

- Who is the target customer?
- What problem are we solving?
- What is the customer value?
- What capabilities are required?
- What differentiates the proposition?
- How will success be measured?
- What dependencies exist?

```mermaid
flowchart TB

    OPPORTUNITY["Opportunity"]

    SEGMENT["Target Segment"]
    VALUE["Value Proposition"]
    CAPABILITY["Required Capabilities"]
    ECONOMICS["Commercial Model"]
    KPI["Success Measures"]

    PRODUCT["Product Proposition"]

    OPPORTUNITY --> SEGMENT
    OPPORTUNITY --> VALUE
    OPPORTUNITY --> CAPABILITY
    OPPORTUNITY --> ECONOMICS
    OPPORTUNITY --> KPI

    SEGMENT --> PRODUCT
    VALUE --> PRODUCT
    CAPABILITY --> PRODUCT
    ECONOMICS --> PRODUCT
    KPI --> PRODUCT
```

---

# 5. Product Strategy Canvas

A product can be represented through six connected dimensions.

```mermaid
flowchart TB

    PRODUCT["Product Strategy"]

    CUSTOMER["Customer<br/>Who?"]
    PROBLEM["Problem<br/>Why?"]
    VALUE["Value<br/>What?"]
    EXPERIENCE["Experience<br/>How?"]
    PLATFORM["Capabilities<br/>With what?"]
    OUTCOME["Outcome<br/>Measure?"]

    PRODUCT --> CUSTOMER
    PRODUCT --> PROBLEM
    PRODUCT --> VALUE
    PRODUCT --> EXPERIENCE
    PRODUCT --> PLATFORM
    PRODUCT --> OUTCOME
```

A strong product proposition should connect all six.

A technically feasible product without customer value is weak.

A commercially attractive product without platform readiness cannot be reliably launched.

---

# 6. Stage 3 — Design

Product design connects commercial intent with customer experience and technical capability.

```mermaid
flowchart LR

    STRATEGY["Product Strategy"]

    EXPERIENCE["Customer Experience"]

    COMMERCIAL["Commercial Design"]

    FUNCTION["Functional Design"]

    TECH["Technology Design"]

    READY["Product Definition Ready"]

    STRATEGY --> EXPERIENCE
    STRATEGY --> COMMERCIAL
    STRATEGY --> FUNCTION

    EXPERIENCE --> READY
    COMMERCIAL --> READY
    FUNCTION --> TECH
    TECH --> READY
```

Product design may define:

- Offering structure
- Bundles
- Add-ons
- Eligibility
- Pricing
- Allowances
- Customer journey
- Activation requirements
- Lifecycle behavior
- Channel availability

---

# 7. Stage 4 — Configure

The product definition now becomes a machine-readable platform configuration.

This is the bridge between **product management and technology enablement**.

```mermaid
flowchart LR

    DESIGN["Product Design"]

    CATALOG["Product Catalog"]

    RULES["Eligibility & Rules"]

    PRICE["Pricing"]

    SERVICE["Service Mapping"]

    RESOURCE["Resource Requirements"]

    READY["Launch-Ready Product"]

    DESIGN --> CATALOG
    DESIGN --> RULES
    DESIGN --> PRICE

    CATALOG --> SERVICE
    SERVICE --> RESOURCE

    RULES --> READY
    PRICE --> READY
    RESOURCE --> READY
```

Where applicable, the Product Catalog capability can align with **TMF620 Product Catalog Management**.

---

# 8. Product Capability Readiness

Before launch, product readiness should be assessed across multiple dimensions.

```mermaid
flowchart TB

    PRODUCT["Product Launch"]

    COMMERCIAL["Commercial<br/>Ready?"]

    CHANNEL["Channel<br/>Ready?"]

    PLATFORM["Platform<br/>Ready?"]

    SERVICE["Service<br/>Ready?"]

    RESOURCE["Resources<br/>Ready?"]

    OPERATIONS["Operations<br/>Ready?"]

    PRODUCT --> COMMERCIAL
    PRODUCT --> CHANNEL
    PRODUCT --> PLATFORM
    PRODUCT --> SERVICE
    PRODUCT --> RESOURCE
    PRODUCT --> OPERATIONS
```

### Example readiness questions

**Commercial**

- Is the proposition approved?
- Is pricing defined?
- Are eligibility rules confirmed?

**Channel**

- Can customers discover the product?
- Can they purchase it?
- Can they manage it after activation?

**Platform**

- Is the catalog configured?
- Are APIs available?
- Are ordering workflows ready?

**Service**

- Can required services be instantiated?

**Resource**

- Are required subscriber resources available?
- Is SIM/eSIM capacity ready?
- Is MSISDN inventory sufficient?

**Operations**

- Is monitoring available?
- Can failures be reconciled?
- Is support prepared?

---

# 9. Stage 5 — Launch

A product launch is a coordinated business and technology event.

```mermaid
flowchart TB

    READY["Launch Readiness"]

    CHANNEL["Channels"]
    CAMPAIGN["Go-to-Market"]
    CATALOG["Catalog"]
    ORDER["Ordering"]
    SUPPORT["Customer Support"]
    OBS["Monitoring"]

    LIVE["Product Live"]

    READY --> CHANNEL
    READY --> CAMPAIGN
    READY --> CATALOG
    READY --> ORDER
    READY --> SUPPORT
    READY --> OBS

    CHANNEL --> LIVE
    CAMPAIGN --> LIVE
    CATALOG --> LIVE
    ORDER --> LIVE
    SUPPORT --> LIVE
    OBS --> LIVE
```

The objective is not simply:

> Product published.

The real objective is:

> **Product discoverable, purchasable, activatable, supportable and measurable.**

---

# 10. Stage 6 — Activate

Once purchased, the commercial product must become an operational service.

```mermaid
flowchart LR

    ORDER["Product Order<br/>TMF622"]

    PRODUCT["Product Inventory<br/>TMF637"]

    SERVICE["Service Order<br/>TMF641"]

    SRM["Subscriber Resource<br/>Manager"]

    RESOURCE["Resource Order<br/>TMF652"]

    ACT["Resource Activation<br/>TMF702"]

    INVENTORY["Resource Inventory<br/>TMF639"]

    ACTIVE["Active Subscriber"]

    ORDER --> PRODUCT
    ORDER --> SERVICE

    SERVICE --> SRM

    SRM --> RESOURCE
    RESOURCE --> ACT

    ACT --> INVENTORY
    ACT --> ACTIVE
```

This is the point where product management and operational architecture meet.

---

# 11. Subscriber Resource Readiness

Digital mobile products may depend on subscriber resources being available before or during activation.

```mermaid
flowchart TB

    PRODUCT["Product Activation"]

    SRM["Subscriber Resource Manager"]

    MSISDN["MSISDN"]
    SIM["SIM / eSIM"]
    IMSI["IMSI"]
    SUB["Subscription"]

    ACT["Activation"]

    PRODUCT --> SRM

    SRM --> MSISDN
    SRM --> SIM
    SRM --> IMSI
    SRM --> SUB

    MSISDN --> ACT
    SIM --> ACT
    IMSI --> ACT
    SUB --> ACT
```

Resource readiness may include:

- Available number inventory
- Number reservation capacity
- SIM inventory
- eSIM profile availability
- IMSI availability
- Allocation policies
- Activation capacity
- Provisioning connectivity

---

# 12. Product Launch Sequence

```mermaid
sequenceDiagram

    autonumber

    participant PM as Product Management
    participant Catalog as Product Platform
    participant Channel as Digital Channel
    participant Order as Order Management
    participant Service as Service Orchestration
    participant SRM as Subscriber Resource Manager
    participant Activation
    participant Analytics

    PM->>Catalog: Configure product offering

    Catalog-->>PM: Product configuration validated

    PM->>Channel: Enable product

    Channel-->>PM: Product available

    Note over PM,Channel: Product launched

    Channel->>Order: Customer purchase

    Order->>Service: Request service

    Service->>SRM: Request subscriber resources

    SRM->>Activation: Activate resources

    Activation-->>SRM: Activation complete

    SRM-->>Service: Subscriber ready

    Service-->>Order: Service active

    Order-->>Channel: Order complete

    Channel->>Analytics: Product interaction / activation events
```

---

# 13. Stage 7 — Adopt

Launch does not equal adoption.

Product adoption can be viewed as a funnel.

```mermaid
flowchart LR

    AWARE["Discover"]

    VIEW["View"]

    SELECT["Select"]

    BUY["Purchase"]

    ACTIVATE["Activate"]

    USE["Use"]

    RETAIN["Retain"]

    AWARE --> VIEW
    VIEW --> SELECT
    SELECT --> BUY
    BUY --> ACTIVATE
    ACTIVATE --> USE
    USE --> RETAIN
```

Each transition can reveal a different problem.

For example:

```text
High views + Low purchase
        ↓
Possible proposition / pricing / eligibility issue

High purchase + Low activation
        ↓
Possible technology / resource / provisioning issue

High activation + Low usage
        ↓
Possible product value / experience issue
```

This distinction is critical because not every product-performance problem is a technology problem.

---

# 14. Stage 8 — Measure

A digital product should be measurable across commercial, experience and technology dimensions.

```mermaid
flowchart TB

    PRODUCT["Product Performance"]

    COMMERCIAL["Commercial"]

    CUSTOMER["Customer"]

    EXPERIENCE["Experience"]

    TECHNOLOGY["Technology"]

    OPERATIONS["Operations"]

    PRODUCT --> COMMERCIAL
    PRODUCT --> CUSTOMER
    PRODUCT --> EXPERIENCE
    PRODUCT --> TECHNOLOGY
    PRODUCT --> OPERATIONS
```

### Commercial

Examples:

- Orders
- Conversion
- Revenue
- Attach rate
- Upgrade rate

### Customer

Examples:

- Adoption
- Retention
- Churn
- Product usage

### Experience

Examples:

- Journey completion
- Drop-off
- Activation time
- Failed journeys

### Technology

Examples:

- API latency
- Error rate
- Activation success
- Provisioning latency

### Operations

Examples:

- Failed orders
- Reconciliation backlog
- Resource exhaustion
- Manual intervention rate

---

# 15. Product-to-Technology KPI Tree

```mermaid
flowchart TB

    SUCCESS["Product Success"]

    GROWTH["Growth"]
    VALUE["Customer Value"]
    QUALITY["Experience Quality"]
    DELIVERY["Technology Delivery"]

    SUCCESS --> GROWTH
    SUCCESS --> VALUE
    SUCCESS --> QUALITY
    SUCCESS --> DELIVERY

    GROWTH --> ORDERS["Orders"]
    GROWTH --> CONVERSION["Conversion"]

    VALUE --> ADOPTION["Adoption"]
    VALUE --> RETENTION["Retention"]

    QUALITY --> COMPLETION["Journey Completion"]
    QUALITY --> TIME["Time to Activate"]

    DELIVERY --> SUCCESSRATE["Activation Success"]
    DELIVERY --> RELIABILITY["Platform Reliability"]
```

The purpose is not to prescribe universal KPIs.

It is to connect product outcomes with the underlying capabilities that influence them.

---

# 16. Stage 9 — Improve

Product management becomes a continuous feedback system.

```mermaid
flowchart LR

    DATA["Product Data"]

    INSIGHT["Insight"]

    HYPOTHESIS["Hypothesis"]

    PRIORITY["Prioritize"]

    CHANGE["Product Change"]

    RELEASE["Release"]

    MEASURE["Measure"]

    DATA --> INSIGHT
    INSIGHT --> HYPOTHESIS
    HYPOTHESIS --> PRIORITY
    PRIORITY --> CHANGE
    CHANGE --> RELEASE
    RELEASE --> MEASURE
    MEASURE --> DATA
```

This turns the product roadmap into an evidence-driven lifecycle rather than a static feature list.

---

# 17. Product Roadmap Model

The roadmap should connect business outcomes with platform capabilities.

```mermaid
flowchart TB

    OUTCOME["Business Outcome"]

    PRODUCT["Product Initiative"]

    CAPABILITY["Required Capability"]

    PLATFORM["Platform Change"]

    API["API / Integration"]

    RESOURCE["Resource Readiness"]

    RELEASE["Release"]

    KPI["Measured Outcome"]

    OUTCOME --> PRODUCT
    PRODUCT --> CAPABILITY
    CAPABILITY --> PLATFORM
    CAPABILITY --> API
    CAPABILITY --> RESOURCE

    PLATFORM --> RELEASE
    API --> RELEASE
    RESOURCE --> RELEASE

    RELEASE --> KPI
```

This prevents a roadmap from becoming merely a collection of features.

---

# 18. Capability-Based Planning

A single capability can support multiple products.

```mermaid
flowchart TB

    CAP["Reusable Capability"]

    P1["Product A"]
    P2["Product B"]
    P3["Product C"]

    CAP --> P1
    CAP --> P2
    CAP --> P3
```

Examples of reusable capabilities include:

- eSIM onboarding
- MSISDN reservation
- Eligibility engine
- Product configuration
- Digital activation
- Add-on management
- Notification
- Usage visibility

This changes technology investment from:

> **Build integration for Product X**

toward:

> **Build reusable capability Y that enables Products X, Z and future propositions.**

---

# 19. Product Portfolio View

Individual products should not be considered in isolation.

```mermaid
quadrantChart
    title Product Portfolio Decision View
    x-axis Low Strategic Value --> High Strategic Value
    y-axis Low Customer Adoption --> High Customer Adoption

    "Invest": [0.80, 0.80]
    "Improve": [0.75, 0.35]
    "Optimize": [0.35, 0.80]
    "Review": [0.25, 0.25]
```

> The quadrant above is a conceptual decision framework, not measured product data.

Portfolio decisions may include:

- Invest
- Improve
- Simplify
- Bundle
- Reposition
- Retire

---

# 20. Product Retirement

A mature lifecycle also includes retirement.

```mermaid
flowchart LR

    REVIEW["Portfolio Review"]

    DECIDE["Retirement Decision"]

    STOP["Stop New Sales"]

    MIGRATE["Customer Migration"]

    TERMINATE["Terminate Product"]

    RELEASE["Release Resources"]

    ARCHIVE["Archive"]

    REVIEW --> DECIDE
    DECIDE --> STOP
    STOP --> MIGRATE
    MIGRATE --> TERMINATE
    TERMINATE --> RELEASE
    RELEASE --> ARCHIVE
```

Retirement should consider both commercial and technical dependencies.

A product may disappear from the catalog while active customer instances continue to exist for a defined period.

---

# 21. Product Lifecycle and TM Forum APIs

The architecture can conceptually map lifecycle stages to relevant standardized capabilities.

```mermaid
flowchart LR

    DISCOVER["Discover"]

    DEFINE["Define"]

    CATALOG["Configure<br/>TMF620"]

    ORDER["Order<br/>TMF622"]

    PINV["Product Inventory<br/>TMF637"]

    SERVICE["Service<br/>TMF641 / TMF638"]

    RESOURCE["Resource<br/>TMF652 / TMF639"]

    ACT["Activate<br/>TMF702"]

    MEASURE["Measure"]

    IMPROVE["Improve"]

    DISCOVER --> DEFINE
    DEFINE --> CATALOG
    CATALOG --> ORDER
    ORDER --> PINV
    ORDER --> SERVICE
    SERVICE --> RESOURCE
    RESOURCE --> ACT
    ACT --> MEASURE
    MEASURE --> IMPROVE
    IMPROVE --> DEFINE
```

TM Forum APIs cover specific operational capabilities.

They do not replace the wider product-management lifecycle shown in this document.

---

# 22. Product and Technology Operating Model

Successful digital product delivery requires collaboration across several perspectives.

```mermaid
flowchart TB

    PRODUCT["Product Management"]

    COMMERCIAL["Commercial"]

    EXPERIENCE["Customer Experience"]

    ENGINEERING["Engineering"]

    ARCH["Architecture"]

    OPERATIONS["Operations"]

    DATA["Data & Analytics"]

    OUTCOME["Product Outcome"]

    PRODUCT --> OUTCOME
    COMMERCIAL --> OUTCOME
    EXPERIENCE --> OUTCOME
    ENGINEERING --> OUTCOME
    ARCH --> OUTCOME
    OPERATIONS --> OUTCOME
    DATA --> OUTCOME
```

The model intentionally avoids treating product management as an isolated business function.

Product success depends on coordinated commercial, experience, technology and operational execution.

---

# 23. Product-to-Activation Traceability

A product decision should ultimately be traceable through implementation and operational execution.

```mermaid
flowchart LR

    OPPORTUNITY["Opportunity"]

    INITIATIVE["Product Initiative"]

    OFFER["Product Offering"]

    ORDER["Product Order"]

    SERVICE["Service"]

    RESOURCE["Resources"]

    ACT["Activation"]

    KPI["Outcome"]

    OPPORTUNITY --> INITIATIVE
    INITIATIVE --> OFFER
    OFFER --> ORDER
    ORDER --> SERVICE
    SERVICE --> RESOURCE
    RESOURCE --> ACT
    ACT --> KPI

    KPI -. "feedback" .-> OPPORTUNITY
```

This creates a closed loop between **strategy and execution**.

---

# 24. North-Star Concept

The target operating model is:

```mermaid
flowchart LR

    IDEA["Idea"]

    CONFIG["Configure"]

    TEST["Validate"]

    LAUNCH["Launch"]

    ACTIVATE["Activate"]

    OBSERVE["Observe"]

    LEARN["Learn"]

    ITERATE["Iterate"]

    IDEA --> CONFIG
    CONFIG --> TEST
    TEST --> LAUNCH
    LAUNCH --> ACTIVATE
    ACTIVATE --> OBSERVE
    OBSERVE --> LEARN
    LEARN --> ITERATE
    ITERATE --> CONFIG
```

The architectural ambition is not simply faster development.

It is:

> **A reusable product engine where commercial ideas can be configured, launched, activated, measured and evolved without rebuilding the underlying technology journey for every proposition.**

---

# 25. Design Principles

1. **Start with customer and market value**
2. **Translate products into reusable capabilities**
3. **Separate commercial products from technical implementation**
4. **Treat platform readiness as part of product readiness**
5. **Treat subscriber resources as managed lifecycle entities**
6. **Design activation for failure and recovery**
7. **Make product outcomes measurable**
8. **Use standardized interfaces where applicable**
9. **Build capabilities once and reuse them across products**
10. **Close the loop between strategy, execution and data**

---

# 26. Relationship to the Reference Architecture

This lifecycle document describes **why and when** product capabilities are needed.

The solution architecture describes **how those capabilities interact technically**.

```mermaid
flowchart LR

    PRODUCT["Product Lifecycle<br/><br/>WHY / WHAT / WHEN"]

    ARCH["Reference Architecture<br/><br/>HOW"]

    EXEC["Activation<br/><br/>EXECUTION"]

    DATA["Measurement<br/><br/>FEEDBACK"]

    PRODUCT --> ARCH
    ARCH --> EXEC
    EXEC --> DATA
    DATA --> PRODUCT
```

---

## Related Documentation

- [Project Overview](../README.md)
- [Reference Architecture](architecture.md)
- [ADR-001 — Domain Separation](design-decisions/ADR-001-domain-separation.md)
- `esim-lifecycle.md`
- `msisdn-lifecycle.md`
- `tmf-api-mapping.md`
- `sid-domain-model.md`

---

## Standards Boundary

This is an independent reference architecture.

TM Forum Open APIs and ODA/SID concepts are referenced for architecture and interoperability purposes. Official TM Forum specifications remain authoritative.

Project-specific lifecycle models, diagrams, capability groupings and architectural abstractions are not presented as official TM Forum definitions.

---

## Author

**Mohamed Salman**

Solution & Enterprise Architecture · Digital Platforms · Telecommunications · Data & AI

---

**Digital Telco Product Activation Architecture**

*From market opportunity to activated and measurable subscriber.*
