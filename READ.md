# Experimentation and Causal Inference

End-to-end experimentation and causal inference on real randomized data (Hillstrom email A/B test, Criteo Uplift). The project compares a naive difference in means against CUPED and uplift models (T-learner, causal forest), judges them on Qini/AUUC, and turns the results into a cost-aware targeting decision.

The central question: **do fancy methods actually beat a simple difference in means?**

## Project Status

| Component | Dataset | Status |
|---|---|---|
| SRM check | Hillstrom | Done |
| Randomisation balance check | Hillstrom | Done |
| Naive difference in means and confidence intervals | Hillstrom | Done |
| CUPED variance reduction | Hillstrom | Done |
| Power analysis and MDE | Hillstrom | Done |
| Unit tests (pytest) | n/a | Done |
| Uplift models (T-learner, causal forest) | Hillstrom, Criteo | Planned |
| Qini / AUUC evaluation | Hillstrom, Criteo | Planned |
| Targeting decision with cost per treatment | Hillstrom, Criteo | Planned |
| Network-interference demo | Simulated | Planned |

## Data

- **Hillstrom:** a real randomized email marketing test. Customers were randomly assigned to a men's email, a women's email, or no email (control).
- **Criteo Uplift:** real randomized ad data, about 14 million rows.
- **Simulated data:** used only for the network-interference demo. It is labelled "SIMULATED" in this README and in every chart title.

Processed Hillstrom data is read from `data/Processed_data/clean_processed_file.csv`.

## Hillstrom Experiment Design

| Group | Description | Customers |
|---|---|---|
| Men's E-Mail (treatment) | Customers sent the men's email | 19,183 |
| Women's E-Mail (treatment) | Customers sent the women's email | 19,174 |
| No E-Mail (control) | Customers not sent any email | 19,081 |

- **Experimental unit:** customer
- **Outcomes:** `visit`, `conversion`, `spend`
- **Cleaning:** about 1,576 duplicate rows were removed

## Methods

1. **Sample ratio mismatch (SRM):** chi-square goodness-of-fit test against an equal one-third split.
2. **Randomisation balance check:** compare pre-experiment variables (`history`, `newbie`) across groups.
3. **Naive difference in means:** treatment mean minus control mean, with a 95% confidence interval from the standard error of the difference.
4. **CUPED:** adjust `spend` using `history` as the pre-experiment covariate, `spend_cuped = spend - theta * (history - mean(history))`, where `theta = cov(history, spend) / var(history)`.
5. **Power and MDE:** power of the observed effects, and the minimum detectable effect at the actual group sizes (alpha 0.05, power 80%).
6. **Uplift models (planned):** T-learner and causal forest, evaluated with Qini and AUUC against the naive estimate.
7. **Targeting decision (planned):** choose who to treat given a cost per treatment, and report expected net revenue.

## Results So Far (Hillstrom)

### SRM check

No sample ratio mismatch (chi-square of about 0.33, p = 0.84). Group sizes are consistent with the intended equal split.

### Randomisation balance

| Segment | Mean history | Median history | Mean newbie |
|---|---|---|---|
| Men's E-Mail | 266.37 | 182.47 | 0.502 |
| No E-Mail | 265.37 | 183.27 | 0.501 |
| Women's E-Mail | 267.03 | 184.83 | 0.504 |

The groups are well balanced on past spend and new-customer status.

### Naive difference vs control

| Outcome | Men's E-Mail | Women's E-Mail |
|---|---|---|
| Spend | 0.8512 | 0.4726 |
| Conversion | 0.0075 | 0.0035 |
| Visit | 0.0787 | 0.0457 |

For the men's email, the 95% CI for the spend difference is 0.5346 to 1.1678, which excludes zero. The women's interval is to be added.

### CUPED

Variance reduction was 0.0002 (about 0.02%). `history` is almost uncorrelated with `spend`, so CUPED barely changes the estimate or its interval. On Hillstrom, CUPED does not meaningfully beat the naive difference in means. This is a genuine finding, not a bug, and CUPED is expected to be more useful on Criteo.

### Power and MDE

| Input | Value |
|---|---|
| Control size | 19,081 |
| Baseline conversion | 0.00639 |
| Std of spend (control) | 12.243 |

- Detecting a 0.3 percentage point conversion lift needs about 13,536 customers per group, fewer than the roughly 19,000 per group available.
- For the men's email, the MDE is 0.0025 for conversion (about 38.9% relative) and $0.35 for spend. The observed effects (0.0075 and $0.85) are well above these.
- Women's email power and MDE rows are to be added.

## Repository Structure

```
.
├── data/
│   └── Processed_data/
│       └── clean_processed_file.csv
├── src/
│   ├── analysis/
│   │   ├── cuped.py          # CUPED adjustment and raw vs adjusted effects
│   │   └── mde.py            # minimum detectable effect
│   ├── design/
│   │   ├── power.py          # sample size and power
│   │   └── randomization.py  # balance check
│   └── monitoring/
│       └── srm.py            # sample ratio mismatch check
├── tests/
│   ├── test_cuped.py
│   ├── test_power.py
│   ├── test_mde.py
│   ├── test_srm.py
│   └── test_randomization.py
├── requirements.txt
└── README.md
```

Adjust this tree to match your actual folders.

## Getting Started

```
git clone <your-repo-url>
cd <your-repo>
pip install -r requirements.txt
```

Run each analysis from the project root:

```
python -m src.monitoring.srm
python -m src.design.randomization
python -m src.analysis.cuped
python -m src.design.power
python -m src.analysis.mde
```

## Tests

Each module has its own test file, so they can be run separately:

```
python -m pytest tests/test_srm.py -v
python -m pytest tests/test_randomization.py -v
python -m pytest tests/test_cuped.py -v
python -m pytest tests/test_power.py -v
python -m pytest tests/test_mde.py -v
```

Run everything with `python -m pytest -v`. The tests check the code against hand-computed values, textbook power benchmarks and simulated data with known effects.

## Planned Work

- Uplift models (T-learner and causal forest) on Hillstrom and Criteo, compared with the naive estimate on Qini and AUUC.
- CUPED on Criteo, where richer pre-experiment features should give a larger variance reduction.
- A targeting policy: treat customers whose expected incremental revenue exceeds the cost per treatment, with expected net revenue reported.
- A network-interference demo on simulated data, clearly labelled SIMULATED in this README and in every chart title.

## Limitations

- Hillstrom spend is mostly zeros with a few large values, so spend intervals are wide relative to the effect.
- Post-hoc power of an observed effect mostly mirrors its p-value, so the MDE is the more informative figure.
- Two treatments are compared against one control across several outcomes, which slightly raises the chance of a false positive.