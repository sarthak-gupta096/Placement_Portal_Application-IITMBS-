# JobSyncr - Full-Stack Placement Portal 🎓

JobSyncr is a robust, full-stack placement portal designed to streamline the recruitment process within academic institutions. Built using a decoupled client-server architecture, the platform features role-based access control (RBAC) to provide customized experiences for students, corporate recruiters, and institutional administrators.

## Key Features & Functionality

* **Role-Based Access Control (RBAC):** Dedicated, secure dashboards tailored specifically for Students, Company HRs, and Institute Admins to guarantee data privacy.
* **Dynamic Job Application Pipelines:** Automated application tracking workflow handling the full lifecycle of placement data from posting to final hiring status mutations.
* **Optimized Frontend Performance:** Implemented reactive front-end state management in Vue.js, significantly reducing redundant API payload delivery during multi-step application wizard forms.
* **Asynchronous Task Processing:** Integrated an asynchronous background worker pipeline to handle resource-intensive scheduled tasks, such as generating monthly placement reports and automated reminders without blocking the main application thread.
* **Automated Communication System:** Integrated event-driven email triggers to instantly notify users of critical status updates (e.g., application shortlists, etc).
* **Data Portability API:** Built a dedicated data-export API allowing students to securely download and export their professional placement history for external use.
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

### Database & Asynchronous Infra
* **Production/Development:** PostgreSQL / SQLite (for rapid prototyping validation)
* **Task Queue Worker:** Celery
* **Message Broker / In-Memory Cache:** Redis
* **SMTP Testing Sandbox:** MailHog

---

## 📊 Database Architecture & Schema Design
The application utilizes an optimized relational database schema designed to handle high-concurrency operations and analytical queries seamlessly.

--- 

## 💻 Local Setup Instructions

### Prerequisites
* Python 3.10+
* Node.js (v16+)
* Redis Server (Running locally or via Docker) - If running locally then save the .exe file in the backend folder.

### 1. Backend & Worker Setup
```bash

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install required dependencies
pip install -r requirements.txt

# Run main.py file
python main.py

# Start the Redis server (in a separate terminal)
cd backend -> cd Redis ->  redis-server.exe

# Start the Celery worker (in a separate terminal)
cd backend -> python -m celery -A main.celery_app worker --loglevel=info --pool=solo

# Start the Celery beat (in a separate terminal)
cd backend -> python -m celery -A main.celery_app beat --loglevel=info

# Run the MailHog server (in a separate terminal)
cd backend -> MailHog_windows_amd64.exe

```
### 2. Frontend Setup

```bash

# Run frontend server (in a separate terminal)
cd frontend -> npm install -> npm run dev

```
