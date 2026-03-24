# Integration Guide

The end-to-end workflow now supports direct verification, gateway-mediated verification, and audit bundle export.

## Direct flow

Manifest -> verifier -> TRQP policy lookup -> process appraisal -> result

## Gateway-mediated flow

Manifest -> verifier -> trust gateway -> TRQP policy lookup -> process appraisal -> result + gateway mediation trace

## Audit flow

Verification request -> verifier -> verification result -> audit bundle export
