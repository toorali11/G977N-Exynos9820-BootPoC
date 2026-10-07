# Stage 15B — UART initialization map

## G977N BL2 evidence

A concrete UART initializer exists at BL2 offset `0x2fd8` (runtime address `0x8f002fd8`).

It constructs the base `0x10440000` and writes these offsets:

- `+0x00`
- `+0x04`
- `+0x08`
- `+0x0c`
- `+0x20`
- `+0x28`
- `+0x2c`
- `+0xc4`
- `+0xc8`

The routine first obtains a clock/divisor-related value from another helper, then programs the UART registers. The exact register semantics are intentionally left unspecified until matched against the Exynos 9820 reference implementation.

A caller at BL2 offset `0x22e0` invokes this initializer at `0x2304`, so it is part of an ordinary initialization path rather than dead data.

## Emulation model

The next minimal UART model should:

1. map `0x10440000-0x10440fff`;
2. record all reads/writes;
3. return stable, conservative values for unimplemented registers;
4. capture writes to `+0x20` as candidate TX output;
5. avoid changing security/authentication state.

The `0x10430000` window from Stage 15A should be mapped separately and logged.

## A/B requirement

Use the identical MMIO behavior for stock and custom-v2. Compare:
- executed PC sequence;
- MMIO read/write sequence;
- UART TX bytes;
- first unmapped access;
- terminal stop reason.

No physical flashing is involved.
