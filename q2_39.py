# ~~~ This is a template for question 2  ~~~

# Imports:

import numpy as np
import pandas as pd

###Part A###
# ~~~  implementation of heap class  ~~~


class Heap:
    def __init__(self):
        # Initialize an empty array to represent the heap and set its size to 0
        self.t = np.array([])
        self.size = 0

    def insert(self, x):
        # Insert a new element into the heap and adjust the heap structure
        self.t = np.append(self.t, x)
        self.size += 1
        self.bubble_up(self.size - 1)

    def delete_min(self):
        # Remove and return the minimum element from the heap
        if self.size == 0:
            return None
        min_elem = self.t[0]
        self.t[0] = self.t[self.size - 1]
        self.t = self.t[:-1]
        self.size -= 1
        self.heapify(0)
        return min_elem

    def bubble_up(self, index):
        # Maintain the heap property by moving the element at the given index up the tree
        parent = (index - 1) // 2
        while index > 0 and self.t[parent] > self.t[index]:
            self.t[parent], self.t[index] = self.t[index], self.t[parent]
            index = parent
            parent = (index - 1) // 2

    def heapify(self, index):
        # Maintain the heap property by moving the element at the given index down the tree
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < self.size and self.t[left] < self.t[smallest]:
            smallest = left
        if right < self.size and self.t[right] < self.t[smallest]:
            smallest = right
        if smallest != index:
            self.t[index], self.t[smallest] = self.t[smallest], self.t[index]
            self.heapify(smallest)

###Part B###


def optimal_value_merge_problem(file_path):
    # Load the company price data from an Excel file
    df = pd.read_excel(file_path, sheet_name='data_1')
    companies = df['buy_me'].values

    # Initialize a minimum heap and insert all company prices into it
    heap = Heap()
    for company in companies:
        heap.insert(company)

    # Continue merging the two smallest companies until all are merged into one
    total_tax = 0
    while heap.size > 1:
        min1 = heap.delete_min()
        min2 = heap.delete_min()
        new_company = min1 + min2
        total_tax += new_company
        heap.insert(new_company)

    return total_tax


file_path = 'data_2.xlsx'
total_tax = optimal_value_merge_problem(file_path)
print(f"The optimal total tax is: {total_tax}")