# Stage 15 — G977N/Exynos 9820 static MMIO map

## Result

Static AArch64 disassembly of the extracted G977N BL2 candidate is working with LLVM 17 after wrapping the flat binary as an ELF section.

Verified candidates:
- stock BL2: 0x110000 bytes
- custom-v2 BL2: 0x110000 bytes
- stock SHA-256: c750d41dce6583bfe1fe94f05c98704a5b2f31903123afcc895d93dd279bfd0d
- custom-v2 SHA-256: 4e7f427456f79177c9c26c1745e89a8bddcffae91ceeb857e45d27c1c5627e0b

## Early execution

Entry path:
`0x000000 -> 0x00000004 -> 0x0000003c -> 0x00032948 -> 0x00000040 -> 0x0000005c -> 0x00000070 -> 0x00000048 -> 0x00000054 -> 0x00054628`.

The first clearly identified memory-mapped peripheral accesses occur in the initialization routine at 0x32948:

- read-modify/write target at `0x10430060`
- second target at `0x10430068`

These are strongly consistent with the Exynos 9820/9810-era peripheral/pinctrl region: Linux DTS material places pinctrl at `0x10430000`. This is a useful anchor, but we should not assume the exact register semantics from the Linux driver without a 9820-specific match.

The BL2 also contains an explicit UART block at `0x10440000`:
- status: `0x10440010`
- TX: `0x10440020`
- RX/data-related access: `0x10440024`

This matches the historical Exynos 9820 emulator/UART model and gives us a high-confidence first console device for the harness.

Other statically identified device bases include:
- `0x10510000` — PMU/PWM-related access cluster
- `0x10c00000` — USB-related access cluster
- `0x11100000` — PHY-related access
- `0x11110000` — UFS-related access
- `0x14060000` — system-controller-related access
- `0x141c0000` — speedy-related access
- `0x14230000` — ADC-related access
- `0x15860000` — debug/controller register cluster
- `0x16010000` and `0x16080000` — display/DSIM-related access

## Important QEMU implication

The 0x110000-byte BL2 candidate is sufficient for code disassembly, but not necessarily sufficient as a standalone runtime image. The code references RAM/global structures at addresses such as `0x178000+` and `0x3e5000+`. Those references are runtime memory/data structures, not proof that those bytes must be present in the extracted BL2 file.

Therefore the next harness should map:
1. BL2 at the historical load address `0x8f000000`
2. a larger RAM window covering the observed global/data addresses
3. UART at `0x10440000`
4. the early `0x10430000` peripheral window
5. minimal read/write stubs for additional MMIO only when execution reaches them

No security-check forcing or verdict manipulation is part of this harness.

## Next step

Build a G977N-specific Unicorn memory model from the observed access sequence. The first milestone is simply to let stock BL2 execute farther than the first peripheral access while logging every unmapped read/write. Custom-v2 remains the A/B test image; no fuse operations or destructive flashing are required.
