import csv
import random
from datetime import date, timedelta


# Configuration
STUDENTS_FILE = "datasets/students.csv"
CLUBS_FILE = "datasets/clubs.csv"
OUTPUT_FILE = "datasets/memberships.csv"

MIN_MEMBERS_PER_CLUB = 5
MAX_MEMBERS_PER_CLUB = 50

BUREAU_PROBABILITY = 0.10


def load_csv(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as file:

        return list(
            csv.DictReader(file)
        )


def generate_adhesion_date(
    inscription_date,
):

    inscription_date = date.fromisoformat(
        inscription_date
    )

    # A student can join a club from
    # their inscription date onwards.
    #
    # We allow membership until the end
    # of the dataset period.
    end_date = date(
        2026,
        12,
        31,
    )

    # If the student enrolled after the
    # end date, use the inscription date.
    if inscription_date >= end_date:

        return inscription_date

    days_between = (
        end_date - inscription_date
    ).days

    random_days = random.randint(
        0,
        days_between,
    )

    return (
        inscription_date
        + timedelta(
            days=random_days
        )
    )


def generate_memberships(
    students,
    clubs,
):

    memberships = []

    for club in clubs:

        # Guarantee that every club has members
        number_of_members = random.randint(
            MIN_MEMBERS_PER_CLUB,
            MAX_MEMBERS_PER_CLUB,
        )

        selected_students = random.sample(
            students,
            number_of_members,
        )

        # Select students who will be
        # part of the club bureau
        number_of_bureau_members = max(
            1,
            int(
                number_of_members
                * BUREAU_PROBABILITY
            ),
        )

        bureau_students = random.sample(
            selected_students,
            number_of_bureau_members,
        )

        for student in selected_students:

            role = (
                "bureau"
                if student in bureau_students
                else "membre"
            )

            membership = {
                "student_id": student["id"],
                "club_id": club["id"],
                "date_adhesion": generate_adhesion_date(
                    student["date_inscription"]
                ),
                "role": role,
            }

            memberships.append(
                membership
            )

    return memberships


def save_memberships(
    memberships,
):

    fieldnames = [
        "student_id",
        "club_id",
        "date_adhesion",
        "role",
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
            memberships
        )


def main():

    students = load_csv(
        STUDENTS_FILE
    )

    clubs = load_csv(
        CLUBS_FILE
    )

    memberships = generate_memberships(
        students,
        clubs,
    )

    save_memberships(
        memberships
    )

    print(
        f"{len(memberships)} memberships generated."
    )


if __name__ == "__main__":
    main()