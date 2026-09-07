# Device configuration exports

**Status:** no configurations exported yet.

Store one complete configuration per network device as `<hostname>.cfg`: HQ-L3, HQ-R1, KAT-R1, RZE-R1, ISP-R1, HQ-SW1, HQ-SW2, KAT-SW1, RZE-SW1, and WAN-SW (ten devices).

## Save and export a device

1. From the privileged EXEC prompt, run `copy running-config startup-config` and accept the default destination if prompted. Save the `.pkt` checkpoint separately. [Cisco configuration guide](https://www.cisco.com/c/en/us/td/docs/routers/ios/config/17-x/syst-mgmt/b-system-management/m_cm-config-files-0.html)
2. Run `show running-config`, advance through every output page, and copy the complete configuration through the final `end` into `<hostname>.cfg`. Exclude CLI prompts and pager markers; record any redaction. Use dedicated lab credentials.
3. Identify the corresponding checkpoint below. Keep earlier exports in a checkpoint-specific archive when replacing them. Record diagnostic output in `docs/evidence/`.

Exports must reflect the actual devices, including configurations awaiting validation. Record Server-PT service settings as `HQ-SRV1.md` and `EXT-SRV1.md`; these devices do not provide IOS configuration exports.

| Checkpoint | Export date | Devices exported |
|---|---|---|
| None | — | None |
