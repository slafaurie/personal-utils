def get_time_lags(df: pl.DataFrame, n_lags: list[int]) -> pl.DataFrame:
    """
    
    Description
    
    Generates time-lagged features for the number of pickups. It receives a list with the lags, in hours, to generate. For example:
    - 1 means 1 hour ago
    - 24 -> 24 hours ago
    - 7*24 -> same hour 7 days ago.

    This function takes a DataFrame and an integer n_lags to generate n_lags new columns in the DataFrame. Each new column represents the number of pickups n hours ago, where n ranges from 1 to n_lags. The function sorts the DataFrame by 'pickup_location_id' and 'pickup_datetime_hour' before shifting to ensure that the lagged values are correctly aligned with the corresponding times and locations.

    Parameters:
    - df (pl.DataFrame): The DataFrame containing the pickup data.
    - n_lags (list[int]): The number of lagged time periods to generate.

    Returns:
    - pl.DataFrame: The original DataFrame with n_lags new columns added, each representing the number of pickups n hours ago.
    """
    return (
        df
        .with_columns([
            pl.col("num_pickup").sort_by(["pickup_location_id", "pickup_datetime_hour"]).shift(i).over("pickup_location_id").alias(f"num_pickup_{i}d_ago") for i in n_lags
        ])
        .drop_nulls()
    )
