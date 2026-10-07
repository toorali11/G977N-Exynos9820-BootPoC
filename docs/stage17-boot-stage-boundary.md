# Stage 17 — Exynos 9820 Boot-Stage Boundary Plan

## Goal

Turn the existing static findings into a runnable, non-destructive emulator boundary for the G977N Exynos 9820 startup path.

This stage does not modify authentication, keys, fuses, secure-boot policy, or physical flashing.

## New public evidence

- Hubble explicitly lists Galaxy S10 5G / `beyondx` as tested Exynos 9820 support, with Creeeeger listed as the tester.
- Hubble is a USB recovery path that sends identified bootloader splits to the device; its public Exynos 9820 split configuration does not expose a separate C9 image.
- Houston publicly describes an Exynos BootROM payload/ACE workflow and supports Exynos 9820, but this is useful primarily as evidence of the earlier BootROM-to-payload boundary, not as a reason to reuse exploit code.

## Working model

```
BootROM / USB recovery
        |
        v
  early boot stages
        |
        v
  0x8f000000 execution region
        |
        +--> initialize MMIO / UART
        |
        +--> copy 0xc917fdf0 -> 0xc8fffff0
        |
        +--> clear 0xc917d000 .. 0xc97d16f8
        |
        v
  callback dispatcher @ 0x8f17ae78
        |
        +--> 0xc905456c
        +--> 0xc9003414
        +--> 0xc9004330
        +--> ...
        |
        v
  later boot-stage handoff
```

The C9 range is therefore treated as a runtime boundary, not assumed to be ordinary BL2-relative code.

## Immediate PoC milestones

### P0 — Rehydrate binary corpus

Recover the exact stock G977N firmware/binary corpus used for stages 10–16.

Required minimum:
- stock `sboot.bin`
- extracted/composite `u-boot.bin`
- stage-13 stock/custom BL2 candidates

Expected reference hashes:
- stock sboot SHA-256: `6c995f8a88bb6a8bdb54d604fe4a55b30d8985150d12a8ed9b9b35150a0f6665`
- stock u-boot SHA-256: `2a07e01c6497bba1e5ecaf72d991e4474cbadf87e19c99ee57adff570412fcc5`

### P1 — Build the smallest executable model

Use ARM64 Unicorn when available, with:
- BL2 mapped at `0x8f000000`
- stack and ordinary RAM
- UART stub at `0x10440000`
- minimal MMIO read/write hooks
- explicit unmapped-access logging

Do not emulate the entire SoC initially.

### P2 — Instrument the boundary

Log:
- first MMIO access
- every access touching `0xc8xxxxxx` / `0xc9xxxxxx`
- writes to `0x8f17ae78`
- indirect branches/calls at `0x8f054628`
- first execution attempt outside `0x8f000000`

This will tell us whether C9 is:
1. copied/relocated executable code,
2. populated by another boot component,
3. shared/runtime secure-world state, or
4. a data/function-pointer staging area.

### P3 — Resolve callback ownership

Once the exact binary is available, search for:
- all references to `0x8f17ae78`
- all stores whose destination resolves to that table
- all literals resolving into `0xc9000000–0xc9ffffff`
- package/ELF boundaries near the S-Boot/CSMC regions

Do not label C9 as CSMC until a load/copy/entry relationship proves it.

### P4 — Emulator success criterion

The first useful PoC is not a boot-to-Android emulator.

Success means:
1. reset entry executes,
2. early initialization completes,
3. UART output is reproduced or at least MMIO behavior is logged,
4. C9 initialization is reproduced,
5. callback dispatch is reached,
6. the first missing external stage is identified precisely.

At that point we can add only the missing component rather than emulating the whole platform.

## Important architecture finding

The Halal Beef/Hubble split named `u-boot.bin` is composite on this 9820 image: it exactly covers the full `sboot.bin[0x0A4000:0x224000]` range, which includes semantic S-Boot/BL2 plus the following CSMC-related regions. Therefore the Hubble split name must not be interpreted as proof that the entire range is one semantic Samsung BL2 image.

## Safety boundary

All work remains static analysis, emulation, and controlled instrumentation on owned hardware/images. No fuse programming, key extraction, secure-boot bypass, attestation bypass, or physical flashing is part of this PoC stage.
