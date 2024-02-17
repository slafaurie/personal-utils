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
    Additionally, for numeric covariates, it annotates the plot with the Pearson correlation value between the target and the covariate.
    The function returns nothing, but displays the plot.
    """
    nrows = int(np.ceil(len(covariates) / ncols))
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 5*nrows))
    axs = axs.flatten()
    for i, covariate in enumerate(covariates):
        if is_numeric(data[covariate]):
            sns.regplot(x=covariate, y=target, data=data, ax=axs[i], **kwargs)
            # Calculate and annotate Pearson correlation
            correlation = data[[covariate, target]].corr().iloc[0,1]
            axs[i].annotate(
                f'Pearson: {correlation:.2f}'
                , xy=(0.05, 0.95)
                , xycoords='axes fraction'
                , ha='left'
                , va='top'
                , fontsize=10
                , bbox=dict(boxstyle="round", alpha=0.5, color="w")
            )
        else:
            sns.boxplot(x=covariate, y=target, data=data, ax=axs[i], **kwargs)
        axs[i].set_title(f'{target} vs {covariate}')
    plt.tight_layout()
    plt.show()

def plot_categories(df:pd.DataFrame, plot_func: callable, x:str, y:str, hue:str, color:str = "grey") -> None:
    """Create a plot for each category in hue. The value of this function
    is that the color is the same for each category. This is meant to be
    used as a background plot for a plot that will be plotted on top of it.

    Args:
        df (pd.DataFrame): _description_
        plot_func (callable): _description_
        x (str): _description_
        y (str): _description_
        hue (str): _description_
        color (str, optional): _description_. Defaults to "grey".
    """
    unique_values = df[hue].unique()
    palette_dict = {value: color for value in unique_values}
    plot_func(
        x=x,
        y=y,
        hue=hue,
        data=df,
        palette=palette_dict,
        legend=False
    )
    plt.show()
