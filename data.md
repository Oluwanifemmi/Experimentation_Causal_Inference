# Hillstrom Email Marketing Experiment

## Business Question

Does a marketing email actually cause customers to spend more money, or are we just observing a difference that would have happened anyway?

## Data Overview

- **Original population:** about 64,000 customers
- **Duplicates:** about 1,576 duplicate rows were found and removed
- **Experimental unit:** customer
- **Outcome measured:** whether the email causes a change in customer behaviour (`visit`, `conversion`, `spend`)

## Experiment Groups

| Group | Description | Customers |
|---|---|---|
| Men's E-Mail (treatment) | Customers sent the men's email | 19,183 |
| Women's E-Mail (treatment) | Customers sent the women's email | 19,174 |
| No E-Mail (control) | Customers not sent any email | 19,081 |

## Sample Ratio Mismatch (SRM) Check

A chi-square goodness-of-fit test against an equal one-third split showed **no sample ratio mismatch** (chi-square of about 0.33, p = 0.84). Group sizes are consistent with the intended randomisation.

## Randomisation Balance Check

Pre-experiment variables should look similar across groups if randomisation worked.

| Segment | Mean history | Median history | Mean newbie |
|---|---|---|---|
| Men's E-Mail | 266.37 | 182.47 | 0.502 |
| No E-Mail | 265.37 | 183.27 | 0.501 |
| Women's E-Mail | 267.03 | 184.83 | 0.504 |

**Conclusion:** the groups are well balanced on past spend (`history`) and new-customer status (`newbie`), so any later difference in outcomes can reasonably be attributed to the emails.

## Naive Difference

The naive difference is the mean outcome in each treatment group minus the mean outcome in the control group (No E-Mail).

| Outcome | Men's E-Mail vs control | Women's E-Mail vs control |
|---|---|---|
| Spend | 0.8512 | 0.4726 |
| Conversion | 0.0075 | 0.0035 |
| Visit | 0.0787 | 0.0457 |

- **Spend** is the average extra amount spent per customer. The men's email adds about $0.85 per customer and the women's email about $0.47.
- **Conversion** is the difference in conversion rate: about 0.75 percentage points for the men's email and 0.35 for the women's email.
- **Visit** is the difference in visit rate: about 7.9 percentage points for the men's email and 4.6 for the women's email.

Because assignment was randomised and the SRM and balance checks passed, the naive difference can be read as an estimate of the causal effect.

## Confidence Interval (Spend)

| Treatment | Difference | 95% CI |
|---|---|---|
| Men's E-Mail | 0.8512 | 0.5346 to 1.1678 |
| Women's E-Mail | 0.4726 | to be added |

**Interpretation:** the interval for the men's email does not include 0, so the increase in spend is statistically significant at the 5% level. The data suggest the true effect is somewhere between about $0.53 and $1.17 per customer.

## CUPED Variance Reduction

CUPED was applied to `spend` using `history` (past spend) as the pre-experiment covariate.

- **Variance reduction:** 0.0002 (about 0.02%)
- **Interpretation:** `history` is almost uncorrelated with `spend`, so CUPED barely changes the estimate or its confidence interval. On Hillstrom, CUPED does not meaningfully improve on the naive difference in means.

## Power Analysis

| Input | Value |
|---|---|
| Control group size | 19,081 |
| Baseline conversion rate | 0.00639 (about 0.64%) |
| Standard deviation of spend (control) | 12.243 |

**Planning sample size:** to detect a 0.3 percentage point lift in conversion on this baseline (alpha 0.05, power 80%), about **13,536 customers per group** are needed. Each group in this experiment has about 19,000, so the experiment was large enough for a lift of that size.

**Power of the observed effects:**

| Treatment | Conversion lift | Conversion power | Spend difference | Spend power |
|---|---|---|---|---|
| Men's E-Mail | 0.0075 | 1.0 | 0.8512 | 1.0 |
| Women's E-Mail | to be added | to be added | to be added | to be added |

Power of 1.0 (rounded) means the experiment was almost certain to detect effects of the size observed for the men's email. This is a post-hoc check and mostly mirrors the p-value, so the MDE below is the more informative number.

## Minimum Detectable Effect (MDE)

The MDE is the smallest effect this experiment could reliably detect (alpha 0.05, power 80%) given the actual group sizes.

| Treatment | Customers | MDE (conversion) | MDE (conversion, relative) | MDE (spend) |
|---|---|---|---|---|
| Men's E-Mail | 19,183 | 0.0025 | 38.9% | $0.35 |
| Women's E-Mail | 19,174 | to be added | to be added | to be added |

**Interpretation:**

- The observed men's email effects are well above the MDE: conversion lift of 0.0075 against an MDE of 0.0025, and a spend difference of $0.85 against an MDE of $0.35. The experiment was adequately powered for them.
- Because baseline conversion is low (0.64%), the conversion MDE is large in relative terms: the experiment could only reliably detect a relative lift of about 39% or more.
- The women's email spend difference ($0.47) is above the $0.35 spend MDE, so it should also be detectable. Confirm this once the women's row is added.