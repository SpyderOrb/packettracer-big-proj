# IR-001 — Access port placed in the Guest VLAN

**Status:** fault reproduced; client service recovered on 2026-09-20.

**Impact:** HQ-PC1 lost internal site access after its access port was moved from Users VLAN 30 to Guest VLAN 50. One workstation was affected in the supplied test.

**Source:** v12 baseline candidate, selected reopen checks passed. Local incident files: `IR-001_fault.pkt` and `IR-001_recovered.pkt`; both exist with distinct disk identities. Test association follows the supplied task context; neither incident file was independently reopened during review. Clean configuration exports are kept separately in [configs](../../configs/README.md).

## Reproduction and diagnosis

The assigned change was `switchport access vlan 50` on HQ-SW1 Fa0/1, followed by a DHCP request on HQ-PC1.

| Observation | Actual result | Evidence |
|---|---|---|
| Client addressing | DHCP succeeds with 10.10.50.11/27, gateway 10.10.50.1, DNS 203.0.113.10: Guest settings instead of Users | [guest lease](evidence/guest_lease.png) |
| Internal site | http://intranet.lab.example displays Host Name Unresolved | [intranet failure](evidence/intranet_failure.png) |
| Access port | show vlan brief places Fa0/1 in VLAN 50; show interfaces Fa0/1 switchport reports static access, Access Mode VLAN 50 (GUEST) | [wrong vlan](evidence/wrong_vlan.png) |

The cause is the incorrect access VLAN, not DHCP-server unavailability: DHCP successfully supplies the settings for the wrong segment. The observed browser failure is name resolution with the external DNS setting. No direct-IP HTTP test or ACL-drop measurement is claimed for this incident.

## Recovery

The assigned correction in a separate recovery copy was:

```ios
configure terminal
interface FastEthernet0/1
 switchport access vlan 30
end
write memory
```

After another DHCP request, HQ-PC1 received **10.10.30.10/26**, gateway **10.10.30.1**, DNS **10.10.40.10** ([users lease restored](evidence/users_lease_restored.png)). The named intranet page then loaded successfully ([intranet restored](evidence/intranet_restored.png)). Recovery is demonstrated by client addressing and service restoration; no separate post-fix switchport output was supplied.

## Escalation and prevention

If correct addressing does not return after restoring the intended VLAN, escalate with the port/VLAN output and client IP settings before changing shared DHCP or ACL configuration. Include an access-VLAN and lease/service check in workstation moves. Preserve the fault copy separately from recovery and the clean baseline.
