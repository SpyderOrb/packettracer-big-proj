# IR-002 — OSPF disabled on the branch WAN interface

**Status:** fault reproduced; OSPF neighbors and internal application service recovered on 2026-09-20.

**Impact:** KAT-PC1 could reach its local gateway but could not resolve the internal site name while KAT-R1 had no OSPF neighbors. Other remote services were not sampled.

**Source:** separate copy of the reviewed representative clean baseline. Local `IR-002_fault.pkt` and `IR-002_recovered.pkt` both exist with distinct disk identities. Screenshots document the exercise; the saved incident files were not independently reopened during review. Clean exports remain separate in [configs](../../configs/README.md).

## Reproduction and diagnosis

On KAT-R1:

```ios
configure terminal
router ospf 1
 passive-interface GigabitEthernet0/1
end
write memory
```

| Check | Expected | Actual and evidence |
|---|---|---|
| WAN interface | Remains up/up | G0/1, 10.255.0.2, remains up/up; this is not a physical-link shutdown ([output](evidence/passive_wan_no_neighbors.png)) |
| OSPF | Neighbors disappear | Both neighbors transition FULL to DOWN; neighbor table is empty. Configuration retains passive-interface default without a G0/1 no-passive exception ([output](evidence/passive_wan_no_neighbors.png)) |
| Local connectivity | Local gateway stays reachable | KAT-PC1 ping 10.20.30.1 succeeds 4/4 ([ping](evidence/local_gateway_reachable.png)) |
| Internal service | Named intranet access fails | Browser shows Host Name Unresolved ([browser](evidence/intranet_resolution_failure.png)) |

The cause is the passive OSPF transit interface. [Cisco documents that OSPF passive interfaces suppress Hello packets](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_pi/configuration/xe-16-12/iri-xe-16-12-book/iri-default-passive-interface.html). The neighbor log says Interface down or detached, but the interface table confirms the physical link stayed up. The browser demonstrates name-resolution failure during the routing fault, not a direct HTTP-server test. No convergence time was measured.

## Recovery

In the separate recovery copy:

```ios
configure terminal
router ospf 1
 no passive-interface GigabitEthernet0/1
end
write memory
```

Both peers returned on G0/1: router ID **10.255.255.1 FULL/BDR**, address 10.255.0.1, and **10.255.255.3 FULL/DR**, address 10.255.0.3 ([restored neighbors](evidence/neighbors_restored.png)). The final process configuration includes the restored G0/1 exception and unchanged area 0 networks; write memory reports OK ([restored configuration](evidence/ospf_exception_restored.png)).

The earlier screenshots confirm OSPF recovery at that time. An initial follow-up in the reported recovery-file context still showed [Host Name Unresolved](evidence/recovery_intranet_unresolved.png). The latest supplied screenshot now shows KAT-PC1 successfully loading **http://intranet.lab.example** ([restored service](evidence/intranet_restored.png)), confirming application recovery as well.

No intervening configuration change or elapsed time was reported. The cause of the intermediate resolution failure is therefore undetermined; it is not attributed to a DNS change or a measured convergence delay. The requested additional client settings and direct-IP tests are no longer needed to establish the demonstrated service outcome.

## Escalation and prevention

If neighbors remain absent after correction, compare link state and OSPF process/interface settings with peers before changing shared routing or ACL policy. Review transit-interface exceptions after applying passive-interface-default templates. Preserve the fault and recovery files separately from the clean baseline.
