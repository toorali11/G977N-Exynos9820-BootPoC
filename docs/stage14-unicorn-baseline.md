# Stage 14 — Unicorn Baseline

## Finding

The historical S9 S-Boot emulator is a stronger immediate baseline than rebuilding the old QEMU tree.

It:
- uses Unicorn ARM64;
- loads a flat BL2 image at `0x8f000000`;
- initializes SP at `0x8f600000`;
- emulates the Exynos UART at `0x10440000`;
- treats UART status as offset `0x10` and TX as offset `0x20`;
- maps additional SoC/MMIO regions and supplies callbacks for chip ID, system controller, timer, UFS, USB and PMIC behavior.

The historical source is `tzf-omkey/s9-sboot-emu`.

## G977N adaptation rule

We will not copy S9-specific hook addresses blindly.

The safe sequence is:

1. Use our G977N BL2 candidate at `0x8f000000`.
2. Start with only generic memory + UART support.
3. Record the first unmapped MMIO access.
4. Add one narrowly scoped emulation stub at a time.
5. Never add authentication-bypass hooks.
6. Compare stock and custom-v2 execution traces.
7. Stop at the first meaningful handoff/authentication boundary.

## Important distinction

The S9 emulator contains patches that redirect certain device/authentication functions for its own research. Those patches are **not** being copied into the G977N harness. Our baseline should observe normal code execution rather than artificially making security checks succeed.

## Current blocker

The current execution environment lacks Unicorn/Capstone and qemu-system-aarch64. The source architecture is now understood; the next practical step is obtaining a local build environment with Unicorn + Capstone or equivalent ARM64 emulation support.

## Expected first observable

The first useful success criterion is not Download Mode or secure-boot acceptance.

It is simply:

`G977N stock BL2 -> emulator starts -> UART activity -> controlled stop/trace`

Then:

`G977N custom-v2 BL2 -> same baseline -> distinguishable execution trace`

