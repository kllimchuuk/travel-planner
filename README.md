# Travel Planner API

REST API for managing travel projects and places, built with FastAPI + SQLite.

## Requirements

- Python 3.11+ or Docker

## Local Setup

```bash
git clone https://github.com/kllimchuuk/travel-planner.git
cd travel-planner

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
uvicorn main:app --reload
```

## Docker Setup

```bash
cp .env.example .env
docker-compose up --build
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./travel_planner.db` | Database connection string |
| `ART_INSTITUTE_API_URL` | `https://api.artic.edu/api/v1` | Art Institute API base URL |
| `BASIC_AUTH_USERNAME` | `admin` | Basic auth username |
| `BASIC_AUTH_PASSWORD` | `secret` | Basic auth password |
| `DEBUG` | `True` | SQLAlchemy query logging |

## Authentication

All endpoints require HTTP Basic Auth. Default credentials: `admin` / `secret`.

## API Docs

Swagger UI available at `http://localhost:8000/docs` after starting the server.

## Endpoints

### Projects
| Method | URL | Description |
|---|---|---|
| `POST` | `/api/v1/projects/` | Create project (with optional places) |
| `GET` | `/api/v1/projects/` | List projects |
| `GET` | `/api/v1/projects/{id}` | Get project |
| `PUT` | `/api/v1/projects/{id}` | Update project |
| `DELETE` | `/api/v1/projects/{id}` | Delete project |

### Places
| Method | URL | Description |
|---|---|---|
| `POST` | `/api/v1/projects/{id}/places` | Add place to project |
| `GET` | `/api/v1/projects/{id}/places` | List places |
| `GET` | `/api/v1/projects/{id}/places/{place_id}` | Get place |
| `PATCH` | `/api/v1/projects/{id}/places/{place_id}` | Update notes / mark visited |

## Example Requests

```bash
# Create project with places
curl -s -X POST http://localhost:8000/api/v1/projects/ \
  -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{"name": "Trip to Chicago", "places": [{"external_id": 27992}]}'

# Add place to existing project
curl -s -X POST http://localhost:8000/api/v1/projects/1/places \
  -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{"external_id": 111628}'

# Mark place as visited
curl -s -X PATCH http://localhost:8000/api/v1/projects/1/places/1 \
  -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{"is_visited": true}'
```
