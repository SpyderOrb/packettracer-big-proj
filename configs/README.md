# Device configurations

One current capture per device. Configuration files describe the supplied state; the [validation record](../docs/VALIDATION.md) identifies what was tested and which checkpoint was used.

| Device | Capture | Reviewed scope / limitation |
|---|---|---|
| HQ-L3 | [HQ-L3.cfg](HQ-L3.cfg) | VLAN gateways, LACP/STP and routed G0/1 at 10.255.1.2/30; opening lines before hostname are missing |
| HQ-R1 | [HQ-R1.cfg](HQ-R1.cfg) | Routed G0/0 at 10.255.1.1/30; opening lines before hostname are missing |
| HQ-SW1 | [HQ-SW1.cfg](HQ-SW1.cfg) | Access VLANs, Po1 trunk and secondary STP priority; supplied through end |
| HQ-SW2 | [HQ-SW2.cfg](HQ-SW2.cfg) | Access VLANs and Po2 trunk; supplied through end |

Reviewed 2026-09-13. The routed-link captures are newer than the reviewed pre-uplink v02 state. v02 was later resaved, so its current contents require verification. Complete export equality with a reopened checkpoint is not yet established. Captures are preserved as supplied; omitted commands have not been reconstructed. Other device exports and server service settings remain pending.

## Restore notes

- Before applying switch captures to a fresh device, create VLANs **10 MGMT, 20 IT, 30 USERS, 40 SERVERS, 50 GUEST and 999 PARKING** from the [design](../docs/NETWORK.md#vlans-and-addressing). VLAN definitions are absent from these captures; normal-range VLAN data can reside separately in `vlan.dat`. [Cisco VLAN storage guide](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-2940-series-switches/109304-manage-vlandat.html)
- Use the matching model and inspect the complete capture before applying it. Management SVIs on access switches, SSH, OSPF, DHCP relay, PAT and ACL policy are not yet represented in these files.
- Server-PT settings must be recorded separately when configured; IOS exports do not include them.

## Save and export

1. Run `copy running-config startup-config` on changed devices, then save the Packet Tracer working file separately.
2. Copy **all** of `show running-config`, including the opening configuration lines through the final `end`. Exclude prompts and pagination markers; record any redaction.
3. Preserve the previous export before replacing `<hostname>.cfg`. Record the checkpoint and its relevant verification results in [Validation](../docs/VALIDATION.md).
