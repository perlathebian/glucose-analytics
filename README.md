# Glucose Analytics

Personal glucose pattern analysis and insulin response tracker built to support
management of a Type 2 diabetic patient's insulin therapy over a 12-day period (more updates later).

Ingested manual clinical data, identified the dawn phenomenon pattern, and analyzed
behavioral and pharmacological factors affecting fasting glucose levels.

---

## Data

- 57 readings across 12 days (Mar 28 – Apr 8, 2026)
- 4–7 readings per day
- Two insulin types tracked: Novorapid (pre-meal) and Lantus (basal, nightly)
- Waking readings flagged separately as primary clinical target

---

## Analysis Results

### Waking Glucose

- Mean waking glucose: **202.9 mg/dL** against a target ceiling of 130
- Standard deviation: **41.7 mg/dL** — high day-to-day variability
- Above 180 mg/dL: **8 out of 11 mornings** (73%)
- Within target range (70–130): **0 out of 11 mornings**

### Lantus Dose vs Next Morning Glucose

Strong statistically significant negative correlation: **r = -0.793, p = 0.0036**
Higher lantus dose consistently produces lower waking glucose:

| Lantus Units | Mean Next Waking Glucose  |
| ------------ | ------------------------- |
| 12           | 293 mg/dL                 |
| 14           | ~221 mg/dL                |
| 16           | ~175 mg/dL                |
| 18           | 183 mg/dL (1 observation) |

Trend indicates current dosing is directionally correct but has not yet reached therapeutic target.

### Meal Spike Analysis

| Meal          | Mean Glucose Change | Notes                                                 |
| ------------- | ------------------- | ----------------------------------------------------- |
| Pre-breakfast | +13.8 mg/dL         | Glucose rises despite insulin — most problematic meal |
| Pre-lunch     | -31.5 mg/dL         | Novorapid working moderately                          |
| Pre-dinner    | -42.4 mg/dL         | Novorapid most effective at this time                 |

Breakfast combines with the dawn phenomenon to produce the highest readings of the day.

### Novorapid Effectiveness

- 34 injections analyzed
- Glucose lowered in **22/34 cases (64.7%)**
- Glucose rose or unchanged in **12/34 cases (35.3%)**

| Dose    | Mean Glucose Change |
| ------- | ------------------- |
| 2 units | +74.0 mg/dL         |
| 6 units | +9.4 mg/dL          |
| 7 units | +35.2 mg/dL         |
| 8 units | **-42.3 mg/dL**     |

Only 8-unit doses produce consistent glucose reduction, likely due to high insulin resistance (HbA1c 12.54%).

---

## Plots

### Glucose Timeline

![Glucose Timeline](outputs/glucose_timeline.png)

Full 12-day glucose trace with insulin events and clinical thresholds overlaid.
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
- scikit-learn — model (upcoming)
