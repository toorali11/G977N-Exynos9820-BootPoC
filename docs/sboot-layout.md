# G977N S-Boot Layout

Verified semantic regions of stock G977N sboot.bin:

| Region | Full-image range |
|---|---|
| EPBL | 0x000000..0x013C00 |
| ACPM | 0x013C00..0x027800 |
| PM code | 0x027800..0x04CC00 |
| PM/charger/PMIC data | 0x04CC00..0x0A4000 |
| BL2 / S-Boot | 0x0A4000..0x1B5000 |
| CSMC package | 0x1B5000..0x264000 |
| TEEGRIS kernel | 0x264000..0x2A0078 |
| TEEGRIS package | 0x2A0078..0x2D8000 |
| startup loader | 0x2D8000..0x2EC697 |
| metadata/reserved | 0x2EC697..0x363DF0 |
| signing metadata tail | 0x363DF0..0x400000 |

Hubble/Halal Beef correlation:
- u-boot.bin = sboot.bin[0x0A4000:0x224000]
- el3_mon.bin = sboot.bin[0x224000:0x264000]

Thus Hubble u-boot.bin is a composite artifact: its beginning contains semantic S-Boot followed by additional CSMC material.
