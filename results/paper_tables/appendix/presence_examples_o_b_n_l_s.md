# Presence examples: O, B, N, L, S

Appendix D of the paper shows, for slots T and U, one expository cell
at each Presence level (0.0 / 0.5 / 1.0). This file provides the same
three-level examples for the remaining five slots. Each block quotes a
generated summary verbatim and explains the gate decision; cells were
chosen among those where both LLM judges and the final label agree.

## O (Outcome/Position)

**O = 0.0** (MTG9, DeepSeek reasoning, 3 sent., run 1)

> Two executive recruitment firms presented qualifications for the city manager search. Council members emphasized community input, candidate diversity, and search timelines. The council has yet to select a firm, leaving the process and engagement approach open.

-> Slot context: the Council heard presentations from two executive-recruitment firms; no disposition selecting, approving, or otherwise closing an acted-on item is recorded beyond the interviews concluding. The summary describes the presentations and an open selection ("has yet to select a firm") -- pendingness, not a disposition tied to an acted-on item. Topic Gate **disposition_verb_tied_to_acted_on_item** fails.

**O = 0.5** (MTG46, Gemini 2.5 Flash Lite, 2 sent., run 3)

> Councilors debated the regulation and siting of cannabis establishments, highlighting issues with the Zoning Board of Appeals process. The discussion led to a referral to committee for further review.

-> Slot context: the Boston hearing order on cannabis-establishment regulation and siting (Docket 0381) was referred to committee. The referral is stated ("led to a referral to committee"), so the Topic Gate passes; but what was referred is never identified -- the summary's only referent is the generic "the discussion", not the docket or the hearing order -- so Quality Gate **acted_on_item_specific** fails.

**O = 1.0** (MTG26, DeepSeek chat, 3 sent., run 3)

> The council approved Resolution 31683 to place Initiative 124 on the November 2016 ballot. Members praised workers' efforts and expressed regret the council could not adopt the initiative directly. The initiative's provisions on panic buttons, workload limits, and anti-retaliation protections remain subject to voter approval.

-> Slot context: Seattle City Council adopted Resolution 31683, placing hotel-employee Initiative 124 on the November 2016 ballot. The disposition (approved) and the specific acted-on item (Resolution 31683, ballot placement of Initiative 124) are both explicit. Quality Gate pass.

## B (Agenda-Setting Background / Precipitating Context)

**B = 0.0** (MTG17, DeepSeek chat, 2 sent., run 1)

> Council rezoned two parcels to allow affordable senior housing. The public had no opposition, but income-mix details remained unresolved.

-> Slot context: the rezoning was shaped by the aging, inefficiently configured Town View affordable-housing site, the parcel's end-of-life condition, prior outreach, and a Planning Board approval. The summary states only the rezoning action and an unresolved detail, with no prior condition or process. Topic Gate **precipitating_context_visible** fails.

**B = 0.5** (MTG32, DeepSeek chat, 2 sent., run 5)

> Council voted to exclude Wells Fargo from banking RFPs and halt new investments until further direction. Discussion centered on Wells Fargo's ethical violations, including fraudulent accounts, Dakota Access pipeline financing, and private prison investments.

-> Slot context: prior Wells Fargo conduct (fraudulent accounts, pipeline financing) and community concern are what brought the Alameda banking referral forward. The summary lists that prior conduct, so the Topic Gate passes; but it presents the conduct only as what the discussion "centered on", without connecting it to why the referral came forward or to its RFP/exclusion form, so Quality Gate **connected_to_current_item_or_form** fails.

**B = 1.0** (MTG31, DeepSeek reasoning, 2 sent., run 3)

> City manager withdrew award recommendation after auditor raised concerns. Council approved a 30-day independent review of the RFP process.

-> Slot context: the recycling-contract award recommendation was withdrawn after the city auditor raised concerns about the RFP process; that withdrawal is why the independent-review motion came forward. The summary states the prior events as their own proposition ("withdrew award recommendation after auditor raised concerns") and they are visibly connected to the current review item. Quality Gate pass.

## N (Outcome-Near Condition / Operative Payload)

**N = 0.0** (MTG16, Gemini 2.5 Flash Lite, 3 sent., run 1)

> The council discussed moving county elections to even years to increase voter turnout.
> Discussions explored potential cost shifts and ballot length impacts from the proposed change.
> Action was deferred to a future meeting to allow for further questions and analysis.

-> Slot context: the proposed charter amendment carried operative payload -- ballot placement, affected county offices, term-transition mechanics, and timing. The summary states only discussion, cost/ballot-length concerns, and deferral; per the gate's not-match wording, saying only that the body deferred or discussed the item attaches no payload to the action. Topic Gate **payload_attached_to_action** fails.

**N = 0.5** (MTG19, Gemini 2.5 Flash Lite, 3 sent., run 5)

> The council debated a referral to explore designating Alameda a sanctuary city. Opponents cited public safety and economic concerns, while proponents emphasized inclusivity and protection for vulnerable residents. The council voted to direct staff to analyze the implications and potential policy options.

-> Slot context: the sanctuary-city referral directed staff to return with analysis of financial impacts, cooperation limits, and policy options. The summary attaches a payload to the action ("direct staff to analyze the implications and potential policy options"), so the Topic Gate passes; but the payload shows no identifiable number, named requirement, scope boundary, or date cutoff, so the any-of Quality Gate fails.

**N = 1.0** (MTG18, Gemini 2.5 Flash Lite, 3 sent., run 4)

> A resolution directing a third-party cost estimate and racial equity analysis for the North Precinct project was debated. Council members expressed concerns about project costs and community engagement time. The council ultimately adopted the resolution to proceed with the analysis and cost-saving measures.

-> Slot context: the adopted North Precinct resolution carried review requirements, including a third-party cost estimate and a racial equity analysis. The summary attaches these named requirements to the resolution ("directing a third-party cost estimate and racial equity analysis"); **named_requirement** satisfies the any-of Quality Gate.

## L (Concrete Concern)

**L = 0.0** (MTG2, DeepSeek reasoning, 2 sent., run 2)

> Jay Osborne was confirmed as director of the King County Department of Human Resources via unanimous vote after an amendment.
> Committee approved a wastewater bond refinancing saving ~$20 million, but deferred final action to later that afternoon.

-> Slot context: the discussion raised concrete operational concerns about HR centralization -- inconsistent HR capacity across departments, slow hiring, hard-to-fill vacancies, and retention risk. The summary states only completed actions and a savings figure; no problem-side condition is asserted anywhere. Topic Gate **concrete_concern_language** fails.

**L = 0.5** (MTG15, Gemini 2.5 Flash Lite, 2 sent., run 3)

> The council reviewed a call for review of the Planning Board's denial of a use permit for off-sale alcohol at a convenience store. Arguments centered on neighborhood impact, precedent, and changing conditions, but no council majority was reached to overturn the original denial.

-> Slot context: concerns around the off-sale alcohol permit included nuisance activity, loitering, drunkenness, over-concentration, and business fairness. The summary asserts concern language ("Arguments centered on neighborhood impact, precedent, and changing conditions"), passing the Topic Gate; but the reader cannot tell what the neighborhood-impact concern actually is, so Quality Gate **specific_concern_content** fails.

**L = 1.0** (MTG48, DeepSeek reasoning, 3 sent., run 5)

> The council passed a $1.33 billion BPS budget and a $3.6 billion capital plan after extensive debate on equity and accountability. Council debate focused on low literacy rates, lack of outcome data, and inequitable capital investments across neighborhoods. The council approved an amended operating budget with over $25 million in amendments, which now awaits the mayor's response.

-> Slot context: concerns in the Boston schools budget debate spanned school performance, missing outcome data, and inequitable capital investment. The summary asserts specific problem-side conditions ("low literacy rates, lack of outcome data, and inequitable capital investments across neighborhoods"). Quality Gate pass.

## S (Shared Concern Synthesis)

**S = 0.0** (MTG17, DeepSeek reasoning, 2 sent., run 1)

> Staff recommended approval to rezone 1660-1684 Grove Street for a dense mixed-use affordable housing project. The measure passed, with council emphasizing integrated income levels and future master planning for up to 300 units.

-> Slot context: the recurring theme was preserving affordable, mixed-income housing in a changing West Colfax area while avoiding displacement. The summary frames affordability only as a feature of the approved project ("emphasizing integrated income levels"), with no problem-side language. Topic Gate **problem_side_concern** fails.

**S = 0.5** (MTG39, Gemini 2.5 Flash Lite, 2 sent., run 2)

> The rezoning of 351 South Jackson Street passed, aligning the property with the Cherry Creek Area Plan and allowing for mixed-use development. Discussions highlighted pedestrian access concerns across Cherry Creek Drive and the use of city reserves for housing initiatives.

-> Slot context: the recurring concern was that Cherry Creek growth was outpacing pedestrian and transportation infrastructure. The summary names the theme ("pedestrian access concerns across Cherry Creek Drive"), passing the Topic Gate; but it does not specify the concern content -- that crossings and mobility investment were not keeping pace with new units -- so Quality Gate **specific_content** fails.

**S = 1.0** (MTG46, DeepSeek chat, 2 sent., run 1)

> Councilor Edwards detailed the Zoning Board of Appeals obstructing equitable cannabis licensing, proposing its removal. Councilors Flaherty, Block, and others debated preserving the half-mile buffer and streamlining approvals.

-> Slot context: the recurring theme was fairness, predictability, and equity in Boston's cannabis approval and siting process. The summary names the theme in problem-side language ("Zoning Board of Appeals obstructing equitable cannabis licensing") and identifies mechanisms of concern (ZBA authority, the half-mile buffer). Quality Gate pass.

