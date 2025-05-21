# ElectroMart – E-Commerce Website

## Project Overview
ElectroMart is a full-featured e-commerce platform built with Flask and PostgreSQL. The application provides a complete shopping experience with user authentication, product browsing, cart management, and order processing.

## Tech Stack
- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Authentication**: Flask-Login
- **Database**: PostgreSQL
- **Deployment**: Railway.app, Docker

## Database Schema
The database consists of the following main tables:
- `users`: User accounts and profiles
- `products`: Product catalog
- `categories`: Product categories
- `brands`: Product brands
- `orders`: Customer orders
- `order_items`: Individual items in orders
- `payments`: Payment records

### Key Constraints
- Foreign key relationships between orders and users
- Unique constraints on usernames and emails
- Check constraints on product prices and quantities
- Cascading deletes for order items

## Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL
- Docker (optional)

### Local Development Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/abdulsamadsheikh/electromart2.git
   cd electromart2
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```bash
   flask db upgrade
   ```

6. Run the application:
   ```bash
   flask run
   ```

### Docker Setup
1. Build the Docker image:
   ```bash
   docker build -t electromart .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 electromart
   ```

## API Endpoints

### Authentication
- `POST /auth/register`: Register new user
- `POST /auth/login`: User login
- `GET /auth/logout`: User logout
- `GET /auth/profile`: View user profile
- `PUT /auth/profile`: Update user profile

### Products
- `GET /products`: List all products
- `GET /product/<id>`: Get product details
- `GET /category/<id>`: Get products by category

### Cart
- `GET /cart`: View cart
- `POST /add_to_cart/<id>`: Add item to cart
- `POST /update_cart_item/<id>`: Update cart item
- `POST /remove_from_cart/<id>`: Remove item from cart

### Orders
- `GET /checkout`: Checkout page
- `POST /process_checkout`: Process order
- `GET /order_history`: View order history

## Deployment
The application is deployed on Railway.app with the following configuration:
- PostgreSQL database
- Docker container
- Environment variables for production

## Database Schema and Data
The complete database schema and sample data are provided in `database_schema.sql`. This includes:
- Table creation statements
- Constraints and indexes
- Sample product data
- Test user accounts

## Testing
Run the test suite:
```bash
pytest
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📦 Overview

ElectroMart is a database-driven e-commerce website built to simulate the operations of an electronics retailer. The system includes a fully normalized relational database and a supporting backend/frontend stack. It enables users to browse electronic products, register and log in, manage carts, place orders, and view order history. The purpose of this project is to demonstrate comprehensive database modeling, implementation, and integration with a working web application.

This project was completed as part of the IDATG2204 course at NTNU and focuses on demonstrating competence in database normalization, schema design, and integration with web technologies.

---

## 👥 Contributors

| Name                        | Candidate Number |
|-----------------------------|------------------|
| Sheikh Abdulsamad           | 10335            |
| Ben Karroum Nourdin         | 10218            |
| Mataev Bilal Rasulovich     | 10340            |
| Alhammod Mohammad Rdwan     | 10352            |
| Halvorsen Ole Bjørn         | 10358            |

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
- **Auth:** Flask-Login (optional)

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
electro_mart_project/
├── backend/
│   ├── app/
│   │   ├── static/
│   │   ├── templates/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── auth.py
│   ├── tests/
│   ├── run.py
│   ├── config.py
│   └── requirements.txt
├── database_design/
│   ├── schema.sql
│   ├── populate_data.sql
│   ├── sample_queries.sql
│   └── normalization/
│       ├── 1nf.md
│       ├── 2nf.md
│       ├── 3nf.md
│       └── bcnf.md
├── report/
│   ├── ElectroMart_Project_Report.docx
│   └── screenshots/
├── .env.example
├── .gitignore
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

## 🧪 Testing

Basic tests are located in `backend/tests/` and can be run using `pytest`:

```bash
pytest backend/tests/
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
