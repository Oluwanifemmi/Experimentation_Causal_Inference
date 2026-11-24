# Does Email Marketing Increase Spending and Conversion?

> An A/B test and causal inference analysis measuring the impact of marketing emails on customer spend and conversion.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Status](https://img.shields.io/badge/status-complete-brightgreen)
![Topic](https://img.shields.io/badge/topic-A%2FB%20Testing%20%7C%20Causal%20Inference-orange)

---

## Business Question

**Does sending marketing emails increase customer spending and conversion?**

**TL:DR:** 

---

## Experiment Design

| Component | Definition |
|---|---|
| **Treatment** | Marketing email sent to male / female customers |
| **Control** | No email sent |
| **Randomization unit** | Customer |
| **Primary metrics** | `spend`, `conversion` |
| **Secondary metrics** | `recency` |
| **Guardrail metric** | `visit` |
| **Pre-experiment covariate** | `history` (past spend, used for CUPED) |
| ** Outcome**| Increase spend and conversion

### Hypotheses
- **H0:** Emails have no effect on spend / conversion (difference = 0)
- **H1:** Emails change spend / conversion (difference is not 0)

---

## Analysis Workflow

```
1. Power analysis  ->  2. Randomization  ->  3. Design validation
        |
4. Data preparation  ->  5. Effect estimation  ->  6. Hypothesis testing
```

### 1. Sample Size and Power Analysis
- Calculated the required sample size per group
- Computed the **Minimum Detectable Effect (MDE)**: the smallest effect the experiment can reliably detect
- Parameters: alpha = , power = , baseline = , variance = 

### 2. Randomization
- Randomly allocated customers into control and treatment groups
- Seed fixed for reproducibility

### 3. Experiment Validation
- **Sample Ratio Mismatch (SRM):** chi-square test confirming the actual split matches the intended split
- **Randomization balance check:** compared pre-treatment covariates (`history`, `recency`, etc.) across groups

### 4. Data Preparation
- Missing value check
- Outlier detection and handling
- Descriptive statistics
- Distribution analysis (spend is typically zero-inflated and right-skewed)

### 5. Treatment Effect Estimation
- **Naive difference** in means between treatment and control
- **CUPED** variance reduction using pre-experiment `history` to get a tighter estimate

### 6. Hypothesis Testing
- p-values
- 95% confidence intervals

---

## Results

| Metric | Control | Treatment | Lift | p-value | 95% CI |
|---|---|---|---|---|---|
| Conversion | | | | | |
| Spend | | | | | |
| Spend (CUPED) | | | | | |
| Recency *(secondary)* | | | | | |
| Visit *(guardrail)* | | | | | |

**Validation checks**
- SRM: 
- Covariate balance: 

**Variance reduction from CUPED:** 

---

## Key Takeaways
1. 
2. 
3. 
4. 

## Limitations
- 

---

## Repository Structure

```
├── data/              # raw and processed data
├── notebooks/         # analysis notebooks
├── src/               # helper functions
├── requirements.txt
└── README.md
```

## How to Run

```bash
git clone 
cd 
pip install -r requirements.txt
jupyter notebook notebooks/analysis.ipynb
```

## Tech Stack
Python, pandas, NumPy, SciPy, statsmodels, matplotlib / seaborn