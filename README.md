## 📦 Overview

ElectroMart is a database-driven e-commerce website built to simulate the operations of an electronics retailer. The system includes a fully normalized relational database and a supporting backend/frontend stack. It enables users to browse electronic products, register and log in, manage carts, place orders, and view order history. The purpose of this project is to demonstrate comprehensive database modeling, implementation, and integration with a working web application.

This project was completed as part of the IDATG2204 course at NTNU and focuses on demonstrating competence in database normalization, schema design, and integration with web technologies.

---

## 👥 Contributors

| Name                        | Candidate Number |
|-----------------------------|------------------|
| Abdulsamad Sheikh           | 10335            |
| Nourdin Ben Karroum         | 10218            |
| Bilal Rasulovich Mataev     | 10340            |
| Mohammad Rdwan Alhammod     | 10352            |
| Ole Bjørn Halvorsen         | 10358            |

---

## 🧠 Project Goals

- Design a normalized relational database schema with entities such as `Product`, `User`, `Order`, `Payment`, etc.
- Develop a basic but functional backend and frontend system to support the database.
- Implement real-world concepts like authentication, order management, and referential integrity.
- Document all assumptions, design decisions, and implementation details clearly in the project report.

---

## 🛠️ Tech Stack

### Backend
- **Language:** Python
- **Framework:** Flask
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy + Flask-Migrate
- **Auth:** Flask-Login

### Frontend
- **HTML/CSS/JavaScript**
- **Templating:** Jinja2

---

## 🗃️ Database Features

- **Normalization:** Schema is designed in 1NF, 2NF, 3NF, and BCNF.
- **EER & Logical Models:** Included in the report with diagrams.
- **SQL Scripts:** 
  - `schema.sql`: Full database schema
  - `populate_data.sql`: Sample data
  - `sample_queries.sql`: Useful queries to demonstrate functionality
- **Constraints & Integrity:** All keys, constraints, and indexes applied.

---

## 🔐 Security & Best Practices

- Environment variables managed with `.env`
- Use of hashed passwords (if implemented)
- Input validation on both frontend and backend
- Referential integrity and transaction safety in SQL operations

---

## 📷 Screenshots & Report

All screenshots, diagrams, and project explanations are included in the official report:
- EER Diagram
- Logical Data Model
- Screenshot evidence of order placement, login, registration, etc.
- Normalization samples
- Explanation of schema decisions and indexing choices

---

## 📁 Project Structure

```plaintext
electromart2/
├── backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── cart.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── static
│   │   │   ├── css
│   │   │   │   └── style.css
│   │   │   ├── images
│   │   │   └── js
│   │   │       └── main.js
│   │   └── templates
│   │       ├── errors
│   ├── app.db
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
├── database_design
│   ├── 01_schema.sql
│   ├── 02_sample_data.sql
│   ├── 03_sample_queries.sql
│   ├── Databaser_Rapport.pdf
│   └── diagrams
├── Dockerfile
└── README.md
````

---

## 🚀 Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/abdulsamadsheikh/electromart2.git
   cd electromart2
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Set up the database**

   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. **Run the app**

   ```bash
   python backend/run.py
   ```

---

## 📌 Notes

* **Version control**: Git was used throughout development for collaboration.
* **Assumptions**: All assumptions regarding data, constraints, and business logic are documented in the report.
* **Focus**: The core grading emphasis is on database quality and integration — not frontend aesthetics.

---

## 📄 License

This project is intended for academic use only.

---
