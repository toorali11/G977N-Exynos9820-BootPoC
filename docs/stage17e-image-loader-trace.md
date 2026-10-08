# Stage 17E — Type-5 Image Loader Trace

## Scope

Static analysis of the exact G977N stock BL2/S-Boot from:

- firmware: G977NKSU6HWD3
- sboot SHA-256: `6c995f8a88bb6a8bdb54d604fe4a55b30d8985150d12a8ed9b9b35150a0f6665`
- semantic BL2 load base: `0x8f0a4000`

No device flashing or secure-boot modification is involved.

## New finding

The C9 load is a generic image-loader operation, not a direct branch into an embedded raw C9 blob.

At `0x8f102b5c`, the loader receives an image/object handle in x0 and an image/type value in w1. The successful path eventually reaches:

```
0x8f102e50:
    x0 = image/object handle
    w1 = parsed image/type result
    x2 = 0xc9000000
    x3 = 0x01000000   # 16 MiB capacity
    x4 = descriptor @ BL2 static data
    x5 = descriptor @ BL2 static data
    bl 0x8f1025e8
```

Thus the loader explicitly targets `0xc9000000` with a 16 MiB capacity.

This must not be confused with the earlier runtime registration:

```
0xc9000000 .. 0xc9c00000   # 12 MiB registered C9 boot-RAM window
```

The remaining 4 MiB is not yet classified.

## Loader internals

`0x8f1025e8` is the common image-loader routine. It first calls `0x8f102418` twice, then processes additional metadata before returning to the caller.

`0x8f102418` begins by calling `0x8f0ff60c` to obtain/validate a structured image object. It then reads a 32-bit header field and performs explicit byte-order reconstruction. The following fields are checked against supplied lengths/types.

The second-stage validation path at `0x8f100e70` also treats the input as a structured image object. It reads:

- header word at +0x4
- secondary fields at +0x14 and +0x20
- bounded entry/record counts
- calculated record sizes

This is strong evidence that x0 at the type-5 loader is a parsed package/image object rather than a raw executable pointer.

## Intermediate buffer

Earlier startup code constructs an image descriptor containing:

```
base/temporary buffer = 0x8a000000
length                  = 0x00100000  # 1 MiB
```

A later path at `0x8f0f8d78` explicitly copies data into `0x8a000000` using BL2's internal memcpy routine `0x8f0fc780`.

The copy source is associated with the parsed object produced by the package-processing path. The exact package identity is still unproven.

Therefore the current model is:

```
package / structured image
        |
        v
parse + validate
        |
        v
0x8a000000 intermediate buffer
        |
        v
generic type-5 image loader
        |
        v
0xc9000000 (16 MiB loader capacity)
        |
        v
C9 runtime image
        |
        v
callback table @ 0x8f17ae78
```

## Important correction

The current evidence does **not** justify calling the source object "CSMC" yet.

The exact caller/input relationship for the parser at `0x8f124ffc` still needs to be established. The safe label is:

> structured boot/package image object

Only after its caller and backing bytes are identified should it be mapped to CSMC, SPKG, UH, or another Samsung package component.

## Next analysis target

1. Enumerate all callers of `0x8f124ffc`.
2. Identify the argument supplying x0/x1/x2/x3 at the relevant caller.
3. Trace the backing bytes to a concrete region of the 4 MiB sboot corpus.
4. Compare that region against the known CSMC/SPKG/package boundaries.
5. Trace the type-5 object into `0x8f1025e8`.
6. Record the first write into `0xc9000000+` as the emulator boundary.

## Safety boundary

This stage intentionally stops at image/package loading and runtime mapping. It does not alter authentication, rollback counters, keys, fuses, or secure-boot policy.
