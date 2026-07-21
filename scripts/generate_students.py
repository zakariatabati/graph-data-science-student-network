import csv
import random
from datetime import date

from faker import Faker


# Configuration
NUMBER_OF_STUDENTS = 1500
OUTPUT_FILE = "datasets/students.csv"
CURRENT_YEAR = 2026

# Faker instance
fake = Faker("fr_FR")


# Fields of study and their distributions
FIELDS_OF_STUDY = [
    "Software Engineering",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Industrial Engineering",
    "Networking Engineering",
    "Other",
]

FIELD_WEIGHTS = [
    20,  
    15, 
    12,  
    13,  
    10,  
    30,  
]


def generate_inscription_date(academic_year):
    """
    Generate a realistic inscription date between August and October
    of the given academic year.
    """

    start_date = date(academic_year, 8, 1)
    end_date = date(academic_year, 10, 31)

    return fake.date_between(
        start_date=start_date,
        end_date=end_date,
    )


def generate_students():
    students = []

    for student_id in range(1, NUMBER_OF_STUDENTS + 1):

        student_year = random.randint(1, 5)

        # Some students may have repeated one or more years
        repeated_years = random.choices(
            [0, 1, 2],
            weights=[80, 15, 5],
            k=1,
        )[0]

        inscription_year = (
            CURRENT_YEAR
            - (student_year - 1)
            - repeated_years
        )

        inscription_date = generate_inscription_date(
            inscription_year
        )

        # Generate the student
        student = {
            "id": student_id,
            "nom": fake.last_name() + " " + fake.first_name(),
            "email": fake.email(),
            "filière": random.choices(
                FIELDS_OF_STUDY,
                weights=FIELD_WEIGHTS,
                k=1,
            )[0],
            "année": student_year,
            "date_inscription": inscription_date,
        }

        students.append(student)

    return students


def save_students_to_csv(students):

    fieldnames = [
        "id",
        "nom",
        "email",
        "filière",
        "année",
        "date_inscription",
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
        writer.writerows(students)


def main():

    students = generate_students()

    save_students_to_csv(students)

    print(
        f"{len(students)} students generated successfully."
    )

    print(
        f"Data saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()