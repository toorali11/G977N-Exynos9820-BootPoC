#!/usr/bin/env python3
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks={'artifacts/G977N_sboot_bl2_stock.bin':0x110000,'artifacts/G977N_sboot_bl2_custom_v2.bin':0x110000}
for rel,expected_size in checks.items():
 p=ROOT/rel; data=p.read_bytes(); print(f'{rel}: size=0x{len(data):x} sha256={hashlib.sha256(data).hexdigest()}'); assert len(data)==expected_size
print('stage13 verification: OK')
