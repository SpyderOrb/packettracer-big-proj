# IR-004 — Required HTTP permit removed from a Users ACL

**Status:** fault reproduced; internal HTTP service recovered on 2026-09-20.

**Impact:** RZE-PC1 could not access the internal web server, while the external site remained available. One client was sampled.

**Source:** separate copy of the reviewed representative clean baseline. Local `IR-004_fault.pkt` and `IR-004_recovered.pkt` exist with distinct disk identities. Screenshot association follows the exercise context; neither incident file was independently reopened during review.

## Reproduction and diagnosis

The supplied RZE-R1 console shows:

```ios
configure terminal
ip access-list extended USERS_RZE_IN
 no permit tcp 10.30.30.0 0.0.0.31 host 10.10.40.10 eq 80
end
write memory
show access-lists USERS_RZE_IN
```

| Check | Expected | Actual and evidence |
|---|---|---|
| Internal HTTP by IP | Fails without the permit | http://10.10.40.10 returns Request Timeout ([browser](evidence/internal_http_timeout.png)) |
| External HTTP by name | Remains available | http://www.lab.example loads the external page ([browser](evidence/external_http_allowed.png)) |
| Users ACL | Internal HTTP permit missing; final deny present | USERS_RZE_IN has no internal TCP/80 permit. External HTTP permit remains with 6 matches, UDP DNS permit has 1, final deny has 12; DHCP broadcast permit has 5 ([ACL](evidence/missing_permit_counters.png)) |

The removed permit leaves internal HTTP subject to the final deny. Testing the internal server by IP bypasses DNS resolution, while the successful external request shows that the sampled client path is not completely disconnected. Counters are observed totals: no before snapshot was supplied, so the 12 denies are not claimed as an exact increase or attributed individually to this request. Startup configuration saving is shown during fault injection.

## Recovery

The assigned correction in a separate recovery copy restores the permit before the final explicit deny:

```ios
configure terminal
ip access-list extended USERS_RZE_IN
 no deny ip any any
 permit tcp 10.30.30.0 0.0.0.31 host 10.10.40.10 eq 80
 deny ip any any
end
write memory
```

After correction, RZE-PC1 loads the internal page both [by name](evidence/intranet_name_restored.png) and [by IP](evidence/intranet_ip_restored.png). These demonstrate application recovery. The correction commands and final ACL order were not separately captured; the block above records the assigned procedure, not a recovered configuration export.

## Escalation and prevention

If HTTP still fails, inspect the required ACE and its position relative to the final deny before changing DNS, routing or the server. Appending a permit below an explicit deny leaves it unreachable. Include one required-service permit and one unaffected-service check in ACL change validation. Keep fault/recovery files separate from the clean baseline and exports.
