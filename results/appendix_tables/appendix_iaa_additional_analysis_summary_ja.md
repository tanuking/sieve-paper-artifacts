# SIEVE IAA 追加分析 A/B/C

作成日: 2026-05-24

## 入力と出力

- Input: `artifacts/iaa/result/iaa_presence_results_merged_200.csv`
- Output directory: `artifacts/iaa/result/additional_analysis`
- Bootstrap: meeting-level, `10000` iterations, seed `42`

## 結論

Analysis B の rank preservation は、全200件でも random-only でも成立しません。
first/final では `T/O/N` が top3 ですが、second author では `B` が top3 に入り、
`N` が top3 から落ちます。
したがって、IAA をそのまま第二の robust finding に転化する構成は採用しない方が安全です。
論文上は、`B/S` を中心とする construct ambiguity /
Topic Gate calibration limitation として扱うのが妥当です。

## Analysis A: Subset別 Slot-Level Agreement

| subset | slot | n | exact | adjacent | severe | quadratic_kappa | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| random | T | 14 | 1.000 | 1.000 | 0.000 | -- | constant in one or both labels |
| random | O | 14 | 0.929 | 1.000 | 0.000 | 0.788 |  |
| random | N | 14 | 0.643 | 1.000 | 0.000 | 0.340 |  |
| random | B | 15 | 0.467 | 0.600 | 0.400 | 0.167 |  |
| random | L | 15 | 0.667 | 1.000 | 0.000 | 0.771 |  |
| random | S | 14 | 0.500 | 0.857 | 0.143 | 0.364 |  |
| random | U | 14 | 0.857 | 1.000 | 0.000 | 0.904 |  |
| hard | T | 5 | 1.000 | 1.000 | 0.000 | -- | constant in one or both labels |
| hard | O | 2 | 0.500 | 1.000 | 0.000 | 0.667 |  |
| hard | N | 23 | 0.609 | 1.000 | 0.000 | 0.303 |  |
| hard | B | 22 | 0.682 | 0.955 | 0.045 | 0.009 |  |
| hard | L | 19 | 0.737 | 1.000 | 0.000 | 0.680 |  |
| hard | S | 14 | 0.286 | 0.929 | 0.071 | -0.400 |  |
| hard | U | 15 | 0.600 | 0.933 | 0.067 | 0.056 |  |

読み取り:

- Random subset では `O/L/U` は強く、`T` は両者が定数のため κ undefined ですが exact は 1.000 です。
- Random subset でも `N/B/S` は quadratic κ が低く、仕様書の理想条件は満たしません。
- Hard subset では `B/S/U` が大きく低下し、boundary-heavy cases での rubric threshold 差が明確です。

## Analysis B: Ordering Preservation, All 200

| slot | n | mean_first | mean_second | diff | ci_lower | ci_upper | rank_first | rank_second | preserved_in_top3 | preserved_in_bottom4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T | 19 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 1 | 1 | yes | no |
| O | 16 | 0.875 | 0.938 | -0.062 | -0.156 | 0.000 | 2 | 2 | yes | no |
| N | 37 | 0.797 | 0.716 | 0.081 | -0.029 | 0.193 | 3 | 6 | no | no |
| S | 28 | 0.696 | 0.768 | -0.071 | -0.271 | 0.107 | 4 | 5 | no | yes |
| L | 34 | 0.676 | 0.794 | -0.118 | -0.206 | -0.029 | 5 | 4 | no | yes |
| B | 37 | 0.676 | 0.919 | -0.243 | -0.375 | -0.112 | 6 | 3 | no | no |
| U | 29 | 0.672 | 0.690 | -0.017 | -0.133 | 0.100 | 7 | 7 | no | yes |

- First rank order: `1:T / 2:O / 3:N / 4:S / 5:L / 6:B / 7:U`
- Second rank order: `1:T / 2:O / 3:B / 4:L / 5:S / 6:N / 7:U`
- T/O/N top3 preservation: `no`
- B/L/S/U bottom4 preservation: `no`

## Analysis B: Ordering Preservation, Random Only

| slot | n | mean_first | mean_second | diff | ci_lower | ci_upper | rank_first | rank_second | preserved_in_top3 | preserved_in_bottom4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T | 14 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 1 | 1 | yes | no |
| N | 14 | 0.929 | 0.821 | 0.107 | -0.036 | 0.250 | 2 | 4 | no | no |
| O | 14 | 0.929 | 0.964 | -0.036 | -0.107 | 0.000 | 2 | 2 | yes | no |
| L | 15 | 0.600 | 0.767 | -0.167 | -0.300 | -0.067 | 4 | 6 | no | yes |
| S | 14 | 0.571 | 0.821 | -0.250 | -0.464 | -0.036 | 5 | 4 | no | yes |
| U | 14 | 0.571 | 0.643 | -0.071 | -0.179 | 0.000 | 5 | 7 | no | yes |
| B | 15 | 0.433 | 0.900 | -0.467 | -0.700 | -0.233 | 7 | 3 | no | no |

- First rank order: `1:T / 2:N,O / 4:L / 5:S,U / 7:B`
- Second rank order: `1:T / 2:O / 3:B / 4:N,S / 6:L / 7:U`
- T/O/N top3 preservation: `no`
- B/L/S/U bottom4 preservation: `no`

## Analysis C: Severe Disagreement Direction

| slot | n_severe | upward | downward | binomial_p | dominant_direction |
| --- | --- | --- | --- | --- | --- |
| B | 7 | 7 | 0 | 0.016 | upward |
| S | 3 | 3 | 0 | 0.250 | mixed |
| U | 1 | 1 | 0 | 1.000 | mixed |

- Severe disagreements total: `11`
- `B` accounts for the majority of severe cases.
- `B`: upward `7` / downward `0`, binomial p = `0.016`.
- Dominant direction observed: B upward (p=0.016).

## 投稿前チェックリスト判定

| Check | Result |
| --- | --- |
| Analysis A: Random subset で T/O/L/U が安定 | partial |
| Analysis A: B/S は hard subset で明確に低下 | yes |
| Analysis B: T/O/N が all で top3 preserved | no |
| Analysis B: B/L/S/U が all で bottom4 preserved | no |
| Analysis B: random-only でも同様に preserved | no |
| Analysis C: B/S に dominant direction | B upward (p=0.016) |

## 論文への反映方針

この結果では、slot-level ordering preservation を robust finding として主張しない方がよいです。
代わりに、`T/O` は安定、`L/U` は概ね許容範囲、
`B/S/N` は独立annotator間で閾値差が残る、という構造化された限界として書くのが安全です。
特に `B` は second author 側で高く評価され、
`N` は Quality Gate scalar / payload specificity の影響で相対順位が落ちます。
そのため、当初想定した `T/O/N > B/L/S/U` の
annotator-independent preservation は支持されません。
