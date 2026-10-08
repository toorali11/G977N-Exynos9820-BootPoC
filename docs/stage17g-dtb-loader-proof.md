# Stage 17G — DTB Loader Proof

## Exact lookup chain

At runtime 0x8f0f8bd0, BL2 passes x0 = 0x8f18b400 to 0x8f0f893c. The corresponding bytes contain the static names DTB, VBMETA, PARAM, etc.

Inside 0x8f0f893c the first operation is a call to 0x8f0f2a68. That lookup routine saves the supplied string pointer, iterates a separate runtime partition-descriptor table, compares entries, and returns the matching descriptor.

Important distinction: 0x8f18b400 is the static partition-name string table; the descriptor table itself is a separate runtime structure referenced through 0x8f4a8fb0.

## DTB load

After resolving the DTB descriptor, 0x8f0f893c extracts descriptor-derived big-endian fields and calls 0x8f0fc780 with destination 0xb0000000. The loaded object is then checked at 0xb0000000.

The first 32-bit word is byte-swapped and compared against 0xd7b7ab1e. The next word is byte-swapped and bounded by 0x08000000. This establishes a bounded container/image format rather than a raw executable.

## Structured-object handoff

The loaded object enters the processing path that reaches 0x8f124ffc. That parser returns an object pointer, which is copied into 0x8a000000 through 0x8f0fc780. The resulting object becomes input to the later type-5 image loader.

## Current chain

static name DTB → partition descriptor lookup → descriptor-derived partition read → 0xb0000000 → header 0xd7b7ab1e → structured parser 0x8f124ffc → 0x8a000000 → type-5 image loader → 0xc9000000 → C9 runtime image.

## Limitation

The exact physical/file bytes corresponding to the DTB partition are not present in the currently uploaded BL tar. The matching firmware version is confirmed by LineageOS as SM-G977N / G977NKSU6HWD3, with sboot.bin, uh.bin, cm.bin and other firmware components separately identified.

The next artifact needed for byte-for-byte reconstruction is the matching AP/DTB partition from the same firmware revision.

## Safety

All work remains offline/static. No flashing, fuse programming, authentication bypass, or secure-boot modification is performed.
