import fastf1


def reorder(session):
    fastest_lap = session.laps.loc[
        session.laps.groupby("Driver")["LapTime"].idxmin(),
        ["DriverNumber", "LapTime", "Compound", "Team"],
    ]

    sorted_fastest = fastest_lap.sort_values("LapTime", ascending=True)

    top3_fastest_laps = sorted_fastest.head(3).merge(
        session.results[["FullName", "DriverNumber"]], on="DriverNumber"
    )
    seconds_total = top3_fastest_laps["LapTime"].dt.total_seconds()
    top3_fastest_laps["LapTime"] = seconds_total.apply(
        lambda s: f"{int(s // 60)}:{s % 60:06.3f}"
    )

    reordered_df = top3_fastest_laps.reindex(
        columns=["FullName", "Team", "LapTime", "Compound"]
    )
    return reordered_df


def get_top_three_in_practice(input_year: int, race_location: str):
    event = fastf1.get_event(input_year, race_location)

    if event["EventFormat"] == "conventional":
        sessions = ["FP1", "FP2", "FP3"]
    elif event["EventFormat"] == "sprint":
        sessions = ["Practice 1", "Practice 2"]
    else:
        print(f"Unrecognised event format: {event['EventFormat']}")
        return False

    try:
        for session_name in sessions:
            session = fastf1.get_session(input_year, race_location, session_name)
            session.load()

            reordered_df = reorder(session)

            print(
                f"----------- {session_name} ----------- {race_location.upper()} -----------\n",
                reordered_df,
                "\n",
            )

        if event["EventFormat"] == "sprint":
            print(
                f"------- NO FP3 - Sprint Weekend ------- {race_location.upper()} -------\n"
            )

    except ValueError:
        print("Input valid year")
        return False
    return True
