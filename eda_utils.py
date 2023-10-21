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


def is_numeric(series: pd.Series) -> bool:
    """
    This function takes a pandas Series as an argument and returns True if the series data type is numeric (float or int).
    """
    return pd.api.types.is_numeric_dtype(series)


def plot_relation_between_target_and_covariates(
        data: pd.DataFrame,
        target:str, 
        covariates:list[str], 
        ncols:int=3, 
        **kwargs
    ):
    """
    This function takes a pandas DataFrame, a target column name, a list of covariate column names, and an optional number of columns for the plot grid as arguments.
    It then plots scatterplots for numeric covariates and boxplots for categorical covariates, with the target column on the y-axis and each covariate on the x-axis.
    The function returns nothing, but displays the plot.
    """
    nrows = int(np.ceil(len(covariates) / ncols))
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 5*nrows))
    axs = axs.flatten()
    for i, covariate in enumerate(covariates):
        if is_numeric(data[covariate]):
            sns.regplot(x=covariate, y=target, data=data, ax=axs[i], **kwargs)
        else:
            sns.boxplot(x=covariate, y=target, data=data, ax=axs[i], **kwargs)
        axs[i].set_title(f'{target} vs {covariate}')
    plt.tight_layout()
    plt.show()
