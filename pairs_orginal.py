# Pairs class is to create set of two pairs to be used in the preferances learning algorithm
from random import randint

class Pairs:
    
    def __init__(self):
        self.index_a = []
        self.index_b = []
        self.index_not = []             # index of pairs not to use 
        self.index_train = []
        self.index_sub = []
        self.BASE_SIZE = 50                             # amount of items that will be compared
        self.TOTAL_COM = self.BASE_SIZE*self.BASE_SIZE  # total amount of comparisions possible, including with each other, is pizza_index square
        # if pizza_index is 50 the max is 2500
        self.LIMIT = 2450                               # amount of maxium pairs possible, not including with each other pizza_index square - pizza_index
        self.USER_COM = 20                              # total amount of comparisons users will make
        # if pizza_index is 50 the max is 2450
        self.TRAING_SET = 30            # set the size of pizza training set for the ML training
        self.train_start = 0            # start point of training set
        self.train_end = 0              # end point of training set
        self.TRAIN_SUB = 10             # set the size of a sub set that will be used for more consitancy
        self.train_sub = { }
        self.rounds = 0                 # set the number of rounds to be compared
        self.rounds_coms = []           # number of comparisions per round
        
    def set_num_rounds(self, i):
        # cap the size of the comparisions
        if i > self.LIMIT:
            i == self.LIMIT
        self.rounds = i
    
    def set_com_rounds(self, comparisions):
        i = 0
        for rnd in comparisions:
            # cap the size of rounds
            if rnd > self.LIMIT/self.rounds:
                self.rounds_coms.append(self.LIMIT/self.rounds)
            else: self.rounds_coms.append(rnd)
            i = i +1
    
    def set_train(self, i):
        # choose training set by splitting the index at point a point
        if i > self.TRAING_SET:
            self.train_start = self.TRAING_SET/i
        else:
            self.train_start = i
            
        self.train_end = self.train_start + self.TRAING_SET
        
        if self.train_end > self.BASE_SIZE:
            self.train_start = self.TRAING_SET-self.BASE_SIZE
            self.train_end = self.BASE_SIZE
        
    def set_sub(self):
        # choose sub set from training set
        full = False
        while(full != True):
            if len(self.train_sub) == 10:
                full = True
            item = randint(self.train_start, self.train_end)
            if self.train_sub.has_key(item):
                pass
            else:
                self.train_sub[item] = len(self.train_sub) + 1

        
    def contains_item(self, item, index, start):
        if len(index) < start: return False
        else:
            for i in range(start, len(index)):
                if item == i: return True
        return False
        
    def get_train_item(self):
        # generantes and returns random training item
        return randint(self.train_start, self.train_end)
        
    
    def add_to_index(self,size, comparisions, boo):
        # create a list the size of the comparisions needed from mixed list
        # check if a (true) or b (false)
        if boo == True:
            # select from full training set
            if size == self.TRAING_SET:
                for i in range(1,comparisions+1):
                    item = self.get_train_item()    #item = randint(self.train_start, self.train_end)
                    self.index_a.append(item)
                    #print i, item, '========================================Check this===== for a Full train', boo, ' comparisions: ', comparisions,'size:', size
            # select from smaller training set
            else:
                for i in range(1,comparisions+1):
                    random_i = randint(1, self.TRAIN_SUB)
                    for item in self.train_sub:
                        if self.train_sub[item] == random_i:
                            self.index_a.append(item)
                            #print i, item, '========================================Check this==================== for a small train','a: ', boo, ' comparisions: ', comparisions,'size:', size
        else:
            if size == self.TRAING_SET:
                for i in range(1,comparisions+1):
                    item = self.get_train_item() #item = randint(self.train_start, self.train_end)
                    self.index_b.append(item)
                    #print i, item, '========================================Check this===== for b Full train', boo, ' comparisions: ', comparisions,'size:', size
            else:
                for i in range(1,comparisions+1):
                    random_i = randint(1, self.TRAIN_SUB)
                    j=0
                    #print 'self.train_sub', self.train_sub
                    item_select = False
                    while(item_select == False):
                        for item in self.train_sub:
                            #print i, 'range 1 to ', comparisions, 'in sub the size', len(self.train_sub), j, 'self.train_sub[item] :' ,self.train_sub[item], 'random_i :', random_i
                            if self.train_sub[item] == random_i:
                                self.index_b.append(item)
                                #print i, item, '========================================Check this====================== for b small train','b: ', boo, ' comparisions: ', comparisions,'size:', size
                                item_select = True
                            j = j+1


    def set_pairs(self, r, list_of_com_per_rnd):
        # create pairings for sub set with each other
        self.set_num_rounds(r)
        self.set_com_rounds(list_of_com_per_rnd)
        rnd = 0
        for comparisions in self.rounds_coms:
            # for all rounds with less than 10 use the sub set
            if rnd < 1:
                # set a random range
                # add sub to index a
                self.add_to_index(self.TRAIN_SUB, comparisions, True)
                # add train to index b
                self.add_to_index(self.TRAIN_SUB, comparisions, False)
                
            elif rnd < 3:
                # add train to index a
                self.add_to_index(self.TRAING_SET, comparisions, True)
                
                if rnd == 1:
                    # add train to index b
                    self.add_to_index(self.TRAING_SET, comparisions, False)
                else:
                    # add sub to index b
                    self.add_to_index(self.TRAIN_SUB, comparisions, False)
            else:
                # add train to index a
                self.add_to_index(self.TRAING_SET, comparisions, True)
                # add train to index b
                self.add_to_index(self.TRAING_SET, comparisions, False)
            rnd = rnd+1
    
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
        
        return left_pair, right_pair
        
    def contains_pair(self, poss_index_of_pair):
        # checks to see if index is within the total amount of comparisions posible
        index_size= self.TOTAL_COM
        if poss_index_of_pair > index_size: return False
        else:        return True
        
    def is_pair(self, left_pair, right_pair):
        # checks to see if pairs would be the total amount of comparisions posible
        no_of_items_in_index = self.BASE_SIZE
        index_size= self.TOTAL_COM
        if (left_pair > index_size) or (right_pair > index_size): return False
        elif (left_pair > no_of_items_in_index) or (right_pair > no_of_items_in_index): return False
        else:        return True
    
    def get_orginal_pair(self, exist_pair, dict_comparisions):
        # recursive function to find orginal pair in dict
        if exist_pair in dict_comparisions:
            # pair exists
            left_pair= self.get_train_item()
            right_pair= self.get_train_item()
            new_pair = self.get_index_of_pair(left_pair, right_pair)
            new_pair = self.get_orginal_pair(new_pair, dict_comparisions)
            return new_pair
        else:
            # pair doesn't exist
            return exist_pair
    
    def get_dict_comparisions(self):
        # create a dictionary of non matching, orginal pairs
        dict_comparisions = { }

        for i in range(len(self.index_a)):

            if self.is_pair(self.index_a[i], self.index_b[i]):
                
                if (self.index_a[i] == self.index_b[i]):
                    # get unmatched right
                    while (self.index_a[i] == self.index_b[i]):
                        self.index_b[i] = self.get_train_item()
                    
                # check pair doesn't exist
                pairs = self.get_index_of_pair(self.index_a[i], self.index_b[i])
                pairs = self.get_orginal_pair(pairs,dict_comparisions)
                dict_comparisions[pairs] = 0
            else:
                print 'Pairs are out of range ', self.index_a[i], self.index_b[i], 'are ' , self.is_pair(self.index_a[i], self.index_b[i])
        
        return dict_comparisions
