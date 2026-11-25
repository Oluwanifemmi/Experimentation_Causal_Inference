# Does Email Marketing Increase Spending and Conversion?

> An A/B test and causal inference analysis measuring the impact of marketing emails on customer spend and conversion.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Status](https://img.shields.io/badge/status-complete-brightgreen)
![Topic](https://img.shields.io/badge/topic-A%2FB%20Testing%20%7C%20Causal%20Inference-orange)

---

## Business Question

**Does sending marketing emails increase customer spending and conversion?**

** Yes. Both emails significantly increased spend and conversion compared with sending no email. The men's email raised spend by $0.85 per customer and conversion by 0.75 percentage points. The women's email raised spend by $0.47 per customer and conversion by 0.35 percentage points.

---

## Experiment Design

| Component | Definition |
|---|---|
| **Treatment** | Men's email, Women's email |
| **Control** | No email sent |
| **Randomization unit** | Customer |
| **Outcome** | Increase in spend and conversion |
| **Primary metrics** | `spend`, `conversion` |
| **Secondary metrics** | `recency` |
| **Guardrail metric** | `visit` |
| **Pre-experiment covariate** | `history` (past spend, used for CUPED) |

### Experiment Groups

| Group | Role | Customers |
|---|---|---|
| Men's E-Mail | Treatment | 19,183 |
| Women's E-Mail | Treatment | 19,174 |
| No E-Mail | Control | 19,081 |

### Hypotheses
- **H0:** Emails have no effect on spend / conversion (difference = 0)
- **H1:** Emails change spend / conversion (difference is not 0)
- **Significance level:** alpha = 0.05, with a Bonferroni correction (0.025) for comparing two treatments against one control

---

## Analysis Workflow

```
1. Power analysis  ->  2. Randomization  ->  3. Design validation
        |
4. Data preparation  ->  5. Effect estimation  ->  6. Hypothesis testing
```

### 1. Sample Size and Power Analysis
- Calculated the required sample size per group: 568 (the experiment used about 19,000 per group)
- Computed the **Minimum Detectable Effect (MDE)**: the smallest effect the experiment can reliably detect
- Parameters: alpha = 0.05, power = 0.80, baseline conversion = 0.00639, standard deviation of spend = 12.243
- MDE for both emails: 0.0025 in conversion (about 39% relative) and $0.35 in spend

### 2. Randomization
- Randomly allocated customers into control and treatment groups
- Seed fixed for reproducibility

### 3. Experiment Validation
- **Sample Ratio Mismatch (SRM):** chi-square test confirming the actual split matches the intended split
- **Randomization balance check:** compared pre-treatment covariates (`history`, `newbie`) across groups

### 4. Data Preparation
- Missing value check
- Outlier detection and handling
- Descriptive statistics
- Distribution analysis (spend is zero-inflated and right-skewed: 98.99% of customers spent $0)

### 5. Treatment Effect Estimation
- **Naive difference** in means between treatment and control
- **CUPED** variance reduction using pre-experiment `history` to get a tighter estimate

### 6. Hypothesis Testing
- Spend: Welch's two-sample t-test
- Conversion: two-proportion z-test
- p-values and 95% confidence intervals

---

## Results

Each email is compared with the no-email control. Baseline conversion in the control group is 0.64%.

| Metric | Treatment | Difference | p-value | 95% CI |
|---|---|---|---|---|
| Conversion | Men's email | +0.75 pp | 2.19e-13 | 0.0055 to 0.0095 |
| Conversion | Women's email | +0.35 pp | 1.62e-04 | 0.0017 to 0.0053 |
| Spend | Men's email | +$0.8512 | 1.38e-07 | 0.5346 to 1.1678 |
| Spend | Women's email | +$0.4726 | 1.15e-03 | 0.1876 to 0.7576 |
| Spend (CUPED) | Men's email | +$0.8503 | | 0.5337 to 1.1668 |
| Spend (CUPED) | Women's email | +$0.4710 | | 0.1861 to 0.7560 |
| Recency *(secondary)* | Men's email | | | |
| Recency *(secondary)* | Women's email | | | |
| Visit *(guardrail)* | Men's email | +7.87 pp | | |
| Visit *(guardrail)* | Women's email | +4.57 pp | | |

**Validation checks**
- SRM: passed (chi-square = 0.3331, p = 0.8466)
- Covariate balance: passed (`history` and `newbie` are similar across all three groups)

**Variance reduction from CUPED:** 0.0002 (about 0.02%). `history` is almost uncorrelated with `spend`, so CUPED barely changed the estimates.

---

## Key Takeaways
1. Both emails significantly increased conversion. The men's email raised it by 0.75 percentage points (about 117% relative to the 0.64% baseline) and the women's email by 0.35 percentage points (about 54%).
2. Both emails significantly increased spend per customer: +$0.85 for the men's email and +$0.47 for the women's email. Both remain significant after Bonferroni correction.
3. The experiment was well powered. Both effects are above the MDE, and the group sizes were about 33 times the minimum required.
4. The men's email shows the larger effect on both metrics. A direct test of men's email against women's email is needed to confirm that it is significantly better.
5. CUPED did not meaningfully reduce variance on this dataset.


---

## Repository Structure

```
├── data/
│   └── Processed_data/   
├── src/
│   └── analysis/         
├── data.md                
├── makefile
├── pyproject.toml
├── requirements.txt
└── README.md
```

## How to Run

```bash
git clone 
cd 
pip install -r requirements.txt
python src/analysis/power_analysis.py
python src/analysis/descriptive_statistics.py
```

## Tech Stack
Python, pandas, NumPy, SciPy, statsmodels, matplotlib / seaborn