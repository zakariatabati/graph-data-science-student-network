import csv
import random
from datetime import date


# Configuration
STUDENTS_FILE = "datasets/students.csv"
EVENTS_FILE = "datasets/events.csv"
OUTPUT_FILE = "datasets/participations.csv"

MIN_EVENTS_PER_STUDENT = 1
MAX_EVENTS_PER_STUDENT = 30


def load_csv(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as file:

        return list(
            csv.DictReader(file)
        )


def generate_feedback():
    """
    Generate a feedback rating between 1 and 5.
    Higher ratings are more likely.
    """

    return random.choices(
        [1, 2, 3, 4, 5],
        weights=[5, 10, 20, 35, 30],
        k=1,
    )[0]


def generate_participations(
    students,
    events,
):

    participations = []

    for student in students:

        inscription_date = date.fromisoformat(
            student["date_inscription"]
        )

        # Keep only events that happened
        # after the student enrolled
        eligible_events = [
            event
            for event in events
            if date.fromisoformat(
                event["date"]
            ) >= inscription_date
        ]

        if not eligible_events:
            continue


        number_of_events = random.randint(
            MIN_EVENTS_PER_STUDENT,
            min(
                MAX_EVENTS_PER_STUDENT,
                len(eligible_events),
            ),
        )

        selected_events = random.sample(
            eligible_events,
            number_of_events,
        )

        for event in selected_events:

            participation = {
                "student_id": student["id"],
                "event_id": event["id"],
                "feedback": generate_feedback(),
            }

            participations.append(
                participation
            )

    return participations


def save_participations(
    participations,
):

    fieldnames = [
        "student_id",
        "event_id",
        "feedback",
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
            participations
        )


def main():

    students = load_csv(
        STUDENTS_FILE
    )

    events = load_csv(
        EVENTS_FILE
    )

    participations = (
        generate_participations(
            students,
            events,
        )
    )

    save_participations(
        participations
    )

    print(
        f"{len(participations)} participations generated."
    )


if __name__ == "__main__":
    main()