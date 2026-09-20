# IR-003 — Missing DHCP relay on the Users subnet

**Status:** fault reproduced; addressing and intranet access recovered on 2026-09-20.

**Impact:** RZE-PC1 could not obtain a new DHCP lease while the relay address was missing from RZE-R1 G0/0.30. Other clients were not sampled.

**Source:** separate copy of the reviewed representative clean baseline. Local `IR-003_fault.pkt` and `IR-003_recovered.pkt` exist with distinct disk identities. Association with the screenshots follows the exercise context; neither saved file was independently reopened during review.

## Reproduction and diagnosis

```ios
configure terminal
interface GigabitEthernet0/0.30
 no ip helper-address 10.10.40.10
end
write memory
show running-config | section interface GigabitEthernet0/0.30
```

| Check | Expected | Actual and evidence |
|---|---|---|
| Users subinterface | Helper missing, other settings retained | VLAN 30, 10.30.30.1/27 and USERS_RZE_IN remain; no helper-address appears. Write memory reports OK ([configuration](evidence/helper_missing.png)) |
| Fresh DHCP request on RZE-PC1 | No lease obtained | DHCP request failed; address and mask fields are blank, gateway and DNS show 0.0.0.0 ([client](evidence/dhcp_failed.png)) |

The missing relay prevents the fresh request from reaching the remote DHCP service through this subinterface. No DHCP-server or ACL change was needed. Existing valid leases can conceal this fault, which is why the exercise requested a fresh acquisition.

## Recovery

```ios
configure terminal
interface GigabitEthernet0/0.30
 ip helper-address 10.10.40.10
end
write memory
```

The supplied console shows the helper restored and write memory completing successfully ([correction](evidence/helper_restored.png)). After a new DHCP request, RZE-PC1 receives **10.30.30.11/27**, gateway **10.30.30.1**, DNS **10.10.40.10**, with DHCP request successful ([lease](evidence/lease_restored.png)). The named intranet page loads ([service](evidence/intranet_restored.png)). Both addressing and the selected application service meet the expected recovery result.

## Escalation and prevention

If a fresh request still fails after restoring the helper, collect the client result and subinterface settings, then inspect relay reachability and DHCP policy. Include the helper address in the provisioning checklist for each remotely served client VLAN. Keep incident files separate from clean configuration exports and the baseline.
