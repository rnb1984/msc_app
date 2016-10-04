import csv

class Pairs:
    
    def __init__(self):
        self.index_a = []
        self.index_b = []
        self.index_ab =[]

        self.BASE_SIZE = 50                             # amount of items that will be compared 
        self.TOTAL_COM = self.BASE_SIZE*self.BASE_SIZE  # total amount of comparisions possible, including with each other, is pizza_index square
        # if pizza_index is 50 the max is 2500
        self.USER_COM = 109                              # total amount of comparisons users will make
    

    def get_index_of_pair(self, left_pair, right_pair):
        # calculating the position a pair is in an index of pairs
        no_of_items_in_index = self.BASE_SIZE
        return (((left_pair * no_of_items_in_index) - no_of_items_in_index)) + right_pair
        
    def get_pairs(self, index_of_pair):
        # returns a pair from the index of all possible pairs in the set
        no_of_items_in_index = self.BASE_SIZE

        # roughly where the pair are in the index
        starting_point_of_pair_set_in_index = index_of_pair / no_of_items_in_index

        right_pair = index_of_pair - starting_point_of_pair_set_in_index * no_of_items_in_index

        if right_pair == no_of_items_in_index: left_pair = starting_point_of_pair_set_in_index
        else: left_pair = starting_point_of_pair_set_in_index + 1
        
        if right_pair == 0:
            right_pair = no_of_items_in_index
            left_pair = starting_point_of_pair_set_in_index
        
        return left_pair, right_pair
    
    def get_dict_comparisions(self):
        # create a dictionary of non matching, orginal pairs
        dict_comparisions = { }

        for i in range(len(self.index_a)):
            # check pair doesn't exist
                pairs = self.get_index_of_pair(self.index_a[i], self.index_b[i])
                dict_comparisions[pairs] = 2 # value of not 0 or 1
                
        return dict_comparisions

