---
layout: default
title: "Implementation Notes"
description: "Compatibility notes and implementation-level clarifications."
parent: "Architecture & Deployment"
nav_order: 6
---
# Implementation Notes

- The verifier remains backward compatible with v0.7.0 request shapes.
- Gateway mediation is optional and only affects live policy routing.
- Audit bundles are exported as JSON in the reference implementation.
- Benchmark fixtures provide deterministic payloads for high-volume and constrained-device scenarios.
