import csv
import random
from datetime import date, timedelta

import networkx as nx


# CONFIGURATION

STUDENTS_FILE = "datasets/students.csv"
OUTPUT_FILE = "datasets/friendships.csv"
M = 5
END_DATE = date(2026, 12, 31)
RANDOM_SEED = 42


# LOAD STUDENTS
def load_students(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as file:

        return list(
            csv.DictReader(file)
        )



# GENERATE FRIENDSHIP DATE

def generate_friendship_date(
    student_1,
    student_2,
):

    inscription_date_1 = date.fromisoformat(
        student_1["date_inscription"]
    )

    inscription_date_2 = date.fromisoformat(
        student_2["date_inscription"]
    )

    earliest_friendship_date = max(
        inscription_date_1,
        inscription_date_2,
    )

    if (
        earliest_friendship_date
        >= END_DATE
    ):
        return earliest_friendship_date
    days_between = (
        END_DATE
        - earliest_friendship_date
    ).days

    random_days = random.randint(
        0,
        days_between,
    )

    return (
        earliest_friendship_date
        + timedelta(
            days=random_days
        )
    )

# GENERATE FRIENDSHIPS
def generate_friendships(
    students,
):

    number_of_students = len(
        students
    )
    graph = nx.powerlaw_cluster_graph(
    n=number_of_students,
    m=M,
    p=0.3,
    seed=RANDOM_SEED,
    )

    friendships = []

    for student_index_1, student_index_2 in graph.edges():

        student_1 = students[
            student_index_1
        ]

        student_2 = students[
            student_index_2
        ]

        friendship = {
            "student_id_1": student_1["id"],
            "student_id_2": student_2["id"],
            "since": generate_friendship_date(
                student_1,
                student_2,
            ),
        }

        friendships.append(
            friendship
        )

    return friendships, graph


# SAVE FRIENDSHIPS

def save_friendships(
    friendships,
):

    fieldnames = [
        "student_id_1",
        "student_id_2",
        "since",
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerows(
            friendships
        )

# PRINT GRAPH STATISTICS

def print_statistics(
    graph,
):

    number_of_students = graph.number_of_nodes()

    number_of_friendships = graph.number_of_edges()

    degrees = [
        degree
        for _, degree
        in graph.degree()
    ]

    average_degree = (
        sum(degrees)
        / number_of_students
    )

    maximum_degree = max(
        degrees
    )

    clustering_coefficient = (
        nx.average_clustering(
            graph
        )
    )

    print(
        "\nFriendship graph statistics:"
    )

    print(
        f"Students: "
        f"{number_of_students}"
    )

    print(
        f"Friendships: "
        f"{number_of_friendships}"
    )

    print(
        f"Average degree: "
        f"{average_degree:.2f}"
    )

    print(
        f"Maximum degree: "
        f"{maximum_degree}"
    )

    print(
        f"Clustering coefficient: "
        f"{clustering_coefficient:.3f}"
    )

# MAIN


def main():

    print(
        "Loading students..."
    )

    students = load_students(
        STUDENTS_FILE
    )

    print(
        f"{len(students)} students loaded."
    )

    print(
        "Generating friendships..."
    )

    friendships, graph = (
        generate_friendships(
            students
        )
    )

    save_friendships(
        friendships
    )

    print(
        f"\n{len(friendships)} friendships "
        f"generated successfully."
    )

    print(
        f"Data saved to: "
        f"{OUTPUT_FILE}"
    )

    print_statistics(
        graph
    )


if __name__ == "__main__":
    main()