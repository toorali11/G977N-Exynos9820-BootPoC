# Stage 17D — C9 Population Source Identified

## Decisive finding

The exact G977N stock BL2 contains an image-loading path that explicitly targets the C9 runtime window.

### Image descriptor

At runtime `0x8f0a625c` BL2 initializes the image descriptor:

- source/base: `0x8a000000`
- source length: `0x100000` (1 MiB)

The same descriptor stores an image/type-related value and is later consumed by the image loader.

### Type-5 C9 load

A loader path beginning around `0x8f102b5c` receives the descriptor.

After the image metadata is validated, the type-5 branch at:

`0x8f102e50`

passes:

- image handle: `x19`
- image/type value: `w20`
- destination: `0xc9000000`
- destination capacity: `0x1000000` (16 MiB)

into the common image loader at:

`0x8f1025e8`.

This is the strongest evidence so far for the C9 population mechanism.

## Intermediate buffer population

Another path at `0x8f0f8d78` explicitly uses:

`0x8a000000`

as a destination for a memcpy-like routine (`0x8f0fc780`).

The source is obtained from a parsed object returned by `0x8f124ffc`, which performs structured header/length parsing and builds object metadata.

This establishes the next chain:

```
parsed package/object
      |
      v
0x8a000000 intermediate buffer
      |
      v
type-5 image loader
      |
      v
0xc9000000 .. 0xca000000
      |
      v
C9 callback addresses
      |
      v
0x8f17ae78 callback dispatch
```

The exact package-to-`0x8a000000` source still needs to be identified, but the runtime destination chain is now concrete.

## Important size distinction

There are two relevant C9 sizes:

- registered primary C9 boot-RAM window: `0xc9000000 .. 0xc9c00000` (12 MiB)
- type-5 loader destination capacity: `0xc9000000 .. 0xca000000` (16 MiB)

Therefore the 12 MiB registered window and 16 MiB loader capacity must not be conflated. The extra 4 MiB may be scratch/adjacent runtime space.

## Emulator consequence

The first useful emulator can now model the exact boundary:

1. Map `0x8a000000` as the intermediate payload buffer.
2. Feed it a controlled representative payload/package object.
3. Implement the loader interface represented by `0x8f1025e8`.
4. Map `0xc9000000 .. 0xca000000`.
5. Instrument writes and execution in C9.
6. Only after the transfer path is understood, execute the callback table at `0x8f17ae78`.

This avoids guessing that raw CSMC bytes are directly executable.

## Remaining question

Identify exactly what `0x8f124ffc` parses and which stock sboot component supplies the object copied into `0x8a000000`.

The likely candidates are the secure/CSMC package areas already identified in the sboot layout, but this must be demonstrated by the call chain rather than assumed.

## Safety

Static analysis and emulation only. No fuse, key, authentication, secure-boot, or physical-flashing modification.
