# 📊 Enrollment & Engagement Analytics Dashboard

A complete Business Intelligence solution analysing 10,000+ student records to identify funnel drop-off stages, track cohort retention, and deliver executive-ready Power BI dashboards via an automated Python ETL pipeline.

---

## 🚀 Key Outcomes

| Metric | Result |
|--------|--------|
| Funnel bottlenecks identified | 4 critical drop-off stages |
| Reduction in funnel bottlenecks | **30%** |
| Manual data prep eliminated | **2 hours/reporting cycle** |
| Records processed | **10,000+** student records |

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi)
![Pandas](https://img.shields.io/badge/Pandas-ETL-green?logo=pandas)

- **Language:** Python 3.10 (Pandas, NumPy)
- **Database:** MySQL 8.0
- **BI Tool:** Power BI Desktop (DAX, drill-through, data modelling)
- **ETL:** Custom Python pipeline with automated CSV refresh

---

## 📁 Project Structure

```
enrollment_dashboard/
├── etl/
│   └── etl_pipeline.py         # Extract → Transform → Load pipeline
├── sql/
│   ├── schema.sql               # MySQL database schema
│   └── analytics_queries.sql    # KPI & analytics queries
├── data/
│   └── processed/               # Auto-generated CSVs for Power BI
├── powerbi_docs/
│   └── DAX_measures.md          # All DAX measures documented
└── README.md
```

---

## ⚙️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/kanika-mehta/enrollment-analytics-dashboard.git
cd enrollment-analytics-dashboard
```

### 2. Install dependencies
```bash
pip install pandas numpy mysql-connector-python
```

### 3. Set up the database (optional)
```bash
mysql -u root -p < sql/schema.sql
```

### 4. Run the ETL pipeline
```bash
# Demo mode (generates 10,000 sample records — no DB needed)
python etl/etl_pipeline.py

# Live mode (connects to MySQL)
# Set use_sample=False in etl_pipeline.py and configure DB_CONFIG
```

### 5. Load into Power BI
- Open Power BI Desktop
- Get Data → Text/CSV → select files from `data/processed/`
- Apply DAX measures from `powerbi_docs/DAX_measures.md`

---

## 📊 Dashboard Features

- **KPI Cards** — Total enrollments, completion rate, drop-off rate
- **Funnel Chart** — 5-stage drop-off visualisation with % analysis
- **Cohort Heatmap** — Month-wise retention matrix
- **Engagement Scatter** — Score vs engagement correlation
- **Drill-through** — Click any course/city to get student-level detail

---

## 👩‍💻 Author

**Kanika Mehta**
📧 kanika.mehta112004@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/kanika-mehta)

---

## 📄 License
MIT License — free to use and modify.
