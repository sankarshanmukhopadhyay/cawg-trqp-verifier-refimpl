# Issue 004: Add revocation delta channel

## Problem
Revocation data exists but is not actively applied as a delta-update mechanism.

## Why it matters
Cache-first and edge verification need timely trust invalidation.

## Proposed work
- apply revocations before authorization success
- define delta polling model
- add tests for revoked entities
