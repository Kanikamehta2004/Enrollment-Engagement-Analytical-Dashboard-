-- ============================================================
-- Enrollment & Engagement Analytics Dashboard
-- Database Schema
-- Author: Kanika Mehta
-- ============================================================

CREATE DATABASE IF NOT EXISTS enrollment_analytics;
USE enrollment_analytics;

-- Students master table
CREATE TABLE students (
    student_id      INT AUTO_INCREMENT PRIMARY KEY,
    full_name       VARCHAR(100) NOT NULL,
    email           VARCHAR(150) UNIQUE NOT NULL,
    gender          ENUM('Male', 'Female', 'Other'),
    age             INT,
    city            VARCHAR(100),
    enrollment_date DATE NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Courses table
CREATE TABLE courses (
    course_id       INT AUTO_INCREMENT PRIMARY KEY,
    course_name     VARCHAR(150) NOT NULL,
    category        VARCHAR(100),
    duration_weeks  INT,
    fee             DECIMAL(10, 2),
    instructor      VARCHAR(100),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enrollments (fact table)
CREATE TABLE enrollments (
    enrollment_id   INT AUTO_INCREMENT PRIMARY KEY,
    student_id      INT NOT NULL,
    course_id       INT NOT NULL,
    enroll_date     DATE NOT NULL,
    status          ENUM('Active', 'Completed', 'Dropped', 'On Hold') DEFAULT 'Active',
    payment_status  ENUM('Paid', 'Pending', 'Failed') DEFAULT 'Pending',
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id)  REFERENCES courses(course_id)
);

-- Engagement tracking
CREATE TABLE engagement (
    engagement_id   INT AUTO_INCREMENT PRIMARY KEY,
    student_id      INT NOT NULL,
    course_id       INT NOT NULL,
    session_date    DATE NOT NULL,
    login_count     INT DEFAULT 0,
    videos_watched  INT DEFAULT 0,
    assignments_done INT DEFAULT 0,
    quiz_score      DECIMAL(5, 2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id)  REFERENCES courses(course_id)
);

-- Funnel stages (tracks drop-off)
CREATE TABLE funnel_stages (
    stage_id        INT AUTO_INCREMENT PRIMARY KEY,
    student_id      INT NOT NULL,
    stage_name      ENUM('Visited', 'Registered', 'Enrolled', 'Active', 'Completed') NOT NULL,
    stage_date      DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
