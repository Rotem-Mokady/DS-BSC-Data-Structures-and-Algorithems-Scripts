# ~~~ This is a template for question 3  ~~~

# Imports:
from typing import Union, Tuple, List, Dict, Any
import pandas as pd


NUMBER_TYPE = Union[int, float]
OPERATIONS_OUTPUT_TYPE = Union[str, int, Tuple[str, int], Tuple[bool, int]]

# Path for data:
path = 'data.xlsx'


# Implement HashTable class:
class HashTable:
    def __init__(
            self, size=int, hash_function_method=str, collision_handling=str,
            m=int, A=float, m_2=None, A_2=None
    ) -> None:
        # Initiate all the parameter for the hash table.

        if not isinstance(size, int):  # check if  size is an int
            raise ValueError('size should be an int')

        if not isinstance(hash_function_method, str):  # check if  hash_function_method is an str
            raise ValueError('hash_function_method should be an str')
        # make sure that hash_function_method refers to a real method type
        elif hash_function_method not in ("mod", "multiplication"):
            raise ValueError(f'inappropriate hash function method: {hash_function_method}')

        if not isinstance(collision_handling, str):  # check if  collision_handling is an str
            raise ValueError('collision_handling should be an str')
        # make sure that collision_handling refers to a real handling type
        elif collision_handling not in ("Chain", "OA_Quadratic_Probing", "OA_Double_Hashing"):
            raise ValueError(f'inappropriate collision handling: {collision_handling}')

        # check that all m and A params are defined in their correct type

        if not isinstance(m, int):  # check if  m is an int
            raise ValueError('m should be an int')
        if not isinstance(A, (float, int)):  # check if  A is an float
            raise ValueError('A should be an float')

        if m_2 is not None:
            if not isinstance(m_2, int):  # check if  m_2 is an int
                raise ValueError('m_2 should be an int')

        if A_2 is not None:
            if not isinstance(A_2, (float, int)):  # check if  A_2 is an float
                raise ValueError('A_2 should be an float')

        # define all relevant global params

        self.hash_function_method = hash_function_method
        self.collision_handling = collision_handling
        self.size = size
        self.keys = [[] for _ in range(size)]  # Data structure for keys.
        self.data = [[] for _ in range(size)]  # Data structure for values.
        self.m = m
        self.A = A
        self.m_2 = m_2
        self.A_2 = A_2
        self.num_keys = 0

        # Check that all the parameters are given for a specific configuration of the hash table:

        if self.hash_function_method == "multiplication" and self.A == float:
            raise ValueError('Need to define A')
        if self.collision_handling == "OA_Double_Hashing" and self.m_2 == int:
            raise ValueError('Need to define m_2')
        if (
                self.collision_handling == "OA_Double_Hashing" and
                self.hash_function_method == "multiplication" and
                self.A_2 == float
        ):
            raise ValueError('Need to define A_2')

### Part A ###

    def hash_function(self, key: NUMBER_TYPE) -> int:
        """
        Logic of the first hash function, with separation for each chosen hash function method.
        The logic is based on unique m and A global parameters.

        :param key: The given key for hashing manipulation.
        :return: Hash value.
        """
        if self.hash_function_method == "mod":
            return self.m - key % self.m
        elif self.hash_function_method == "multiplication":
            return int(self.m*(key*self.A-int(key*self.A)))

    def hash_function_2(self, key: NUMBER_TYPE) -> int:
        """
        Logic of the second hash function, with separation for each chosen hash function method.
        The logic is based on unique m and A global parameters (different from those of the first hash function).
        The using might be relevant for OA_Double_Hashing implementation.

        :param key: The given key for hashing manipulation.
        :return: Hash value.
        """
        if self.hash_function_method == "mod":
            return self.m_2 - key % self.m_2
        elif self.hash_function_method == "multiplication":
            return int(self.m_2*(key*self.A_2-int(key*self.A_2)))

    def insert(self, key=int, value=str) -> OPERATIONS_OUTPUT_TYPE:
        """
        Logic of insertion operation for a new key and value.

        :param key: The new key.
        :param value: The new value.
        :return: The number of total operations that have been done during the process (int) or a message of a reason
        in case of failure (str).
        """
        # type checkers
        if not isinstance(key, int):  # check if  key is an int
            raise ValueError('key should be an int')
        if not isinstance(value, str):  # check if  str is an int
            raise ValueError('value should be an str')

        # We will use the counter later to create our metric of efficiency.
        counter = 0
        # Get the mapped index based on the chosen hash logic
        place = self.hash_function(key)

        # If we did not have any collision.
        if self.keys[place] == [] or self.keys[place] == [-1]:
            # insert the new key and value to their appropriate index
            self.keys[place] = [key]
            self.data[place] = [value]
            counter += 1

            # we just added another key
            self.num_keys += 1
            return counter

        # Replacing the value if the current key is the only key the connected to the current index
        elif self.keys[place] == [key]:
            self.data[place] = [value]
            counter += 1
            # in that case we did not add any new key
            return counter

        # handling collisions:

        # implement 'Chain' method
        elif self.collision_handling == "Chain":
            counter += 1
            for i in range(len(self.keys[place])):
                counter += 1

                # Replacing the value if the current key is already exists in the linked list
                if self.keys[place][i] == key:
                    self.data[place][i] = value
                    counter += 1
                    # Returns the amount of operations.
                    return counter

            # Using 'Chain'.
            self.keys[place].append(key)
            self.data[place].append(value)
            counter += 1
            self.num_keys += 1

            # Returns the amount of operations.
            return counter

        elif self.collision_handling == "OA_Quadratic_Probing":
            # In open addressing, we can not have more keys then the size of the data structure.
            if self.num_keys == self.size:
                return "Hash Table is full"
            counter += 1

            # start to search for another empty place
            for i in range(1, self.size):
                counter += 1
###Part B###
                new_place = (place + i ** 2) % self.size

                # Replacing the value if the key is the only key the connected to the new index
                if self.keys[new_place] == [key]:
                    self.data[new_place] = [value]
                    # Returns the amount of operations.
                    return counter

                # Using 'OA_Quadratic_Probing' if the new index is free
                elif self.keys[new_place] == [] or self.keys[new_place] == [-1]:
                    self.keys[new_place] = [key]
                    self.data[new_place] = [value]
                    self.num_keys += 1
                    # Returns the amount of operations.
                    return counter

        elif self.collision_handling == "OA_Double_Hashing":
            # In open addressing, we can not have more keys then the size of the data structure.
            if self.num_keys == self.size:
                return "Hash Table is full"
            counter += 1

            for i in range(1, self.size):
                counter += 1
                new_place = (self.hash_function(key) + i * self.hash_function_2(key)) % self.size

                # Replacing the value if the key is the only key the connected to the new index
                if self.keys[new_place] == [key]:
                    self.data[new_place] = [value]
                    # Returns the amount of operations.
                    return counter

                # Using 'OA_Double_Hashing' if the new index is free
                elif self.keys[new_place] == [] or self.keys[new_place] == [-1]:
                    self.keys[new_place] = [key]
                    self.data[new_place] = [value]
                    self.num_keys += 1
                    # Returns the amount of operations.
                    return counter

    def delete(self, key=int) -> OPERATIONS_OUTPUT_TYPE:
        """
        Logic of delete operation for a given key that already exists in the table.

        :param key: The key that we want to remove.
        :return: The number of total operations that have been done during the process (int), a message of a reason
        in case of failure (str) or both of them together (tuple).
        """
        # check if key is an int
        if not isinstance(key, int):
            raise ValueError('key should be an int')

        # We will use the counter later to create our metric of efficiency.
        counter = 0
        # Get the mapped index based on the chosen hash logic
        place = self.hash_function(key)

        # If we did not have any collision.
        if self.keys[place] == [key]:
            # change the status of the key to be free
            self.keys[place] = [-1]
            # delete the data of the chosen key
            del self.data[place]
            counter += 1
            # Update the number of keys in the hash table.
            self.num_keys -= 1
            # Returns the amount of operations.
            return counter

        elif self.collision_handling == "Chain":
            if not self.keys[place]:
                counter += 1
                # Data is not in the Hash Table and there is nothing to delete. Returns the amount of operations.
                return "Data is not in Hash Table", counter

            counter += 1
            # Go over all keys in a specific place in the hash table.
            for i in range(len(self.keys[place])):
                counter += 1
                if self.keys[place][i] == key:
                    # Found and deleted
                    del self.keys[place][i]
                    del self.data[place][i]
                    # Update the number of keys in the hash table.
                    self.num_keys -= 1
                    # Returns the amount of operations.
                    return counter
            # Data is not in the Hash Table and there is nothing to delete. Returns the amount of operations.
            return "Data is not in Hash Table", counter

        elif self.collision_handling == "OA_Quadratic_Probing":
            counter += 1

            # Go over all places the key can be - using OA Quadratic Probing.
            for i in range(1, self.size):
                counter += 1
                new_place = self.hash_function(place + i * i) % self.size

                # If we have an empty slot, this means that we do not have the key in the table.
                if not self.keys[new_place]:
                    break

                if self.keys[new_place] == [key]:
                    # Found and deleted
                    self.keys[new_place] = [-1]
                    # delete the data
                    del self.data[new_place]
                    # Update the number of keys in the hash table.
                    self.num_keys -= 1
                    # Returns the amount of operations.
                    return counter
            # Data is not in the Hash Table and there is nothing to delete. Returns the amount of operations.
            return "Data is not in Hash Table", counter

        elif self.collision_handling == "OA_Double_Hashing":
            counter += 1

            # Go over all places the key can be - using OA Double Hashing.
            for i in range(1, self.size):
                counter += 1

###Part C###
                new_place = (self.hash_function(key) + i * self.hash_function_2(key)) % self.size

                # If we have an empty slot, this means that we do not have the key in the table.
                if self.keys[new_place] == []:
                    break

                if self.keys[new_place] == [key]:
                    # Found and deleted
                    self.keys[new_place] = [-1]
                    # delete the data
                    del self.data[new_place]
                    # Update the number of keys in the hash table.
                    self.num_keys -= 1
                    # Returns the amount of operations.
                    return counter
            # Data is not in Hash Table, Returns the amount of operations.
            return "Data is not in Hash Table", counter

    def member(self, key=int) -> OPERATIONS_OUTPUT_TYPE:
        """
        Logic of member operation for a given key.

        :param key: The key that we want to check about.
        :return: True if the key exists and False if it doesn't, plus the number of total operations that have been done
        during the process (tuple of boolean value and integer value).
        """
        # check if  key is an int
        if not isinstance(key, int):
            raise ValueError('key should be an int')

        # We will use the counter later to create our metric of efficiency.
        counter = 0
        # Get the mapped index based on the chosen hash logic
        place = self.hash_function(key)

        # If we did not have any collision.
        if self.keys[place] == [key]:
            counter += 1
            # Returns True and the amount of operations.
            return True, counter

        elif self.collision_handling == "Chain":
            # if there is no actual data for the given key
            if self.keys[place] == [] or self.keys[place] == [-1]:
                counter += 1
                return False, counter

            # Go over all keys in a specific place in the hash table
            for i in range(len(self.keys[place])):
                counter += 1
                # if the key is in it return True and the amount of operations
                if self.keys[place][i] == key:
                    return True, counter
            # if the key does not exist return False and the amount of operations
            return False, counter

        elif self.collision_handling == "OA_Quadratic_Probing":
            counter += 1

            # Go over all places the key can be - using OA Quadratic Probing,
            for i in range(1, self.size):

                counter += 1
                new_place = self.hash_function(place + i * i) % self.size

                # If we have an empty slot, this means that we do not have the key in the table.
                if not self.keys[new_place]:
                    break
                # if the key is in it return True and the amount of operations,
                if self.keys[new_place] == [key]:
                    return True, counter
            # if the key does not exist return False and the amount of operations
            return False, counter

        elif self.collision_handling == "OA_Double_Hashing":
            counter += 1
            # Go over all places the key can be - using OA Double Hashing
            for i in range(1, self.size):
                counter += 1
                new_place = (self.hash_function(key) + i * self.hash_function_2(key)) % self.size

                # If we have an empty slot, this means that we do not have the key in the table.
                if not self.keys[new_place]:
                    break
                # if the key is in it return True and the amount of operations
                if self.keys[new_place] == [key]:
                    return True, counter
            # if the key does not exist return False and the amount of operations
            return False, counter


class DataSetsHandler:
    def __init__(self, file_path: str) -> None:
        """
        :param file_path: The path of the excel file with the datasets.
        """
        self.file_path = file_path

        # make sure that the file has the correct type
        file_extension = self.file_path.split('.')[-1]
        if file_extension != 'xlsx':
            raise ValueError(f"inappropriate dataset file type, {file_extension}")

        # read all the dataframes
        self.datasets = self._read_excel_to_dict()

    def _read_excel_to_dict(self) -> Dict[str, pd.DataFrame]:
        """
        Read the Excel file into a dictionary of dataframes, when the key is the name of the sheet and the value is the
        table inside the sheet.
        """
        xls = pd.ExcelFile(self.file_path)
        sheets_dict = {
            sheet_name: pd.read_excel(self.file_path, sheet_name=sheet_name)
            for sheet_name in xls.sheet_names
        }
        return sheets_dict

    @property
    def _question_d_conf(self) -> List[Dict[str, Any]]:
        """
        :return: Configuration that based on the demands of question D.
        When using our two hash function methods, it's recommended to choose the size to be equal to the 'm' parameter
        Note that it's actually larger by one because the first index is always 0 and not 1.
        """
        return [
            {
                'hash_function_method': 'mod', 'collision_handling': 'Chain',
                'size': 150, 'm': 149, 'A': -1
            },
            {
                'hash_function_method': 'mod', 'collision_handling': 'OA_Quadratic_Probing',
                'size': 150, 'm': 149, 'A': -1
            },
            {
                'hash_function_method': 'mod', 'collision_handling': 'OA_Double_Hashing',
                'size': 150, 'm': 149, 'm_2': 97, 'A': -1
            },
            {
                'hash_function_method': 'multiplication', 'collision_handling': 'Chain',
                'size': 150, 'm': 149, 'A': 0.589
            },
            {
                'hash_function_method': 'multiplication', 'collision_handling': 'OA_Quadratic_Probing',
                'size': 150, 'm': 149, 'A': 0.589
            },
            {
                'hash_function_method': 'multiplication', 'collision_handling': 'OA_Double_Hashing',
                'size': 150, 'm': 149, 'm_2': 97, 'A': 0.589, 'A_2': 0.405
            }
        ]

    @property
    def _fields_to_role_convertor(self) -> Dict[str, str]:
        """
        Simple mapping between the name of the fields in the datasets and their actual role during the building of the
        Hash table.
        """
        return {'ID': 'key', 'Name': 'value'}

    def _insert_data_to_hash_table(self, df: pd.DataFrame, hash_table: HashTable) -> Tuple[HashTable, int]:
        """
        :param df: The dataset that we want to load into the Hash table.
        :param hash_table: Empty Hash table object.
        :return: Hash table populated with the new data and plus the number of total operations that have been done
        during the process.
        """
        # prepare the data
        records = df.rename(self._fields_to_role_convertor, axis=1).to_dict(orient='records')
        operations_counter = 0
        # insert each records to it's appropriate place
        for record in records:
            current_counter = hash_table.insert(**record)
            # add the number of done operations for the current record to the total number
            if isinstance(current_counter, int):
                operations_counter += current_counter
        # return populated hash table with total operations number
        return hash_table, operations_counter

    def hash_tables_generator(self) -> List[Dict[str, Any]]:
        """
        The main function of the object.
        :return: List with the datasets, their Hash tables and their metadata.
        """
        # go over each one of the dataframes
        final_results = []
        for sheet_name, df in self.datasets.items():
            df_size = len(df)

            # for each dataframe create all the requested hash tables
            for idx, sub_conf in enumerate(self._question_d_conf):
                # create empty hash table
                initialized_hash_table = HashTable(**sub_conf)
                # insert data to hash table
                populated_hash_table, operations_counter = self._insert_data_to_hash_table(
                    df=df, hash_table=initialized_hash_table
                )
                # create final data object of the current sheet and the current hash table
                results = {
                    'sheet_name': sheet_name,
                    'raw_df': df,
                    'size': df_size,
                    'hash_table_index': idx + 1,
                    'hash_table_obj': populated_hash_table,
                    'hash_function_method': populated_hash_table.hash_function_method,
                    'collision_handling': populated_hash_table.collision_handling,
                    'insertion_counted_operations': operations_counter,
                    'insertion_efficiency_value': round(operations_counter / df_size, 3)
                }
                # add it to the final results of all the dataframes with all their hash tables
                final_results.append(results)

        # return the total results
        return final_results

    @property
    def insertion_efficiency_value_necessary_fields(self) -> List[str]:
        # all the relevant fields for question E
        return ['sheet_name', 'size', 'hash_function_method', 'collision_handling',
                'insertion_counted_operations', 'insertion_efficiency_value']


def data_hashing(path: str) -> pd.DataFrame:
    ### Part D ###
    # data handling

    handler = DataSetsHandler(file_path=path)
    hash_tables_with_metadata = handler.hash_tables_generator()

    ### Part E ###
    # create efficiency value table and return it

    results_df = pd.DataFrame(hash_tables_with_metadata)
    relevant_fields = handler.insertion_efficiency_value_necessary_fields

    insertion_efficiency_value_df = results_df[relevant_fields]
    return insertion_efficiency_value_df


if __name__ == '__main__':
    data_hashing(path=path)
