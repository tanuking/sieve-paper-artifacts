# Experimental Protocol

Current instrument tag: `sieve_v6_2026_05_02`

## Current Paper Implementation Note

The reproducibility source of truth for the current paper run is the
code/artifact pair below.

- Sampling manifest:
  `artifacts/segment_main_50_body_balanced/manifests/sample_50.csv`
- Sampling provenance:
  `artifacts/segment_main_50_body_balanced/manifests/provenance.json`
- Summary generation:
  `src/meetingbank/summary_artifacts.py`
- Model profiles:
  `src/llm/config.py`

Current main paper analyses use the active `meeting01_50` artifact set:
50 original MeetingBank segments, each from a distinct reconstructed
meeting. The separate `calibration_meetings/` directory contains three
instrument-development meetings and is not part of the final quantitative
sample.

## Sampling Strategy

### 単位
segment（MeetingBank の original row）

本研究の primary evaluation unit は、MeetingBank の original
segment transcript とする。full-meeting transcript の再構成は
primary task から外し、必要な場合のみ supplementary context と
して扱う。論文では "we sample one original MeetingBank segment per
meeting and evaluate segment-level summarization under fixed sentence
budgets" と明記する。

**Important**: MeetingBank は dataset-provided meeting identifier を
持たない。`meeting_id` は `uid` の `会議体 + 日付` から operational に
再構成するが、その用途は **one-meeting-one-sample 制約の適用** に
限る。評価対象そのものは `uid` で識別される original segment である。

### 長さ尺度

長さ threshold の正本は character count ではなく word count とする。
実装上は `segment_word_count = len(transcript.split())` を用いる。

理由は以下。
- model context / cost と直接対応する
- 既存 metadata / sampling script と整合する
- punctuation やレイアウト由来の文字数ノイズに引きずられにくい

### プール定義

sampling pool は以下をすべて満たす original segment に限定する。

- `2500 <= segment_word_count < 20000`
- `summary_word_count >= 15`
- transcript が空でない

理由は以下。
- 2,500 words未満: agenda exchange や短い procedural item が多く、
  2 / 3 / 6文 budget に対する圧縮圧力が弱い
- 20,000 words以上: single segment としては outlier であり、
  latency / cost / context stability が悪化する
- `summary_word_count >= 15`: dataset-provided summary を auxiliary
  validation に使う際、agenda label に近すぎる stub を除外したい

### One-Meeting-One-Sample Rule

confirmatory set と calibration set の両方で、**同一 reconstructed
meeting から複数 sample を取ることを禁止**する。

理由は以下。
- 同一会議内の近接議題は語彙と制度文脈を共有し、独立サンプルとして
  扱いにくい
- one-to-many sampling を許すと、長い会議が過大に効く
- meeting-cluster dependence を analysis に持ち込まずに済む

### Representative Segment Selection

同一 meeting に複数の eligible segment がある場合、代表 segment は
以下の deterministic rule で 1 本に固定する。

1. `meeting_id = uid の 会議体 + 日付` で group 化する
2. その meeting 内で pool 条件を満たす segment だけを残す
3. `segment_word_count` が最大の segment を選ぶ
4. tie の場合は `summary_word_count` が大きい segment を選ぶ
5. それでも tie の場合は `uid` の辞書順で最初の segment を選ぶ

この代表選定では `Ordinance / Resolution / Motion / Other` の type
優先は入れない。meeting 内で model にとって最も圧縮圧力の高い
segment を、恣意的 cherry-picking なしに固定することを優先する。

### Segment Type Stratification

sampling 用の `decision_type` は gold label ではなく、**固定規則による
stratification metadata** として付与する。

- source: dataset-provided segment `summary`
- rule:
  1. `summary.lower()` に `motion` が明示的に現れれば `Motion`
  2. それ以外で `resolution` が明示的に現れれば `Resolution`
  3. それ以外で `ordinance` が明示的に現れれば `Ordinance`
  4. それ以外は `Other`

binary strata は以下。

- `decision-bearing`: `Motion / Resolution / Ordinance`
- `non-decision`: `Other`

この分類は sampling balance 用であり、judge scoring や transcript-first
authoring の gold source ではない。

### Length Bins

balancing variable として以下の length bin を保持する。

- `2.5k-5k`
- `5k-10k`
- `10k-20k`

### Final Sample Selection Algorithm

50本の選定は、代表 segment を確定した後に **固定 seed + city cap** で
行う。

固定仕様:

- random seed: `20260322`
- initial per-stratum city cap: `5`
- sample target: `25 decision-bearing + 25 non-decision`

手順:

1. representative segments を `decision-bearing` / `non-decision` の
   2 strata に分ける
2. 各 stratum 内で固定 seed から `random_key` を 1 つ付与する
3. 各 stratum 内の候補を `(random_key, meeting_id, uid)` で sort する
4. 各 stratum で上から順に候補を見ていき、当該 city の採択数が
   current city cap 未満なら採択する
5. `screen_status` を manifest に残す。current artifact では
   `pending_slot_completeness_screen` として記録されており、この screen
   による除外は current `sample_50` の選定条件には含めない
6. その round で 1 件も採択できなくなった場合のみ、その stratum の
   city cap を `+1` して継続する
7. 各 stratum で 25件ずつ確定採択した時点で `sample_50` を固定する
8. 各 stratum の採択順上位 5件を `calibration_10` とする
9. `sample_50` から `calibration_10` を除いた残りを
   `confirmatory_eval_40` とする

manifest には少なくとも以下を残す。

- `uid`
- `meeting_id`
- `decision_type`
- `segment_type`
- `segment_word_count`
- `summary_word_count`
- `length_bin`
- `city`
- `random_key`
- `candidate_rank_within_stratum`
- `selection_order_within_stratum`
- `selection_city_cap`
- `excluded_reason`

### サンプル数

- 50本
- calibration 10本: `decision-bearing 5` + `non-decision 5`
- confirmatory eval 40本: `decision-bearing 20` + `non-decision 20`
- 全50本が distinct meeting 由来でなければならない

### Slot-Completeness Screen Status

The manifest retains a `screen_status` field for planned slot-completeness
screening. In the current paper artifacts, all 50 rows are marked
`pending_slot_completeness_screen`; therefore slot-completeness screening is
not a completed exclusion criterion for the current sample. Slot applicability
is handled downstream through event-sheet / QA authoring and SIEVE scoring.

### Development / Freeze

- Development phase では instrument を反復改訂する
- 改訂対象は QA schema、judge prompt、authoring-stage static review
  checklist、handoff guard を含む
- Current paper run では、`calibration_meetings/` に退避した3本を
  instrument-development / calibration 用に使用し、active `meetings/`
  の50本を最終 quantitative analysis に使用する
- `sample_50.csv` 内の `calibration_10` / `confirmatory_eval_40` は
  sampling manifest 上の subset metadata として保持されているが、
  current `meeting01_50` analyses では active 50本全体を対象にする
- **Judge prompt content constraint:** judge prompt の共通部分は
  **slot-neutral かつ content-neutral** とする。sample 固有の
  `score_examples` は secondary anchor として bundle から注入されるが、
  共通 prompt 本体は特定 domain の例に依存してはならない。

### Calibration / Pilot Notes

Historical protocol drafts refer to a `calibration_10` / `confirmatory_eval_40`
split. The current artifact tree also contains a separate
`calibration_meetings/` directory with three meetings:

- `01_DenverCityCouncil_10202014`
- `02_KingCountyCC_06022021`
- `03_LongBeachCC_09062016`

These three meetings were moved out of the active 50-meeting set on
2026-05-15 and retained for calibration/test use. They were used for rubric
debugging, QA / judge-prompt development, boundary clarification, and pipeline
checks. They are not included in the final `meeting01_50` quantitative results.

The `calibration_10` rows inside `sample_50.csv` are a manifest subset
(`decision-bearing 5` + `non-decision 5`). Do not confuse this manifest subset
with the separate three-meeting `calibration_meetings/` directory.

Pilot / calibration work is separate from the final quantitative reporting.
Pre-freeze development outputs should not be treated as final SIEVE scores.

**disagreement cell** は、human adjudication 前の
`segment × budget × generator × run × slot` judgment 1件を指す。

pilot pass 条件:

- overall disagreement rate ≤ 18%
- worst-slot disagreement rate ≤ 30%（S は 35% まで許容）
- presence / fact-check routing error が systematic でない（sporadic
  のみ）
- agreement-row silent-error audit ≤ 8%

PASS の場合: instrument を freeze し、active paper sample を統一的に
処理する。

FAIL の場合: instrument を修正し、authoring-stage static review を再実行
して再 pilot。

2 回 FAIL した場合: instrument 設計自体を再検討する。

Pre-freeze pilot labels are not used in the final analysis.


---

## Rule Admission and Human Adjudication

Empirical GPT-vs-Claude disagreement during development does not
automatically imply that a new protocol rule should be added. Before a
disagreement cell is used to revise the instrument, classify it using
`adjudication_policy.md`.

A disagreement may be promoted to a slot semantics or protocol rule only
when all of the following hold:

1. the rule is slot-general rather than meeting-specific;
2. the positive and negative cases are clear to a careful human reader;
3. the rule preserves the Presence / Fact Check separation;
4. the rule can be applied without importing facts outside the QA,
   event sheet, and slot semantics;
5. the ambiguity is likely to recur across summaries or meetings.

If these conditions are not met, the cell remains a human-adjudication
case or is returned to QA authoring / validation, rather than being
converted into a new rule.

Accepted semantic rules are added to `slot_semantics.json`. The judge
prompt must render such rules from `slot_semantics.json`; it must not
own independent semantic rules.

Generated summaries that are internally conflicting can be adjudicated by
humans without being forced into a new general rule. In particular, if a
summary both asserts final passage/enactment and also states that final
handling remained pending, and the wording cannot be resolved by the
existing stage rules, the case is flagged for human adjudication rather
than patched through meeting-specific QA wording.

---

## Authoring Documents

event sheet と `qa_<meeting_order>.json` の作成規則は以下に分離した。

artifact filename は transition 期間中しばらく `meeting_order` という
legacy 名を残してもよいが、各 artifact が指す実体は sampled segment
である。

- slot の意味定義: [`slot_semantics.json`](./slot_semantics.json)
- event sheet の作成規則: [`event_sheet_protocol.md`](./event_sheet_protocol.md)
- QA の作成規則: [`qa_authoring.md`](./qa_authoring.md)
- QA の検証規則: [`qa_validation.md`](./qa_validation.md)

QA authoring では 7 slot を一貫した schema で作成し、その後
`qa_validation.md` に従って authoring-stage static review artifact を
作成する。

MeetingBank の dataset-provided `summary` は **primary source ではない**。
event sheet と QA は transcript-first で作成する。ただし
`qa_validation` PASS 後に、dataset summary との auxiliary alignment
check を追加する。

この cross-check の役割は以下に限る。

- slot T / O / N の gross framing が transcript 読みと大きく
  食い違っていないか確認する
- actor / stage / issue の取り違えを早期に発見する
- transcript を primary source としたまま、segment-level 既存
  annotation を weak validation として利用する

dataset summary は gold target ではなく、judge scoring の直接参照
ラベルにも使わない。

cross-check で gross mismatch が見つかった場合は、freeze 前に
event sheet / QA を reopen し、以下のいずれかに解決する。

1. transcript-first authoring error
2. dataset summary の不完全さ / 誤り
3. harmless framing difference

解決結果は authoring audit に記録する。

この `protocol.md` は sampling / generation / evaluation / pilot /
analysis の運用プロトコルを扱う。slot-level semantics, gate
construction, and QA validation criteria are not restated here. Those
are defined in [`slot_semantics.json`](./slot_semantics.json),
[`qa_authoring.md`](./qa_authoring.md), and
[`qa_validation.md`](./qa_validation.md). If this file and those files
appear to disagree about slot behavior, the slot-specific method files
are the source of truth.

## 要約生成

### Budget sweep

Current paper run uses 2 / 3 / 6 sentence budgets. Each sentence is instructed
to contain no more than 25 words. The implementation validates the exact number
of sentences after generation and retries up to three times; it does not
post-hoc truncate summaries.

### Generation Input

primary task の生成入力は **sampled original segment transcript only**
とする。full-meeting reconstruction は generator に渡さない。
Dataset-provided summaries, event sheets, QA files, reference summaries, and
metadata are not included in the generation prompt.

### プロンプト

source of truth は `summary_artifacts.py` の `SUMMARY_PROMPT_TEMPLATE`。
freeze 時に固定。

The system prompt used by the shared LLM client is:

```text
You are a concise helpful assistant.
```

The user prompt is:

```text
You are summarizing one sampled public-meeting segment for a policy
analyst. The analyst needs a concise, factual briefing on what happened
in this segment, what shaped the discussion, and what remains open
afterward.

Write exactly {N} sentences. Each sentence must contain no more than
25 words. Use plain prose only — no bullet points, numbered lists,
or headings. Each sentence should express one main point.

Prioritize the developments that materially changed, clarified, or
constrained the item during this segment. Avoid trivial procedural
detail such as roll call, adjournment times, and routine declarations,
but retain procedural outcomes when they are substantively important.

=== TRANSCRIPT START ===
{transcript}
=== TRANSCRIPT END ===
```

### Run設計

Each `meeting × generator × budget` condition has five independent runs
(`run_01` ... `run_05`). Current main paper profiles are:

| profile | provider model | request options |
|---|---|---|
| `deepseek_temp1_chat` | `deepseek-chat` | `temperature=1.0` |
| `deepseek_reasoning` | `deepseek-reasoner` | provider default temperature |
| `gemini_2_5_flash_lite` | `gemini-2.5-flash-lite` | provider default temperature |

Qwen profiles exist in code as exploratory / supplementary profiles, but they
are excluded from the current main paper analyses.

---

## 評価パイプライン

### Step Order

運用順序は以下とする。

1. `event_sheet`
2. `qa_authoring` (`qa_<meeting_order>.json` を作成; recommended order is
   `T/O/N` then `B/L/S/U`)
3. `qa_validation` (`annotations/preflight_<meeting_order>.md` を作成し
   PASS を確認)
4. dataset-summary auxiliary cross-check
5. `step3` (`check_bundles` build)
6. `QA -> step4 handoff check`
7. `step4` machine judging
8. pilot analysis (calibration 10 only; see Pilot section above)

`qa_validation` の PASS artifact がなければ `step3` に進めない。

ここで authoring-stage static review は `qa_<meeting_order>.json` の
静的 judgeability review であり、LLM API や empirical judge output は
使わない。

`QA -> step4 handoff check` は別工程であり、生成済み `check_bundles` の
metadata が current `event_sheet_<meeting_order>.md`、
`qa_<meeting_order>.json`、judge prompt version と一致していることを
確認する。

この handoff check が未実施または不一致の場合、その `step4` judge
output は無効とみなす。

### Provenance / Version Guard

`check_bundles` には少なくとも以下の metadata を埋め込む。

- `protocol_version`
- `qa_schema_version`
- `judge_prompt_version`
- `slot_semantics_sha`
- `event_sheet_sha`
- `qa_sha`
- `question_bundle_version`

同じ metadata は judge outputs と downstream aggregate artifacts にも
伝播させる。

`step4` 実行前には、bundle 側 metadata が current `event_sheet`、
current `qa`、current judge prompt version と一致していることを確認
する。不一致なら hard-fail とする。

aggregation 時にも mixed-version artifact を拒否する。
`protocol_version`, `qa_schema_version`, `judge_prompt_version`,
`slot_semantics_sha`, `event_sheet_sha`, `qa_sha`,
`question_bundle_version` のいずれかが混在している場合、その集計は
停止しなければならない。

### Judge

GPT-5 + Claude Sonnet 4.6。生成モデル（DS, QW）と judge が別ファミリー。

### Judge API Configuration

| Parameter | GPT-5 | Claude Sonnet 4.6 |
|---|---|---|
| Max output tokens | 8192 | 8192 |
| Temperature | unset | 0 |
| Reasoning effort | low | N/A |

### Scoring

- Scoring order is fixed: `Topic Gate` -> `Quality Gate` -> `Fact Check`
- Presence is locked immediately after the quality-gate decision and
  must not be revised by later fact-check reasoning
- Presence uses three values only: `0.0`, `0.5`, `1.0`
- `0.0`: topic gate fail
- `0.5`: topic gate pass + quality gate fail
- `1.0`: topic gate pass + quality gate pass
- Fact check is evaluated only when `Presence > 0`
- Omission is not penalized in fact check; only contradiction or
  meaning-changing inaccuracy is penalized
- Multi-part canonical answers may be partially covered; partial but
  accurate coverage is reflected in Presence rather than
  double-penalized in fact check

Gate operators, per-slot positive/negative boundaries, and example
design rules are defined outside this file in the slot-specific method
docs. This file does not restate slot-by-slot scoring behavior.

### Adjudication

- 2 judge 一致 → そのスコア
- 2 judge 不一致 → human adjudication

primary analysis の outcome は **adjudicated final label** である。raw
judge labels は reliability / disagreement / QC diagnostics に使うが、
main model の repeated-measure observation には使わない。

### Silent Error Audit

agreement rows の 5-10% を transcript に対する human audit に回す。
audited agreement row が誤りだった場合は、final adjudicated label を修正し、
修正理由を audit log に残す。silent-error rate は報告する。

---

## 分析計画

独立な分析単位は 40 confirmatory segments。

primary outcome cell は
`segment × budget × generator × run × slot` の adjudicated final label
である。

main analysis の within-segment repeated factors は以下。

- `budget`
- `slot`
- `generator family`
- `generation mode`
- `run`

judge は main analysis の repeated factor ではなく、reliability
diagnostic として扱う。

**Confirmatory spine:** 論文の主張は以下の3軸で構成する。

1. **budget** (2 / 3 / 6 sentences)
2. **slot** (7 compression-failure roles)
3. **segment type** (`decision-bearing` / `non-decision`)

**answer property tags (`answer_locality` / `marker_presence` /
`surface_salience`) は confirmatory spine には含めない。** secondary
diagnostic / exploratory moderator として annotate は続けるが、
main claim には最初から入れない。

### Evidentiary Framing

本評価系は、meeting 全体の complete coverage を測るのではなく、
**selected segment fidelity** を測る。各 slot の source of truth は、
event sheet に記録された slot-specific evidence である。

### Structural Segment Variables

segment structure の evidentiary covariates として、少なくとも以下を
保持する。

- `segment_word_count`
- `summary_word_count`
- `decision_type`
  - `Ordinance / Resolution / Motion / Other`
- `city`
- `meeting_segment_count`
  - sampled segment が属していた original meeting 内の total segment 数

`segment_word_count` は圧縮率の強さを表す。
`summary_word_count` は weak validation source の情報量を表す。
`decision_type` は segment の制度的 form を表す。
`meeting_segment_count` は sampled unit の背後にある meeting clutter の
粗い proxy として使う。

これらは judge score そのものではなく、segment-structure moderator
として扱う。

### Auxiliary Validation Diagnostic

`dataset_summary_alignment` を QC 用の derived diagnostic として導入
する。

- 定義: transcript-first authoring 結果と dataset-provided summary の
  整合 / 不整合フラグ
- 目的: segment-level の既存 annotation を weak validation として記録し、
  明らかな transcript misread を点検する
- 入力:
  - transcript-first event sheet / QA
  - dataset-provided `summary`

この指標は confirmatory main outcome ではなく、QC appendix と
authoring audit に使う。

### Cross-Family Structural Sensitivity

cross-family に一貫して落ちる slot は、segment type や length に対する
感度が高い slot とみなす。

現時点では `U` よりも `T` と `N` の方が、segment length や decision
form に対する構造感度の強い候補である。したがって
structure-related moderator を main text で扱う場合、まず `T / N` を
優先して検証する。

### 主分析1: Slot別 retention curve

各 budget × 各 slot × chat/reasoning の presence 率。slot は主説明
変数として常に main analysis に含める。

### 主分析2（secondary moderator）: Answer property別分析

`answer_locality`, `marker_presence`, derived `surface_salience` を
moderator 変数として検討する。

**事前判定規則（pre-registered）**: 各 tag について、applicable
instances のうち少なくとも 20-25% が slot 典型値から外れる slot が
3つ以上ある場合に限り、tag moderator を main text で解釈する。この
条件を満たさない場合、descriptive statistics としてのみ報告し、
slot カテゴリ変数で代替する。

### 補助分析1: Run間安定性
### 補助分析2: length bin別分析
### 補助分析3: モデルファミリー比較（QW replication）
### 補助分析4: dataset summary alignment audit

**Claim scope note**: 主分析1（retention curve）を main claim。
主分析2 は answer property tag の pre-registered 条件次第で
supplementary または descriptive のみ。補助分析1-4 は supplementary。
