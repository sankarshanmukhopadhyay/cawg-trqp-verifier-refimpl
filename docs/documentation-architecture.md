---
layout: default
title: Documentation Architecture
nav_order: 2
parent: Documentation
permalink: /docs/documentation-architecture/
has_toc: true
---
# Documentation Architecture

The site separates orientation, implementation contracts, operations, assurance evidence and industry adoption so readers can move from intent to a testable deployment without treating all documents as equally authoritative.

| Layer | Purpose | Start page | Evidence or decision |
|---|---|---|---|
| Orientation | Establish value, scope and route | [Guided learning](guided-learning.md) | Audience route and completion criteria |
| System model | Explain components and boundaries | [Architecture](architecture.md) | Trust-boundary and responsibility model |
| Integration contracts | Define inputs, transport and outputs | [Integration guide](INTEGRATION_GUIDE.md) | Interoperable implementation |
| Governance and assurance | Explain TRQP, policy and receipts | [How TRQP enables assurance](how-trqp-enables-assurance.md) | Governed decision chain |
| Operations | Deploy, scale, refresh and recover | [Deployment guide](deployment-guide.md) | Operational control evidence |
| Risk and privacy | Identify threats, harms and obligations | [Threats](threats-and-risks/index.md), [privacy](privacy/index.md) | Residual-risk and data-handling decisions |
| Adoption | Convert capability into institutional action | [Industry adoption](industry-adoption/index.md) | Pilot and governance plan |

The maintained routes are declared in `_data/learning_paths.json`. `scripts/validate_learning_paths.py` checks that every step resolves to a repository file and states a concrete outcome.

[Choose your route →](guided-learning.md)
