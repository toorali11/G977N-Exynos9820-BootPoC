# Stage 17C — C9 Window Registration

## Confirmed facts

Static analysis of the exact stock G977N image found multiple independent uses of the C9 base.

### 1. Boot-RAM descriptor

At `0x8f013558` BL2 prepares a region descriptor containing:

- base `0xc9000000`
- size `0xc00000` (12 MiB)

and passes it to the common region-registration routine at `0x8f0100ac`.

The associated configuration strings identify this path as boot-RAM/memory setup, not an authentication bypass.

### 2. Runtime address-map boundaries

At `0x8f09c1dc` BL2 stores a set of boot memory boundaries including:

- `0xc9000000`
- `0xc9c00000`
- `0xc9d00000`
- adjacent secure/runtime regions

This independently confirms that `0xc9c00000` is treated as the end of the primary C9 window.

### 3. Callback execution

At `0x8f054628`:

- callback table = `0x8f17ae78`
- first entry is loaded
- `blr x0` executes it
- subsequent 64-bit entries are walked until zero.

The table is physically stored at `u-boot + 0x17ae78` / `sboot + 0x21ee78`.

### 4. C9 callback targets

The table targets:

```
0xc905456c
0xc9003414
0xc9004330
0xc904f254
0xc9047540
0xc90526d4
0xc9052754
0xc90a7814
0xc90036a8
0xc90045c0
0xc9042790
0xc90545ec
0xc905460c
0xc9054594
0x00000000
```

All targets lie inside the registered C9 window.

## Interpretation

We now have three independent pieces of evidence:

```
C9 package/data in stock sboot
        |
        v
BL2 registers 0xc9000000..0xc9c00000
        |
        v
runtime address map records 0xc9c00000 boundary
        |
        v
callback table points into that window
        |
        v
BL2 executes those addresses with BLR
```

The remaining unknown is population of the C9 window.

The small embedded ELF at `sboot + 0x1c3e2b` is not large enough to directly explain all callback targets. Therefore we should not assume the entire C9 callback code is simply the ELF's .text. The package may contain a loader plus a transformed/relocated payload, or the payload may be prepared by a secure-world operation.

## Next target

Trace calls involving:

- `load_secure_payload`
- `TEEGRIS_EXYNOS9820_CSMC`
- `CSMC: BEGIN`
- `Fail to load Secure Payload`
- SMC wrappers immediately preceding secure-payload setup

and identify the first source/destination/length tuple involving the C9 window.

## Emulator consequence

The first emulator should map:

- `0x8f000000` execution image
- ordinary RAM/stack
- UART/MMIO stubs
- `0xc9000000–0xc9c00000` as a dedicated runtime region

and log every write to the C9 region.

This gives us a deterministic breakpoint even before the exact C9 population mechanism is reproduced.

## Safety

Static analysis/emulation only. No fuse, key, authentication, secure-boot, or physical-flashing modification.
