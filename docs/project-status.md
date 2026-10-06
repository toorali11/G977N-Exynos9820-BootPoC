# Project Status

## Stage 13 — QEMU research

The public astarasikov/qemu exynos9820 branch uses a raw second-stage bootloader image at load address 0x8f000000.

The public S9 S-Boot emulator independently uses the same BL2 base address and expects an extracted sboot_bl2.bin.

For G977N, verified firmware mapping gives:
- full sboot.bin: 0x400000 bytes
- semantic S-Boot/BL2: 0x0A4000..0x1B5000
- size: 0x110000 bytes
- Hubble/Halal Beef u-boot.bin: full sboot.bin[0x0A4000:0x224000]

Therefore the emulation candidate is the first 0x110000 bytes of G977N u-boot.bin.

## Custom v2

1. u-boot + 0x54654: 00 00 80 52 -> E0 03 1F 2A
2. u-boot + 0xE6D60: Samsung -> Custom!

The first is behavior-preserving; the second is a diagnostic marker. Neither is intended to bypass authentication.

## Next

1. Build/reconstruct historical Exynos 9820 QEMU.
2. Boot stock BL2 in emulation.
3. Boot custom BL2.
4. Compare UART and early execution behavior.
5. Continue trust-chain mapping only after baseline is reproducible.
