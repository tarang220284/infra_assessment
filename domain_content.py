"""
domain_content.py — Authored facilitator content for all non-Backup/Storage domains.

Sources: Excel discovery workbook tabs (Service Management, Identity, Network,
Security and Risk, Compute and Virtualization, Cloud (AWS)). Subdomain and topic
taxonomy from each tab is distilled into the 5-layer / cyber-recovery
facilitator format that matches Backup Discussion.docx.

Operational-only tabs / subdomains (Performance & Capacity, EOL/EOS, Tooling,
Configuration Review, Cost Optimization, DevOps & CI/CD) are deliberately
excluded from the recovery questionnaires; they remain available as Excel
granular reference inside seed.json.
"""

# ─────────────────────────────────────────────────────────────────────────────
# SERVICE MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────
SERVICE_MGMT_DOMAIN = {
    "title": "Service Management Resilience",
    "facilitator_intro": (
        "Start with the CMDB and crown-jewel service identification before testing whether dependency mapping, "
        "change governance, and incident response can actually support a cyber-recovery scenario rather than "
        "routine operations."
    ),
    "layers": [
        {
            "id": 1, "title": "CMDB & Service Catalogue Foundation",
            "intent": "Establish what the CMDB contains, who owns it, and whether crown-jewel services are explicitly identified within it.",
            "questions": [
                {"id": 1, "primary": "Paint a picture of the CMDB — what platform, what classes of CI are populated, who owns the data, and who actually consumes it?",
                 "sub_questions": [
                    "Which CMDB platform is in use, and is there a single authoritative instance or multiple parallel sources?",
                    "Which CI classes are populated — applications, servers, databases, network, identity, business services?",
                    "Who owns CMDB data integrity, and how is that ownership operationally enforced?",
                    "Which downstream processes consume CMDB data — change, incident, problem, recovery — and which bypass it?",
                    "What percentage of CIs have an active owner attribute, and what fraction is orphaned?",
                 ]},
                {"id": 2, "primary": "How are crown-jewel and tier-1 services explicitly identified in the CMDB, and is that identification maintained or last touched years ago?",
                 "sub_questions": [
                    "Is there a documented crown-jewel / tier-1 / MAS-critical attribute on services, and when was it last reviewed?",
                    "Who has authority to assign or change a service tier — IT, business, risk, or no one cleanly?",
                    "Are tier assignments aligned with BIA outputs and regulatory criticality (MAS TRM, CSA CCoP)?",
                    "How is tier inheritance handled — does a tier-1 service automatically tier its dependencies, or are they classified separately?",
                    "Show us the current tier-1 service list — would the business agree it is complete and accurate?",
                 ]},
                {"id": 3, "primary": "What is the discovery and freshness model — automated scanning, periodic attestation, or manual entry — and what fraction of CIs are stale beyond policy thresholds?",
                 "sub_questions": [
                    "What discovery tooling populates the CMDB, and what is its coverage across the estate?",
                    "How often are CIs reconciled or re-attested, and by whom?",
                    "What is the documented staleness threshold, and what fraction of CIs are currently in breach?",
                    "Are shadow IT assets (departmental SaaS, unmanaged systems) flagged as outside CMDB coverage?",
                    "When was the last full reconciliation between CMDB and a ground-truth source (vCenter, AD, AWS Org)?",
                 ]},
            ],
        },
        {
            "id": 2, "title": "Dependency Modelling & Service Impact",
            "intent": "Move from 'what exists' to 'what depends on what' — dependency depth is where service-management maturity diverges from operational reality.",
            "questions": [
                {"id": 4, "primary": "How are service-to-CI dependencies mapped today — top-down by service owner, bottom-up by discovery, or hybrid — and how deep does the mapping go?",
                 "sub_questions": [
                    "What approach is used — manual mapping, automated topology discovery, observability-driven, or hybrid?",
                    "How deep does mapping go — application only, or down through middleware, database, storage, network, identity?",
                    "Are external dependencies (SaaS, third parties, payment networks, market data) captured?",
                    "Are dependencies versioned over time, or only kept current?",
                    "Who validates dependency accuracy, and how often?",
                 ]},
                {"id": 5, "primary": "What is the operational use of dependency data — does it inform change, incident, and recovery decisions, or is it referenced only during audits?",
                 "sub_questions": [
                    "Does CAB use dependency data to assess change blast radius?",
                    "During an incident, is the dependency map consulted to triage impact, or is institutional knowledge relied on?",
                    "When was the last documented case of dependency data preventing a bad change or accelerating a recovery?",
                    "Do business service owners trust the dependency view enough to act on it in a crisis?",
                    "Is the dependency map referenced in cyber-recovery playbooks, or only in routine continuity docs?",
                 ]},
                {"id": 6, "primary": "For a named tier-1 business service, can you trace its dependency tree end-to-end (app → middleware → database → storage → network → identity), and how confident are you the trace is correct today?",
                 "sub_questions": [
                    "Pick a tier-1 service today — can you produce its dependency tree from CMDB in under five minutes?",
                    "How many of those dependencies have current, verified ownership in the CMDB?",
                    "Have any of those dependencies changed in the last 30 days, and was the CMDB updated?",
                    "If a single CI in that tree is encrypted in a ransomware event, what is the immediate impact assessment process?",
                    "Where would the dependency trace fail — and how often does it fail in practice?",
                 ]},
            ],
        },
        {
            "id": 3, "title": "Change, Incident & IR Governance",
            "intent": "Test whether change and incident processes are coherent, integrated with security, and capable of operating under pressure.",
            "questions": [
                {"id": 7, "primary": "What change governance model is in place, and how is risk specifically evaluated for changes touching crown-jewel services or recovery infrastructure?",
                 "sub_questions": [
                    "What change categories exist (standard, normal, emergency), and how is each routed?",
                    "How is risk scored for a change, and who has veto authority for high-risk changes?",
                    "Are changes to backup, storage, identity, and recovery infrastructure flagged for elevated scrutiny?",
                    "What is the documented post-implementation review cadence, and who reads the output?",
                    "When was the last change-induced incident traceable to a CAB gap?",
                 ]},
                {"id": 8, "primary": "How are post-change outcomes managed — do failures feed back into the CAB, CMDB, and process improvements, or are they handled in isolation?",
                 "sub_questions": [
                    "What fraction of changes are categorised as successful vs partial vs failed, and is the trend visible?",
                    "Where do change-failure root causes land — service management, security, or both?",
                    "Are recurring change-failure patterns surfaced and addressed structurally?",
                    "Does change failure data influence the assessed risk of future similar changes?",
                    "Are change outcomes correlated to incident records to identify change-induced outages?",
                 ]},
                {"id": 9, "primary": "Describe your incident response model — who owns severity, who declares major, and how does the IT-side IR intersect with security IR?",
                 "sub_questions": [
                    "What is the severity taxonomy, and who has authority to escalate or de-escalate?",
                    "At what severity is security IR automatically engaged?",
                    "Are IT incident and security incident streams reconciled in real time, or only post-mortem?",
                    "What is the documented hand-off process when an IT incident is suspected to be a cyber event?",
                    "Who chairs the war room when the line between incident and breach is unclear?",
                 ]},
                {"id": 10, "primary": "How are incident, problem, and major-incident records integrated with the security operations stream and the threat intel pipeline?",
                 "sub_questions": [
                    "Are incident tickets and SIEM cases correlated through a shared identifier or workflow?",
                    "Do post-incident reviews include security review, or only operational review?",
                    "Is threat-intel context attached to incident records when relevant?",
                    "When was the last incident reclassified as a cyber event mid-flight, and how did the model handle it?",
                    "Are root-cause findings shared between SOC and ITSM teams structurally, or only ad-hoc?",
                 ]},
                {"id": 11, "primary": "When was your last major outage, and walk us through how the execution model actually performed — comms, war room, business engagement, decision pace?",
                 "sub_questions": [
                    "Who chaired the major-incident bridge, and how was authority for tough calls established?",
                    "How fast was the business engaged, and what did they need that you couldn't provide?",
                    "What communications template was used, and was it the right cadence for the audience?",
                    "Where did the execution model break down — comms, decisions, escalation, or data?",
                    "What changed structurally after the post-mortem, and is the change still in place?",
                 ]},
            ],
        },
        {
            "id": 4, "title": "Recovery-Oriented Service Awareness",
            "intent": "Probe whether CMDB and ITSM artefacts are usable when a cyber-recovery is in motion rather than only during routine operations.",
            "questions": [
                {"id": 12, "primary": "When recovery decisions need to be made under pressure, is the CMDB actually the source of truth, or is it quietly bypassed because trust in it is low?",
                 "sub_questions": [
                    "In the last incident, was the CMDB consulted, or was a side document or institutional memory used?",
                    "If CMDB and reality disagree mid-incident, which one wins, and why?",
                    "How is CMDB trust measured — by users, by audit, or not at all?",
                    "When ITSM tooling itself is degraded during an incident, what is the fallback?",
                    "Does the cyber-recovery playbook assume CMDB is available — and is that assumption safe?",
                 ]},
                {"id": 13, "primary": "What is the documented recovery sequence per tier-1 service, and where does that sequence actually live — CMDB, runbook, BCP doc, or someone's head?",
                 "sub_questions": [
                    "For a named tier-1 service, can you produce its recovery sequence document today?",
                    "Has the sequence been tested in a tabletop or real test in the last 12 months?",
                    "Are upstream dependencies (identity, KMS, network, fabric) explicit in the sequence?",
                    "Who maintains the sequence, and how is drift caught when the underlying service changes?",
                    "If the service owner is unavailable during a recovery, who has the authority and knowledge to execute the sequence?",
                 ]},
            ],
        },
        {
            "id": 5, "title": "Evidence & Priorities",
            "intent": "Anchor in what has actually been proven and where the largest service-management uplift to cyber-recovery readiness sits.",
            "questions": [
                {"id": 14, "primary": "What evidence demonstrates that CMDB and IR processes can support a cyber-recovery scenario rather than only routine ops — and where has that been independently validated?",
                 "sub_questions": [
                    "Show us the most recent cyber-recovery tabletop or live test that exercised ITSM and CMDB.",
                    "What did the test reveal about CMDB accuracy under stress?",
                    "Have auditors or independent reviewers tested ITSM-side recovery claims, or have they been self-attested?",
                    "What is the evidence chain from incident declared → service impact understood → recovery sequenced?",
                    "Are after-action reviews recorded in a way that surfaces systemic vs one-off issues?",
                 ]},
                {"id": 15, "primary": "If you had budget and political capital for exactly one service-management improvement this year, what would most materially strengthen cyber-recovery readiness — and why hasn't it been done?",
                 "sub_questions": [
                    "Name the single highest-impact ITSM improvement, and the constraint preventing it today.",
                    "Where does the 12-month ITSM roadmap explicitly invest in recovery readiness vs efficiency?",
                    "What political or organisational blocker stops better cross-domain integration with security and recovery?",
                    "If a regulator demanded evidence of dependency-aware recovery tomorrow, where would the gap show first?",
                    "What is the smallest credible step that could change the recovery posture in 90 days?",
                 ]},
            ],
        },
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# IDENTITY (AD + Entra ID)
# ─────────────────────────────────────────────────────────────────────────────
IDENTITY_DOMAIN = {
    "title": "Identity Resilience & Recovery",
    "facilitator_intro": (
        "Identity is tier-zero — the question is not whether AD and Entra are present, but whether they survive contact "
        "with a determined attacker and whether crown-jewel services can be recovered when identity itself is impaired. "
        "Push past 'we have MFA' answers to what is operationally proven."
    ),
    "layers": [
        {
            "id": 1, "title": "AD & Entra Architecture, Tiering, Hardening",
            "intent": "Establish forest, tenant, trust, and tiering posture before probing authentication and recovery.",
            "questions": [
                {"id": 1, "primary": "Paint a picture of the identity architecture today — AD forests, domains, trusts, Entra tenants, federation — and where the boundaries of trust actually sit.",
                 "sub_questions": [
                    "How many forests and domains exist, and what trusts (forest, external, shortcut) link them?",
                    "How many Entra tenants are in scope, and how do they federate or sync with on-prem AD?",
                    "Where do legacy or vendor-acquired domains sit, and are they isolated or implicitly trusted?",
                    "Are there test, dev, or sandbox identity environments with paths into production?",
                    "Which third parties (vendors, MSPs) have B2B guest, federated, or trusted access?",
                 ]},
                {"id": 2, "primary": "What tiering model is in place across the AD estate — ESAE / Microsoft Tier 0/1/2 / Red Forest — and where does the tiering hold in practice versus break on the ground?",
                 "sub_questions": [
                    "Is a documented tiering model in place, and does it match deployed reality?",
                    "Are Tier 0 assets (DCs, ADCS, ADFS, Entra Connect, PAM) genuinely separated from Tier 1/2 admin paths?",
                    "Can Tier 0 admin credentials be used from Tier 1 workstations today?",
                    "Where do shared service accounts cross tier boundaries?",
                    "When was the tiering model last validated by purple-team or AD-specific assessment?",
                 ]},
                {"id": 3, "primary": "What hardening posture is in place on DCs, GPOs, and identity infrastructure — and what dependencies must survive for identity itself to come back?",
                 "sub_questions": [
                    "Are DCs hardened against CIS or Microsoft baselines, and is the baseline drift-monitored?",
                    "What GPO governance exists — change control, drift detection, version control?",
                    "Are critical GPO settings (audit, restricted groups, LSA, NTLM) regularly attested?",
                    "What does the bootstrap recovery sequence look like for the identity stack itself?",
                    "Where is the AD installation media, schema baseline, and last known good system state actually held?",
                 ]},
            ],
        },
        {
            "id": 2, "title": "Privileged Access, Authentication & MFA",
            "intent": "Move from architecture to active controls — privileged-access lifecycle, authentication strength, MFA coverage, legacy exposure.",
            "questions": [
                {"id": 4, "primary": "How is privileged access provisioned, approved, and time-bound — and is just-in-time / just-enough access the norm, or are standing admin privileges still common?",
                 "sub_questions": [
                    "What approval workflow is required for privileged access, and who can self-approve?",
                    "Is PIM / JIT enforced for high-tier roles in Entra and on-prem?",
                    "How many standing Domain Admin / Enterprise Admin / Global Admin accounts exist today, and why?",
                    "Are vendor and break-glass accounts time-bound and reviewed?",
                    "When was the last review of privileged-account inventory?",
                 ]},
                {"id": 5, "primary": "What is the scope and governance of PAM — which platforms, which accounts, which paths are actually brokered through PAM versus bypassed?",
                 "sub_questions": [
                    "Which platforms route through PAM today (AD, Entra, Linux, network, storage, cloud, SaaS)?",
                    "Are session recordings retained, and is any high-risk-action review performed?",
                    "Which admin paths intentionally or unintentionally bypass PAM?",
                    "Is PAM-controlled credential rotation automated for service accounts, or aspirational?",
                    "Has PAM availability been tested under degraded conditions?",
                 ]},
                {"id": 6, "primary": "Describe the authentication architecture — Kerberos, NTLM, certificate-based, FIDO, OAuth — and which legacy protocols still carry real traffic.",
                 "sub_questions": [
                    "Is NTLM still enabled, and what is the documented removal plan?",
                    "Are Kerberos delegations (unconstrained, constrained, RBCD) inventoried and reviewed?",
                    "Are SPNs and msDS-AllowedToActOnBehalfOfOtherIdentity attributes audited?",
                    "Is ADCS hardened against ESC1–ESC15 known abuse paths?",
                    "Which apps still require legacy authentication (basic, IMAP, SMTP)?",
                 ]},
                {"id": 7, "primary": "What is the MFA policy, coverage, and threat resistance today — and where does the policy diverge from reality on the ground?",
                 "sub_questions": [
                    "Is MFA enforced for 100% of user accounts, or are exceptions extensive?",
                    "Which MFA factors are in use (SMS, push, FIDO2, certificate), and what fraction is phishing-resistant?",
                    "Is MFA enforced at the protocol level (Conditional Access, AD FS claims) or only at the app level?",
                    "How are MFA fatigue and push-bombing scenarios detected?",
                    "When was the last attempted MFA bypass observed, and what was the response?",
                 ]},
                {"id": 8, "primary": "How are legacy authentication paths and outage scenarios handled — what happens when CA, FIDO, or KMS dependencies degrade?",
                 "sub_questions": [
                    "What auth paths remain if Entra is unavailable?",
                    "What auth paths remain if AD is unavailable?",
                    "How are break-glass accounts protected, rotated, and access-tested?",
                    "Has a 'no MFA service available' scenario been walked through end-to-end?",
                    "Are legacy auth fallbacks one-way disabled, or could they be re-enabled under pressure?",
                 ]},
            ],
        },
        {
            "id": 3, "title": "Hybrid Identity, Conditional Access & Database IAM",
            "intent": "Probe Entra integration, Conditional Access drift, and the identity controls that protect database-resident crown-jewel data.",
            "questions": [
                {"id": 9, "primary": "What is the Entra integration model — Password Hash Sync, Pass-Through Authentication, Federation — and what is the security and recovery posture of the chosen path?",
                 "sub_questions": [
                    "Which sync model is in use, and what drove the choice?",
                    "Where does Entra Connect itself run, and is it treated as Tier 0?",
                    "Is seamless SSO enabled, and is the AZUREADSSOACC account protected accordingly?",
                    "Are sync filters and write-back policies reviewed for drift?",
                    "If Entra Connect is destroyed, how long until identity sync is restored?",
                 ]},
                {"id": 10, "primary": "How is Conditional Access governed — policy inventory, change control, drift detection — and where does CA divergence quietly weaken the perimeter?",
                 "sub_questions": [
                    "How many CA policies are in production, and who owns them?",
                    "How is CA change control enforced — peer review, ticket, drift alert?",
                    "Are 'exclude' groups in CA policies reviewed for sprawl?",
                    "Are report-only policies ever promoted without measurement?",
                    "When was the last CA-policy red-team review?",
                 ]},
                {"id": 11, "primary": "How are database-resident identity controls implemented — managed identities, AAD authentication, IAM database users — and how is permission drift detected and remediated?",
                 "sub_questions": [
                    "How do production databases authenticate workloads — local accounts, AAD, managed identities?",
                    "Are database-resident permissions reviewed and recertified?",
                    "Are privileged DB roles (sysadmin, db_owner, root) explicitly inventoried?",
                    "How are DB service accounts rotated and tied back to identity governance?",
                    "What happens to DB authentication if AAD is unavailable?",
                 ]},
            ],
        },
        {
            "id": 4, "title": "Identity Recovery & Resilience",
            "intent": "Test whether identity itself can be recovered when compromise reaches tier zero.",
            "questions": [
                {"id": 12, "primary": "What is the AD forest recovery posture today — Microsoft AD Forest Recovery plan, frequency of tested forest recovery, and isolation of the recovery copy?",
                 "sub_questions": [
                    "Is a documented AD forest recovery plan current and maintained?",
                    "When was the last live forest recovery test, and how long did it take?",
                    "Where is the AD system-state backup actually held, and is it isolated from production?",
                    "Are FSMO transfer and metadata cleanup steps rehearsed?",
                    "What is the validated RTO for a full forest recovery?",
                 ]},
                {"id": 13, "primary": "What is the Entra tenant recovery posture — soft-delete, backup of Conditional Access and configuration, recovery from tenant-wide compromise?",
                 "sub_questions": [
                    "What Entra tenant configuration is backed up — CA policies, app registrations, role assignments?",
                    "What backup tooling is in use (Microsoft 365 Backup, third party), and how is it tested?",
                    "How would tenant-wide credential theft be contained today?",
                    "Has a tenant-takeover scenario been walked through with Microsoft support engaged?",
                    "What is the documented RTO for restoring critical Entra configuration?",
                 ]},
                {"id": 14, "primary": "What is the documented recovery sequence when identity is impaired — what comes back first, how do downstream systems re-authenticate, and what dependencies are assumed to be alive?",
                 "sub_questions": [
                    "Is the recovery sequence documented and exercised, or only conceptual?",
                    "What systems (KMS, PAM, monitoring, ticketing) depend on identity to recover?",
                    "Are tier-0 admin paths preserved when standard auth is unavailable?",
                    "Have downstream systems been tested for graceful behaviour during identity outage?",
                    "Has a 'cold start' from identity loss been walked through end-to-end?",
                 ]},
            ],
        },
        {
            "id": 5, "title": "Evidence & Priorities",
            "intent": "Anchor in proven evidence of identity resilience and highest-leverage improvements.",
            "questions": [
                {"id": 15, "primary": "Show us the most recent AD purple-team, forest-recovery, or identity-compromise simulation — what was tested, what failed, and how was it remediated?",
                 "sub_questions": [
                    "What scenarios were exercised — DCSync, Kerberoasting, golden ticket, ADCS abuse, Entra token replay?",
                    "What controls broke, and was remediation tracked to closure?",
                    "Were findings shared cross-team or kept inside identity?",
                    "Have auditors or regulators reviewed AD posture in the last 12 months?",
                    "What residual identity risk would you flag to the CISO today?",
                 ]},
                {"id": 16, "primary": "If you had budget and political capital for exactly one identity improvement this year, what would most materially reduce cyber-recovery risk — and why hasn't it been done?",
                 "sub_questions": [
                    "Name the single highest-impact identity improvement currently on the backlog.",
                    "What constraint blocks it — funding, ownership, risk appetite, vendor capability?",
                    "Where does the 12-month identity roadmap most explicitly invest in recovery readiness?",
                    "What would change if Tier 0 isolation was truly enforced tomorrow?",
                    "What residual risk would remain even after the best single improvement?",
                 ]},
            ],
        },
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# NETWORK
# ─────────────────────────────────────────────────────────────────────────────
NETWORK_DOMAIN = {
    "title": "Network Resilience & Segmentation",
    "facilitator_intro": (
        "Start with what the network architecture actually looks like and where the trust boundaries sit, then push "
        "past polished segmentation diagrams to what enforcement is operationally proven and what would survive a "
        "real cyber-compromise."
    ),
    "layers": [
        {
            "id": 1, "title": "Data Centre & Network Architecture Baseline",
            "intent": "Establish DC topology, redundancy posture, and documentation state before probing controls.",
            "questions": [
                {"id": 1, "primary": "Paint a picture of the data centre and network topology — JDC, KDC, sites, inter-DC links, cloud on-ramps — and where the network actually carries crown-jewel traffic.",
                 "sub_questions": [
                    "How many DCs, sites, and cloud regions carry production workloads?",
                    "What are the inter-DC link types, capacities, and providers?",
                    "Which workloads traverse public internet, MPLS, or dedicated cloud paths?",
                    "Are there test, dev, or vendor environments riding the same network?",
                    "Where does crown-jewel traffic concentrate, and are those paths explicitly mapped?",
                 ]},
                {"id": 2, "primary": "What is the availability design — redundancy at each layer, ECMP, multi-path routing — and what single points of failure remain despite the diagrams?",
                 "sub_questions": [
                    "Where is redundancy genuine (active-active, ECMP) versus active-passive with manual failover?",
                    "Are uplinks, route reflectors, and gateways all redundant across both DCs?",
                    "Are layer-2 extension dependencies (VXLAN, OTV) understood as risk?",
                    "What network SPOFs are known and accepted today?",
                    "When was the last documented network-path SPOF discovery exercise?",
                 ]},
                {"id": 3, "primary": "What is the state of network documentation and recovery artefacts — diagrams, configs, vendor support data — and how confident are you it is current?",
                 "sub_questions": [
                    "When were architecture diagrams last refreshed to match production?",
                    "Where do device configurations live, and how are they backed up and versioned?",
                    "Is golden-config baseline maintained, and is drift detected?",
                    "Are runbooks for major path failures current, owned, and tested?",
                    "Where does vendor support contact and serial-number data live?",
                 ]},
            ],
        },
        {
            "id": 2, "title": "Segmentation & Control Points",
            "intent": "Probe the segmentation design and where enforcement actually holds versus is documented but bypassable.",
            "questions": [
                {"id": 4, "primary": "Describe the segmentation model — zones, VRFs, microsegmentation, software-defined — and how it maps to business risk and crown-jewel services.",
                 "sub_questions": [
                    "What zone model is in use (PCI, prod, dev, OT, DMZ), and what enforces zone boundaries?",
                    "Is microsegmentation in place (Illumio, NSX, Cisco SD-Access), and what is its coverage?",
                    "Where do east-west flows cross zones without enforcement?",
                    "Are crown-jewel services in dedicated zones, or share with general workloads?",
                    "What process governs zone-boundary exceptions?",
                 ]},
                {"id": 5, "primary": "What enforcement points actually inspect east-west traffic — firewalls, microseg agents, fabric ACLs — and how are exceptions tracked?",
                 "sub_questions": [
                    "Where are inter-zone flows inspected today?",
                    "What inspection happens within a zone, if any?",
                    "How are temporary exceptions (project, testing) governed and retired?",
                    "Are policy changes peer-reviewed and tested before push?",
                    "What is the documented review cadence for east-west rules?",
                 ]},
                {"id": 6, "primary": "How is segmentation effectiveness validated — purple-team, breach-and-attack simulation, real-world incident — and what has it revealed?",
                 "sub_questions": [
                    "Has segmentation been tested with adversary emulation (Atomic Red Team, AttackIQ, SafeBreach)?",
                    "When was the last lateral-movement test, and which controls failed?",
                    "Are findings tracked to closure with measured re-test?",
                    "Are detection-side controls validated alongside enforcement?",
                    "What residual lateral-movement risk would you flag to leadership today?",
                 ]},
            ],
        },
        {
            "id": 3, "title": "Perimeter, External Access & Resilience",
            "intent": "Test perimeter design, third-party connectivity, and failover behaviour.",
            "questions": [
                {"id": 7, "primary": "What is the perimeter and DMZ design — inbound zones, reverse proxies, WAF, DDoS — and where does the design fall short under pressure?",
                 "sub_questions": [
                    "What sits at the edge — firewalls, WAF, DDoS, reverse proxies — and in what order?",
                    "Is the DMZ a real zone with inspection or a flat segment with port openings?",
                    "How are SSL/TLS inspection decisions made and governed?",
                    "What inbound services are exposed today, and is the inventory current?",
                    "When was the last edge configuration peer-reviewed?",
                 ]},
                {"id": 8, "primary": "How are third-party connectivity paths (MPLS, dedicated circuits, SaaS, partners, vendors) governed — and which are over-trusted relative to risk?",
                 "sub_questions": [
                    "Inventory of third-party connections — circuits, IPSec, peering, SaaS integrations?",
                    "What controls sit between third-party endpoints and production?",
                    "How is third-party connectivity reviewed and retired when no longer needed?",
                    "Are vendor accesses time-bound and session-recorded where they touch admin planes?",
                    "What would happen if a major third party (SWIFT, market data, payment) became hostile or compromised?",
                 ]},
                {"id": 9, "primary": "What is the SPOF and failover model — links, devices, paths — and what is the validated RTO for each failure mode?",
                 "sub_questions": [
                    "Where is failover automatic versus manual?",
                    "What is the measured failover time per major scenario?",
                    "When was each failover scenario last live-tested?",
                    "Are devices clustered, and what is the failure mode if cluster syncing fails?",
                    "Are LB and DNS failover scripts current and tested?",
                 ]},
                {"id": 10, "primary": "How are load balancers and DNS — both authoritative and resolver — protected and operated, and what is the cyber-recovery posture for those layers?",
                 "sub_questions": [
                    "What LB platforms are in use, and are they redundant across DCs?",
                    "Where does authoritative DNS live, and what is the change-control posture?",
                    "How is DNSSEC handled, and how is cache-poisoning resistance measured?",
                    "If DNS is compromised, what is the documented containment path?",
                    "Are LB configurations versioned and recoverable?",
                 ]},
            ],
        },
        {
            "id": 4, "title": "Recovery & Business-Service Continuity",
            "intent": "Probe whether the network plane itself can be recovered and whether business-service mapping is real.",
            "questions": [
                {"id": 11, "primary": "Can a tier-1 business service be traced end-to-end through the network — paths, zones, devices — and how confident are you the trace is current?",
                 "sub_questions": [
                    "For a named tier-1 service, what is the network path from user to data?",
                    "Are paths documented per service or only per device?",
                    "What network change in the last 90 days could have invalidated the trace?",
                    "Who owns the trace and keeps it current?",
                    "How is the trace used during incident triage?",
                 ]},
                {"id": 12, "primary": "What is the recovery sequence for the network plane itself — management, control, data — if compromise reaches the network management stack?",
                 "sub_questions": [
                    "Is the network management plane separated from production, with its own identity?",
                    "Where do device configs and credentials live during a network-management compromise?",
                    "What is the rebuild plan for the management plane?",
                    "Are out-of-band paths to devices defined and tested?",
                    "What dependencies (DNS, NTP, identity, monitoring) must be alive for network recovery to start?",
                 ]},
                {"id": 13, "primary": "How is the network management plane itself protected during cyber events — out-of-band, jump hosts, OOB credentials?",
                 "sub_questions": [
                    "Is OOB connectivity to devices in place and tested?",
                    "Are admin jump hosts dedicated, hardened, and monitored?",
                    "Where are device credentials stored if the credential vault is unavailable?",
                    "Has a 'network management plane down' scenario been exercised?",
                    "Who has the authority to invoke OOB paths during an incident?",
                 ]},
            ],
        },
        {
            "id": 5, "title": "Evidence & Priorities",
            "intent": "Anchor in evidence and the single biggest network-domain uplift.",
            "questions": [
                {"id": 14, "primary": "Show us the most recent segmentation, lateral-movement, or perimeter validation evidence — what was tested, what failed, what was fixed?",
                 "sub_questions": [
                    "What red-team or purple-team activity has stressed the network in the last 12 months?",
                    "What east-west controls were proven, and which assumed?",
                    "Were findings tracked to closure with measured re-test?",
                    "Are auditors / regulators satisfied with current network posture?",
                    "What residual network risk would you raise to leadership today?",
                 ]},
                {"id": 15, "primary": "If you had budget and political capital for exactly one network improvement this year, what would most materially strengthen cyber-recovery readiness — and why hasn't it been done?",
                 "sub_questions": [
                    "Name the single highest-impact network improvement, and the constraint blocking it.",
                    "Where does the 12-month network roadmap explicitly invest in recovery rather than capacity or refresh?",
                    "What would change if microsegmentation was truly enforced across crown-jewel services tomorrow?",
                    "What residual risk remains even after the best single improvement?",
                    "What is the smallest credible step that could change recovery posture in 90 days?",
                 ]},
            ],
        },
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# SECURITY AND RISK
# ─────────────────────────────────────────────────────────────────────────────
SECURITY_RISK_DOMAIN = {
    "title": "Security Controls & Risk Posture",
    "facilitator_intro": (
        "Start with the perimeter and segmentation controls that constitute the primary security envelope, then push "
        "through PAM, EDR, SIEM, and ransomware-IR readiness to what is operationally proven rather than documented."
    ),
    "layers": [
        {
            "id": 1, "title": "Perimeter & Boundary Security Controls",
            "intent": "Establish firewall and segmentation posture and the change-management discipline around them.",
            "questions": [
                {"id": 1, "primary": "Paint a picture of the firewall estate — platforms, generations, where each one sits, and which crown-jewel flows it protects.",
                 "sub_questions": [
                    "Which firewall platforms and generations are in production (Palo Alto, Fortinet, Check Point, Cisco)?",
                    "Where does each firewall sit — perimeter, internal, DC, branch, cloud edge?",
                    "Which flows traverse multiple firewall layers, and which are inspected at only one point?",
                    "Are firewall licenses, capacity, and EOL status known and tracked?",
                    "Where do legacy or unmanaged firewalls still exist?",
                 ]},
                {"id": 2, "primary": "Describe the firewall policy model — rule structure, NAT, application identification, threat prevention — and how policy hygiene is maintained.",
                 "sub_questions": [
                    "Is policy structured by zone, app, or legacy port-based?",
                    "What fraction of rules are using application-ID and identity-based criteria?",
                    "How many shadowed, overlapping, or any-any rules exist today?",
                    "When was the last rule-base cleanup, and what was the rule-count delta?",
                    "Is rule expiry / review enforced, or are rules eternal?",
                 ]},
                {"id": 3, "primary": "How is firewall change governance enforced — peer review, testing, drift detection, separation of duty?",
                 "sub_questions": [
                    "Is firewall change peer-reviewed, and by whom?",
                    "Are emergency changes tracked and reconciled post-event?",
                    "How is config drift between intended and actual policy detected?",
                    "What separation-of-duty exists between policy author, approver, and pusher?",
                    "Are firewall change failures categorised and fed back into governance?",
                 ]},
            ],
        },
        {
            "id": 2, "title": "Endpoint, Identity Access & PAM",
            "intent": "Move from boundary to host-level and identity-level controls — PAM scope, EDR coverage, integration with the broader stack.",
            "questions": [
                {"id": 4, "primary": "What is PAM coverage and lifecycle governance today — scope, account types, vault rotation, session brokerage?",
                 "sub_questions": [
                    "Which platforms route through PAM (AD, network, storage, backup, cloud, SaaS, DB)?",
                    "Which privileged-account types are in PAM versus outside (vendor, service, break-glass)?",
                    "Are session recordings retained, and is high-risk-action review performed?",
                    "What credential-rotation cadence is enforced, and is it automated?",
                    "When was the PAM platform itself last security-reviewed?",
                 ]},
                {"id": 5, "primary": "What is the EDR / XDR platform, coverage, and operating model — and where does coverage end?",
                 "sub_questions": [
                    "Which EDR platform is in use, and what is the deployed fleet coverage (% endpoints, % servers)?",
                    "Are unmanaged or legacy endpoints (OT, IoT, vendor) excluded — and why?",
                    "Is EDR data forwarded to SIEM or operated as a separate console?",
                    "Is EDR in detect, prevent, or block mode for each control class?",
                    "What is the alert-to-investigation pipeline, and who owns it?",
                 ]},
                {"id": 6, "primary": "How is EDR detection and prevention designed — out-of-the-box vs tuned, custom rules, identity correlation?",
                 "sub_questions": [
                    "What custom detections have been authored beyond vendor defaults?",
                    "Are MITRE ATT&CK coverage and gaps measured?",
                    "Is EDR-identity correlation in place (suspicious logon + suspicious binary)?",
                    "Are EDR exclusions inventoried and reviewed?",
                    "How often is the detection rule-set tuned vs left static?",
                 ]},
                {"id": 7, "primary": "How does EDR integrate with the broader stack — SOAR, SIEM, identity, network — and what is the validated MTTR for an EDR-triggered case?",
                 "sub_questions": [
                    "What automated actions are wired between EDR and SOAR (isolate, quarantine, reset)?",
                    "Is enrichment (identity, asset tier, recent change) automatic on case creation?",
                    "What is the measured MTTD and MTTR for high-fidelity EDR cases?",
                    "Are EDR cases reviewed for false-positive vs true-positive ratios?",
                    "How is EDR coverage and uptime monitored?",
                 ]},
            ],
        },
        {
            "id": 3, "title": "Detection, Logging & Monitoring",
            "intent": "Probe SIEM coverage, use-case maturity, and oversight to assess whether tampering or compromise would actually be seen in time.",
            "questions": [
                {"id": 8, "primary": "What is the SIEM coverage and logging architecture — sources, retention, ingest health — and where are critical sources missing?",
                 "sub_questions": [
                    "Which platform is in use, and what is the daily ingest volume?",
                    "Which log sources are required by policy but not connected today?",
                    "What is the retention model for hot vs cold logs?",
                    "How is ingest health monitored, and what is the alert if a source goes silent?",
                    "Are tier-0 sources (DC security log, KMS, PAM, backup admin) all on?",
                 ]},
                {"id": 9, "primary": "What is the use-case library maturity — MITRE coverage, custom analytics, tuning cadence — and where are detection gaps known to be?",
                 "sub_questions": [
                    "How many production use-cases exist, and how are they mapped to ATT&CK?",
                    "What is the documented coverage gap, and where is it documented?",
                    "How often are use-cases tuned, retired, or added?",
                    "Are detections measured for false-positive rate, true-positive rate, time-to-detect?",
                    "Is detection engineering a defined team function or an ad-hoc activity?",
                 ]},
                {"id": 10, "primary": "What is the monitoring and oversight model — 24x7 SOC, MDR, hybrid — and where are blind spots in escalation or analyst tier coverage?",
                 "sub_questions": [
                    "Is SOC in-house, MSSP, or hybrid, and what is each tier responsible for?",
                    "What is the documented escalation path during off-hours and major incidents?",
                    "Are analyst tier handoffs clean, and is context preserved?",
                    "Are MDR providers SLA-bound on response time and outcome?",
                    "When did SOC last surface a tier-1 incident in real time?",
                 ]},
            ],
        },
        {
            "id": 4, "title": "Incident, Ransomware & Remote-Access Readiness",
            "intent": "Test whether ransomware-IR and remote-access controls hold under real conditions.",
            "questions": [
                {"id": 11, "primary": "Describe the ransomware IR playbook and ownership today — who owns it, how current is it, when was it last exercised?",
                 "sub_questions": [
                    "Who is the named owner of the ransomware playbook, and when was it last updated?",
                    "Is the playbook scenario-specific (encryption, exfiltration, double-extortion) or generic?",
                    "Are roles defined down to the named individual or only by function?",
                    "When was the last tabletop or live exercise?",
                    "What changed structurally after the last exercise?",
                 ]},
                {"id": 12, "primary": "How is ransomware detection and escalation designed — what triggers a 'this is ransomware' declaration, and who has authority to do it?",
                 "sub_questions": [
                    "What technical signals trigger ransomware suspicion (mass file change, EDR, honey-file)?",
                    "Who declares ransomware, and what timeline must they meet?",
                    "Are SOC, ITSM, identity, and storage teams simultaneously alerted?",
                    "What is the documented decision authority for shutting down critical systems?",
                    "When was the last suspected ransomware incident, and how did the declaration timeline behave?",
                 ]},
                {"id": 13, "primary": "What containment and isolation capability exists — network, identity, endpoint — and how fast can it be invoked?",
                 "sub_questions": [
                    "Can the SOC isolate endpoints at scale via EDR — what is the measured time?",
                    "Can identity disable affected accounts or revoke tokens at scale?",
                    "Are network containment paths (BGP, ACL, NAC) ready and tested?",
                    "Can third-party connectivity be cut quickly?",
                    "What is the documented blast-radius containment objective?",
                 ]},
                {"id": 14, "primary": "How is recovery decisioning structured — who decides to pay versus rebuild, who validates clean state, who signs off on reintroduction?",
                 "sub_questions": [
                    "Is there a pre-approved decision tree for ransom payment versus rebuild?",
                    "Who validates that a recovery candidate is clean before reintroduction?",
                    "What is the documented criteria for declaring a system clean?",
                    "Who has signing authority for each major recovery decision?",
                    "Has the legal / regulatory / insurance path been pre-walked?",
                 ]},
                {"id": 15, "primary": "What is the VPN, ZTNA, and internet-access posture for remote work and third-party access — and where does it remain a soft target?",
                 "sub_questions": [
                    "What VPN / ZTNA platform is in use, and is it MFA-enforced end-to-end?",
                    "How is split-tunnel vs full-tunnel governed?",
                    "Are vendor / third-party VPN paths separated from employee paths?",
                    "How are exposure and patching of the VPN/ZTNA platform itself managed?",
                    "When was the last VPN posture review or red-team exercise?",
                 ]},
            ],
        },
        {
            "id": 5, "title": "Framework Alignment & Priorities",
            "intent": "Anchor in security framework posture and the single biggest improvement.",
            "questions": [
                {"id": 16, "primary": "Which security frameworks anchor your control set today — NIST CSF, ISO 27001, MAS TRM, CSA CCoP, PCI-DSS — and where does framework coverage hide real gaps?",
                 "sub_questions": [
                    "Which frameworks are formally adopted, and which are mapped but not adopted?",
                    "Where do frameworks overlap, and where do gaps fall between them?",
                    "What is the documented owner of framework conformance?",
                    "How is framework drift detected as controls change?",
                    "Are framework results communicated to leadership and the board?",
                 ]},
                {"id": 17, "primary": "What is the audit and certification posture — open findings, remediation track record, regulator-facing evidence — and where are findings repeatedly recurring?",
                 "sub_questions": [
                    "What audit / certification activity is current (ISO, SOC 2, regulator, internal)?",
                    "How many findings are open, and how many are aged beyond SLA?",
                    "Which findings recur audit-over-audit, and why?",
                    "How is evidence collection automated versus manual?",
                    "When was the last regulator interaction, and what was their take?",
                 ]},
                {"id": 18, "primary": "If you had budget and political capital for exactly one security improvement this year, what would most materially strengthen cyber-recovery readiness — and why hasn't it been done?",
                 "sub_questions": [
                    "Name the single highest-impact security improvement on the backlog.",
                    "What constraint blocks it — funding, ownership, vendor capability, risk appetite?",
                    "Where does the 12-month security roadmap explicitly invest in recovery rather than detection alone?",
                    "What residual risk would remain even after the best single improvement?",
                    "What is the smallest credible step that could change recovery posture in 90 days?",
                 ]},
            ],
        },
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# COMPUTE AND VIRTUALIZATION
# ─────────────────────────────────────────────────────────────────────────────
COMPUTE_DOMAIN = {
    "title": "Compute & Virtualisation Resilience",
    "facilitator_intro": (
        "Start with the compute estate and hardening posture, then test whether privilege controls, hosting boundaries, "
        "and rebuild capability can actually deliver service-level recovery rather than just bring up VMs."
    ),
    "layers": [
        {
            "id": 1, "title": "Compute Estate Baseline & Hardening",
            "intent": "Establish what compute exists, the hardening standard, and patch hygiene before probing privilege and hosting controls.",
            "questions": [
                {"id": 1, "primary": "Paint a picture of the compute estate — physical, virtual, container, cloud-hosted — and where crown-jewel workloads actually run.",
                 "sub_questions": [
                    "What is the breakdown of physical, virtual, and container workloads?",
                    "Which hypervisor and container platforms are in use, and what versions?",
                    "Where do crown-jewel workloads land — dedicated clusters, shared infrastructure, cloud?",
                    "Are there legacy or end-of-life OS instances still in production?",
                    "What is the inventory accuracy compared to the CMDB?",
                 ]},
                {"id": 2, "primary": "What hardening baseline is enforced — CIS, vendor, internal — and how is drift from baseline detected and remediated?",
                 "sub_questions": [
                    "What baseline standard is in use per OS family?",
                    "What fraction of the estate is baseline-conformant, and how is that measured?",
                    "How is drift detected — periodic scan, agent, continuous monitoring?",
                    "Are exceptions tracked and time-bound?",
                    "When was the baseline last revised against current threats?",
                 ]},
                {"id": 3, "primary": "How is patch governance and cadence run — risk-based, SLA-based, exception-heavy — and which workloads are habitually behind?",
                 "sub_questions": [
                    "What is the documented patching cadence per OS and per tier?",
                    "What is the measured patch compliance rate today?",
                    "Which workloads habitually breach SLA, and on what rationale?",
                    "How are vendor / appliance / OT systems patched, if at all?",
                    "When was the last critical zero-day patch cycle, and how did it perform?",
                 ]},
            ],
        },
        {
            "id": 2, "title": "Privilege & Lateral Movement Controls",
            "intent": "Probe admin identity, privilege scoping, and lateral-movement prevention on compute.",
            "questions": [
                {"id": 4, "primary": "What is the admin and identity structure on compute — local accounts, domain, cloud — and how is privileged access scoped?",
                 "sub_questions": [
                    "Are local-admin accounts removed or LAPS-rotated?",
                    "What is the model for compute admin — domain admin, jumpbox, PAW?",
                    "Are admin actions tied back to named individuals?",
                    "Are service accounts inventoried, scoped, and rotated?",
                    "What is the policy for shared admin credentials?",
                 ]},
                {"id": 5, "primary": "How are admin access paths restricted — jump hosts, PAW, bastion, ZTNA — and what is the credential-caching posture?",
                 "sub_questions": [
                    "Is admin access only via PAW or jump host, or are direct connections allowed?",
                    "Are credentials cached on intermediate hosts?",
                    "How is RDP / SSH from user endpoints to servers governed?",
                    "Is just-in-time elevation enforced for admin operations?",
                    "When was the last review of allowed admin paths?",
                 ]},
                {"id": 6, "primary": "What lateral-movement prevention exists — LAPS, SMB hardening, AppLocker / WDAC, exploit protection — and where does it fall short?",
                 "sub_questions": [
                    "Is LAPS deployed across the Windows estate, and is rotation healthy?",
                    "Is SMB v1 fully removed and SMB signing enforced?",
                    "Is AppLocker / WDAC / equivalent enforced on servers?",
                    "Are credential-theft protections (Credential Guard, RemoteCredentialGuard) enforced?",
                    "When were lateral-movement controls last validated by purple team?",
                 ]},
            ],
        },
        {
            "id": 3, "title": "Application Hosting & Data Boundaries",
            "intent": "Probe how production, dev, and test environments are separated and how data flows between them.",
            "questions": [
                {"id": 7, "primary": "What is the hosting environment layout — Prod / Dev / Test / Staging — and how strictly are boundaries enforced?",
                 "sub_questions": [
                    "Are environments on separate clusters, separate identity, separate network zones?",
                    "Can a Dev account or workload reach Prod data?",
                    "How are environment promotions controlled?",
                    "Are shared services (DNS, identity, monitoring) properly partitioned?",
                    "Where do boundaries blur in practice?",
                 ]},
                {"id": 8, "primary": "How are shared services (identity, KMS, monitoring, backup) hosted relative to the workloads they serve, and where do their failure modes converge?",
                 "sub_questions": [
                    "Are shared services architected with their own tier and resilience posture?",
                    "Do shared services depend on each other in undesirable ways?",
                    "How are shared services secured at the management plane?",
                    "What is the impact radius if a shared service is compromised?",
                    "When was the last shared-services-dependency review?",
                 ]},
                {"id": 9, "primary": "How is data handling and movement between environments governed — masking, synthetic data, vendor access?",
                 "sub_questions": [
                    "Is production data ever present in Dev or Test, and on what controls?",
                    "Are masking or synthetic-data tools in place?",
                    "How is vendor access to data governed?",
                    "What controls prevent data exfiltration from lower environments?",
                    "When was the last data-movement audit?",
                 ]},
            ],
        },
        {
            "id": 4, "title": "Resilience, Recovery & Database Hosting",
            "intent": "Test cluster HA, rebuild capability, and database-resident workload protection — where compute is the recovery surface.",
            "questions": [
                {"id": 10, "primary": "What is the clustering and HA architecture across the estate — VMware HA, FT, Kubernetes, application clustering — and what is the measured failover behaviour?",
                 "sub_questions": [
                    "Which workloads use vendor HA / FT versus application clustering?",
                    "What is the measured failover time for each major class?",
                    "When was HA last actively exercised?",
                    "Where do clusters share dependencies that could fail simultaneously?",
                    "Are split-brain and quorum failure modes understood?",
                 ]},
                {"id": 11, "primary": "What are the RTO and RPO targets per workload tier, and what is technically achievable today rather than committed in policy?",
                 "sub_questions": [
                    "Are RTO/RPO documented per workload tier and per service?",
                    "What is the proven RTO/RPO in tests rather than committed in BIA?",
                    "Where do business commitments diverge from technical reality?",
                    "Are RTO/RPO gaps formally accepted or unmanaged risk?",
                    "Who owns the gap when objectives are missed?",
                 ]},
                {"id": 12, "primary": "What is the rebuild and reprovisioning capability — golden images, IaC, automated rebuild — and what is the measured time to stand up a clean replacement?",
                 "sub_questions": [
                    "Are golden images current and signed?",
                    "Is rebuild automated via IaC (Terraform, Ansible, ARM, CloudFormation)?",
                    "What fraction of the estate is rebuildable from code today?",
                    "When was the last full rebuild test for a tier-1 workload?",
                    "Where do manual steps still dominate rebuild?",
                 ]},
                {"id": 13, "primary": "When was the last comprehensive recovery test, and what did it reveal about service-level recovery rather than VM bring-up?",
                 "sub_questions": [
                    "Was the last test scenario-based (cyber, regional, supply-chain) or technical-only?",
                    "Did the test exercise full business service recovery, or stop at infrastructure?",
                    "Were business owners and risk participants part of validation?",
                    "What did the test reveal that surprised the team?",
                    "Were findings closed out and re-tested?",
                 ]},
                {"id": 14, "primary": "How are databases hosted today — bare-metal, VM, container, managed cloud — and how do their service identities and access models behave during recovery?",
                 "sub_questions": [
                    "What is the hosting model per crown-jewel database?",
                    "How do databases authenticate (local, AD, managed identity)?",
                    "Are service identities inventoried and recoverable?",
                    "What is the recovery dependency tree for a tier-1 DB?",
                    "Have DBAs, storage, and infra teams jointly tested recovery?",
                 ]},
                {"id": 15, "primary": "What dependencies must be alive before compute recovery can begin — network, identity, storage, fabric — and have they been cold-started together?",
                 "sub_questions": [
                    "Is the dependency chain documented per workload, or only per platform?",
                    "Have dependencies been cold-started together, not just individually?",
                    "What dependency would most likely block recovery today?",
                    "Are vendor-support and license dependencies recoverable when external systems are down?",
                    "What is the documented minimum viable infrastructure to begin recovery?",
                 ]},
            ],
        },
        {
            "id": 5, "title": "Evidence & Priorities",
            "intent": "Anchor in evidence and single biggest compute-side improvement.",
            "questions": [
                {"id": 16, "primary": "Show us the most recent compute rebuild evidence, DR test, or cyber-recovery exercise — what was tested, what failed, what was fixed?",
                 "sub_questions": [
                    "What scenarios were tested in the last 12 months?",
                    "Were findings closed, or do they recur?",
                    "Have auditors or regulators reviewed compute recovery claims?",
                    "What is the evidence chain from build → harden → patch → recover?",
                    "What residual compute risk would you flag today?",
                 ]},
                {"id": 17, "primary": "If you had budget and political capital for exactly one compute improvement this year, what would most materially strengthen cyber-recovery readiness — and why hasn't it been done?",
                 "sub_questions": [
                    "Name the single highest-impact compute improvement on the backlog.",
                    "What constraint blocks it — funding, ownership, complexity?",
                    "Where does the 12-month compute roadmap invest explicitly in recovery?",
                    "What would change if rebuild were truly automated for tier-1 workloads?",
                    "What is the smallest credible step that could change posture in 90 days?",
                 ]},
            ],
        },
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# CLOUD (AWS)
# ─────────────────────────────────────────────────────────────────────────────
CLOUD_AWS_DOMAIN = {
    "title": "Cloud (AWS) Resilience & Recovery",
    "facilitator_intro": (
        "Start with the AWS account structure and IAM baseline before probing network controls, data protection, "
        "detection, and recovery posture. Press past 'we use CloudTrail' answers to whether cloud compromise would "
        "actually be contained and recovered."
    ),
    "layers": [
        {
            "id": 1, "title": "Cloud Account & IAM Baseline",
            "intent": "Establish account topology, identity model, and privileged access in cloud before probing controls.",
            "questions": [
                {"id": 1, "primary": "Paint a picture of the AWS estate today — Organizations, OUs, accounts, regions — and which accounts host crown-jewel workloads.",
                 "sub_questions": [
                    "How many AWS accounts are in use, and what is their OU structure?",
                    "Which accounts host crown-jewel data and workloads?",
                    "Are accounts deployed via Control Tower or a custom landing zone?",
                    "Which regions are active, and are non-active regions blocked or unrestricted?",
                    "Are dev / sandbox / vendor accounts isolated from production?",
                 ]},
                {"id": 2, "primary": "How is identity into AWS structured — federation, SSO, IAM Identity Center, local IAM users — and where does local IAM still persist?",
                 "sub_questions": [
                    "Is human access to AWS federated, or are local IAM users present?",
                    "Which IdP federates with AWS, and is MFA enforced at the IdP?",
                    "Are IAM roles structured by job function and least privilege?",
                    "Are static access keys present, rotated, and minimised?",
                    "What is the inventory of break-glass access in cloud?",
                 ]},
                {"id": 3, "primary": "How is privileged access in cloud governed — root account, Organization management, OU-level admin, SCP escalation paths?",
                 "sub_questions": [
                    "How is the management account protected — root MFA, hardware token, minimal usage?",
                    "What SCPs are in place to constrain privilege, including in management account?",
                    "Are AdministratorAccess assignments time-bound and PIM-equivalent?",
                    "Who can create new accounts or invite external accounts?",
                    "When was the last privileged-access review in AWS?",
                 ]},
            ],
        },
        {
            "id": 2, "title": "Network Segmentation & Cloud Firewalls",
            "intent": "Probe cloud network architecture and enforcement points.",
            "questions": [
                {"id": 4, "primary": "What is the VPC, peering, and Transit Gateway topology — and how is east-west traffic controlled in cloud?",
                 "sub_questions": [
                    "How are VPCs structured per account and per workload tier?",
                    "Is Transit Gateway in use, and how are routing and security controlled?",
                    "Are VPC peerings inventoried, time-bound, and reviewed?",
                    "How are on-prem to cloud paths governed (Direct Connect, VPN)?",
                    "Where do cloud accounts share networking with on-prem zones?",
                 ]},
                {"id": 5, "primary": "How are Security Groups, NACLs, and route tables managed at scale — drift, exceptions, governance — and where are over-permissive paths known?",
                 "sub_questions": [
                    "Is SG management code-driven or click-ops?",
                    "How is drift between intended and actual SGs detected?",
                    "What process governs 0.0.0.0/0 ingress exceptions?",
                    "Are NACLs used as a defence-in-depth layer or left at default?",
                    "When was the last SG / NACL audit?",
                 ]},
                {"id": 6, "primary": "What cloud-native and third-party firewalls are in use — AWS Network Firewall, WAF, third-party — and what do they actually inspect?",
                 "sub_questions": [
                    "Is AWS Network Firewall or third-party FW deployed at egress?",
                    "Is WAF deployed in front of customer-facing apps, and tuned?",
                    "Are TLS-inspection trade-offs documented?",
                    "Is egress traffic inspected and constrained?",
                    "How is firewall policy code-managed and tested?",
                 ]},
            ],
        },
        {
            "id": 3, "title": "Data Protection in Cloud",
            "intent": "Probe S3 / EBS / RDS protection, encryption posture, and KMS governance.",
            "questions": [
                {"id": 7, "primary": "How is public exposure of S3, snapshots, AMIs, and KMS keys prevented, monitored, and remediated?",
                 "sub_questions": [
                    "Is S3 Block Public Access enforced at the org level?",
                    "Are public AMIs and EBS snapshots actively detected and blocked?",
                    "Are KMS key policies reviewed for cross-account exposure?",
                    "What is the response when a public-exposure event is detected?",
                    "When was the last data-exposure audit?",
                 ]},
                {"id": 8, "primary": "What is the encryption-at-rest posture across cloud storage classes — S3, EBS, RDS, DynamoDB, EFS, FSx?",
                 "sub_questions": [
                    "Is encryption enforced by default for all storage classes?",
                    "Are SCPs preventing creation of unencrypted resources?",
                    "Where do legacy unencrypted resources still exist?",
                    "How is encryption verified and reported?",
                    "Are KMS CMKs used where appropriate vs AWS-managed keys?",
                 ]},
                {"id": 9, "primary": "How are KMS keys structured, rotated, and protected — and what is the cross-account, cross-region, and key-policy posture?",
                 "sub_questions": [
                    "How are CMKs organised — per account, per workload, per data class?",
                    "Is key rotation enforced, and on what cadence?",
                    "How are key policies governed against privilege creep?",
                    "Are multi-region keys used where needed, and replicated correctly?",
                    "What is the recovery posture if a key is accidentally scheduled for deletion?",
                 ]},
            ],
        },
        {
            "id": 4, "title": "Detection, Logging & Cloud Recovery",
            "intent": "Probe CloudTrail coverage, detection use cases, and multi-region / cross-account recovery.",
            "questions": [
                {"id": 10, "primary": "What is the CloudTrail, Config, GuardDuty, and Security Hub coverage — across all accounts and regions — and where are blind spots?",
                 "sub_questions": [
                    "Is CloudTrail organization-trail enabled with multi-region and management+data events?",
                    "Are CloudTrail logs delivered to a separate, hardened logging account?",
                    "Is GuardDuty on across all accounts and regions?",
                    "Is Security Hub centralising findings, and who triages them?",
                    "Where are blind spots known — accounts, regions, services?",
                 ]},
                {"id": 11, "primary": "What detection use cases are live for cloud-specific compromise — root account use, key policy change, console login anomaly, exfil pattern?",
                 "sub_questions": [
                    "What is the alerting on root account or management-account activity?",
                    "Are detections in place for IAM policy escalation and key-policy change?",
                    "Are exfiltration-pattern detections (large S3 GET, snapshot copy across account) in place?",
                    "Are GuardDuty findings tuned and triaged, or noise-filtered?",
                    "What is the documented MTTD for cloud-resource compromise?",
                 ]},
                {"id": 12, "primary": "What is the multi-region and multi-AZ DR posture — and which workloads are actually capable of regional failover today rather than only documented as such?",
                 "sub_questions": [
                    "Which crown-jewel workloads are multi-region capable today?",
                    "What is the proven RTO/RPO per workload class in cloud?",
                    "Are DR runbooks IaC-driven and tested?",
                    "Are dependencies (DNS, identity, KMS) regionally distributed?",
                    "When was the last regional-failover test executed?",
                 ]},
                {"id": 13, "primary": "What is the cross-account and cross-region recovery posture for crown-jewel data — and where does the recovery path itself depend on the compromised account?",
                 "sub_questions": [
                    "Are backups and snapshots copied to a separate, isolated recovery account?",
                    "What permissions does the recovery account hold over source accounts?",
                    "Could a compromised management account destroy the recovery account?",
                    "Is the recovery account on a different identity provider or tenant?",
                    "Has cross-account recovery been live-tested?",
                 ]},
                {"id": 14, "primary": "What is the account-takeover and cloud-incident playbook — containment, identity revocation, regional pivot, vendor escalation?",
                 "sub_questions": [
                    "Is there a documented account-takeover playbook current and exercised?",
                    "What is the documented containment time for a compromised IAM principal?",
                    "Is AWS support and the AWS account team pre-engaged for major-incident escalation?",
                    "Who has authority to invoke the playbook and at what threshold?",
                    "When was the playbook last exercised?",
                 ]},
            ],
        },
        {
            "id": 5, "title": "Evidence & Priorities",
            "intent": "Anchor in cloud evidence and the single biggest improvement.",
            "questions": [
                {"id": 15, "primary": "Show us the most recent AWS red-team, regional-failover, or account-takeover exercise — what was tested, what failed, what was fixed?",
                 "sub_questions": [
                    "What cloud-specific scenarios have been tested in the last 12 months?",
                    "What controls broke, and was remediation tracked to closure?",
                    "Have cloud auditors or regulators reviewed posture?",
                    "What residual cloud risk would you flag today?",
                    "How is cloud risk reported to leadership and board?",
                 ]},
                {"id": 16, "primary": "If you had budget and political capital for exactly one cloud improvement this year, what would most materially strengthen cyber-recovery readiness — and why hasn't it been done?",
                 "sub_questions": [
                    "Name the single highest-impact cloud improvement on the backlog.",
                    "What constraint blocks it — funding, vendor capability, ownership?",
                    "Where does the 12-month cloud roadmap invest explicitly in recovery and isolation?",
                    "What would change if cross-account isolation was truly enforced tomorrow?",
                    "What is the smallest credible step that could change posture in 90 days?",
                 ]},
            ],
        },
    ],
}

# Public catalogue keyed by domain identifier.
DOMAINS = {
    "service_mgmt":   {"label": "Service Management", "excel_sheet": "Service Management",       "domain": SERVICE_MGMT_DOMAIN},
    "identity":       {"label": "Identity",           "excel_sheet": "Identity",                 "domain": IDENTITY_DOMAIN},
    "network":        {"label": "Network",            "excel_sheet": "Network",                  "domain": NETWORK_DOMAIN},
    "security_risk":  {"label": "Security & Risk",    "excel_sheet": "Security and Risk",        "domain": SECURITY_RISK_DOMAIN},
    "compute":        {"label": "Compute & Virtualisation", "excel_sheet": "Compute and Virtualization", "domain": COMPUTE_DOMAIN},
    "cloud_aws":      {"label": "Cloud (AWS)",        "excel_sheet": "Cloud (AWS)",              "domain": CLOUD_AWS_DOMAIN},
}
