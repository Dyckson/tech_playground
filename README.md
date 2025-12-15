# Tech Playground - Employee Feedback Analytics

Full-stack analytics platform for employee feedback data with REST API, React dashboard, and PostgreSQL.

## 🚀 Quick Start

**Prerequisites:** Docker & Docker Compose

```bash
# Recommended: using Make
make up

# Or directly with docker-compose
docker-compose up -d
```

**Access:**
- 🎨 Dashboard: http://localhost:3000
- 📊 API Docs: http://localhost:9876/docs

**Stop:**
```bash
make down  # or: docker-compose down
```

That's it! The system automatically:
- Creates and migrates PostgreSQL database
- Imports 500 employees from CSV
- Starts all 3 services (Database, Backend API, Frontend)

---

## 📖 Requirements

- Docker 20.10+
- Docker Compose 1.29+
- Available ports: 3000, 9876, 9432

---

## 🏗️ Tech Stack

**Backend:** FastAPI 2.0 + Python 3.11 + PostgreSQL 15  
**Frontend:** React 18 + TypeScript + Material-UI + Vite  
**Testing:** Pytest (161 tests, 94.64% coverage)  
**Data:** 500 employees, 500 evaluations, 3,500 responses

---

## 📊 Features

**Dashboard:**
- eNPS score: -30.4 (Promoters 27.6% | Passives 14.4% | Detractors 58%)
- Satisfaction scores across 7 dimensions (Likert scale 1-7)
- Employee distribution by generation, gender, tenure, location
- Interactive Material-UI charts

**Employee Management:**
- Complete employee list (500 records)
- Search and pagination
- Individual profiles and analytics

**REST API:**
- `GET /analytics/enps` - eNPS metrics
- `GET /analytics/satisfaction` - Satisfaction by dimension  
- `GET /funcionarios` - List employees (paginated)
- `GET /funcionarios/{id}/detailed-profile` - Employee analytics

Full API documentation: http://localhost:9876/docs

---

## 🧪 Testing

```bash
# Run all tests (161 tests)
make test

# Run with coverage report
make test-cov

# Or manually
docker exec tech_playground_backend pytest tests/ -v
```

---

## 🛠️ Available Commands

Run `make help` to see all available commands:

```bash
make help          # Show all commands with descriptions
make up            # Start all containers
make down          # Stop all containers
make logs          # View logs (live)
make restart       # Restart containers
make test          # Run all tests (161 tests)
make test-cov      # Run tests with coverage report
make lint          # Check code quality
make format        # Format code
```

---

## 🔧 Troubleshooting

**Ports in use or containers not starting?**
```bash
make down
docker-compose down -v && docker-compose up -d --build
```

**Check logs:**
```bash
make logs
```

**Verify database:**
```bash
docker-compose exec postgres pg_isready -U tech_user
```

---

## 📚 Documentation

- `DATABASE_DESIGN.md` - Complete database schema and normalization
- `DATABASE_ARCHITECTURE.md` - Design decisions and alternatives
- Interactive API Docs: http://localhost:9876/docs (when running)

---

## 📁 Project Structure

```
tech_playground/
├── backend/           # FastAPI application
│   ├── app/          # API controllers, services, repositories
│   ├── database/     # Migrations and schema
│   ├── scripts/      # Data import scripts
│   └── tests/        # Test suite (161 tests)
├── frontend/         # React application
│   └── src/          # Components, pages, services
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## ✅ Completed Challenge Tasks

- ✅ Task 1: Database (PostgreSQL, normalized 5NF schema, 14 tables)
- ✅ Task 2: Dashboard (React + Material-UI, responsive)
- ✅ Task 3: Test Suite (195 tests, 91.13% coverage, unit + integration)
- ✅ Task 4: Docker Compose (3 services, auto-setup)
- ✅ Task 6: Company Level Analytics (eNPS, satisfaction metrics)
- ✅ Task 7: Data Visualization - Area Level (hierarchical analytics, area comparisons)
- ✅ Task 8: Employee Level Analytics (profiles, comparisons)
- ✅ Task 9: REST API (FastAPI + OpenAPI/Swagger docs)

---

## 📄 License

Educational and demonstration purposes.
