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

A chi-square goodness-of-fit test against an equal one-third split showed **no sample ratio mismatch** (χ² ≈ 0.33, p = 0.84). Group sizes are consistent with the intended randomisation.

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
| Women's E-Mail | 0.4726 | *to be added* |

**Interpretation:** the interval for the men's email does not include 0, so the increase in spend is statistically significant at the 5% level. The data suggest the true effect is somewhere between about $0.53 and $1.17 per customer.