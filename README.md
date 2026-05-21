# JobSyncr - Full-Stack Placement Portal 🎓

JobSyncr is a robust, full-stack placement portal designed to streamline the recruitment process within academic institutions. Built using a decoupled client-server architecture, the platform features role-based access control (RBAC) to provide customized experiences for students, corporate recruiters, and institutional administrators.

## Key Features & Functionality

* **Role-Based Access Control (RBAC):** Separate, secure dashboards tailored specifically for Students, Company HRs, and Institute Admins.
* **Dynamic Job Application Pipelines:** Automated application tracking workflow from job posting to final hiring selection.
* **Advanced Analytics & Reporting:** Dedicated admin and company dashboards featuring complex data filtering, student performance aggregations, and recruitment tracking metrics.
* **Optimized Performance:** Implemented efficient front-end state management to minimize redundant API payload delivery during multi-step application wizard forms.

---

## 🛠️ Tech Stack

### Front-End
* **Framework:** Vue.js (Single Page Application architecture)
* **Styling:** Bootstrap (Fully responsive layout)
* **State Management & Routing:** Vue Router & Native Vue State Management

### Back-End
* **Core Framework:** Flask (Python)
* **API Design:** RESTful Architecture
* **ORM:** SQLAlchemy

### Database
* **Production/Development:** PostgreSQL / SQLite (for rapid prototyping validation)

---

## 📊 Database Architecture & Schema Design
The application utilizes an optimized relational database schema designed to handle high-concurrency operations and analytical queries seamlessly.
