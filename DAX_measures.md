# Power BI DAX Measures — Enrollment & Engagement Dashboard
## Author: Kanika Mehta

---

## KPI Measures

### 1. Total Enrollments
```dax
Total Enrollments = COUNTROWS(enrollments_clean)
```

### 2. Completion Rate
```dax
Completion Rate =
DIVIDE(
    COUNTROWS(FILTER(enrollments_clean, enrollments_clean[status] = "Completed")),
    COUNTROWS(enrollments_clean),
    0
)
```

### 3. Drop-off Rate
```dax
Drop-off Rate =
DIVIDE(
    COUNTROWS(FILTER(enrollments_clean, enrollments_clean[status] = "Dropped")),
    COUNTROWS(enrollments_clean),
    0
)
```

### 4. Average Engagement Score
```dax
Avg Engagement Score =
AVERAGE(engagement_clean[engagement_score])
```

### 5. Month-over-Month Enrollment Growth
```dax
MoM Growth =
VAR CurrentMonth = CALCULATE(COUNTROWS(enrollments_clean))
VAR PrevMonth    = CALCULATE(COUNTROWS(enrollments_clean),
                     DATEADD(enrollments_clean[enroll_date], -1, MONTH))
RETURN
DIVIDE(CurrentMonth - PrevMonth, PrevMonth, 0)
```

### 6. Funnel Conversion Rate (Visited → Completed)
```dax
Funnel Conversion =
DIVIDE(
    CALCULATE(COUNTROWS(funnel_summary), funnel_summary[stage] = "Completed"),
    CALCULATE(COUNTROWS(funnel_summary), funnel_summary[stage] = "Visited"),
    0
)
```

---

## Dashboard Pages

| Page | Visuals |
|------|---------|
| Overview | KPI cards, Enrollment trend line, Status donut |
| Funnel Analysis | Funnel chart, Drop-off % bar chart |
| Cohort Retention | Matrix heatmap, Retention rate line |
| Engagement Deep Dive | Scatter (engagement vs score), Top students table |
| Course Performance | Bar chart, Slicers by category/city |

---

## How to Connect Power BI to CSV Files
1. Open Power BI Desktop
2. Home → Get Data → Text/CSV
3. Load each file from `data/processed/`:
   - `enrollments_clean.csv`
   - `engagement_clean.csv`
   - `funnel_summary.csv`
   - `cohort_analysis.csv`
4. In Model view, create relationships:
   - `enrollments_clean[student_id]` → `engagement_clean[student_id]`
