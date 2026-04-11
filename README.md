# Glucose Analytics

Personal glucose pattern analysis and insulin response tracker built to support
management of a Type 2 diabetic patient's insulin therapy over a 15-day period (more updates later).

Ingested manual clinical data, identified the dawn phenomenon pattern, and analyzed
behavioral and pharmacological factors affecting fasting glucose levels.

---

## Data

- 68 readings across 15 days (Mar 28 – Apr 11, 2026)
- 3–7 readings per day
- Two insulin types tracked: Novorapid (pre-meal) and Lantus (basal, nightly)
- Waking readings flagged separately as primary clinical target
- Skipped doses recorded explicitly to capture compliance gaps

---

## Analysis Results

### Waking Glucose

- Mean waking glucose: **190.9 mg/dL** against a target ceiling of 130
- Median: **192.0 mg/dL**
- Standard deviation: **48.5 mg/dL** — high day-to-day variability
- Above 180 mg/dL: **9 out of 14 mornings** (64%)
- Within target range (70–130): **2 out of 14 mornings**

First two mornings hitting target both followed 18-unit Lantus doses (Apr 9: 110, Apr 10: 122).

### Lantus Dose vs Next Morning Glucose

Negative correlation: **r = -0.434, p = 0.1208**
Correlation weakened from earlier r = -0.793 as more data was added and variability at the
18-unit dose increased — a more honest reflection of the data with multiple observations per dose level.
The 0-unit skipped night directly produced the highest recent waking reading (208 mg/dL).

| Lantus Units | Next Waking Glucose           |
| ------------ | ----------------------------- |
| 12           | 293 mg/dL                     |
| 14           | 242, 197, 246, 198 mg/dL      |
| 16           | 164, 200, 152, 187, 170 mg/dL |
| 18           | 183, 110, 122 mg/dL           |
| 0 (skipped)  | 208 mg/dL                     |

18-unit dose is the first showing occasional target-range results. Dosing trend is directionally
correct but has not yet reached consistent therapeutic target.

### Meal Spike Analysis

| Meal          | Mean Glucose Change | Notes                                                 |
| ------------- | ------------------- | ----------------------------------------------------- |
| Pre-breakfast | +13.7 mg/dL         | Glucose rises despite insulin — most problematic meal |
| Pre-lunch     | -35.7 mg/dL         | Novorapid working moderately                          |
| Pre-dinner    | -35.8 mg/dL         | Novorapid effective at this time                      |

Breakfast combines with the dawn phenomenon to produce the highest readings of the day.

### Novorapid Effectiveness

- 39 injections analyzed
- Glucose lowered in **24/39 cases (61.5%)**
- Glucose rose or unchanged in **15/39 cases (38.5%)**

| Dose    | Mean Glucose Change |
| ------- | ------------------- |
| 2 units | +74.0 mg/dL         |
| 6 units | +9.4 mg/dL          |
| 7 units | +29.5 mg/dL         |
| 8 units | **-43.8 mg/dL**     |

Only 8-unit doses produce consistent glucose reduction, likely due to high insulin resistance (HbA1c 12.54%).

### Predictive Model

Ridge regression trained on lantus dose and previous waking glucose to predict next morning's waking glucose.
Evaluated using leave-one-out cross-validation given small dataset size.

- Training pairs: 13
- Mean Absolute Error: **33.8 mg/dL**
- Lantus coefficient: -18.159 (higher dose → lower waking glucose)
- Previous waking glucose coefficient: +18.518 (higher starting glucose → higher next morning)

Prediction for Apr 12 given 18 units Lantus tonight and today's waking glucose of 183: **166.7 mg/dL ± 33.8**

---

## Plots

### Glucose Timeline

![Glucose Timeline](outputs/glucose_timeline.png)

Full 15-day glucose trace with insulin events and clinical thresholds overlaid.
Orange downward triangles mark Novorapid injections. Red upward triangles mark
Lantus injections. Green diamonds mark first waking readings of each day.
Dashed lines indicate hyperglycemia threshold (180), target ceiling (130),
and hypoglycemia threshold (70).

---

### Hourly Distribution

![Hourly Distribution](outputs/hourly_distribution.png)

Boxplot grouping all readings by hour of day. Reveals which hours consistently
produce high or volatile glucose levels. Elevated and wide boxes in early morning
hours (7–9) confirm the dawn phenomenon; cortisol and adrenaline raise glucose
overnight independently of evening insulin.

---

### Daily Average

![Daily Average](outputs/daily_average.png)

Mean glucose per day across the full observation period. Smooths out intra-day
noise to show the overall management trend. Bars above 180 indicate days where
average glucose remained in hyperglycemic range throughout the day.

---

### Insulin Response

![Insulin Response](outputs/insulin_response.png)

Each dot represents one Novorapid injection. X axis is dose in units, Y axis is
glucose change to the next reading. Dots below zero indicate the injection
successfully lowered glucose. Dots above zero indicate glucose continued rising
despite the injection. Wide vertical spread at the same dose confirms inconsistent
insulin response likely driven by variable meal size, injection timing, and
physiological factors including active inflammation.

---

## Stack

- Python 3.12
- pandas — data loading and transformation
- matplotlib — plotting
- seaborn — statistical visualization
- scikit-learn — Ridge regression, LOO cross-validation
