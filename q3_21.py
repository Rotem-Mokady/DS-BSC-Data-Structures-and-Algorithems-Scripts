# ~~~ This is a template for question 3  ~~~

# imports

from typing import Dict, List, Union, Optional
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from q1_21 import merge_sort_implementation
from q2_21 import insertion_sort_implementation

# functions


def _convert_df_to_numbers_array(df: pd.DataFrame) -> List[Union[int, float]]:
    """
    Parse raw data to the sorting function's expected input format.
    """
    if len(df.columns) != 1:
        raise NotImplemented("the dataframe must include only one field.")

    field_name = df.columns[0]
    numbers_list = df[field_name].tolist()

    return numbers_list


def read_excel_to_dict(path: str) -> Dict[str, List[Union[int, float]]]:
    """
    Read the Excel file into a dictionary of dataframes.
    """
    xls = pd.ExcelFile(path)
    sheets_dict = {
        sheet_name: _convert_df_to_numbers_array(pd.read_excel(path, sheet_name=sheet_name))
        for sheet_name in xls.sheet_names
    }
    return sheets_dict


def _sort_array_by_all_methods(
        array: List[Union[int, float]], label: Optional[str] = 'given array'
) -> Dict[str, Union[str, int]]:
    """
    The function gets an array of numbers and sorts it with two different algorithm - Merge Sort and Insertion Sort.
    The function returns the number of the done basic operations of each algorithm process.

    :param array: List[Union[int, float]]. An array of numbers.
    :param label: Optional[str], default "given array". The name of the given array.
    :return: dict. Includes three key -> value couples:
        1) label -> label.
        2) merge_sort -> operations counter results of the Merge Sort implementation.
        3) insertion_sort -> operations counter results of the Insertion Sort implementation.
    """
    _, merge_sort_basic_operations = merge_sort_implementation(_input=array)
    _, insertion_sort_basic_operations = insertion_sort_implementation(_input=array)

    results = {
        'label': label,
        'merge_sort_counter': merge_sort_basic_operations,
        'insertion_sort_counter': insertion_sort_basic_operations
    }
    return results


def main(raw_arrays_data: Dict[str, List[Union[int, float]]]) -> pd.DataFrame:
    """
    The main and the only relevant function for the comparison between Merge Sort Algorithm and Insertion Sort
    Algorithm.

    :param raw_arrays_data: Dict[str, List[Union[int, float]]].
        Dictionary of the datasets, when the key is the dataset's name and the value it's the array of numbers itself.

    :return: dataframe. Three fields:
        1) dataset name.
        2) number of operations for Merge Sort implementation.
        3) number of operations for Insertion Sort implementation.
    """
    results = [_sort_array_by_all_methods(array=array, label=label) for label, array in raw_arrays_data.items()]
    df = pd.DataFrame(results)

    return df


# load data:

raw_data = read_excel_to_dict(path="data.xlsx")

# sort data and save results:

final_results = main(raw_arrays_data=raw_data)

# merge_sort:

merge_sort_final_results = final_results.drop(columns='insertion_sort_counter')

# insertion sort:

insertion_sort_final_results = final_results.drop(columns='merge_sort_counter')

# plot figure:

# define basic settings
plt.figure(figsize=(10, 6))

bar_width = 0.35
x_indices = np.arange(len(final_results['label']))

# plotting bars for Merge Sort and Insertion Sort
plt.bar(x_indices - bar_width/2, final_results['merge_sort_counter'], width=bar_width,
        color='blue', label='Merge Sort')
plt.bar(x_indices + bar_width/2, final_results['insertion_sort_counter'], width=bar_width,
        color='orange', label='Insertion Sort')

# adding labels and title
plt.xlabel('Dataset Name')
plt.ylabel('Number of Basic Operations')
plt.title('Number of Basic Operations by each Algorithm during the Sorting Process')
plt.legend()

# setting x-axis ticks and rotating x-axis labels for better readability
plt.xticks(x_indices, final_results['label'])
plt.xticks(rotation=45)

# show plot
plt.tight_layout()
plt.show()



