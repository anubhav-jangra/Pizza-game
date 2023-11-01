import constants
from tokenize import String
from typing import Tuple, List
from utils import pizza_calculations

import numpy as np
from math import pi, sin, cos, tan, sqrt


class Player:
    def __init__(self, num_toppings, rng: np.random.Generator) -> None:
        """Initialise the player"""
        self.rng = rng
        self.num_toppings = num_toppings
        self.BUFFER = 0.001

    def customer_gen(self, num_cust, rng = None):
        
        """Function in which we create a distribution of customer preferences

        Args:
            num_cust(int) : the total number of customer preferences you need to create
            rng(int) : A random seed that you can use to generate your customers. You can choose to not pass this, in that case the seed taken will be self.rng

        Returns:
            preferences_total(list) : List of size [num_cust, 2, num_toppings], having all generated customer preferences
        """
        rng_today = rng if rng else self.rng
        
        def get_person_preferences():
            prefs = list()
            remains = 12.0
            for i in range(self.num_toppings-1):
                p = rng_today.random()
                prefs.append(remains*p)
                remains *= (1-p)
            prefs.append(remains)
            prefs = np.array(prefs)
            rng_today.shuffle(prefs)
            return prefs

        return [[get_person_preferences() for i in range(2)] for j in range(num_cust)]

    def _get_topping_default(self, preferences):
        x_coords = [np.sin(pi/2)]
        pizzas = np.zeros((10, 24, 3))
        for j in range(constants.number_of_initial_pizzas):
            pizza_indiv = np.zeros((24,3))
            i = 0
            while i<24:
                angle = self.rng.random()*2*pi
                dist = self.rng.random()*6
                x = dist*np.cos(angle)
                y = dist*np.sin(angle)
                clash_exists = pizza_calculations.clash_exists(x, y, pizza_indiv, i)
                if not clash_exists:
                    pizza_indiv[i] = [x, y, i%self.num_toppings + 1]
                    i = i+1
            pizza_indiv = np.array(pizza_indiv)
            pizzas[j] = pizza_indiv
        print(pizzas)
        return list(pizzas)

    def _get_topping_2(self, preferences):
        radius = self.BUFFER + 0.375 / sin(pi / 24)
        theta = pi/24
        pizza = [[radius*cos((2*i+1)*theta), radius*sin((2*i+1)*theta), 1+i//12] for i in range(24)]
        return [pizza] * 10

    def _get_topping_3(self, preferences):
        inner_radius = self.BUFFER + 0.375 / sin(pi / 16)
        outer_radius = self.BUFFER + 0.375 / sin(pi / 32)
        return self._get_topping_default(preferences)

    def _get_topping_4(self, preferences):
        inner_radius = self.BUFFER + 0.375 / sin(pi / 12)
        outer_radius = self.BUFFER + 0.375 / sin(pi / 24) # might need to make it bigger to have more flexibility
        return self._get_topping_default(preferences)

    def choose_toppings(self, preferences):
        """Function in which we choose position of toppings

        Args:
            num_toppings(int) : the total number of different topics chosen among 2, 3 and 4
            preferences(list) : List of size 100*2*num_toppings for 100 generated preference pairs(actual amounts) of customers.

        Returns:
            pizzas(list) : List of size [10,24,3], where 10 is the pizza id, 24 is the topping id, innermost list of size 3 is [x coordinate of topping center, y coordinate of topping center, topping number of topping(1/2/3/4) (Note that it starts from 1, not 0)]
        """
        if self.num_toppings == 2:
            return self._get_topping_2(preferences)
        elif self.num_toppings == 3:
            return self._get_topping_3(preferences)
        elif self.num_toppings == 4:
            return self._get_topping_4(preferences)
        else:
            return self._get_topping_default(preferences)


    def _get_cut_default(self, pizzas, remaining_pizza_ids, customer_amounts):
        return remaining_pizza_ids[0], [0,0], np.random.random()*pi
    
    def _get_cut_2(self, pizzas, remaining_pizza_ids, customer_amounts):
        # not considering non-integer cuts
        angle = customer_amounts[0][0]/12 * pi
        radius = 6 - self.BUFFER
        return remaining_pizza_ids[0], [radius*cos(pi+angle), radius*sin(pi+angle)], angle

    def _get_cut_3(self, pizzas, remaining_pizza_ids, customer_amounts):
        return self._get_cut_default(pizzas, remaining_pizza_ids, customer_amounts)

    def _get_cut_4(self, pizzas, remaining_pizza_ids, customer_amounts):
        return self._get_cut_default(pizzas, remaining_pizza_ids, customer_amounts)

    def choose_and_cut(self, pizzas, remaining_pizza_ids, customer_amounts):
        """Function which based n current game state returns the distance and angle, the shot must be played

        Args:
            pizzas (list): List of size [10,24,3], where 10 is the pizza id, 24 is the topping id, innermost list of size 3 is [x coordinate of topping, y coordinate of topping, topping number of topping(1/2/3/4)]
            remaining_pizza_ids (list): A list of remaining pizza's ids
            customer_amounts (list): The amounts in which the customer wants their pizza

        Returns:
            Tuple[int, center, first cut angle]: Return the pizza id you choose, the center of the cut in format [x_coord, y_coord] where both are in inches relative of pizza center of radius 6, the angle of the first cut in radians. 
        """
        if self.num_toppings == 2:
            return self._get_cut_2(pizzas, remaining_pizza_ids, customer_amounts)
        elif self.num_toppings == 3:
            return self._get_cut_3(pizzas, remaining_pizza_ids, customer_amounts)
        elif self.num_toppings == 4:
            return self._get_cut_4(pizzas, remaining_pizza_ids, customer_amounts)
        else:
            return self._get_cut_default(pizzas, remaining_pizza_ids, customer_amounts)
