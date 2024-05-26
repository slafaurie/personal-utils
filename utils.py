import os


def add_root(file, root):
    """
    Apend root to path
    """
    return os.path.join(root,file)

##################

import math 

def convert_int_into_2d_array(data_points, number_of_columns):    
    """
    Take an integer and convert it in a 2d array defined by the number of column. For example:
    10, 2 columns -> [[1,1], [1,2], [2,1], [2,2]....[5,1], [5,2]
    
    """

    numbers_of_rows = math.ceil(data_points / number_of_columns)
    two_dim_array = []
    counter = 1
    for row in range(1,numbers_of_rows+1):
        for col in range(1,number_of_columns+1):
            if counter <= data_points: 
                two_dim_array.append([row, col])
            counter += 1
    return two_dim_array

##################

def chunk_list(data, size):
    """
    Yield successive size chunks from data.
    - Why not return?
    Return would only get you the first slice, while yield make sure to loop over the full list

    - What if the slice is longer than the length? no problem as long as the left index is not ouf of bound.
    Python returns whatever values are left without throwing error.
    """
    for i in range(0, len(data), size):
        yield data[i:i + size]

