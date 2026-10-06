# G977N Exynos 9820 Boot PoC

Non-destructive reverse-engineering and emulation research for Samsung Galaxy S10 5G (SM-G977N, Exynos 9820).

## Scope

This repository tracks analysis of Samsung S-Boot/BL2 layout, controlled diagnostic binary modifications, and an emulation path based on public Exynos 9820 research.

Safety boundary: offline analysis/emulation only. No private signing keys, fuse operations, or secure-boot defeat instructions.

## Current status

- G977N stock sboot.bin mapped.
- Samsung u-boot.bin / Hubble split relationship established.
- Semantic G977N S-Boot/BL2 region identified as full-image 0x0A4000..0x1B5000.
- Controlled custom S-Boot PoC v2 produced.
- Public Exynos 9820 QEMU research mapped.
- Stage 13 emulation candidates prepared.
- Next target: reproduce historical Exynos 9820 QEMU environment and compare stock vs custom BL2 UART/control flow.

## Device

SM-G977N / Galaxy S10 5G / Exynos 9820 (beyondxks).
