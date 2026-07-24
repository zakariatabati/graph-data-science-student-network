import csv
import random

from faker import Faker


# Configuration
NUMBER_OF_CLUBS = 70
OUTPUT_FILE = "datasets/clubs.csv"

fake = Faker("en_US")


# Club categories and their distributions
CLUB_CATEGORIES = [
    "Technology",
    "Sports",
    "Culture",
    "Gaming",
    "Social",
    "Entrepreneurship",
    "Arts",
    "Science",
]

CLUB_WEIGHTS = [
    20,  
    20,  
    15,  
    10,  
    10, 
    10,  
    10,  
    5,   
]

CLUB_NAMES = {
    "Technology": [
        "AI & Robotics Club",
        "Coding Club",
        "Cybersecurity Club",
        "Web Development Club",
        "Data Science Club",
        "Software Engineering Club",
        "Open Source Club",
        "IoT Club",
        "Cloud Computing Club",
        "Programming Club",
        "Computer Science Club",
        "Tech Innovation Club",
        "Machine Learning Club",
        "DevOps Club",
    ],

    "Sports": [
        "Football Club",
        "Basketball Club",
        "Tennis Club",
        "Volleyball Club",
        "Running Club",
        "Swimming Club",
        "Athletics Club",
        "Martial Arts Club",
        "Fitness Club",
        "Table Tennis Club",
        "Handball Club",
        "Cycling Club",
        "Badminton Club",
        "Chess Sports Club",
    ],

    "Culture": [
        "Cultural Exchange Club",
        "Moroccan Heritage Club",
        "World Cultures Club",
        "Languages Club",
        "International Students Club",
        "History Club",
        "Cultural Discovery Club",
        "Literature Club",
        "Philosophy Club",
        "Debate & Culture Club",
    ],

    "Gaming": [
        "Gaming Club",
        "Esports Club",
        "Chess Club",
        "Board Games Club",
        "Video Games Club",
        "Strategy Games Club",
        "Game Development Club",
    ],

    "Social": [
        "Social Impact Club",
        "Community Service Club",
        "Volunteering Club",
        "Student Community Club",
        "Charity Club",
        "Social Activities Club",
        "Humanitarian Club",
    ],

    "Entrepreneurship": [
        "Entrepreneurship Club",
        "Startup Club",
        "Business Innovation Club",
        "Young Entrepreneurs Club",
        "Leadership Club",
        "Innovation & Business Club",
        "Future Leaders Club",
    ],

    "Arts": [
        "Music Club",
        "Photography Club",
        "Drama Club",
        "Painting Club",
        "Film Club",
        "Creative Arts Club",
        "Dance Club",
    ],

    "Science": [
        "Science Club",
        "Physics Club",
        "Mathematics Club",
        "Research Club",
        "Astronomy Club",
    ],
}




def generate_clubs():
    clubs = []
    used_names = set()

    while len(clubs) < NUMBER_OF_CLUBS:

        # Select a category according to the defined distribution
        category = random.choices(
            CLUB_CATEGORIES,
            weights=CLUB_WEIGHTS,
            k=1,
        )[0]

        # Select a random name from the category
        club_name = random.choice(CLUB_NAMES[category])

        # Avoid duplicate club names
        if club_name in used_names:
            continue

        club = {
            "id": len(clubs) + 1,
            "nom": club_name,
            "catégorie": category,
            "date_creation": fake.date_between(
                start_date="-5y",
                end_date="today",
            ),
        }

        clubs.append(club)
        used_names.add(club_name)

    return clubs


def save_clubs_to_csv(clubs):

    fieldnames = [
        "id",
        "nom",
        "catégorie",
        "date_creation",
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
        writer.writerows(clubs)


def main():

    clubs = generate_clubs()

    save_clubs_to_csv(clubs)

    print(
        f"{len(clubs)} clubs generated successfully."
    )

    print(
        f"Data saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()