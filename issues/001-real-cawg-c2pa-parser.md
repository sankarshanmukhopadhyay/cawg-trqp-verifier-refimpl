# Issue 001: Add real CAWG/C2PA parser

## Problem
The current implementation uses simplified JSON fixtures instead of real CAWG/C2PA manifests.

## Why it matters
This limits fidelity and prevents parser-level interoperability testing.

## Proposed work
- integrate manifest parser
- extract actor, issuer, and assertion signals from real fixtures
- preserve current simplified fixture path for tests
