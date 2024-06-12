# ~~~ This is a template for question 2  ~~~
from copy import copy
from typing import List, Tuple, Union

from utils import compare_arrays, numbers_list_type_checker

# implementation of insertion sort


class InsertionSortImp:
    def __init__(self, given_array: List[Union[int, float]]) -> None:
        """
        This object gets an array of numbers as an input, and sort it according to "Insertion Sort" sorting method.
        The main and the only relevant method for external using is named "run". During the sorting process, there is a
        counting of done basic operations.

        :param given_array: List[Union[int, float]].
        """
        self.given_array = numbers_list_type_checker(given_input=given_array)
        self.operations_counter = 0

    def _insert(
            self, current_checked_number: Union[int, float], current_checked_array: List[Union[int, float]]
    ) -> List[Union[int, float]]:
        """
        This method takes an number and sorted array, and insert the number to the appropriate index in the sorted
        array that the new array will be als sorted as well.

        :param current_checked_number: Union[int, float]. The number that we want to insert.
        :param current_checked_array: List[Union[int, float]]. All the numbers from the left of the current checked
            number in the full array.
        :return: List[Union[int, float]]. Sorted array of the checked number and the checked array.
        """
        # iterate the indexes of the array from the right to the left
        for idx in range(len(current_checked_array) - 1, -1, -1):

            # if checking is a basic operation
            self.operations_counter += 1
            if current_checked_number >= current_checked_array[idx]:

                final_array = (
                        current_checked_array[:idx + 1] + [current_checked_number] + current_checked_array[idx + 1:]
                )
                # switching operation includes two basic operations
                self.operations_counter += 2
                return final_array

        # add a number from the beginning is a basic operation
        self.operations_counter += 1
        return [current_checked_number] + current_checked_array

    def _array_progressing(self, array: List[Union[int, float]]) -> List[Union[int, float]]:
        """
        The main implementation of Insertion Sort method.

        :param array: List[Union[int, float]].
        :return: List[Union[int, float]].
        """
        # created a copied array, to keep the original array as it is.
        copied_array = copy(array)
        # iterate all array's indexes except the first one.
        for idx in range(1, len(array)):
            # get the current checked number and all the numbers from it's left
            current_checked_number, left_array = copied_array[idx], copied_array[:idx]
            # generate one sorted array with the new number
            new_sorted_array = self._insert(
                current_checked_number=current_checked_number, current_checked_array=left_array
            )
            # replace the current number and the sorted array from it's left by the new sorted array with both two.
            # make sure that size of the new array is the appropriate size
            if len(copied_array[:idx + 1]) != len(new_sorted_array):
                raise NotImplementedError(
                    f"original array length: {len(copied_array[:idx + 1])}, new array length: {len(new_sorted_array)}"
                )
            copied_array[:idx + 1] = new_sorted_array

        return copied_array

    def run(self) -> Tuple[List[Union[int, float]], int]:
        """
        :return: The sorted array and the number of the done basic operations.
        """
        sorted_array = self._array_progressing(self.given_array)
        return sorted_array, self.operations_counter


# this function gets a list and uses insertion sort
def insertion_sort_implementation(_input: List[Union[int, float]]) -> Tuple[List[Union[int, float]], int]:
    sorted_array, number_of_basic_operations = InsertionSortImp(given_array=_input).run()
    return sorted_array, number_of_basic_operations


if __name__ == '__main__':

    compare_arrays(total_comparisons=100, array_size=100, sorting_foo=insertion_sort_implementation)