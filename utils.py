import random
from typing import List, Callable, Any, Union


def numbers_list_type_checker(given_input: Any) -> Union[List[int], None]:
    """
    make sure that the input is a list of numbers only.
    """
    # make sure it's a list
    if not isinstance(given_input, list):
        raise TypeError(f"inappropriate input type: {type(given_input).__name__}")
    # make sure that every element is an integer
    for elem in given_input:
        if not isinstance(elem, (int, float)):
            raise TypeError(f"inappropriate element type: {type(elem).__name__}")

    return given_input


def generate_random_array(length: int) -> List[int]:
    """
    :param length: int. Length of the output array
    :return: List[int]. Array which each one of it's element is a random integer between 1 to 1000.
    """
    return [random.randint(1, 1000) for _ in range(length)]


def compare_arrays(total_comparisons: int, array_size: int, sorting_foo: Callable) -> None:
    """
    The function generates a list of arrays, and sorts each one of them by two different methods:
    1) The built-in function "sorted"
    2) An external function that also sorts an array of integers.
    If the results of the two methods are different from each other, it will show the original random array and the
    output array of the external function implementation.

    :param total_comparisons: int. How many comparisons to do.
    :param array_size: int. The size of each checked array.
    :param sorting_foo: callable. External function that sorts given array of integers.
    """
    # generate data to check
    list_of_arrays = [generate_random_array(array_size) for _ in range(total_comparisons)]

    for arr in list_of_arrays:
        # create the two arrays for the comparison
        default_py_sorting, another_sorting_imp = sorted(arr), sorting_foo(arr)[0]
        # the comparison itself
        if default_py_sorting != another_sorting_imp:
            print(f"""
                {'*' * 50}
                bad sorting implementation.\n
                original array: {arr}.\n
                final results: {another_sorting_imp}.
                {'*' * 50}
            """)
