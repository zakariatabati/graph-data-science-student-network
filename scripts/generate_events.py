import csv
import random

from faker import Faker


# Configuration
NUMBER_OF_EVENTS = 300
OUTPUT_FILE = "datasets/events.csv"

fake = Faker("fr_FR")


# Event types and their distributions
EVENT_TYPES = [
    "Workshop",
    "Conference",
    "Competition",
    "Seminar",
    "Career",
    "Cultural",
    "Sports",
    "Social",
]

EVENT_WEIGHTS = [
    20, 
    10, 
    15,  
    15,  
    10,  
    10, 
    15,  
    5,   
]


# Realistic event names by category
EVENT_NAMES = {
    "Workshop": [
        "Introduction to Artificial Intelligence",
        "Python Programming Workshop",
        "Web Development Workshop",
        "Cybersecurity Fundamentals",
        "Machine Learning Workshop",
        "Data Science Workshop",
        "Cloud Computing Workshop",
        "Git and GitHub Workshop",
        "Docker Workshop",
        "Public Speaking Workshop",
    ],

    "Conference": [
        "Technology Innovation Conference",
        "Future of Artificial Intelligence",
        "Digital Transformation Conference",
        "Cybersecurity Conference",
        "Software Engineering Conference",
        "Data Science Conference",
        "Sustainable Technology Conference",
        "Future of Education Conference",
    ],

    "Competition": [
        "Hackathon",
        "Programming Contest",
        "Robotics Competition",
        "AI Challenge",
        "Cybersecurity Challenge",
        "Startup Competition",
        "Innovation Challenge",
        "Chess Tournament",
        "Football Tournament",
        "Gaming Tournament",
    ],

    "Seminar": [
        "Introduction to Machine Learning",
        "Software Engineering Best Practices",
        "Cybersecurity Awareness",
        "Artificial Intelligence and Society",
        "Career Development Seminar",
        "Research Methodology Seminar",
        "Entrepreneurship Seminar",
        "Leadership Seminar",
    ],

    "Career": [
        "Career Fair",
        "Tech Companies Recruitment Day",
        "CV and Interview Workshop",
        "Meet the Professionals",
        "Internship Opportunities Day",
        "Job Opportunities Forum",
        "Career in Technology",
    ],

    "Cultural": [
        "Moroccan Culture Day",
        "International Culture Festival",
        "Cultural Exchange Day",
        "World Languages Day",
        "Traditional Arts Exhibition",
        "Heritage Celebration",
    ],

    "Sports": [
        "University Football Tournament",
        "Basketball Tournament",
        "Tennis Tournament",
        "Volleyball Tournament",
        "University Running Challenge",
        "Sports Day",
        "Athletics Competition",
        "Inter-Club Sports Tournament",
    ],

    "Social": [
        "Student Welcome Day",
        "Community Meetup",
        "Charity Event",
        "Volunteer Day",
        "Student Social Night",
        "Community Service Day",
    ],
}


def generate_event_name(event_type):
    """
    Select a realistic event name based on its type.
    """
    return random.choice(EVENT_NAMES[event_type])


def generate_events():
    events = []

    for event_number in range(1, NUMBER_OF_EVENTS + 1):

        event_type = random.choices(
            EVENT_TYPES,
            weights=EVENT_WEIGHTS,
            k=1,
        )[0]

        event = {
            "id": f"event-{event_number:03d}",
            "name": generate_event_name(event_type),
            "date": fake.date_between(
                start_date="-5y",
                end_date="today",
            ),
            "type": event_type,
        }

        events.append(event)

    return events


def save_events_to_csv(events):

    fieldnames = [
        "id",
        "name",
        "date",
        "type",
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
        writer.writerows(events)


def main():

    events = generate_events()

    save_events_to_csv(events)

    print(
        f"{len(events)} events generated successfully."
    )

    print(
        f"Data saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()