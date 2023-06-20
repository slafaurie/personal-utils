import matplotlib.pyplot as plt
from dataclasses import dataclass
import pandas as pd


@dataclass
class Chart:
    callabe: plt.Axes
    args: dict[str, any]

def get_n_rows(n_columns:int, total_items:int):
    """Generates the number of rows for a given number of columns and total items.
    For example, if you have 10 items and want to display them in 3 columns, you will need 4 rows.
    Args:
        n_columns (int): _description_
        total_items (int): _description_

    Returns:
        _type_: _description_
    """
    n_rows = int(total_items / n_columns)
    if total_items % n_columns != 0:
        n_rows += 1
    return n_rows


def make_subplots(charts: list[Chart], data: pd.DataFrame, columns: list[str], n_columns:int=2, **kwargs):
    """Generates small multiples for a given list of charts and columns.
    Args:
        charts (list[Chart]): A chart is a dataclass with a callable and a dict of args. The callable is a
        plt.Axes type, therefore, it supports Seaborn and Matplotlib charts. The args are the arguments
        that will be passed to the callable to customize the chart.
        
        data (pd.DataFrame): _description_
        columns (list[str]): _description_
        n_columns (int, optional): _description_. Defaults to 2.
    """
    n_rows = get_n_rows(n_columns, len(columns))
    f, axs = plt.subplots(n_rows, n_columns, **kwargs)
    axs = axs.flatten()
    for i, kpi in enumerate(columns):
        for chart in charts:
            chart.callabe(data=data, x=kpi, ax=axs[i], **chart.args)
        axs[i].set_title(kpi)
        axs[i].set_xlabel("")
        
        
 
histplot_args = Chart(sns.histplot, {"bins": 10, "kde": True})
rugplot_args = Chart(sns.rugplot, {"color": "red", "height": 0.1, "alpha": 0.5})
kpis = ["avg_weekly_gfv", "avg_weekly_frequency", "avg_weekly_incentivized_rate", "avg_weekly_incentives", "avg_weekly_customer_fees"]
make_subplots([histplot_args, rugplot_args], gp_db, kpis, n_columns=2, figsize=(15, 20))
