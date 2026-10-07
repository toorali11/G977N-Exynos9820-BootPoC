# Stage 16 — Runtime Callback / C9 Memory Boundary

## Scope
Static analysis of the G977N Exynos 9820 S-Boot/BL2 startup path, focusing on the callback table observed at runtime address `0x8f17ae78` and its `0xc9xxxxxx` targets.

This stage is observational only. No fuse, key, authentication bypass, or physical flashing is involved.

## Key evidence

1. Reset reaches `0x8f054628` after early initialization.
2. `0x8f00005c` copies from `0xc917fdf0` to `0xc8fffff0`.
3. `0x8f000070` clears `0xc917d000` through `0xc97d16f8`.
4. `0x8f054628` dispatches a callback table at `0x8f17ae78` using `blr x0`.
5. The table contains pointers such as `0xc905456c`, `0xc9003414`, `0xc9004330`, `0xc904f254`, `0xc9047540`, `0xc90526d4`, `0xc9052754`, and `0xc90a7814`.

## Early C9 initialization literals

| BL2 offset | value |
|---:|---:|
| `0x0cd0` | `0xc9250dc8` |
| `0x0cd8` | `0xc917fdf0` |
| `0x0ce0` | `0xc8fffff0` |
| `0x0ce8` | `0xc917d000` |
| `0x0cf0` | `0xc97d16f8` |

The clear span is approximately `0x60,000` bytes. This is strong evidence that the C9 address range is a real runtime memory boundary used during stock startup.

## Callback dispatcher

At `0x8f054628`, the code forms `0x8f17ae78`, loads the first 64-bit entry, conditionally calls it with `blr`, then walks subsequent 8-byte entries until a zero entry is reached.

Observed table entries begin:

`0x8f17ae78 = 0xc905456c`
`0x8f17ae80 = 0xc9003414`
`0x8f17ae88 = 0xc9004330`
`0x8f17ae90 = 0xc904f254`
`0x8f17ae98 = 0xc9047540`
`0x8f17aea0 = 0xc90526d4`
`0x8f17aea8 = 0xc9052754`
`0x8f17aeb0 = 0xc90a7814`

The first eight values occur only at their table positions in the extracted `u-boot.bin`, so they are pointer-like runtime state rather than ordinary duplicated constants in the BL2 image.

## Interpretation

The BL2-only emulator boundary is now known to be incomplete. Stock startup executes from the `0x8f000000` region, explicitly initializes a separate `0xc9xxxxxx` runtime window, and later dispatches function pointers into that window.

The remaining unknown is ownership/loading: which boot component populates the C9 executable/runtime region and when the callback table receives these pointers. We should not guess the target code or map it as BL2-relative code.

## Next target

1. Identify the component associated with `0xc917d000–0xc97d16f8`.
2. Trace writes/population of `0x8f17ae78`.
3. Determine whether the C9 code comes from BL2 relocation, CSMC/secure-world state, or another boot-stage handoff.
4. Extend the emulator only after that boundary is identified.

## Safety boundary

No authentication, key, fuse, or secure-boot policy modification is part of this stage. The goal is stock control/data-flow reconstruction in an emulator.