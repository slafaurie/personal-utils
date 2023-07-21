from dataclasses import dataclass, asdict
import numpy as np
import pandas as pd

@dataclass
class BootstrapStatistics:
    mean:float
    low_ci:float
    high_ci:float

    def asdict(self):
        return asdict(self)

def get_bootstrap_indexes(n:int, B:int) -> np.ndarray:
    """Creates an array of Bxn where each row represent
    a random number between 0 and n. For the bootstrapp sampling,
    this means that each row is a index value to be used when sampling
    the data

    Args:
        n (int): _description_
        B (int, optional): _description_.
    """
    idx = np.random.randint(0, n, (B, n))
    return idx

def calculate_CIs(means:np.ndarray, CIs:list[int]=[2.5, 97.5]) -> BootstrapStatistics:
    """Calculates the Bootstrapp CIs and mean

    Args:
        means (np.ndarray): _description_
        CIs (list[int], optional): _description_. Defaults to [2.5, 97.5].

    Returns:
        BootstrapStatistics: _description_
    """
    low_ci, high_ci = np.percentile(means, CIs)
    mean = np.mean(means)
    return BootstrapStatistics(mean, low_ci, high_ci)

def vectorized_bootstrap(data:pd.DataFrame, column:str, B:int, CIs:list[int]=[2.5, 97.5]) -> BootstrapStatistics:
    """
    Performs a Bootstrap resampling using Numpy's broadcasting and Advanced Indexing.
    The function calculates the mean of a specific column in the DataFrame 'data' by leveraging
    the vectorized capabilities of Numpy.

    Args:
        data (pd.DataFrame): The input DataFrame containing the data to be resampled.
        column (str): The name of the column in 'data' for which the bootstrap resampling will be performed.
        B (int): The number of bootstrap iterations to perform.
        CIs (list[int], optional): A list of two values representing the lower and upper percentiles
                                   for the confidence interval. Defaults to [2.5, 97.5].

    Returns:
        BootstrapStatistics: An object containing the bootstrap statistics, including the mean and the
                             confidence interval of the mean.

    Description:
        The vectorized_bootstrap function performs a Bootstrap resampling on the specified column of the
        input DataFrame 'data'. The Bootstrap resampling technique is used to estimate the sampling
        distribution of a statistic (in this case, the mean) by repeatedly resampling with replacement
        from the original data. By leveraging Numpy's broadcasting and advanced indexing capabilities,
        the function efficiently calculates the bootstrap mean for the specified number of iterations.

        The 'bootstrap_idx' is an array of shape (B, N), where each row represents an array of random
        indexes drawn with replacement from the original data. The 'values' array is created by repeating
        the column values of 'data' 'B' times, effectively broadcasting the original data into an array
        of shape (B, N). The 'means' array is computed by using advanced indexing to select the values
        from 'values' corresponding to the random indexes in 'bootstrap_idx', and then calculating the
        mean along the axis of the samples.

        Finally, the function calculates the confidence interval for the bootstrap means by using the
        'calculate_CIs' function, which computes the percentiles based on the provided 'CIs' list.

        The result is an object of type 'BootstrapStatistics' containing the bootstrap mean and the
        confidence interval of the mean.
    """
    bootstrap_idx = get_bootstrap_indexes(data.shape[0], B)
    values = np.tile(data[column].values[np.newaxis, :], (B,1))
    means = values[np.arange(B)[:, np.newaxis], bootstrap_idx].mean(axis=1)
    # means = samples.mean(axis=1)
    stats = calculate_CIs(means)
    return stats

def comprehension_list_bootstrap(data:pd.DataFrame, column:str, B:int, CIs:list[int]=[2.5, 97.5]) -> BootstrapStatistics:
    """
    Performs a Bootstrap resampling using list comprehension.
    The function calculates the mean of a specific column in the DataFrame 'data' by using list comprehension
    to iterate through the bootstrap samples.

    Args:
        data (pd.DataFrame): The input DataFrame containing the data to be resampled.
        column (str): The name of the column in 'data' for which the bootstrap resampling will be performed.
        B (int): The number of bootstrap iterations to perform.
        CIs (list[int], optional): A list of two values representing the lower and upper percentiles
                                   for the confidence interval. Defaults to [2.5, 97.5].

    Returns:
        BootstrapStatistics: An object containing the bootstrap statistics, including the mean and the
                             confidence interval of the mean.

    Description:
        The comprehension_list_bootstrap function performs a Bootstrap resampling on the specified column
        of the input DataFrame 'data' by using list comprehension. The Bootstrap resampling technique is
        used to estimate the sampling distribution of a statistic (in this case, the mean) by repeatedly
        resampling with replacement from the original data.

        The 'bootstrap_idx' is an array of shape (B, N), where each row represents an array of random
        indexes drawn with replacement from the original data. The function iterates through 'B' bootstrap
        samples using list comprehension. For each iteration, it selects the values from 'data'
        corresponding to the random indexes in 'bootstrap_idx' and calculates the mean for the specified
        'column'.

        Finally, the function calculates the confidence interval for the bootstrap means by using the
        'calculate_CIs' function, which computes the percentiles based on the provided 'CIs' list.

        The result is an object of type 'BootstrapStatistics' containing the bootstrap mean and the
        confidence interval of the mean.
    """
    bootstrap_idx = get_bootstrap_indexes(data.shape[0], B)
    means = [data.iloc[bootstrap_idx[x]][column].mean() for x in range(B)]
    stats = calculate_CIs(means)
    return stats
