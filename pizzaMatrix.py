# Pizza Matrix to help create datbase and ML predictions
class PizzaMatrix:
    
    def __init__(self):
        self.Bredth=0
        self.Depth=0
        
    def set_size(self, bredth, depth):
        # Creates a n amount of pizzas by m amount of toppings matrix
        self.Depth = depth
        self.Bredth = bredth
        self.Matrix = [[0 for x in range(bredth)]for y in range(depth)]
    
    def has_pizza(self, pizza_indx):
        # checks if the the size of matrix has will contain the index number of existing pizza
        if (pizza_indx > self.Depth): return False
        else: return True
    
    def has_ing(self, pizza_indx, ingrd_indx):
        # see's if ingredients in pizza index is set to 1
        if self.Matrix[pizza_indx][ingrd_indx] == 1: return True
        else: return False
    
    def add_ing(self, pizza_indx, ingrd_indx):
        # Takes in pizza index number and ingredients index number sets ingredient to 1
        self.Matrix[pizza_indx][ingrd_indx] = 1
    
    def get_num_ing(self, pizza_indx):
        # Passing a pizzas index number will return the amount of ingredients it has
        count = 0
        for i in range(self.Bredth):
            if self.Matrix[pizza_indx][i] == 1:
                count = count + 1
        return count