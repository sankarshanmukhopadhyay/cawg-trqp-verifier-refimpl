# Issue 002: Add signed policy snapshots

## Problem
Offline snapshot behavior is modeled but snapshot signatures are not verified.

## Why it matters
Edge and disconnected verification need trustworthy snapshot provenance.

## Proposed work
- define snapshot signature format
- verify signatures before loading
- add snapshot freshness and expiry enforcement
