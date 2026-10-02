import fastf1


def get_qualifying_results(input_year: int, race_location: str) -> bool:
    """Fetch and print the full qualifying grid, in Q3/Q2/Q1 order, with
    positions continuing correctly across all three segments."""
    try:
        session = fastf1.get_session(input_year, race_location, "Q")
        session.load()
    except ValueError as e:
        print(f"Could not load qualifying session: {e}")
        return False

    results = session.results

    groups = {
        "Q3": results[results["Q3"].notna()],
        "Q2": results[results["Q2"].notna() & results["Q3"].isna()],
        "Q1": results[results["Q1"].notna() & results["Q2"].isna()],
    }

    position_counter = 1

    for segment_name, group in groups.items():
        if group.empty:
            print(f"----------- {segment_name} ----------- no data -----------\n")
            continue

        group = group.sort_values(segment_name, ascending=True)

        merged = group.merge(
            session.laps[["DriverNumber", "Compound"]].drop_duplicates("DriverNumber"),
            on="DriverNumber",
            how="left",
        )

        seconds_total = merged[segment_name].dt.total_seconds()
        merged[segment_name] = seconds_total.apply(
            lambda s: f"{int(s // 60)}:{s % 60:06.3f}"
        )

        merged["Position"] = range(position_counter, position_counter + len(merged))
        position_counter += len(merged)

        display_df = merged.reindex(
            columns=["Position", "FullName", "TeamName", segment_name, "Compound"]
        )

        print(
            f"----------- {segment_name} ----------- {race_location.upper()} -----------\n",
            display_df,
            "\n",
        )

    return True
