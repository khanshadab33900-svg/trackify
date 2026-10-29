# 🛡️ Trackify - Enterprise Software Bug & Issue Tracking Ecosystem

[![Python Version](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-6.0+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Database](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![UI Framework](https://img.shields.io/badge/Frontend-Bootstrap_5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Deployment](https://img.shields.io/badge/Deploy-Render_Web_Service-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://render.com/)

**Trackify** is an enterprise-grade, full-stack defect lifecycle and issue management platform designed for modern software engineering teams. Built using **Python, Django, SQLite, and Bootstrap 5.3**, Trackify provides end-to-end bug logging, developer assignment workflows, severity triage, screenshot evidence handling, real-time analytics dashboards, and an automated **Render Free Tier Zero-Delay Wakeup Mechanism**.

---

## 📑 Table of Contents
1. [Academic Problem Statement & Relevance](#-academic-problem-statement--relevance)
2. [System Architecture](#-system-architecture)
3. [Key Features by User Role](#-key-features-by-user-role)
4. [Render Free-Tier Auto-Wakeup Mechanism](#-render-free-tier-auto-wakeup-mechanism)
5. [Visual Interface Gallery (Screenshots)](#-visual-interface-gallery-screenshots)
6. [Database Schema & Entity Relationship](#-database-schema--entity-relationship)
7. [Local Setup & Installation Guide](#-local-setup--installation-guide)
8. [Step-by-Step Render Deployment](#-step-by-step-render-deployment)
9. [Pre-Populated Demo Credentials](#-pre-populated-demo-credentials)
10. [Authors & Project Representation](#-authors--project-representation)

---

## 🎯 Academic Problem Statement & Relevance

In modern Software Development Life Cycle (SDLC) methodologies (Agile/Scrum), managing software defects through unstructured channels like spreadsheets or communication channels leads to:
* **Untracked Critical Bugs:** High-severity runtime defects get lost in communication threads.
* **Lack of Accountability:** Unclear developer assignment and absence of an audit log for ticket resolutions.
* **Zero Visibility:** Project managers cannot quantify defect density or project stability.

**Trackify** solves this by establishing a structured, role-based defect management pipeline where quality assurance testers log reproducible defects with visual proof, project managers assign workloads based on priority, and developers diagnose and patch issues with timestamped resolution notes.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    User([End User / QA Tester / Dev]) -->|HTTPS Request| CloudFrontend[Client Browser / Static Site]
    CloudFrontend -->|Health Ping| WakeCheck{Is Render Backend Sleeping?}
    
    WakeCheck -->|Yes| AutoWakeModal[Display Animated Wakeup Modal]
    AutoWakeModal -->|Background Ping 20-35s| HealthAPI[/api/health/]
    WakeCheck -->|No / Awake| HealthAPI
    
    HealthAPI -->|200 OK Response| RenderService[Render Web Service: Gunicorn + Django]
    RenderService --> Security[SecurityMiddleware & WhiteNoise Static Storage]
    Security --> Auth[Custom User Authentication & RBAC]
    Auth --> AppLogic[Tracker Core Views & Forms]
    AppLogic --> DB[(SQLite Database: db.sqlite3)]
    AppLogic --> Media[(Uploaded Defect Screenshots)]
```

---

## 🚀 Key Features by User Role

### 1. 🛡️ Administrator / Project Manager
* **Project Directory Management:** Provision software repositories (Active, Completed, On Hold).
* **Defect Assignment Engine:** Allocate incoming defect tickets directly to available developers.
* **Executive Metrics Dashboard:** Live KPI cards displaying Total Projects, Total Bugs Logged, In Progress tickets, and Resolved bug ratios.

### 2. 👨‍💻 Software Engineer / Developer
* **Assigned Tickets Queue:** Personalized view of bugs prioritized for immediate patching.
* **Status Lifecycle Progression:** Update ticket state from `Open` ➔ `In Progress` ➔ `Resolved`.
* **Technical Collaboration Log:** Append debugging updates, root-cause analyses, and patch commit hashes in ticket comment threads.

### 3. 🔍 QA Engineer / Tester
* **Detailed Defect Reporting:** Log issues with title, reproduction steps, severity level (`High`, `Medium`, `Low`), and software module.
* **Visual Evidence Attachment:** Upload failure screenshots directly for diagnostic clarity.

---

## ⚡ Render Free-Tier Auto-Wakeup Mechanism

Free cloud hosting platforms (such as Render) automatically suspend / spin down inactive web services after 15 minutes of inactivity. When a new user hits the service, spinning up instances can take 20 to 45 seconds, often resulting in browser 502/504 gateway timeout errors.

**Trackify features an intelligent proactive warm-up solution:**
1. **Instantaneous DOM Handshake:** As soon as the frontend loads, a non-blocking asynchronous `fetch('/api/health/')` ping is dispatched to the backend.
2. **Dynamic Sleep Detector:** If the backend does not respond within 1.5 seconds, an animated glassmorphic overlay automatically appears:
   > *"⚡ Waking Up Server... Render Free Tier is booting instances. Elapsed: Xs (Est: 20-35s)"*
3. **Automatic Auto-Dismissal:** As soon as the backend returns `200 OK`, the modal seamlessly closes, and a success toast confirms connection readiness.
4. **Zero Authentication Failures:** Users are shielded from timeout errors, ensuring clean login and flawless demonstration during viva evaluations.

---

## 📸 Visual Interface Gallery (Screenshots)

### 1. Modern SaaS Sign In Screen (with 1-Click Demo Buttons)
![Sign In Screen](docs/screenshots/01_login_page.png)

### 2. Account Registration & Role Selection
![Register Screen](docs/screenshots/02_register_page.png)

### 3. Real-Time Analytics & Defect Dashboard
![Analytics Dashboard](docs/screenshots/03_analytics_dashboard.png)

### 4. Software Projects & Repository Overview
![Projects Management](docs/screenshots/04_projects_management.png)

### 5. Centralized Defect & Bug Tickets Directory
![Bug Tickets Directory](docs/screenshots/05_bug_tickets_directory.png)

### 6. Defect Inspection, Screenshot & Developer Comments
![Ticket Detail View](docs/screenshots/06_ticket_detail_and_discussion.png)

### 7. Comprehensive Defect Logging & File Upload Form
![Report Bug Form](docs/screenshots/07_report_bug_form.png)

---

## 🗄️ Database Schema & Entity Relationship

```
+-------------------------------------------------------------+
|                         User (AbstractUser)                 |
+-------------------------------------------------------------+
| id (PK) | username | email | password | role (admin/dev/qa) |
+-------------------------------------------------------------+
                             | 1
                             |
                             | N
+-------------------------------------------------------------+
|                          Project                            |
+-------------------------------------------------------------+
| id (PK) | name | description | start_date | status          |
+-------------------------------------------------------------+
                             | 1
                             |
                             | N
+-------------------------------------------------------------+
|                          Ticket                             |
+-------------------------------------------------------------+
| id (PK)             | title           | description         |
| priority (L/M/H)    | status (O/IP/R) | screenshot          |
| project_id (FK)     | creator_id (FK) | assigned_dev_id(FK) |
| created_at          | updated_at                            |
+-------------------------------------------------------------+
                             | 1
                             |
                             | N
+-------------------------------------------------------------+
|                          Comment                            |
+-------------------------------------------------------------+
| id (PK) | ticket_id (FK) | user_id (FK) | content | created |
+-------------------------------------------------------------+
```

---

## 💻 Local Setup & Installation Guide

### Prerequisites
* Python 3.10, 3.11, or 3.12 installed
* Git installed

### 1. Clone the Repository
```bash
git clone https://github.com/khanshadab33900-svg/trackify.git
cd trackify
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py runserver
```

Open your browser at **`http://127.0.0.1:8000/`**.

---

## ☁️ Step-by-Step Render Deployment

### Option A: Full-Stack Web Service on Render (Recommended)
1. Fork or push this repository to your GitHub account: `https://github.com/khanshadab33900-svg/trackify.git`.
2. Log into [Render Dashboard](https://dashboard.render.com/) and click **New +** ➔ **Web Service**.
3. Connect your GitHub repository.
4. Configure the service settings:
   * **Name:** `trackify-app` (or any custom name)
   * **Region:** Oregon (US West) or Singapore
   * **Branch:** `main` (or `master`)
   * **Runtime:** `Python 3`
   * **Build Command:** `./build.sh` (or `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`)
   * **Start Command:** `gunicorn bug_tracker.wsgi:application`
   * **Plan Type:** `Free`
5. Click **Create Web Service**. Your application will be live in 2-3 minutes!

### Option B: Backend on Render + Frontend on Static Site (Vercel / Netlify)
1. Deploy the backend on Render as a Web Service using Option A above.
2. In `frontend_static/index.html`, enter your live Render URL (e.g. `https://trackify-app.onrender.com`).
3. Deploy `frontend_static/` to Vercel, Netlify, or Render Static Site in 1 click!

---

## 🔑 Pre-Populated Demo Credentials

For live demonstration, evaluation panels, and viva assessments:

| Role | Username | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **System Admin** | `admin` | `admin123` | Full system access, project provisioning, developer assignment |
| **Lead Developer** | `rahul_dev` | `admin123` | Ticket status updates, debugging notes, code comments |
| **QA / Tester** | `sneha_qa` | `admin123` | Bug reporting, screenshot uploads, defect tracking |

---

## 👨‍💻 Project Information & License

* **Project:** Final Year Computer Science & Engineering Capstone Project
* **Architecture:** Model-View-Template (MVT) Pattern
* **License:** [MIT License](LICENSE)
