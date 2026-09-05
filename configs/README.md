# Device configuration exports

**No configurations have been exported yet.**

Keep one complete configuration per network device, named after its hostname, for example `HQ-R1.cfg`. Export from the actual Packet Tracer device and identify the saved checkpoint; do not present handwritten commands as an observed running configuration. Working configurations may be exported for troubleshooting before tests pass; label their state as unvalidated.

Expected network devices: HQ-R1, KAT-R1, RZE-R1, ISP-R1, HQ-SW1, HQ-SW2, KAT-SW1, RZE-SW1, and WAN-SW.

At each export, record the checkpoint filename and export date below. The current files represent one checkpoint; use older `.pkt` checkpoints to recover previous states. Preserve older text exports in a checkpoint-specific archive if they already exist before replacement.

| Checkpoint | Export date | Devices exported |
|---|---|---|
| None | — | None |

Use dedicated lab credentials. Document any redaction or command-output cleanup. Record Server-PT GUI service settings alongside the exports as `HQ-SRV1.md` and `EXT-SRV1.md` when configured; they do not have IOS running-config exports. Record endpoint addressing in validation evidence.

## Save and export a device

1. Finish the current configuration slice and capture the requested checks, including failures.
2. Open the device CLI. Enter `enable` from a `>` prompt, or `end` from configuration mode, to reach the privileged EXEC prompt such as `HQ-R1#`.
3. Run `copy running-config startup-config`. If prompted for `Destination filename [startup-config]?`, press Enter. This saves the device startup configuration; also save the Packet Tracer `.pkt` checkpoint separately. [Cisco configuration file guide](https://www.cisco.com/c/en/us/td/docs/routers/ios/config/17-x/syst-mgmt/b-system-management/m_cm-config-files-0.html)
4. Run `show running-config`. If output pauses at `--More--`, press Space until the final `end` and device prompt are visible. Copy the complete configuration body into a plain-text file named `configs/<hostname>.cfg`; exclude pager markers, command prompts, and unrelated output. Report unsupported commands or missing output instead of filling gaps from memory.
5. Identify the checkpoint in the export table above and in your review message. During a small review, supply the changed devices and their link/routing peers as needed. Before claiming a complete checkpoint export, capture all nine network devices or explicitly verify that retained exports still match unchanged devices in that checkpoint.

Keep diagnostic `show` output in `docs/evidence/`, separate from `.cfg` files. A screenshot is useful for an error or GUI setting; text is easier to review for a complete configuration. Do not rewrite an export to match a proposed fix before applying that fix to the device and exporting again.
