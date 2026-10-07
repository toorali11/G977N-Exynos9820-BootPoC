# Stage 15C — Runtime-state boundary

## Finding

The reset sequence reaches BL2 offset `0x54628`.

That routine loads a callback pointer from a global location corresponding to runtime address `0x17ae78`, then iterates through an 8-byte callback table and invokes each non-null pointer with `blr`.

The `0x17ae78` location is outside the semantic BL2 candidate (`0x000000-0x10ffff`). In the verified full `u-boot.bin` it contains pointer-like values, including:

- `0xc905456c`
- `0xc9003414`
- `0xc9004330`
- `0xc904f254`
- `0xc9047540`
- `0xc90526d4`
- `0xc9052754`
- `0xc90a7814`

These values are not BL2-relative addresses, so they should not be treated as ordinary in-image function addresses without further relocation/runtime mapping analysis.

## Consequence

The historical `-bios`/BL2-only model is useful as an architectural reference, but for G977N we need to reproduce the relevant runtime state surrounding BL2:

- callback/global table storage;
- any relocation performed before BL2 reaches `0x54628`;
- external code/data regions referenced by the callback pointers;
- the same UART and `0x10430000` MMIO windows.

The safest next step is therefore **not** to fabricate callback targets. Instead, trace how those pointers are initialized and determine whether they point into another extracted component, a relocated RAM image, or a firmware service region.

## Safety boundary

This is static/runtime-structure analysis only. No secure-boot or attestation bypass is being developed.
