# Issue 003: Add HTTP TRQP service

## Problem
The current mock TRQP service is in-process only.

## Why it matters
It does not yet exercise transport, serialization, or service deployment behavior.

## Proposed work
- expose authorization and recognition endpoints over HTTP
- preserve in-process mode for tests
- add service error handling
