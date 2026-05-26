"""
storage_content.py — Facilitator-grade Storage domain questionnaire.

Mirrors the structure of Backup Discussion.docx (5 layers, 15 primary questions,
4-6 probing sub-questions each), distilled from the Storage tab of the Excel
discovery workbook: subdomains Data Integrity & Protection, Admin Access &
Segregation, Replication & DR Storage, Encryption & Data-at-Rest, Crown Jewels &
Snapshot Governance, and Database Data Protection. Operational sub-domains
(Performance & Capacity, EOL/EOS, Tooling, Policy/Config Review) are excluded
from the cyber-recovery questionnaire by design and remain available via the
Excel granular reference inside seed.json.
"""

STORAGE_DOMAIN = {
    "title": "Storage Resilience & Recovery",
    "facilitator_intro": (
        "Start with the storage estate and what protects it before testing whether snapshots, "
        "replication, and encryption controls survive contact with a real cyber-recovery scenario. "
        "Use the sub-questions to push past polished answers and surface what has been operationally proven "
        "versus what is documented in policy."
    ),
    "layers": [
        {
            "id": 1,
            "title": "Architecture, Integrity & Protection Foundation",
            "intent": (
                "Establish what storage platforms exist, where crown-jewel data is actually written, "
                "and what controls keep that data intact and recoverable before probing isolation and access."
            ),
            "questions": [
                {
                    "id": 1,
                    "primary": (
                        "Paint a picture of the storage estate — what block, file, object, on-prem and cloud "
                        "platforms protect which workload classes today, and where are the crown-jewel datasets "
                        "actually written?"
                    ),
                    "sub_questions": [
                        "Which platforms protect which workload class — block, file, object, on-prem, cloud, hybrid?",
                        "Where are the crown-jewel datasets actually written, and which array or service hosts each?",
                        "Are there shadow storage systems — DAS, departmental NAS, unmanaged object stores — outside enterprise visibility?",
                        "What fraction of in-scope storage capacity is reporting health green today, and what is unmonitored?",
                        "Which workloads are explicitly out of scope of enterprise storage policy, and on what rationale?",
                    ],
                },
                {
                    "id": 2,
                    "primary": (
                        "What controls prevent and detect data corruption across storage platforms — array "
                        "checksums, end-to-end protection, replication consistency — and how would silent bit-rot "
                        "or storage-side corruption be discovered before recovery time?"
                    ),
                    "sub_questions": [
                        "What corruption-detection mechanisms run continuously — array checksum, T10-PI, scrubbing — and on which platforms?",
                        "How is replication consistency verified, and would a bit-flip propagating through replication be caught before or after recovery?",
                        "When was the last documented case of silent corruption on a production array, and how was it detected?",
                        "Are integrity scans periodic, on-demand, or triggered only at restore time?",
                        "For long-retention snapshots and immutable copies, how would year-old bit-rot be discovered before someone tries to recover from it?",
                    ],
                },
                {
                    "id": 3,
                    "primary": (
                        "What snapshot strategy underpins storage-layer protection — frequency, retention, "
                        "immutability — and how confident are you that snapshots themselves are not at risk from "
                        "the same threats they are meant to mitigate?"
                    ),
                    "sub_questions": [
                        "What is the snapshot frequency, retention, and immutability posture per tier — primary, secondary, vault?",
                        "Who owns snapshot policy — storage team, application owners, central protection function, or no one cleanly?",
                        "Where are snapshots load-bearing for recovery, and where are they decorative because backups will be used anyway?",
                        "Can a storage admin destroy or shorten snapshot retention unilaterally?",
                        "If ransomware ran against the array today, would the snapshot copies survive — and on what control basis?",
                    ],
                },
            ],
        },
        {
            "id": 2,
            "title": "Replication, Isolation & Encryption Governance",
            "intent": (
                "Move from 'what is captured' to 'how is it isolated and protected' — this is where DR design "
                "intent and operational reality commonly diverge."
            ),
            "questions": [
                {
                    "id": 4,
                    "primary": (
                        "How is data replicated for resilience — synchronous, asynchronous, multi-site, "
                        "vendor-native versus host-based — and what is the RPO each replication path actually "
                        "delivers in production rather than on the design slide?"
                    ),
                    "sub_questions": [
                        "Which workloads replicate synchronous, async, or batch, and what is the actual measured RPO per path?",
                        "Is replication array-to-array, host-based, or vendor cyber-recovery (e.g. CyberSense, SnapMirror, SnapLock)?",
                        "Where are replication paths genuinely multi-site, and where is the DR copy sitting on the same fabric as production?",
                        "How is replication health monitored, and what is the MTTD on a replication path going silent?",
                        "Has a planned failover to the replicated copy been performed end-to-end in the last 12 months?",
                    ],
                },
                {
                    "id": 5,
                    "primary": (
                        "Is the replicated copy genuinely isolated from production identity, network, and admin "
                        "plane — or does a compromised production storage admin reach the DR copy through the same "
                        "blast radius?"
                    ),
                    "sub_questions": [
                        "Does the DR storage estate share identity with production — if production AD is encrypted, can DR storage be administered?",
                        "Is the management plane of replicated arrays reachable from the same admin network as production?",
                        "Are replication credentials and array service accounts held in production-side vaults that would be unavailable post-compromise?",
                        "Could a single compromised storage admin destroy production AND the replicated copy within the same session?",
                        "Where is the 'last known good' storage replica actually isolated, and who by name has the authority to invoke it?",
                    ],
                },
                {
                    "id": 6,
                    "primary": (
                        "What encryption is enforced at-rest across storage tiers, and where do the keys live — "
                        "array-resident, external KMS, HSM, customer-managed — and what is the dependency posture "
                        "between production identity and key access?"
                    ),
                    "sub_questions": [
                        "Which storage platforms enforce data-at-rest encryption today, and where is encryption configured but not enabled?",
                        "For each platform, where does the data-encryption key actually reside — array, external KMS, HSM, cloud KMS?",
                        "Are customer-managed keys (CMK) used where the platform supports them, or are vendor-managed defaults relied on?",
                        "Is encryption enforced consistently across primary, replicated, snapshot, and archival copies, or does archive silently drop encryption?",
                        "If production identity is unavailable, can storage admins still unlock encrypted volumes for recovery?",
                    ],
                },
                {
                    "id": 7,
                    "primary": (
                        "How are encryption keys rotated, escrowed, and recovered — and what happens to old "
                        "immutable copies and long-retention snapshots when keys rotate or custodians turn over?"
                    ),
                    "sub_questions": [
                        "What is the documented key rotation cadence, and when was each platform's keys last rotated?",
                        "How does key rotation interact with snapshots and immutable copies — are old copies re-keyed, retained under old key, or invalidated?",
                        "Where are escrow / recovery copies of keys held, and who controls escrow access?",
                        "Has a 'no KMS, no identity, recover anyway' path ever been walked through end-to-end for storage?",
                        "What happens to long-retention immutable copies if their original key custodian leaves the firm?",
                    ],
                },
            ],
        },
        {
            "id": 3,
            "title": "Access Controls, Detection & Integrity Validation",
            "intent": (
                "Probe who can touch storage administration, whether destructive actions can be performed unilaterally, "
                "and whether tampering would be seen in time to matter."
            ),
            "questions": [
                {
                    "id": 8,
                    "primary": (
                        "Who can administer storage arrays today — is admin identity separated from production, "
                        "is MFA enforced, and is privileged access brokered through PAM, or are admins logging in "
                        "with cached credentials?"
                    ),
                    "sub_questions": [
                        "Is storage admin identity in the same forest or Entra tenant as production users, or genuinely separated?",
                        "Is MFA enforced for every storage console, array management plane, and out-of-band controller?",
                        "Are storage admin sessions brokered through PAM, or do admins log in directly with cached credentials?",
                        "How are vendor support accounts (NetApp, Dell, Pure, HPE, IBM) granted access — time-bound, per-session approved, fully logged?",
                        "If the PAM platform itself is unavailable during a recovery scenario, how do storage admins authenticate?",
                    ],
                },
                {
                    "id": 9,
                    "primary": (
                        "What controls prevent unauthorized modification or deletion of storage objects, "
                        "snapshots, LUNs and shares — and where does the line between 'soft-delete recoverable' "
                        "and 'permanently destroyed' actually sit per platform?"
                    ),
                    "sub_questions": [
                        "What soft-delete or grace-period windows exist before snapshot delete, LUN destroy, or share removal becomes permanent?",
                        "Are destructive admin actions (snapshot delete, retention shorten, replication suspend, encryption disable) gated by dual-control or quorum?",
                        "Are storage admin actions session-recorded and reviewed for high-risk operations?",
                        "Can a single privileged admin destroy enough recovery surface in one session to break a tier-1 recovery objective?",
                        "Where does the line between 'recoverable mistake' and 'permanently destroyed' actually sit per platform?",
                    ],
                },
                {
                    "id": 10,
                    "primary": (
                        "What dual-control, quorum, or cooling-off enforcement exists for destructive storage "
                        "actions — and would a single compromised admin be enough to dismantle the recovery posture?"
                    ),
                    "sub_questions": [
                        "Walk us through the approval flow if someone wanted to shorten a snapshot retention lock today — who signs, who approves?",
                        "Is dual-authorization or 4-eyes enforced for storage destructive actions, or documented but not technically enforced?",
                        "Are retention or lock changes logged immutably, and who actively reviews those logs?",
                        "Is there a cooling-off delay between request and execution for destructive operations, or do they execute immediately on approval?",
                        "What happens to delete requests during a declared incident — automatically frozen, or processed on the normal path?",
                    ],
                },
                {
                    "id": 11,
                    "primary": (
                        "How are storage and array logs forwarded, monitored and alerted on — and what specific "
                        "scenarios trigger SOC action, and how fast?"
                    ),
                    "sub_questions": [
                        "Where are storage array logs forwarded — enterprise SIEM, isolated cyber-recovery SOC, or only locally retained?",
                        "What specific SIEM alerts fire for mass snapshot delete, retention change, replication suspension, encryption disable?",
                        "What is the documented MTTD for malicious storage tampering, and has it been measured rather than modelled?",
                        "Are storage admin actions correlated with identity-side anomalies (privileged logons, new accounts, AD changes)?",
                        "Are canary LUNs, honeypot shares, or decoy snapshots deployed to detect intruder reconnaissance on storage?",
                    ],
                },
            ],
        },
        {
            "id": 4,
            "title": "Recovery Readiness & Dependencies",
            "intent": (
                "Test whether snapshots, replicas, and storage-side recovery can actually deliver under pressure, "
                "including database-resident data and the dependencies a responder would need to be alive first."
            ),
            "questions": [
                {
                    "id": 12,
                    "primary": (
                        "Have crown-jewel datasets been recovered end-to-end from storage replicas or snapshots in "
                        "the last 12 months — under what scenarios, and what failed?"
                    ),
                    "sub_questions": [
                        "Of recovery tests in the last 12 months, how many specifically sourced data from storage snapshots or replicas rather than backup tier?",
                        "What is the documented recovery sequence when storage is the source of truth — DNS, identity, KMS, fabric — what must come first?",
                        "Have recovery tests included end-to-end snapshot-restore validation, or stopped at 'snapshot mounted'?",
                        "Are scenario-based tests run against storage (ransomware, regional loss, supply chain), or only technical-only failover drills?",
                        "Has a full end-to-end recovery from the DR-side storage replica been completed in the last 12 months?",
                    ],
                },
                {
                    "id": 13,
                    "primary": (
                        "How are database-resident datasets protected — application-consistent snapshots, log-shipping, "
                        "native vendor backup — and are recovery procedures aligned across DBA, storage and infra teams, "
                        "or do they diverge under pressure?"
                    ),
                    "sub_questions": [
                        "For each crown-jewel database (Oracle, MSSQL, Postgres, Mongo, Hadoop), what is the protection model — snapshot, native backup, log shipping, replication?",
                        "Are storage snapshots of databases application-consistent (quiesced, snapshot-aware), or crash-consistent?",
                        "Are DBA-side recovery procedures aligned with storage-side recovery procedures, or do they diverge under pressure?",
                        "When did the DBA, storage and infrastructure teams last run a joint database recovery test?",
                        "Where would database recovery hit the wall first — log replay, identity, schema mismatch, capacity?",
                    ],
                },
                {
                    "id": 14,
                    "primary": (
                        "What dependencies — identity, KMS, vCenter, hypervisor, network, fabric — must be alive "
                        "before storage recovery can even begin, and have those dependencies themselves been "
                        "recovery-tested or only assumed?"
                    ),
                    "sub_questions": [
                        "If production identity, DNS, and network are all unavailable, can storage admins still log in to initiate recovery?",
                        "Where is storage management metadata, snapshot catalogs, and replication state stored, and what is its own recovery posture?",
                        "Have storage dependencies (fabric, vCenter, hypervisor management, monitoring, ticketing) themselves been recovery-tested?",
                        "What is the documented rebuild plan for the storage management plane if it is compromised?",
                        "Has a 'cold start' — every dependency down, storage recovers from scratch — ever been walked through?",
                    ],
                },
            ],
        },
        {
            "id": 5,
            "title": "Evidence & Priorities",
            "intent": (
                "Anchor the conversation in what has actually been proven on the storage side and where the "
                "highest-impact improvements lie."
            ),
            "questions": [
                {
                    "id": 15,
                    "primary": (
                        "If a cyber-compromise hit today and crown-jewel recovery depended on storage-resident "
                        "snapshots or replicas, what would most likely undermine that recovery — and what single "
                        "storage-domain improvement would most materially strengthen cyber recovery readiness?"
                    ),
                    "sub_questions": [
                        "Show us the most recent successful cyber-recovery test report that used storage as the recovery source — scenario, scope, outcomes?",
                        "What scenarios have been run against immutable snapshots or replicated copies in the last 12 months, and what failed?",
                        "If you had to name a single storage dependency that would break recovery today, what would it be — and why hasn't it been fixed?",
                        "Where would Day 2 of a real ransomware recovery hit the wall on the storage side — capacity, fabric, identity, snapshot integrity, scanning?",
                        "If you had budget and political capital for exactly one storage-domain improvement this year, what would deliver the most cyber-recovery uplift?",
                        "What does the 12-month storage-domain cyber-recovery roadmap actually look like, and how was it prioritised?",
                    ],
                },
            ],
        },
    ],
}
