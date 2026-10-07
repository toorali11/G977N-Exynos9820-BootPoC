# Stage 15A — Early MMIO evidence

## Verified disassembly

The G977N BL2 candidate is loaded at `0x8f000000`.

The reset path contains:

- `0x8f00003c: bl 0x8f032948`
- `0x8f032948: ldr x0, [pc,#0x28]`
- `0x8f03294c: ldr w1, [pc,#0x18]`
- `0x8f032950: str w1, [x0]`
- `0x8f032954: ldr x0, [pc,#0x24]`
- `0x8f032958: ldr w1, [pc,#0x10]`
- `0x8f03295c: str w1, [x0]`
- `0x8f032960: ret`

The embedded literals resolve to:

- first target: `0x10430060`
- first value: `0x00003300`
- second target: `0x10430068`
- second value: `0x00000000`

Therefore the first identified peripheral operation is:

`*(volatile uint32_t *)0x10430060 = 0x3300;`

followed by:

`*(volatile uint32_t *)0x10430068 = 0x00000000;`

This is stronger evidence than merely finding the address in a binary string/literal scan.

## Harness consequence

The minimum early MMIO model should include the `0x10430000` window and specifically preserve/log writes to offsets `0x60` and `0x68`.

The UART remains the next high-value model from historical 9820 research:
- base `0x10440000`
- status `0x10440010`
- TX `0x10440020`
- RX/data `0x10440024`

We should not invent register semantics for the `0x10430000` block yet; the harness should initially log accesses and return conservative values.

## A/B rule

Stock BL2 and custom-v2 must execute against exactly the same device model. Any difference in execution trace is therefore attributable to the controlled diagnostic modifications, not to different MMIO behavior.

No authentication forcing, attestation manipulation, fuse operation, or physical flashing is part of this stage.
