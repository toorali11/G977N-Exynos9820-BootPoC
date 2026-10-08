# Stage 17F — DTB Container Boundary

## Decisive finding

The immediate source feeding the `0x8a000000 -> C9` path is loaded from a partition identified by the string `DTB`.

Relevant chain:

```
static partition-name table
        |
        | lookup("DTB")
        v
partition descriptor
        |
        v
load/transform into 0xb0000000
        |
        v
header validation
        |
        v
structured parser @ 0x8f124ffc
        |
        v
intermediate object
        |
        v
copy to 0x8a000000
        |
        v
type-5 image loader
        |
        v
0xc9000000
```

### Evidence

At `0x8f0f893c`, BL2 calls `0x8f0f2a68` with:

```
x0 = 0x8f18b400
```

The data at that address begins with the partition-name table:

```
DTB
VBMETA
...
PARAM
SYSTEM
SUPER
VENDOR
OPTICS
PRODUCT
PRISM
...
```

The lookup routine at `0x8f0f2a68` searches a static partition descriptor table and returns the descriptor corresponding to the supplied name.

The resulting descriptor is then used to load data into:

```
0xb0000000
```

BL2 subsequently checks the first 32-bit word at that address against the big-endian value:

```
0xd7b7ab1e
```

The same code validates a bounded length and then passes the loaded object into the structured parser at `0x8f124ffc`.

## Consequence

This changes the source hypothesis.

The current evidence does **not** support:

> raw CSMC bytes are directly copied into C9.

Instead, the stronger model is:

> BL2 obtains a structured payload from the DTB partition/container, parses it, extracts an image/object, and feeds that object through the type-5 loader into the C9 runtime region.

The exact semantic meaning of the `0xd7b7ab1e` container/header is not yet established. It should not be mislabeled as standard FDT/DTB magic.

## Missing corpus

The current local artifact set contains the exact BL tar and its `sboot.bin`, but not the corresponding DTB partition contents.

Therefore the next useful artifact is the matching G977N firmware component containing the `DTB` partition for:

```
G977NKSU6HWD3
```

Once that byte corpus is available, the parser can be matched directly against the container.

## Safe next step

Do not flash anything.

Acquire/locate the matching DTB bytes, hash them, and analyze them offline. The emulator fixture can then use the real DTB container as input while keeping authentication, fuses, rollback state, and device boot policy untouched.

## Confidence

High confidence that the immediate partition lookup is `DTB`.

Medium confidence that the `0xd7b7ab1e` object is the complete DTB container format; its internal semantics still require identification.

High confidence that the C9 load path consumes a parsed object rather than raw sboot bytes.
