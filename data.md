# Hillstrom Email Marketing Experiment: Analysis Report

## 1. Business Question

Does sending marketing emails increase customer spending and conversion, or are we just observing a difference that would have happened anyway?

**Answer:** Yes. Both emails significantly increased spend and conversion compared with sending no email. The men's email shows the larger effect on both metrics.

---

## 2. Hypotheses

| Item | Definition |
|---|---|
| Null hypothesis (H0) | Sending marketing emails has no effect on customer spending and conversion |
| Alternative hypothesis (H1) | Sending marketing emails changes customer spending and conversion |
| Significance level (alpha) | 0.05 |
| Power | 0.80 |
| Multiple comparison correction | Bonferroni for two treatments vs one control (threshold 0.025) |

---

## 3. Experiment Design

| Component | Definition |
|---|---|
| Treatment | Men's email, Women's email |
| Control | No email |
| Randomization unit | Customer |
| Primary metrics | `spend`, `conversion` |
| Secondary metric | `recency` |
| Guardrail metric | `visit` |
| Pre-experiment covariates | `history`, `newbie` |

### Experiment Groups

| Group | Role | Customers |
|---|---|---|
| Men's E-Mail | Treatment | 19,183 |
| Women's E-Mail | Treatment | 19,174 |
| No E-Mail | Control | 19,081 |
| **Total** | | **57,438** |

### Data Overview

| Item | Value |
|---|---|
| Original population | About 64,000 customers |
| Duplicate rows removed | About 1,576 |
| Customers in final analysis | 57,438 |
| Experimental unit | Customer |
| Outcomes measured | `visit`, `conversion`, `spend` (whether the email causes a change in customer behaviour) |

---

## 4. Data Preparation and Descriptive Analysis

### 4.1 Missing Values

All variables have a count of 57,438, so there are no missing values in `recency`, `history` or `spend`.

### 4.2 Summary Statistics

| Statistic | recency | history | spend |
|---|---|---|---|
| Count | 57,438 | 57,438 | 57,438 |
| Mean | 5.66 | 266.26 | 1.17 |
| Std | 3.50 | 259.61 | 15.87 |
| Min | 1.00 | 29.99 | 0.00 |
| 25% | 2.00 | 88.86 | 0.00 |
| Median | 5.00 | 183.70 | 0.00 |
| 75% | 9.00 | 351.96 | 0.00 |
| 95% | 11.00 | 777.73 | 0.00 |
| 99% | 12.00 | 1,250.36 | 29.99 |
| Max | 12.00 | 3,345.93 | 499.00 |
| Skewness | 0.18 | 2.38 | 19.50 |

### 4.3 Binary Variables (share of 1s)

| Variable | Proportion |
|---|---|
| visit | 0.1567 |
| conversion | 0.0101 |
| newbie | 0.5022 |
| mens | 0.5563 |
| womens | 0.5560 |

### 4.4 Outliers (1.5 x IQR rule)

| Variable | n | Lower fence | Upper fence | Outliers | Outlier % | Max |
|---|---|---|---|---|---|---|
| recency | 57,438 | -8.50 | 19.50 | 0 | 0.00 | 12.00 |
| history | 57,438 | -305.78 | 746.59 | 3,211 | 5.59 | 3,345.93 |
| spend (buyers only) | 578 | -149.34 | 334.97 | 39 | 6.75 | 499.00 |

### 4.5 Distribution Findings

- **recency** is roughly symmetric (skewness 0.18) with no outliers.
- **history** is right-skewed (skewness 2.38). All 3,211 outliers are high-spending customers, not data errors.
- **spend** is zero-inflated: 98.99% of customers spent $0, so only 578 customers bought anything. Skewness is 19.50.
- Outliers were kept in the main analysis because they are genuine customers.
- `history` and `spend` are almost uncorrelated (0.016), which explains why CUPED gave almost no benefit.

---

## 5. Experiment Design Validation

### 5.1 Sample Ratio Mismatch (SRM)

A chi-square goodness-of-fit test against an equal one-third split.

| Statistic | Value |
|---|---|
| Chi-square | 0.3331 |
| p-value | 0.8466 |

**Result:** no sample ratio mismatch. Group sizes are consistent with the intended randomisation.

### 5.2 Randomisation Balance Check

| Segment | Mean history | Median history | Mean newbie |
|---|---|---|---|
| Men's E-Mail | 266.37 | 182.47 | 0.502 |
| No E-Mail | 265.37 | 183.27 | 0.501 |
| Women's E-Mail | 267.03 | 184.83 | 0.504 |

**Result:** the groups are balanced on past spend (`history`) and new-customer status (`newbie`), so differences in outcomes can reasonably be attributed to the emails.

---

## 6. Power Analysis and Minimum Detectable Effect

### 6.1 Inputs

| Input | Value |
|---|---|
| Minimum sample size per group (design requirement) | 568 |
| Target effect size used for this figure | |
| Actual customers per group | About 19,000 |
| Control group size | 19,081 |
| Baseline conversion rate | 0.00639 (about 0.64%) |
| Standard deviation of spend (control) | 12.243 |
| Alpha / power | 0.05 / 0.80 |

The experiment used about 33 times the minimum required sample size per group.

### 6.2 Power of the Observed Effects

| Treatment | Conversion lift | Conversion power | Spend difference | Spend power |
|---|---|---|---|---|
| Men's E-Mail | 0.0075 | 1.0000 | 0.8512 | 1.0000 |
| Women's E-Mail | 0.0035 | 0.9667 | 0.4726 | 0.9652 |

This is a post-hoc check and mostly mirrors the p-value, so the MDE below is the more informative number.

### 6.3 Minimum Detectable Effect (MDE)

The smallest effect this experiment could reliably detect (alpha 0.05, power 80%) at the actual group sizes.

| Treatment | Customers | MDE (conversion) | MDE (conversion, relative) | MDE (spend) |
|---|---|---|---|---|
| Men's E-Mail | 19,183 | 0.0025 | 38.87% | $0.3507 |
| Women's E-Mail | 19,174 | 0.0025 | 38.87% | $0.3507 |

### 6.4 Observed Effects vs MDE

| Treatment | Conversion lift | Conversion MDE | Spend difference | Spend MDE |
|---|---|---|---|---|
| Men's E-Mail | 0.0075 | 0.0025 | $0.85 | $0.35 |
| Women's E-Mail | 0.0035 | 0.0025 | $0.47 | $0.35 |

- Both emails exceed the MDE on both metrics, so the experiment was adequately powered for them.
- Because baseline conversion is low (0.64%), the conversion MDE is large in relative terms: only a relative lift of about 39% or more could be reliably detected.
- The women's effects are above the MDE by a smaller margin than the men's.

---

## 7. Treatment Effect Estimation

### 7.1 Naive Difference in Means (treatment minus control)

| Outcome | Men's E-Mail | Women's E-Mail |
|---|---|---|
| Spend | 0.8512 | 0.4726 |
| Conversion | 0.0075 | 0.0035 |
| Visit | 0.0787 | 0.0457 |
| Recency | | |

- **Spend** is the average extra amount spent per customer. The men's email adds about $0.85 per customer and the women's email about $0.47.
- **Conversion** is the difference in conversion rate: about 0.75 percentage points for the men's email and 0.35 for the women's email.
- **Visit** is the difference in visit rate: about 7.9 percentage points for the men's email and 4.6 for the women's email.

Because assignment was randomised and the SRM and balance checks passed, the naive difference can be read as an estimate of the causal effect.

### 7.2 CUPED Variance Reduction (spend, covariate: history)

| Item | Value |
|---|---|
| Variance reduction | 0.0002 (about 0.02%) |
| Theta | 0.00096 |

| Treatment | Method | Effect | SE | 95% CI low | 95% CI high | CI width |
|---|---|---|---|---|---|---|
| Men's E-Mail | Raw | 0.8512 | 0.1615 | 0.5346 | 1.1678 | 0.6332 |
| Men's E-Mail | CUPED | 0.8503 | 0.1615 | 0.5337 | 1.1668 | 0.6331 |
| Women's E-Mail | Raw | 0.4726 | 0.1454 | 0.1876 | 0.7576 | 0.5700 |
| Women's E-Mail | CUPED | 0.4710 | 0.1454 | 0.1861 | 0.7560 | 0.5699 |

**Interpretation:** `history` is almost uncorrelated with `spend`, so CUPED barely changes the estimates or the confidence intervals. The raw difference is reported as the primary result, and CUPED confirms it.

---

## 8. Hypothesis Testing

Spend was tested with Welch's two-sample t-test (unequal variances). Conversion was tested with a two-proportion z-test. Each email was compared with the control separately. Confidence intervals are 95%.

### 8.1 Spend

| Treatment | Difference | p-value | 95% CI |
|---|---|---|---|
| Men's E-Mail | $0.8512 | 1.38e-07 | 0.5346 to 1.1678 |
| Women's E-Mail | $0.4726 | 1.15e-03 | 0.1876 to 0.7576 |

**Interpretation:** neither interval includes 0, so the increase in spend is statistically significant at the 5% level for both emails. The data suggest the true effect of the men's email is between about $0.53 and $1.17 per customer, and of the women's email between about $0.19 and $0.76 per customer.

**Decision:** reject the null hypothesis for spend. Both emails significantly increased spend per customer, and both remain significant after Bonferroni correction.

### 8.2 Conversion

| Treatment | Lift | p-value | 95% CI |
|---|---|---|---|
| Men's E-Mail | +0.75 percentage points | 2.19e-13 | 0.0055 to 0.0095 |
| Women's E-Mail | +0.35 percentage points | 1.62e-04 | 0.0017 to 0.0053 |

**Decision:** reject the null hypothesis for conversion. Both emails raised the conversion rate, and both remain significant after Bonferroni correction.

With a baseline conversion rate of 0.64%, the men's email lift is about a 117% relative increase and the women's about 54%.

### 8.3 Guardrail Metric (visit)

| Treatment | Difference | p-value | 95% CI |
|---|---|---|---|
| Men's E-Mail | 0.0787 | | |
| Women's E-Mail | 0.0457 | | |

### 8.4 Men's Email vs Women's Email

| Outcome | Difference (men minus women) | p-value | 95% CI |
|---|---|---|---|
| Spend | | | |
| Conversion | | | |

---

## 9. Conclusion

| Outcome | Men's E-Mail | Women's E-Mail |
|---|---|---|
| Spend | +$0.85 per customer, p = 1.38e-07 | +$0.47 per customer, p = 1.15e-03 |
| Conversion | +0.75 percentage points, p = 2.19e-13 | +0.35 percentage points, p = 1.62e-04 |

1. The design is valid: no sample ratio mismatch (p = 0.8466) and balanced pre-experiment covariates.
2. The experiment was well powered: both effects exceed the MDE.
3. Both emails significantly increased spend and conversion compared with no email.
4. The men's email shows the larger effect on both metrics. Whether it is significantly better than the women's email depends on the direct comparison in section 8.4.
5. CUPED did not meaningfully reduce variance on this dataset.

## 10. Limitations