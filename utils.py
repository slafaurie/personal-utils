def get_unique_val_col(df):
    """
    Return a dictionary with the names of the columns and the unique values in it
    """
    return {c:df[c].nunique() for c in df.columns}


def add_root(file, root):
    """
    Apend root to path
    """
    return os.path.join(root,file)


def randomize_date_col(df, date_col, max_delta):
    """
    Randomize a date column by a random number defined by delta
    """
    df[f"{date_col}_random"] = df[date_col].apply(lambda x: x - timedelta(days=random.randint(1,max_delta)))
    return df


def coalesce_two_cols(df, cols, new_col=None):
    """
    Perform a SQL-like coalese function for two columns.
    """
    if not new_col:
        new_col = f'{cols[0]}_coalesce'
        
    col1, col2 = cols
    df[new_col] = np.where(df[col1].isnull(), df[col2], df[col1])
    return df