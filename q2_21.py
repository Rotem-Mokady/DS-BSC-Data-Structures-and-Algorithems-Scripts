# ~~~ This is a template for question 2  ~~~
from copy import copy
from typing import List, Tuple

from utils import compare_arrays, integers_list_type_checker

# implementation of insertion sort


class InsertionSortImp:
    def __init__(self, given_array: List[int]) -> None:
        """
        This object gets an array of integers as an input, and sort it according to "Insertion Sort" sorting method.
        The main and the only relevant method for external using is named "run". During the sorting process, there is a
        counting of done basic operations.

        :param given_array: List[int].
        """
        self.given_array = integers_list_type_checker(given_input=given_array)
        self.operations_counter = 0

    def _insert(self, current_checked_integer: int, current_checked_array: List[int]) -> List[int]:
        """
        This method takes an integer and sorted array, and insert the integer to the appropriate index in the sorted
        array that the new array will be als sorted as well.

        :param current_checked_integer: int. The integer that we want to insert.
        :param current_checked_array: List[int]. All the integers on the left of the current checked integer in
            the full array.
        :return: List[int]. Sorted array of the checked integer and the checked array.
        """
        # iterate the indexes of the array from the right to the left
        for idx in range(len(current_checked_array) - 1, -1, -1):

            # if checking is a basic operation
            self.operations_counter += 1
            if current_checked_integer >= current_checked_array[idx]:

                final_array = (
                        current_checked_array[:idx + 1] + [current_checked_integer] + current_checked_array[idx + 1:]
                )
                # switching operation includes two basic operations
                self.operations_counter += 2
                return final_array

        # add an integer from the beginning is a basic operation
        self.operations_counter += 1
        return [current_checked_integer] + current_checked_array

    def _array_progressing(self, array: List[int]) -> List[int]:
        """
        The main implementation of Insertion Sort method.

        :param array: List[int].
        :return: List[int].
        """
        # created a copied array, to keep the original array as it is.
        copied_array = copy(array)
        # iterate all array's indexes except the first one.
        for idx in range(1, len(array)):
            # get the current checked integer and all the integers from it's left
            current_checked_integer, left_array = copied_array[idx], copied_array[:idx]
            # generate one sorted array with the new integer
            new_sorted_array = self._insert(
                current_checked_integer=current_checked_integer, current_checked_array=left_array
            )
            # replace the current integer and the sorted array from it's left by the new sorted array with both two.
            copied_array[:idx + 1] = new_sorted_array

        return copied_array

    def run(self) -> Tuple[List[int], int]:
        """
        :return: The sorted array and the number of the done basic operations.
        """
        sorted_array = self._array_progressing(self.given_array)
        return sorted_array, self.operations_counter


# this function gets a list and uses insertion sort
def insertion_sort_implementation(_input: List[int]) -> Tuple[List[int], int]:
    sorted_array, number_of_basic_operations = InsertionSortImp(given_array=_input).run()
    return sorted_array, number_of_basic_operations


if __name__ == '__main__':

    compare_arrays(total_comparisons=100, array_size=100, sorting_foo=insertion_sort_implementation)