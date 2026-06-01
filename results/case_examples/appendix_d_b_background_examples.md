# Appendix D: Background (B) Presence Boundary Examples

These are real evaluated cells from the SIEVE artifacts, not constructed examples.
The first three examples show final B Presence labels 0.0, 0.5, and 1.0. The fourth example shows a V1 IAA severe disagreement where the main/final label was 0.0 and the second-author audit label was 1.0.

## B_presence_0.0

- Segment / meeting: `01_DenverCityCouncil_09122016` / `MTG1`
- Generator / budget / run: `deepseek_reasoning` / `budget_02` / `run_05`
- Final B Presence: `0.0`

**Generated summary text**

The council voted 7-5 to advance Council Bill 626, an alternative affordable housing fund, to second reading. After hearing from concerned community members, the council approved the Sun Valley rezoning to allow up to eight-story development.

**B source-side context**

Several agenda items were shaped by source-side background conditions. Council Bill 430 was postponed because notice requirements had not been met. Council Bill 509 came forward because an old, narrow PUD tied to a former bakery no longer fit the separately addressed and separately taxed parcels. Council Bill 563 came forward to implement recently adopted Sun Valley and Decatur-Federal station-area plans and to move away from industrial zoning that was treated as a barrier to the neighborhood vision. The on-call contract block was called out because council members wanted routine utilization and spending information. Council Bill 626 arose because some council members viewed the original affordable-housing funding proposal as insufficient or too slow and wanted to explore more funding sources. Resolution 759 was shaped by prior debate over red-light-camera enforcement and yellow-light timing.

**Why this label**

The summary reports current action/debate content but does not state a separate prior condition, process, problem, or pressure that visibly shaped why the item came forward or took its current form.

## B_presence_0.5

- Segment / meeting: `07_LongBeachCC_06102014` / `MTG7`
- Generator / budget / run: `deepseek_reasoning` / `budget_02` / `run_01`
- Final B Presence: `0.5`

**Generated summary text**

Council debated delaying RMD implementation but motions tied, leaving prior authorization intact. Public testimony opposed cuts, but no policy change was adopted.

**B source-side context**

The discussion was shaped by several prior and current conditions: RMD had been discussed for years and included in the FY14 budget, implementation had been delayed, the Fire Department was projected to finish FY14 on budget because of one-time funds and salary savings, the FY15 proposed budget included RMD, and eliminating RMD would require about $1.4 million in other Fire Department reductions. The item also arose against County EMS pilot authorization and past budget-deficit reasoning for the model.

**Why this label**

The summary names background or prior conditions, so B is partly reached, but the connection to the current item/proposal form/handling is too thin or incomplete for full Presence.

## B_presence_1.0

- Segment / meeting: `31_LongBeachCC_03222016` / `MTG31`
- Generator / budget / run: `deepseek_reasoning` / `budget_03` / `run_03`
- Final B Presence: `1.0`

**Generated summary text**

City manager recommended rejecting all bids for a 30-day independent review after auditor raised concerns.  
Council approved a compromise motion for a third-party review selected by the city attorney, avoiding contract extension.  
The review will examine written protests, verbal allegations, and RFP steps, reporting by June 14th.

**B source-side context**

The current action was shaped by a prior recycling RFP process, vendor protests and comments, questions raised at earlier council discussion, and a City Auditor memorandum expressing concern. The timeline pressure came from the existing Waste Management contract expiring on June 30, 2016, making a long audit, rebid, or extension operationally consequential.

**Why this label**

The summary states prior events, conditions, process history, or pressure-setting facts and visibly connects them to the current item, debate frame, timing, or handling.

## B_audit_severe_main_0_to_second_1 (IAA143)

- Segment / meeting: `13_LongBeachCC_03102015` / `MTG13`
- Generator / budget / run: `deepseek_temp1_chat` / `budget_03` / `run_03`
- Final B Presence: `0.0`
- Second-author audit B Presence: `1.0`

**Generated summary text**

Council adopted mandatory spay/neuter for dogs with exemptions, effective October 1, 2015. A councilmember proposed grandfathering currently licensed unaltered dogs to mitigate revenue loss and budget impact. Opponents argued enforcement would burden low-income owners, while supporters cited reduced shelter euthanasia as the primary benefit.

**B source-side context**

The ordinance was shaped by a prior November 2014 council direction to return with an ordinance, a longer reform narrative dating back years, and continuing concerns that pet overpopulation, shelter intake, and euthanasia remained problems despite increased adoptions and prior voluntary efforts.

**Why this label**

Severe audit disagreement example: main/final B=0.0, second-author audit B=1.0.

**Main-label-side reading**

Human-final reading required a prior or existing condition that shaped why the item came forward or took its form; general topic context was insufficient.

**Second-author audit reading**

Summary states background (grandfather clause proposal, enforcement burden, shelter euthanasia rationale) connected to the ordinance adoption.
