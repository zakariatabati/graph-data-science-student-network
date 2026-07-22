import os
import csv
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv('.env ')
URI      = os.getenv("NEO4J_URI")
USER     = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


# ── 1. Constraints ────────────────────────────────────────────────────────────
CONSTRAINTS = [
    "CREATE CONSTRAINT student_id IF NOT EXISTS FOR (s:Student) REQUIRE s.id IS UNIQUE",
    "CREATE CONSTRAINT club_id    IF NOT EXISTS FOR (c:Club)    REQUIRE c.id IS UNIQUE",
    "CREATE CONSTRAINT event_id   IF NOT EXISTS FOR (e:Event)   REQUIRE e.id IS UNIQUE",
]

# ── 2. Indexes ────────────────────────────────────────────────────────────────
# Added Student.annee and Event.type (queried often)
INDEXES = [
    "CREATE INDEX student_filiere IF NOT EXISTS FOR (s:Student) ON (s.filière)",
    "CREATE INDEX student_annee   IF NOT EXISTS FOR (s:Student) ON (s.annee)",
    "CREATE INDEX club_categorie  IF NOT EXISTS FOR (c:Club)    ON (c.catégorie)",
    "CREATE INDEX event_date      IF NOT EXISTS FOR (e:Event)   ON (e.date)",
    "CREATE INDEX event_type      IF NOT EXISTS FOR (e:Event)   ON (e.type)",
]


def apply_constraints_and_indexes(tx):
    print("\n── Applying constraints ──────────────────────────────")
    for cypher in CONSTRAINTS:
        tx.run(cypher)
        label = cypher.split("CONSTRAINT ")[1].split(" ")[0]
        print(f"  ✓ {label}")

    print("\n── Creating indexes ──────────────────────────────────")
    for cypher in INDEXES:
        tx.run(cypher)
        label = cypher.split("INDEX ")[1].split(" ")[0]
        print(f"  ✓ {label}")


# ── 3. Node queries 
STUDENT_QUERY = """
UNWIND $batch AS s
MERGE (n:Student {id: s.id})
SET n.nom              = s.nom,
    n.email           = s.email,
    n.filiere          = s.filière,
    n.annee            = toInteger(s.année),
    n.date_inscription = date(s.date_inscription)
"""

CLUB_QUERY = """
UNWIND $batch AS c
MERGE (n:Club {id: c.id})
SET n.nom           = c.nom,
    n.categorie     = c.catégorie,
    n.date_creation = date(c.date_creation)
"""

EVENT_QUERY = """
UNWIND $batch AS e
MERGE (n:Event {id: e.id})
SET n.nom  = e.name,
    n.date = date(e.date),
    n.type = e.type
"""


def import_nodes(tx, students, clubs, events, batch_size=500):
    print("\n── Importing Student nodes ───────────────────────────")
    for i in range(0, len(students), batch_size):
        batch = students[i:i + batch_size]
        tx.run(STUDENT_QUERY, batch=batch)
        print(f"  ✓ {min(i + batch_size, len(students))} / {len(students)}")

    print("\n── Importing Club nodes ──────────────────────────────")
    for i in range(0, len(clubs), batch_size):
        batch = clubs[i:i + batch_size]
        tx.run(CLUB_QUERY, batch=batch)
        print(f"  ✓ {min(i + batch_size, len(clubs))} / {len(clubs)}")

    print("\n── Importing Event nodes ─────────────────────────────")
    for i in range(0, len(events), batch_size):
        batch = events[i:i + batch_size]
        tx.run(EVENT_QUERY, batch=batch)
        print(f"  ✓ {min(i + batch_size, len(events))} / {len(events)}")


# ── 4. Relationship queries ────────
# Friendship: undirected conceptually — stored directed, queried with -[]-
FRIENDSHIP_QUERY = """
UNWIND $batch AS r
MATCH (a:Student {id: r.student_id_1}), (b:Student {id: r.student_id_2})
MERGE (a)-[rel:EST_AMI_DE]->(b)
SET rel.since = date(r.since)
"""

# Membership: date_adhesion from CSV
MEMBERSHIP_QUERY = """
UNWIND $batch AS r
MATCH (s:Student {id: r.student_id}), (c:Club {id: r.club_id})
MERGE (s)-[rel:MEMBRE_DE]->(c)
SET rel.date_adhesion = date(r.date_adhesion),
    rel.role          = r.role
"""

PARTICIPATION_QUERY = """
UNWIND $batch AS r
MATCH (s:Student {id: r.student_id}), (e:Event {id: r.event_id})
MERGE (s)-[rel:A_PARTICIPE_A]->(e)
SET rel.feedback = r.feedback
"""


def import_relationships(tx, friendships, memberships, participations, batch_size=500):
    print("\n── Importing EST_AMI_DE ──────────────────────────────")
    for i in range(0, len(friendships), batch_size):
        batch = friendships[i:i + batch_size]
        tx.run(FRIENDSHIP_QUERY, batch=batch)
        print(f"  ✓ {min(i + batch_size, len(friendships))} / {len(friendships)}")

    print("\n── Importing MEMBRE_DE ───────────────────────────────")
    for i in range(0, len(memberships), batch_size):
        batch = memberships[i:i + batch_size]
        tx.run(MEMBERSHIP_QUERY, batch=batch)
        print(f"  ✓ {min(i + batch_size, len(memberships))} / {len(memberships)}")

    print("\n── Importing A_PARTICIPE_A ───────────────────────────")
    for i in range(0, len(participations), batch_size):
        batch = participations[i:i + batch_size]
        tx.run(PARTICIPATION_QUERY, batch=batch)
        print(f"  ✓ {min(i + batch_size, len(participations))} / {len(participations)}")


# ── 5. Verification ───────────────────────────────────────────────────────────
def verify_counts(tx):
    print("\n── Node counts ───────────────────────────────────────")
    result = tx.run("MATCH (n) RETURN labels(n) AS label, count(*) AS count")
    for record in result:
        print(f"  {record['label'][0]:<12} : {record['count']}")

    print("\n── Relationship counts ───────────────────────────────")
    result = tx.run("MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS count")
    for record in result:
        print(f"  {record['type']:<20} : {record['count']}")

    print("\n── Exact count assertions ────────────────────────────")
    counts = tx.run("""
        MATCH (s:Student)          WITH count(s) AS students
        MATCH (c:Club)             WITH students, count(c) AS clubs
        MATCH (e:Event)            WITH students, clubs, count(e) AS events
        RETURN students, clubs, events
    """).single()

    assert counts['students'] == 1500, f"❌ Students: expected 1500, got {counts['students']}"
    assert counts['clubs']    == 70,   f"❌ Clubs: expected 70, got {counts['clubs']}"
    assert counts['events']   == 300,  f"❌ Events: expected 300, got {counts['events']}"
    print("  ✓ 1500 students / 70 clubs / 300 events — all correct.")


# ── Load CSVs ─────────────────────────────────────────────────────────────────
def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def load_data():
    students       = read_csv("datasets/students.csv")
    clubs          = read_csv("datasets/clubs.csv")
    events         = read_csv("datasets/events.csv")
    friendships    = read_csv("datasets/friendships.csv")
    memberships    = read_csv("datasets/memberships.csv")
    participations = read_csv("datasets/participations.csv")

    print("\n── Data loaded from datasets/ ────────────────────────")
    print(f"  Students      : {len(students)}")
    print(f"  Clubs         : {len(clubs)}")
    print(f"  Events        : {len(events)}")
    print(f"  Friendships   : {len(friendships)}")
    print(f"  Memberships   : {len(memberships)}")
    print(f"  Participations: {len(participations)}")

    return students, clubs, events, friendships, memberships, participations


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("═══════════════════════════════════════════════════════")
    print("   Neo4j Import Script")
    print("  URI:", URI)
    print("═══════════════════════════════════════════════════════")

    students, clubs, events, friendships, memberships, participations = load_data()

    with driver.session() as session:
        session.execute_write(apply_constraints_and_indexes)
        session.execute_write(import_nodes, students, clubs, events)
        session.execute_write(import_relationships, friendships, memberships, participations)
        session.execute_read(verify_counts)

    driver.close()
    print("\n  ✓ Import complete.")


if __name__ == "__main__":
    main()