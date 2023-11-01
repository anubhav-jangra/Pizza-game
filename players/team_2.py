from tokenize import String
import numpy as np
from typing import Tuple, List
import constants
from utils import pizza_calculations

class Player:
    def __init__(self, num_toppings, rng: np.random.Generator) -> None:
        """Initialise the player"""
        self.rng = rng
        self.num_toppings = num_toppings
        self.uniform_ = 0
        self.topping_1 = 0
        self.topping_2 = 0
        self.topping_3 = 0
        self.topping_4 = 0
        #print("This is team 2.")

    def customer_gen(self, num_cust, rng = None):
        
        """Function in which we create a distribution of customer preferences

        Args:
            num_cust(int) : the total number of customer preferences you need to create
            rng(int) : A random seed that you can use to generate your customers. You can choose to not pass this, in that case the seed taken will be self.rng

        Returns:
            preferences_total(list) : List of size [num_cust, 2, num_toppings], having all generated customer preferences
        """
        
        preferences_total = []
        if rng==None:
            for i in range(num_cust):
                preferences_1 = self.rng.random((self.num_toppings,))
                preferences_1 = 12*preferences_1/np.sum(preferences_1)
                preferences_2 = self.rng.random((self.num_toppings,))
                preferences_2 = 12*preferences_2/np.sum(preferences_2)
                preferences = [preferences_1, preferences_2]
                equal_prob = self.rng.random()
                if equal_prob <= 0.0:
                    preferences = (np.ones((2,self.num_toppings))*12/self.num_toppings).tolist()
                preferences_total.append(preferences)
        else : 
            for i in range(num_cust):
                preferences_1 = rng.random((self.num_toppings,))
                preferences_1 = 12*preferences_1/np.sum(preferences_1)
                #print("These are the preferences_1 ", preferences_1)
                preferences_2 = rng.random((self.num_toppings,))
                preferences_2 = 12*preferences_2/np.sum(preferences_2)
                #print("These are the preferences_2 ", preferences_2)
                preferences = [preferences_1, preferences_2]
                equal_prob = rng.random()
                if equal_prob <= 0.0:       #change this if you want toppings to show up
                    preferences = (np.ones((2,self.num_toppings))*12/self.num_toppings).tolist()
                preferences_total.append(preferences) 
        #print("These are the preferences #2 ", preferences_total)
        return preferences_total

        


    #def choose_discard(self, cards: list[str], constraints: list[str]):
    def choose_toppings(self, preferences):
        """Function in which we choose position of toppings

        Args:
            num_toppings(int) : the total number of different topics chosen among 2, 3 and 4
            preferences(list) : List of size 100*2*num_toppings for 100 generated preference pairs(actual amounts) of customers.

        Returns:
            pizzas(list) : List of size [10,24,3], where 10 is the pizza id, 24 is the topping id, innermost list of size 3 is [x coordinate of topping center, y coordinate of topping center, topping number of topping(1/2/3/4) (Note that it starts from 1, not 0)]
        """
        #uniform = 0
        count=0
        three_topping_tracker = 0
        four_topping_tracker = 0
        for pair in preferences:
            for array in pair:
                self.uniform_ = self.isUniform(array)
                #print("Is it uniform", self.uniform_, self.isUniform(array))
                count+=1
                #print("this is the array we are dealing with", array, " #", count)
                if self.uniform_==1:
                    break
                else:
                   #print("TOP 1", array[0], 12/len(array))
                    if array[0] > 12/len(array):     
                        self.topping_1+=1
                    if array[1] > 12/len(array):
                        self.topping_2+=1
                    if len(array) > 2:
                        if array[2] > 12/len(array):
                            self.topping_3+=1
                        if len(array) > 3:
                            if array[3] > 12/len(array):
                                self.topping_4+=1
                

        #print("these are the topping stats", self.uniform_, self.topping_1, self.topping_2, self.topping_3, self.topping_4)
        
        x_coords = [np.sin(np.pi/2)]
        pizzas = np.zeros((10, 24, 3))
        type_of_topping = 0
        for j in range(constants.number_of_initial_pizzas):
            pizza_indiv = np.zeros((24,3))
            i = 0
            first_dist = 0
            while i<24:
                
                if self.num_toppings == 2:
                    first_dist = 3
                elif self.num_toppings == 3:
                    first_dist = 3
                else:
                    first_dist = 3 
                #print("This is the distance: ", dist)
                
                angle = i/24*2*np.pi
               # print("This is the angle: ", angle)


                if self.num_toppings == 2: 
                    x = first_dist*np.cos(angle)
                    y = first_dist*np.sin(angle)
                    
                    #print("this is x and y", x , y)
                    if angle < np.pi:
                        type_of_topping = 1
                    else:
                        type_of_topping = 2
                
                if self.num_toppings == 3:
                    x = first_dist*np.cos(angle)
                    y = first_dist*np.sin(angle)
                    
                    #print("this is x and y", x , y)
                    if angle < (2/3*(np.pi)):
                        type_of_topping = 1
                    elif angle >= (2/3*(np.pi)) and angle < (4/3*(np.pi)):
                        type_of_topping = 2
                    else: 
                        type_of_topping = 3


                if self.num_toppings == 4:
                    x = first_dist*np.cos(angle)
                    y = first_dist*np.sin(angle)
                    
                    #print("this is x and y", x , y)
                    if angle < (2/4*(np.pi)):
                        type_of_topping = 1
                    elif angle >= (2/4*(np.pi)) and angle < ((np.pi)):
                        type_of_topping = 2
                    elif angle >= ((np.pi)) and angle < (6/4*(np.pi)):
                        type_of_topping = 3
                    else: 
                        type_of_topping = 4

                


                    # three_topping_tracker+=1
                    # angle = i/16*2*np.pi
                    # x = first_dist*np.cos(angle)
                    # y = first_dist*np.sin(angle)
                    # print("This is the x, y: ", x, y)

                    # if angle < np.pi and three_topping_tracker<17:
                    #     type_of_topping = 1
                    #     print("Getting in: ", x, y)
                    # elif angle >= np.pi and three_topping_tracker<17:
                    #     type_of_topping = 2
                    #     print("Making the circle ", x, y)
                    # else:
                    #     first_dist = 4.5
                    #     angle = ((i%8)+1)/8*2*np.pi
                    #     # if three_topping_tracker<21:
                    #     print("three_topping_tracker: ", three_topping_tracker)
                    #     x = first_dist*np.cos(angle)
                    #     y = first_dist*np.sin(angle)
                    #     type_of_topping = 3
                    #     # else: 
                        #     x = -first_dist*(((three_topping_tracker%4+1)/2)*np.pi)
                        #     y = -(first_dist*(((three_topping_tracker%4+1)/2)*np.pi))

                    

                clash_exists = pizza_calculations.clash_exists(x, y, pizza_indiv, i)
                if not clash_exists:
                    pizza_indiv[i] = [x, y, type_of_topping]
                    i = i+1
                pizza_indiv = np.array(pizza_indiv)
                pizzas[j] = pizza_indiv
        # print("These are the pizzas ", list(pizzas))
        return list(pizzas)
    

    def isUniform(self, array):
        for index in range(len(array)-1):
            if array[index+1]==array[index]:
                self.uniform_+=1
        
        if self.uniform_== len(array)-1:
            return 1
        else:
            return 0



    #def play(self, cards: list[str], constraints: list[str], state: list[str], territory: list[int]) -> Tuple[int, str]:
    def choose_and_cut(self, pizzas, remaining_pizza_ids, customer_amounts):
        """Function which based n current game state returns the distance and angle, the shot must be played

        Args:
            pizzas (list): List of size [10,24,3], where 10 is the pizza id, 24 is the topping id, innermost list of size 3 is [x coordinate of topping, y coordinate of topping, topping number of topping(1/2/3/4)]
            remaining_pizza_ids (list): A list of remaining pizza's ids
            customer_amounts (list): The amounts in which the customer wants their pizza

        Returns:
            Tuple[int, center, first cut angle]: Return the pizza id you choose, the center of the cut in format [x_coord, y_coord] where both are in inches relative of pizza center of radius 6, the angle of the first cut in radians. 
        """
        pizza_id = remaining_pizza_ids[0]
        return  remaining_pizza_ids[0], [0,0], np.pi/8
