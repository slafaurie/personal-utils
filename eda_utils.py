def check_nulls(df:pd.DataFrame, selected_cols: list[str], threshold: float = 0.05) -> list[str]:
    """Checks for problematic nulls in the selected columns and all the columns.

    Returns a list of columns with nulls over the threshold.
    """
    for col in selected_cols:
        print(f'Column: {col}')
        print(df[col].isnull().mean())
        print('-------------------')

    columns_with_nulls_over_threshold = (
        df
        .isnull()
        .mean()
        .gt(threshold)
        .loc[lambda x: x]
        .index
        .tolist()
    )

    print(f"Rows with more than {threshold:.0%} nulls")
    print(df[columns_with_nulls_over_threshold].isnull().mean())
    print('-------------------')

    return columns_with_nulls_over_threshold
