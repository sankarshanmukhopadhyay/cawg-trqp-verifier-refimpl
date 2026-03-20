# Implementation Notes

## Current simplifications

- Asset integrity is modeled through fixture fields rather than a full binary parser.
- CAWG identity extraction is modeled through fixture content.
- TRQP is served by an in-process mock service backed by JSON policy files.
- Offline behavior is modeled using signed-snapshot-like local state, without actual signature verification.

## Why this is acceptable at this stage

The purpose of this repo is to make the **position and function of TRQP** implementation-clear. It shows where governance lookup belongs in the pipeline and how different verifier profiles behave under varying constraints.
