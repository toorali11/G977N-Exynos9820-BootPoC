# Stage 14A — Unicorn Harness Reconstruction

The historical S9 harness is being used as an emulation architecture reference, not as a security-bypass recipe.

## Minimal components confirmed

- Unicorn ARM64 engine
- Capstone for diagnostic disassembly
- BL2 mapped at 0x8f000000
- initial SP 0x8f600000
- UART 0x10440000..0x10440fff
- UART status 0x10440010
- UART TX 0x10440020
- additional MMIO is added only when execution requires it

The original Makefile links -lunicorn, -lcapstone and -pthread.

## G977N experiment design

The first harness should intentionally omit the historical S9 patch table and start with RAM regions, UART, basic system-controller reads, a trace hook, and an invalid-memory hook.

When S-Boot reaches an unsupported peripheral, record PC, LR, accessed address, read/write, width, and register state. Then add a narrowly scoped model for that peripheral.

This lets us identify which hardware assumptions are genuinely required by G977N S-Boot.

## Why this matters

A successful run will establish that our extracted G977N BL2 is executable independently of the Samsung firmware container. Only after that baseline will we compare the custom-v2 image.
