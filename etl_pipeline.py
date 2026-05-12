"""
Enrollment & Engagement Analytics Dashboard
ETL Pipeline: MySQL → Cleaned DataFrames → Power BI Ready CSVs
Author: Kanika Mehta
"""

import pandas as pd
import numpy as np
import mysql.connector
import os
from datetime import datetime

# ── CONFIG ────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": "enrollment_analytics",
}

OUTPUT_DIR = "data/processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── 1. EXTRACT ────────────────────────────────────────────────
def extract(query: str, conn) -> pd.DataFrame:
    """Run a SQL query and return a DataFrame."""
    return pd.read_sql(query, conn)


# ── 2. TRANSFORM ──────────────────────────────────────────────
def clean_enrollments(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.drop_duplicates(inplace=True)
    df["enroll_date"] = pd.to_datetime(df["enroll_date"])
    df["month"]       = df["enroll_date"].dt.to_period("M").astype(str)
    df["year"]        = df["enroll_date"].dt.year
    df["status"]      = df["status"].str.strip().str.title()
    df["is_completed"] = (df["status"] == "Completed").astype(int)
    df["is_dropped"]   = (df["status"] == "Dropped").astype(int)
    return df


def clean_engagement(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.drop_duplicates(inplace=True)
    df["quiz_score"] = pd.to_numeric(df["quiz_score"], errors="coerce").fillna(0)
    df["engagement_score"] = (
        df["videos_watched"]   * 0.4 +
        df["assignments_done"] * 0.4 +
        df["quiz_score"]       * 0.2
    ).round(2)
    return df


def build_funnel_summary(df: pd.DataFrame) -> pd.DataFrame:
    order = ["Visited", "Registered", "Enrolled", "Active", "Completed"]
    summary = (
        df.groupby("stage_name")["student_id"]
        .nunique()
        .reindex(order)
        .reset_index()
    )
    summary.columns = ["stage", "count"]
    summary["drop_off"] = summary["count"].diff().abs().fillna(0).astype(int)
    summary["drop_off_pct"] = (
        (summary["drop_off"] / summary["count"].shift(1) * 100)
        .fillna(0).round(2)
    )
    return summary


def build_cohort_table(enrollments: pd.DataFrame) -> pd.DataFrame:
    cohort = (
        enrollments.groupby("month")
        .agg(
            cohort_size   =("student_id", "nunique"),
            completions   =("is_completed", "sum"),
            drop_offs     =("is_dropped", "sum"),
        )
        .reset_index()
    )
    cohort["retention_rate"] = (
        cohort["completions"] / cohort["cohort_size"] * 100
    ).round(2)
    return cohort


# ── 3. LOAD ───────────────────────────────────────────────────
def save(df: pd.DataFrame, name: str):
    path = os.path.join(OUTPUT_DIR, f"{name}.csv")
    df.to_csv(path, index=False)
    print(f"  ✅ Saved {name}.csv  ({len(df)} rows)")


# ── 4. GENERATE SAMPLE DATA (for demo / no DB needed) ─────────
def generate_sample_data(n=10000):
    np.random.seed(42)
    cities  = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata"]
    courses = ["Data Analytics", "Web Development", "Machine Learning",
               "Digital Marketing", "Python Basics", "Power BI Masterclass"]
    statuses = ["Active", "Completed", "Dropped", "On Hold"]

    students = pd.DataFrame({
        "student_id":      range(1, n + 1),
        "full_name":       [f"Student_{i}" for i in range(1, n + 1)],
        "gender":          np.random.choice(["Male", "Female", "Other"], n),
        "age":             np.random.randint(18, 35, n),
        "city":            np.random.choice(cities, n),
        "enrollment_date": pd.date_range("2023-01-01", periods=n, freq="H")
                           .normalize()[:n]
                           .map(lambda d: d + pd.Timedelta(days=np.random.randint(0, 365))),
        "status":          np.random.choice(statuses, n, p=[0.4, 0.35, 0.2, 0.05]),
        "course":          np.random.choice(courses, n),
    })
    students["enroll_date"] = students["enrollment_date"]
    students["is_completed"] = (students["status"] == "Completed").astype(int)
    students["is_dropped"]   = (students["status"] == "Dropped").astype(int)
    students["month"] = pd.to_datetime(students["enroll_date"]).dt.to_period("M").astype(str)
    students["year"]  = pd.to_datetime(students["enroll_date"]).dt.year

    engagement = pd.DataFrame({
        "student_id":       range(1, n + 1),
        "videos_watched":   np.random.randint(0, 50, n),
        "assignments_done": np.random.randint(0, 20, n),
        "quiz_score":       np.random.uniform(40, 100, n).round(2),
    })
    engagement["engagement_score"] = (
        engagement["videos_watched"]   * 0.4 +
        engagement["assignments_done"] * 0.4 +
        engagement["quiz_score"]       * 0.2
    ).round(2)

    funnel_data = pd.DataFrame({
        "stage_name": ["Visited", "Registered", "Enrolled", "Active", "Completed"],
        "student_id": [n, int(n * 0.72), int(n * 0.55), int(n * 0.42), int(n * 0.35)],
    })

    return students, engagement, funnel_data


# ── MAIN ──────────────────────────────────────────────────────
def run_etl(use_sample=True):
    print(f"\n{'='*55}")
    print(f"  ETL Pipeline Started — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*55}")

    if use_sample:
        print("\n📦 Using sample data (10,000 records)...")
        enrollments, engagement, funnel_raw = generate_sample_data()
    else:
        print("\n🔌 Connecting to MySQL...")
        conn = mysql.connector.connect(**DB_CONFIG)
        enrollments = extract("SELECT * FROM enrollments e JOIN students s USING(student_id)", conn)
        engagement  = extract("SELECT * FROM engagement", conn)
        funnel_raw  = extract("SELECT * FROM funnel_stages", conn)
        conn.close()

    print("\n🔄 Transforming data...")
    enrollments = clean_enrollments(enrollments)
    engagement  = clean_engagement(engagement)
    funnel      = build_funnel_summary(funnel_raw)
    cohort      = build_cohort_table(enrollments)

    print("\n💾 Saving processed files...")
    save(enrollments, "enrollments_clean")
    save(engagement,  "engagement_clean")
    save(funnel,      "funnel_summary")
    save(cohort,      "cohort_analysis")

    print(f"\n✅ ETL Complete — files saved to '{OUTPUT_DIR}/'")
    print(f"   Load these CSVs directly into Power BI via 'Get Data → Text/CSV'\n")


if __name__ == "__main__":
    run_etl(use_sample=True)   # Set use_sample=False to use live MySQL DB
