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

