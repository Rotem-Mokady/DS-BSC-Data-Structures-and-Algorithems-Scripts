# ~~~ This is a template for question 1  ~~~

from typing import List, Tuple, Union

# implementation of merge sort


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


class MergeSortImp:
    def __init__(self, given_array: List[Union[int, float]]) -> None:
        """
        This object gets an array of numbers as an input, and sort it according to "Merge Sort" sorting method.
        The main and the only relevant method for external using is named "run". During the sorting process, there is a
        counting of done basic operations.

        :param given_array: List[Union[int, float]].
        """
        self.given_array = numbers_list_type_checker(given_input=given_array)
        self.operations_counter = 0

    def _merge(self, array_a: List[Union[int, float]], array_b: List[Union[int, float]]) -> List[Union[int, float]]:
        """
        This method takes two sorted arrays of numbers and return one sorted array from their elements.
        The sorting process is done according to "Merge" procedure.

        :param array_a: List[Union[int, float]].
        :param array_b: List[Union[int, float]].
        :return: List[Union[int, float]].
        """
        final_result = []

        # stop the transfer process when there is an empty array
        while len(array_a) > 0 and len(array_b) > 0:
            first_element_a, first_element_b = array_a[0], array_b[0]

            # take the minimum value between the two, insert it to the final array
            # and remove it from it's original array
            if first_element_a <= first_element_b:
                min_value, array_a = first_element_a, array_a[1:]
            else:
                min_value, array_b = first_element_b, array_b[1:]

            final_result.append(min_value)
            # three basic operations have been done:
            # 1) if-else conditions
            # 2) remove minimum value from it's original array
            # 3) insert minimum value to the final array
            self.operations_counter += 3

        # concat the left part of the non-empty array to the end of the final array
        # consider the left numbers transfer as operations
        full_array = final_result + array_a + array_b
        self.operations_counter += len(array_a + array_b)

        return full_array

    def _divide_and_conquer(self, array: List[Union[int, float]]) -> List[Union[int, float]]:
        """
        The main recursive implementation of Merge Sort method.

        :param array: List[Union[int, float]].
        :return: List[Union[int, float]].
        """
        # finish the recursion we've got an array of one element for each element of the input.
        # if checking is a basic operation
        self.operations_counter += 1
        if len(array) == 1:
            return array

        # divide the given array to two slices, from the left to the middle and from the middle to the right.
        mid = len(array) // 2
        left_side, right_side = array[:mid], array[mid:]
        array_a, array_b = self._divide_and_conquer(left_side), self._divide_and_conquer(right_side)

        # when we have to sorted arrays, create on sorted array from them by using "merge" procedure
        return self._merge(array_a, array_b)

    def run(self) -> Tuple[List[Union[int, float]], int]:
        """
        :return: The sorted array and the number of the done basic operations.
        """
        sorted_array = self._divide_and_conquer(self.given_array)
        return sorted_array, self.operations_counter


# this function gets a list and uses merge sort
def merge_sort_implementation(_input: List[Union[int, float]]) -> Tuple[List[Union[int, float]], int]:
    sorted_array, number_of_basic_operations = MergeSortImp(given_array=_input).run()
    return sorted_array, number_of_basic_operations


# algorithm sanity check - please ignore

# if __name__ == '__main__':
#
#     from utils import compare_arrays
#
#     compare_arrays(total_comparisons=100, array_size=100, sorting_foo=merge_sort_implementation)

