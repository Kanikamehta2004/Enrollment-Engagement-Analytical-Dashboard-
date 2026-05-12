-- ============================================================
-- Enrollment & Engagement Analytics — KPI Queries
-- Used as data sources in Power BI
-- Author: Kanika Mehta
-- ============================================================

USE enrollment_analytics;

-- ── 1. Enrollment Rate by Month ───────────────────────────
SELECT
    DATE_FORMAT(enroll_date, '%Y-%m') AS month,
    COUNT(enrollment_id)              AS total_enrollments,
    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
    SUM(CASE WHEN status = 'Dropped'   THEN 1 ELSE 0 END) AS dropped
FROM enrollments
GROUP BY month
ORDER BY month;

-- ── 2. Funnel Drop-off Analysis ───────────────────────────
SELECT
    stage_name,
    COUNT(DISTINCT student_id) AS student_count,
    ROUND(
        COUNT(DISTINCT student_id) * 100.0 /
        MAX(COUNT(DISTINCT student_id)) OVER (), 2
    ) AS pct_of_top
FROM funnel_stages
GROUP BY stage_name
ORDER BY FIELD(stage_name, 'Visited','Registered','Enrolled','Active','Completed');

-- ── 3. Cohort Retention Analysis ─────────────────────────
SELECT
    DATE_FORMAT(e.enroll_date, '%Y-%m') AS cohort_month,
    COUNT(DISTINCT e.student_id)         AS cohort_size,
    SUM(CASE WHEN e.status = 'Completed' THEN 1 ELSE 0 END) AS retained,
    ROUND(SUM(CASE WHEN e.status = 'Completed' THEN 1 ELSE 0 END) * 100.0 /
          COUNT(DISTINCT e.student_id), 2) AS retention_rate
FROM enrollments e
GROUP BY cohort_month
ORDER BY cohort_month;

-- ── 4. Top Performing Courses ─────────────────────────────
SELECT
    c.course_name,
    c.category,
    COUNT(e.enrollment_id)  AS total_enrolled,
    ROUND(AVG(eng.quiz_score), 2) AS avg_quiz_score,
    SUM(CASE WHEN e.status = 'Completed' THEN 1 ELSE 0 END) AS completions
FROM courses c
LEFT JOIN enrollments e  ON c.course_id = e.course_id
LEFT JOIN engagement eng ON c.course_id = eng.course_id
GROUP BY c.course_id, c.course_name, c.category
ORDER BY total_enrolled DESC;

-- ── 5. Student Engagement Score (KPI) ─────────────────────
SELECT
    s.student_id,
    s.full_name,
    SUM(eng.videos_watched)   AS total_videos,
    SUM(eng.assignments_done) AS total_assignments,
    ROUND(AVG(eng.quiz_score), 2) AS avg_score,
    ROUND(
        (SUM(eng.videos_watched) * 0.4 +
         SUM(eng.assignments_done) * 0.4 +
         AVG(eng.quiz_score) * 0.2), 2
    ) AS engagement_score
FROM students s
JOIN engagement eng ON s.student_id = eng.student_id
GROUP BY s.student_id, s.full_name
ORDER BY engagement_score DESC;

-- ── 6. City-wise Enrollment Distribution ──────────────────
SELECT
    s.city,
    COUNT(e.enrollment_id) AS enrollments,
    ROUND(AVG(eng.quiz_score), 2) AS avg_performance
FROM students s
JOIN enrollments e  ON s.student_id = e.student_id
LEFT JOIN engagement eng ON s.student_id = eng.student_id
GROUP BY s.city
ORDER BY enrollments DESC;
