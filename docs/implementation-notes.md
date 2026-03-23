# Implementation Notes

## Current simplifications

- Asset integrity is modeled through fixture fields rather than a full binary parser.
- CAWG identity extraction is modeled through fixture content.
- TRQP is served by an in-process mock service backed by JSON policy files.
- Process evidence appraisal uses a compact scoring model rather than a full Proof of Process verifier stack.
- Offline behavior is modeled using signed snapshot state plus local process appraisal.

## Why this is acceptable at this stage

The purpose of this repo is to make the **position and function of TRQP** implementation-clear while showing how process evidence can alter trust outcomes without turning TRQP itself into an evidence-generation protocol.

## Selective adoption model

This repo deliberately does not import the full Proof of Process stack. Instead it adopts three patterns that are strategically useful here:

1. evidence packets can be represented as manifest-bound process assertions
2. appraisal output can be represented as a structured confidence-bearing object
3. policy can express when process proof is required for a trusted outcome

That keeps boundaries clean:

- process evidence remains an input
- TRQP remains the policy authority
- the verifier remains the synthesis engine
