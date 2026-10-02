from practice import get_top_three_in_practice
from quali import get_qualifying_results
from config import CACHE_DIR

while True:
    race_year = input("Enter the race year (e.g., 2021): ")
    race_location = input("Enter the race location (e.g., Silverstone): ")
    try:
        input_year = int(race_year)
        if input_year < 2018:
            print("Year must be after 2018.")
            continue
    except ValueError:
        print(
            "Invalid race year, must be after 2018. Please check your input and try again."
        )
        continue

    result = get_top_three_in_practice(
        input_year, race_location
    ) and get_qualifying_results(input_year, race_location)

    if result:
        break
