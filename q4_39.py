# ~~~ This is a template for question 4 (bonus)  ~~~
from copy import copy
from typing import List, Tuple, Union

# implementation of selection sort


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


class SelectionSortImp:
    def __init__(self, given_array: List[Union[int, float]]) -> None:
        """
        This object gets an array of numbers as an input, and sort it according to "Selection Sort" sorting method.
        The main and the only relevant method for external using is named "run". During the sorting process, there is a
        counting of done basic operations.

        :param given_array: List[Union[int, float]].
        """
        self.given_array = numbers_list_type_checker(given_input=given_array)
        self.operations_counter = 0

    def _switch_with_min_value(
            self, current_checked_number: Union[int, float], current_checked_array: List[Union[int, float]]
    ) -> List[Union[int, float]]:
        """
        This function finds the smallest value from the right of a checked number, and if it's smaller than the check
        number, moves it to the first position of the array and replaces the old position of it by the checked number.

        :param current_checked_number: Union[int, float]. The number that we want to switch (if necessary) with the
            smallest value from it's right.
        :param current_checked_array: List[Union[int, float]. All the numbers from the right of the current checked
            number in the full array.
        :return: List[Union[int, float]. The original checked array with the new number in it's appropriate position.
        """
        min_value_idx, min_value = None, None
        # iterate all the numbers from the right of the checked number
        for idx, number in enumerate(current_checked_array):
            # check if the number from the right would be replaced by the checked number, based on the information that
            # we have at this point. it must to be smaller than the checked number and the smallest value that we
            # already found.
            # this if checking includes three sub-checks, so it's actually three basic operations.
            self.operations_counter += 3
            if number < current_checked_number and (min_value is None or number < min_value):
                min_value_idx, min_value = idx, number

        # if-else checking is a basic operation
        self.operations_counter += 1

        if min_value_idx is not None:
            # replace the smallest value that smaller from the checked number with the checked number itself.
            current_checked_array[min_value_idx] = current_checked_number
            # add the smallest value that smaller from the checked number to the left of the array
            final_array = [min_value] + current_checked_array
            # those are twp basic operations
            self.operations_counter += 2

        else:
            # add the current checked number to the left of the array if the switch is not necessary
            final_array = [current_checked_number] + current_checked_array
            # it's a basic operation too
            self.operations_counter += 1

        return final_array

    def _array_progressing(self, array: List[Union[int, float]]) -> List[Union[int, float]]:
        """
        The main implementation of Selection Sort method.

        :param array: List[Union[int, float]].
        :return: List[Union[int, float]].
        """
        # created a copied array, to keep the original array as it is.
        copied_array = copy(array)
        # iterate all array's indexes
        for idx, number in enumerate(array):
            # get the current checked number and all the numbers from it's right
            current_checked_number, left_array = copied_array[idx], copied_array[idx + 1:]
            # generate one array with the new number
            new_sorted_array = self._switch_with_min_value(
                current_checked_number=current_checked_number, current_checked_array=left_array
            )
            # replace the current number and the array from it's right by the new array with both two.
            # make sure that size of the new array is the appropriate size
            if len(copied_array[idx:]) != len(new_sorted_array):
                raise NotImplementedError(
                    f"original array length: {len(copied_array[:idx + 1])}, new array length: {len(new_sorted_array)}"
                )
            copied_array[idx:] = new_sorted_array

        return copied_array

    def run(self) -> Tuple[List[Union[int, float]], int]:
        """
        :return: The sorted array and the number of the done basic operations.
        """
        sorted_array = self._array_progressing(self.given_array)
        return sorted_array, self.operations_counter


# this function gets a list and uses selection sort
def selection_sort_implementation(_input: List[Union[int, float]]) -> Tuple[List[Union[int, float]], int]:
    sorted_array, number_of_basic_operations = SelectionSortImp(given_array=_input).run()
    return sorted_array, number_of_basic_operations


# algorithm sanity check - please ignore

# if __name__ == '__main__':
#
#     from utils import compare_arrays
#
#     compare_arrays(total_comparisons=100, array_size=100, sorting_foo=selection_sort_implementation)

