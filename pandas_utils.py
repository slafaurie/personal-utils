import pandas as pd
import numpy as np
from datetime import timedelta
from random import random

def normalize_by_colum(data, columns_to_normalize, div_col, sufix= None):
    """
    Divide all selected columns by a single columns and append it to the current dataframe 
    """
    if not sufix:
        sufix = f'per_{div_col}'
    cols_to_add = (
                    data
                    .loc[:, columns_to_normalize]
                    .div(data[div_col], axis = 0)
                    .rename(columns = {x: f'{x}_{sufix}' for x in columns_to_normalize})
                )
    return pd.concat([data, cols_to_add], axis=1)


def lead_window(data, partition_cols, sort_col, value_col, shifts = 1):
    """
    SQL-like lead function
    """
    return (
        data
        .sort_values(by= sort_col, ascending=True)
        .groupby(partition_cols)[value_col]
        .shift(shifts)
    )

def row_number(data, partition_cols, sort_col):
    """
    SQL-like row_number function
    """
    return (
        data
        .sort_values(by= sort_col, ascending=True)
        .groupby(partition_cols)
        .cumcount() + 1
    )

def binarize(ser, step, max_cap = None):
    """
    Transform a continuous series into a discrete one by step bins
    """
    if max_cap:
        ser = ser[ser <= max_cap]
        min_val, max_val = ser.min(), ser.max()
        bins = np.linspace(min_val, max_val, step)
    return pd.cut(ser, bins)

def get_unique_val_col(df):
    """
    Return a dictionary with the names of the columns and the unique values in it
    """
    return {c:df[c].nunique() for c in df.columns}

def coalesce_two_cols(df, cols, new_col=None):
    """
    Perform a SQL-like coalese function for two columns.
    """
    if not new_col:
        new_col = f'{cols[0]}_coalesce'
        
    col1, col2 = cols
    df[new_col] = np.where(df[col1].isnull(), df[col2], df[col1])
    return df

def randomize_date_col(df, date_col, max_delta):
    """
    Randomize a date column by a random number defined by delta
    """
    df[f"{date_col}_random"] = df[date_col].apply(lambda x: x - timedelta(days=random.randint(1,max_delta)))
    return df