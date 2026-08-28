# Graph Data Science — Student Social Network

> Community detection and recommendation system built on a student social network using Neo4j, Graph Data Science algorithms, and FastAPI.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Graph Model](#graph-model)
- [Algorithms](#algorithms)
- [Getting Started](#getting-started)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Dataset](#dataset)
- [Future Improvements](#future-improvements)

---

## Overview

This project models a university student social network as a property graph and applies **Graph Data Science** techniques to extract knowledge from the graph structure.

It solves two main problems :

**Community Detection** — automatically identify groups of students who share strong social connections, using three different algorithms (Louvain, Leiden, Label Propagation) and compare their results quantitatively.

**Recommendation System** — suggest new friends, clubs, and events to each student using graph-based similarity methods (Common Neighbors, Jaccard, Adamic-Adar, Node2Vec embeddings, and a hybrid approach).

All functionalities are exposed through a **REST API** built with FastAPI, documented via OpenAPI/Swagger.

---

## Features

- **Graph modeling** — Student, Club, and Event nodes connected by friendship, membership, and participation relationships stored in Neo4j
- **Synthetic dataset generation** — 1,500 students, 70 clubs, 300 events with realistic power-law friendship distribution
- **Graph statistics** — degree, density, clustering coefficient, centrality measures (Degree, PageRank, Betweenness, Closeness)
- **Community detection** — Louvain, Leiden, and Label Propagation with modularity evaluation
- **Friend recommendations** — 5 methods: Common Neighbors, Jaccard, Adamic-Adar, Node2Vec, Hybrid
- **Club recommendations** — based on friends' memberships
- **Event recommendations** — based on friends' participation history
- **REST API** — FastAPI with full OpenAPI/Swagger documentation
- **Dockerized** — one command to start Neo4j + API together

---

## Tech Stack

| Layer                    | Technology                            |
| ------------------------ | ------------------------------------- |
| Graph database           | Neo4j 5.x (Community Edition)         |
| Graph algorithms         | Neo4j Graph Data Science (GDS) plugin |
| Backend API              | FastAPI + Uvicorn                     |
| Data validation          | Pydantic                              |
| Graph analytics (Python) | NetworkX                              |
| Embeddings               | Node2Vec (via Neo4j GDS)              |
| Data generation          | Python, Faker                         |
| Testing                  | pytest, FastAPI TestClient            |
| Containerization         | Docker, Docker Compose                |
| Language                 | Python 3.11+                          |

---

## Project Structure

```
graph-data-science-student-network/
│
├── app/
│   ├── main.py                          # FastAPI app entry point
│   │
│   ├── routers/
│   │   ├── recommendations.py           # Recommendation endpoints
│   │   ├── communities.py               # Community detection endpoints
│   │   ├── students.py                  # Student endpoints
│   │   └── graph.py                     # Graph statistics endpoints
│   │
│   ├── services/
│   │   ├── recommendation_service.py    # Recommendation business logic
│   │   └── community_service.py         # Community detection logic
│   │
│   ├── repositories/
│   │   ├── neo4j.py                     # Neo4j driver connection
│   │   └── recommendation_repository.py # Cypher queries
│   │
│   ├── schemas/
│   │   └── recommendation.py            # Pydantic models
│   │
│   └── graph_algorithms/
│       ├── common_neighbors.py          # Common Neighbors algorithm
│       ├── jaccard.py                   # Jaccard Similarity algorithm
│       ├── adamic_adar.py               # Adamic-Adar algorithm
│       ├── node2vec.py                  # Node2Vec cosine similarity
│       └── hybrid.py                   # Weighted hybrid recommender
│
├── datasets/
│   ├── students.csv                     # Generated student nodes
│   ├── clubs.csv                        # Generated club nodes
│   ├── events.csv                       # Generated event nodes
│   ├── friendships.csv                  # EST_AMI_DE relationships
│   ├── memberships.csv                  # MEMBRE_DE relationships
│   └── participations.csv              # A_PARTICIPE_A relationships
│
├── scripts/
│   ├── generate_data.py                 # Synthetic dataset generator
│   └── import_neo4j.py                  # Neo4j import script
│
├── notebooks/
│   ├── 01_eda.ipynb                     # Exploratory data analysis
│   ├── 02_centrality.ipynb              # Centrality analysis
│   ├── 03_community_detection.ipynb     # Community detection experiments
│   └── 04_recommendations.ipynb        # Recommendation evaluation
│
├── docs/
│   └── adr/
│       ├── ADR-001-neo4j-vs-relational.md
│       ├── ADR-002-node2vec-before-gnn.md
│       └── ADR-003-fastapi-vs-flask-django.md
│
├── tests/
│   └── test_recommendations.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## Graph Model

The network is modeled as a property graph with **3 node types** and **3 relationship types**.

### Nodes

| Label     | Key Properties                                                |
| --------- | ------------------------------------------------------------- |
| `Student` | `id`, `nom`, `prenom`, `filiere`, `annee`, `date_inscription` |
| `Club`    | `id`, `nom`, `categorie`, `date_creation`                     |
| `Event`   | `id`, `nom`, `date`, `lieu`, `type`                           |

### Relationships

| Relationship    | Direction         | Key Properties          |
| --------------- | ----------------- | ----------------------- |
| `EST_AMI_DE`    | Student ↔ Student | `since`                 |
| `MEMBRE_DE`     | Student → Club    | `date_adhesion`, `role` |
| `A_PARTICIPE_A` | Student → Event   | `feedback`              |

```
(Student) -[:EST_AMI_DE]->  (Student)
(Student) -[:MEMBRE_DE]->   (Club)
(Student) -[:A_PARTICIPE_A]-> (Event)
```

---

## Algorithms

### Community Detection

| Algorithm         | Method                                 | Modularity Q |
| ----------------- | -------------------------------------- | ------------ |
| Louvain           | Modularity maximization                | 0.3187       |
| Leiden            | Louvain + well-connectivity refinement | 0.3240       |
| Label Propagation | Iterative label spreading              | —            |

### Recommendation

| Method           | Approach                                       | Normalized   |
| ---------------- | ---------------------------------------------- | ------------ |
| Common Neighbors | `\|N(u) ∩ N(v)\|`                              | Yes          |
| Jaccard          | `\|N(u) ∩ N(v)\| / \|N(u) ∪ N(v)\|`            | Native [0,1] |
| Adamic-Adar      | `Σ 1/log(deg(w))` over common neighbors        | Yes          |
| Node2Vec         | Cosine similarity on GDS embeddings            | Native [0,1] |
| Hybrid           | `0.3·Jaccard + 0.3·Adamic-Adar + 0.4·Node2Vec` | Yes          |

---

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Git

### Clone the repository

```bash
git clone https://github.com/your-username/graph-data-science-student-network.git
cd graph-data-science-student-network
```

### Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your values :

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

### Install Python dependencies

```bash
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Running the Project

### Step 1 — Start Neo4j with Docker

```bash
docker-compose up -d neo4j
```

Wait about 20 seconds for Neo4j to fully start, then open the browser at:

```
http://localhost:7474
```

Login with `neo4j / your_password` (from your `.env` file).

### Step 2 — Generate the synthetic dataset

```bash
python scripts/generate_data.py
```

This creates 6 CSV files in `datasets/`.

### Step 3 — Import the data into Neo4j

```bash
python scripts/import_neo4j.py
```

This applies constraints, creates indexes, imports all nodes and relationships, and verifies the final counts.

Expected output :

```
── Verification ──────────────────────────────
  Student      : 1500
  Club         : 70
  Event        : 300
  EST_AMI_DE   : 7465
  MEMBRE_DE    : 2047
  A_PARTICIPE_A: 19179
  ✓ All counts verified successfully.
```

### Step 4 — Generate Node2Vec embeddings (required for the node2vec and hybrid methods)

Run this query once in the Neo4j Browser (`http://localhost:7474`) :

```cypher
CALL gds.graph.project('student-friendship-graph', 'Student',
    { EST_AMI_DE: { orientation: 'UNDIRECTED' } });

CALL gds.node2vec.write('student-friendship-graph', {
    writeProperty: 'embedding',
    embeddingDimension: 64,
    walkLength: 80,
    walksPerNode: 10,
    inOutFactor: 0.5,
    returnFactor: 1.0
});
```

### Step 5 — Start the API

```bash
uvicorn app.main:app --reload
```

The API is now running at `http://localhost:8000`.

### Or — Start everything with Docker Compose

```bash
docker-compose up
```

This starts both Neo4j and the FastAPI service together.

---

## API Endpoints

Interactive documentation is available at :

- **Swagger UI** → `http://localhost:8000/docs`
- **ReDoc** → `http://localhost:8000/redoc`

### Recommendations

| Method | Endpoint                                       | Description            |
| ------ | ---------------------------------------------- | ---------------------- |
| GET    | `/api/v1/recommendations/{student_id}/friends` | Friend recommendations |
| GET    | `/api/v1/recommendations/{student_id}/clubs`   | Club recommendations   |
| GET    | `/api/v1/recommendations/{student_id}/events`  | Event recommendations  |

**Friend recommendations** accept a `method` query parameter :

```
GET /api/v1/recommendations/S001/friends?method=jaccard&top_k=10
```

Available methods : `common_neighbors`, `jaccard`, `adamic_adar`, `node2vec`, `hybrid`

**Example response :**

```json
{
  "student_id": "S001",
  "method": "jaccard",
  "top_k": 10,
  "recommendations": [
    { "student_id": "S042", "score": 0.87 },
    { "student_id": "S117", "score": 0.74 }
  ]
}
```

### Communities

| Method | Endpoint                                  | Description                         |
| ------ | ----------------------------------------- | ----------------------------------- |
| POST   | `/api/v1/communities/detect`              | Run a community detection algorithm |
| GET    | `/api/v1/communities`                     | List all detected communities       |
| GET    | `/api/v1/communities/{community_id}`      | Details of one community            |
| GET    | `/api/v1/students/{student_id}/community` | Community of a student              |

### Graph Statistics

| Method | Endpoint                   | Description             |
| ------ | -------------------------- | ----------------------- |
| GET    | `/api/v1/graph/stats`      | Global graph statistics |
| GET    | `/api/v1/graph/centrality` | Centrality scores       |

---

## Dataset

The synthetic dataset was generated to simulate a realistic student social network :

| Entity               | Count   |
| -------------------- | ------- |
| Students             | 1,500   |
| Clubs                | 70      |
| Events               | 300     |
| Friendships          | ~7,465  |
| Club memberships     | ~2,047  |
| Event participations | ~19,179 |

Friendships follow a **power-law degree distribution** (Zipf) — most students have 5–20 friends, while a small number of hub students have 100+ connections, consistent with real-world social network topology.

---

## Future Improvements

- **GraphSAGE link prediction** — implement a GraphSAGE model via PyTorch Geometric for learned node embeddings, benchmarked against the current structural baselines
- **Real data integration** — replace synthetic data with anonymized real student data (subject to data protection compliance)
- **Authentication** — add JWT-based authentication to the API
- **Caching** — cache pre-computed recommendation scores with Redis for faster response times
- **Dashboard** — build an interactive visualization frontend using Neovis.js or D3.js

---

## Author

**Zakaria** — Génie Informatique, ENSA Marrakech, 2026

---

## License

MIT License
