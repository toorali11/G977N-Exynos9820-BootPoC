# Exynos 9820 QEMU Research

The historical astarasikov/qemu exynos9820 branch provides a QEMU-based environment for running Exynos 9820 S-Boot.

Relevant details:
- BL2 fallback load address: 0x8f000000
- Fake peripheral window: 0x00000000..0x1fffffff
- Fake IMEM: 0x20000000..0x21ffffff
- Fake TZMEM: 0x22000000..0x23ffffff
- UART status register: 0x10440010
- UART transmit register: 0x10440020
- Basic UFS, timer, PMU/DBGC and other MMIO stubs are supplied.

The historical S9 emulator tzf-omkey/s9-sboot-emu independently documents the same BL2 load address and UART behavior.

The old environment is preferable to inventing a new hardware model because the objective is to reproduce observed S-Boot behavior.

Reproducibility note: the historical branch is old and the current execution environment does not provide qemu-system-aarch64. Stage 14 therefore focuses first on reconstructing the build environment and validating loader assumptions.
