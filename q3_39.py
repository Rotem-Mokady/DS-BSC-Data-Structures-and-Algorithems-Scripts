# ~~~ This is a template for question 3  ~~~

# Imports:
from typing import Union, Tuple


NUMBER_TYPE = Union[int, float]
OPERATION_OUTPUT_TYPE = Union[str, int, Tuple[str, int]]

# Path for data:
path = 'Write here the file path, and use is later'


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
        elif collision_handling not in ("Chain", "OA_Double_Hashing", "OA_Quadratic_Probing"):
            raise ValueError(f'inappropriate collision handling: {collision_handling}')

        # check the all m and A params are defined in their correct type

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

        # define all relevant params

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

    def hash_function(self, key: NUMBER_TYPE) -> Union[NUMBER_TYPE, None]:
        """
        Logic of the first hash function, with separation for each chosen hash function method.
        The logic is based on unique m and A global parameters.

        :param key: The given key for hashing manipulation.
        :return: The hash value
        """
        if self.hash_function_method == "mod":
            return self.m - key % self.m
        elif self.hash_function_method == "multiplication":
            return int(self.m*(key*self.A-int(key*self.A)))

    def hash_function_2(self, key: NUMBER_TYPE) -> Union[NUMBER_TYPE, None]:
        """
        Logic of the second hash function, with separation for each chosen hash function method.
        The logic is based on unique m and A global parameters (different from those of the first hash function).
        The using might be relevant for OA_Double_Hashing implementation.

        :param key: The given key for hashing manipulation.
        :return: The hash value
        """
        if self.hash_function_method == "mod":
            return self.m_2 - key % self.m_2
        elif self.hash_function_method == "multiplication":
            return int(self.m_2*(key*self.A_2-int(key*self.A_2)))

    def insert(self, key=int, value=str) -> OPERATION_OUTPUT_TYPE:
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
            # TODO: why are we skipping the first index (0)?
            for i in range(1, len(self.keys[place])):
                counter += 1

                # Replacing the value if the current key is already exists in the linked list
                if self.keys[place][i] == key:
                    self.data[place][i] = value
                    # TODO: why are we adding another key if it's already exists?
                    self.num_keys += 1
                    # Returns the amount of operations.
                    return counter

            # Using 'Chain'.
            # TODO: shouldn't we add 1 to the counter here?
            self.keys[place].append(key)
            self.data[place].append(value)
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
                new_place = (self.hash_function(key) + i * self.hash_function_2(key)) % self.m

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

    def delete(self, key=int) -> OPERATION_OUTPUT_TYPE:
        """
        Logic of delete operation for a given key that already exists in the table.

        :param key: The key that we want to remove from the table.
        :return: The number of total operations that have been done during the process (int) or a message of a reason
        in case of failure (str).
        """
        # check if key is an int
        if not isinstance(key, int):
            raise ValueError('key should be an int')

        # We will use the counter later to create our metric of efficiency.
        counter = 0
        # Get the mapped index based on the chosen hash logic
        place = self.hash_function(key)

        if self.keys[place] == [key]:
            self.keys[place] == [-1]
            del self.data[place]
            counter += 1                                #If we did not have any collision.
            self.num_keys -= 1                          #Update the number of keys in the hash table.
            return counter                              #Returns the amount of operations.

        elif self.collision_handling == "Chain":
            if self.keys[place] == []:
                counter += 1
                return "Data is not in Hash Table", counter  #Data is not in Hash Table, Returns the amount of operations.
            counter+=1
            for i in range(1,len(self.keys[place])):
                counter += 1
                if self.keys[place][i] == key:
                    del self.keys[i]                   #Go over all keys in a specific place in the hash table.
                    del self.data[place][i]
                    self.num_keys -= 1                 #Update the number of keys in the hash table.
                    return counter                     #Found and deleted, Returns the amount of operations.
            return "Data is not in Hash Table",counter #Data is not in Hash Table, Returns the amount of operations.

        elif self.collision_handling == "OA_Quadratic_Probing":
            counter+=1
            for i in range(1, self.size):
                counter += 1
                new_place = self.hash_function(place + i * i)
                if self.keys[new_place] == []:              #If we have an empty slot, this means that we do not have the key in the table.
                    break
                if self.keys[new_place] == [key]:
                    self.keys[new_place]=-1
                    del self.data[new_place]                #Go over all places the key can be - using OA Quadratic Probing.
                    self.num_keys -= 1                      #Update the number of keys in the hash table.
                    return counter                          #Found and deleted, Returns the amount of operations.
            return "Data is not in Hash Table",counter      #Data is not in Hash Table, Returns the amount of operations.

        elif self.collision_handling == "OA_Double_Hashing":
            counter+=1
            for i in range(1, self.size):
                counter += 1

###Part C###
                new_place = '----Replace Me------'

                if self.keys[new_place] == []:              #If we have an empty slot, this means that we do not have the key in the table.
                    break
                if self.keys[new_place] == [key]:
                    self.keys[new_place]=-1                #Go over all places the key can be - using OA Double Hashing.
                    del self.data[new_place]
                    self.num_keys -= 1                      #Update the number of keys in the hash table.
                    return counter                          #Found and deleted, Returns the amount of operations.
            return "Data is not in Hash Table"  ,counter    #Data is not in Hash Table, Returns the amount of operations.

    def member(self, key=int):
        if not isinstance(key, (int)):  # check if  key is an int
            raise ValueError('key should be an int')

        counter = 0                                         #We will use the counter later to create our metric of efficiency.
        place = self.hash_function(key)
        if self.keys[place] == [key]:                       #If we did not have any collision.
            counter += 1
            return True, counter                            #Returns True and the amount of operations.

        elif self.collision_handling == "Chain":
            if self.keys[place] == [] or self.keys[place] == [-1] :
                counter += 1
                return False, counter                       #Go over all keys in a specific place in the hash table,
                                                            #if the key is in it return True and the amount of operations,
            counter+=1                                      #elsr False and the amount of operations
            for i in range(1,len(self.keys[place])):
                counter += 1
                if self.keys[place][i] == key:
                    return True,counter
            return False,counter

        elif self.collision_handling == "OA_Quadratic_Probing":
            counter+=1
            for i in range(1, self.size):

                counter += 1                                    #Go over all places the key can be - using OA Quadratic Probing,
                new_place = self.hash_function(place + i * i)   #if the key is in it return True and the amount of operations,
                if self.keys[new_place] == []:                  #If we have an empty slot, this means that we do not have the key in the table.
                    break
                if self.keys[new_place] == [key]:               #else False and the amount of operations.
                    return True,counter
            return False,counter

        elif self.collision_handling == "OA_Double_Hashing":
            counter+=1
            for i in range(1, self.size):                                                          #Go over all places the key can be - using OA Double Hashing,
                counter += 1                                                                       #if the key is in it return True and the amount of operations,
                new_place = (self.hash_function(key) + i * self.hash_function_2(key)) % self.m     #else False and the amount of operations.
                if self.keys[new_place] == []:                                                     #If we have an empty slot, this means that we do not have the key in the table.
                    break
                if self.keys[new_place] == [key]:
                    return True,counter
            return False,counter

def data_hashing(path):
    ###Part D###
    #data handling
    pass
    ###Part E###
    #efficiency value
    pass