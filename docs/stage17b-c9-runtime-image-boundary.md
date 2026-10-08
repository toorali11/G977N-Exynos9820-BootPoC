# Stage 17B — C9 Runtime Image Boundary

## Verified binary basis

Uploaded G977N BL package reproduces the previously recorded stock sboot SHA-256:

`6c995f8a88bb6a8bdb54d604fe4a55b30d8985150d12a8ed9b9b35150a0f6665`

The composite Hubble/Halal-Beef `u-boot.bin` is exactly `sboot[0xA4000:0x224000]` and is loaded for analysis at `0x8f000000`.

## Correct callback mapping

The dispatcher is real code at:

`0x8f054628`

It builds:

`0x8f17ae78`

and executes the entries with `blr x0`.

The corresponding composite-image file offset is:

`0x17ae78` in `u-boot.bin`

or:

`0x21ee78` in `sboot.bin`.

The complete callback list is stored there:

`c905456c, c9003414, c9004330, c904f254, c9047540, c90526d4, c9052754, c90a7814, c90036a8, c90045c0, c9042790, c90545ec, c905460c, c9054594, 0`.

## C9 package boundary

A second ELF header begins at:

`sboot + 0x1c3e2b`.

Its ELF entry point is `0x2000`. It contains a small PIE-style ELF loader/image with .text around virtual `0x2000` and writable data around `0x4000`.

Immediately after/around that ELF is a much larger CSMC-associated payload extending toward the `0x264000` boundary.

Crucially, the callback addresses are all in the `0xc9000000+` address space. Their offsets from `0xc9000000` line up with locations in this larger CSMC-associated payload region when treated as a runtime image boundary, rather than as ordinary BL2 addresses.

This does **not** yet prove that the raw payload is directly executable. Several callback targets land outside the small ELF's PT_LOAD ranges, so they may represent a runtime-transformed/decrypted/copied image.

## Strong loader evidence

BL2 constructs a memory-region descriptor with:

- destination/base: `0xc9000000`
- size: `0xc00000` (12 MiB)

at `0x8f013558`, then passes it through the common region-registration routine at `0x8f0100ac`.

Earlier startup also clears:

`0xc917d000 .. 0xc97d16f8`

and copies:

`0xc917fdf0 -> 0xc8fffff0`.

Therefore the C9 window is an explicit boot-time memory region, not an accidental address.

## Current interpretation

The strongest model is now:

1. BL2 reserves/registers a ~12 MiB C9 runtime window.
2. A CSMC-associated package is present in the stock sboot image.
3. BL2's static callback table points into the C9 runtime address space.
4. The exact population mechanism is still unresolved.
5. Because several callback addresses do not correspond to ordinary code bytes in the small embedded ELF, the runtime may involve a copy, relocation, decompression, decryption, or secure-world service before callbacks execute.

## Next binary-level target

Trace the caller chain around `0x8f013558` and all uses of the `0xc9000000` constant.

Then correlate those calls with:
- early SMC wrappers,
- CSMC/TEEGRIS loading strings,
- source/destination buffer descriptors,
- the UH/secure payload loader,
- and writes into the C9 window.

The first decisive result we want is one concrete operation of the form:

`source in sboot/CSMC -> destination 0xc9xxxxxx -> length`

or an SMC call whose arguments identify that transfer.

## Safety

Static analysis and emulation only. No fuse/key/authentication modification or physical flashing.
