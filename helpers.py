import random
from typing import List, Callable


def generate_random_array(length: int) -> List[int]:
    return [random.randint(1, 1000) for _ in range(length)]


def compare_arrays(total_comparisons: int, array_size: int, sorting_foo: Callable) -> None:
    list_of_arrays = [generate_random_array(array_size) for _ in range(total_comparisons)]

    for arr in list_of_arrays:
        default_py_sorting, another_sorting_imp = sorted(arr), sorting_foo(arr)[0]

        if default_py_sorting != another_sorting_imp:
            print(f"bad sorting implementation, final results: {another_sorting_imp}")
