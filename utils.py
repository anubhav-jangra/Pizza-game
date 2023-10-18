import numpy as np
import constants
import copy

class pizza_calculations():
    def __init__(self):
        self.num_pizzas = constants.number_of_initial_pizzas
        self.rng = np.random.default_rng(int(9))


    def final_score(self, pizzas, pizza_choices, preferences, cuts, num_toppings, multiplier, x, y):
        #calculate U for all 10 pizzas
        #calculate S for all 10 pizzas
        #self.pizzas[self.pizza_id], self.cuts[self.pizza_id], self.num_toppings, self.multiplier, self.x, self.y 
        B = []
        C = []
        U = []
        obtained_preferences = []
        for i in range(len(preferences)):
            pizza_id = pizza_choices[i]
            obtained_pref = np.array(self.ratio_calculator(pizzas[pizza_id], cuts[pizza_id], num_toppings, multiplier, x, y))
            #Try to fix if theta is 0
            random_pref = np.array(self.ratio_calculator(pizzas[pizza_id], [x, y, self.rng.random()*2*np.pi], num_toppings, multiplier, x, y))
            required_pref = np.array(preferences[i])
            uniform_pref = np.ones((2, num_toppings))*(12/num_toppings)
            b = np.round(np.absolute(required_pref - uniform_pref), 3)
            c = np.round(np.absolute(obtained_pref - required_pref), 3)
            u = np.round(np.absolute(random_pref - uniform_pref), 3)
            B.append(b)
            C.append(c)
            U.append(u)
            obtained_preferences.append(np.round(obtained_pref, 3))
        return B, C, U, obtained_preferences


    
    def ratio_calculator(self, pizza, cut_1, num_toppings, multiplier, x, y):
        cut = copy.deepcopy(cut_1)
        result = np.zeros((2, num_toppings))
        cut[0] = (cut[0]-x)/multiplier
        cut[1] = (cut[1]-y)/multiplier
        center = [cut[0], cut[1]]
        theta  = -cut[2]                #Because y axis is inverted in tkinter window
        for topping_i in pizza:
            top_abs_x = topping_i[0]
            top_abs_y = topping_i[1]
            distance_to_top = np.sqrt((top_abs_x-center[0])**2 + (top_abs_y - center[1])**2)
            theta_edge = np.arctan(0.375 / distance_to_top)
            if top_abs_x == center[0]:
                theta_top = 0
            else:
                theta_top = np.arctan(-(top_abs_y - center[1])/(top_abs_x-center[0]))
            #print(theta, theta_edge, theta_distance, theta_top)
            topping_i[2] = int(topping_i[2])
        
            theta_distance = (theta_top - theta + (np.pi * 10))%(2*np.pi)
            if (theta_edge + theta_distance)*4//np.pi   ==  (-theta_edge + theta_distance)*4//np.pi:
                if (theta_distance*4//np.pi) %2 == 0:
                    result[1][int(topping_i[2]) - 1] = result[1][int(topping_i[2]) - 1] + (np.pi*0.375*0.375)
                else:
                    result[0][int(topping_i[2]) - 1] = result[0][int(topping_i[2]) - 1] + (np.pi*0.375*0.375)
            elif (theta_edge + theta_distance)*4//np.pi ==  (-theta_edge + theta_distance)*4//np.pi + 1:
                if (theta_distance*4//np.pi) %2 == 0:
                    small_angle_theta = min(theta_distance%(np.pi/4), ((30*np.pi)-theta_distance)%(np.pi/4))
                    phi = np.arcsin(distance_to_top*np.sin(small_angle_theta)/0.375)
                    area_smaller = (np.pi/2 - phi - (np.cos(phi)*np.sin(phi)))*0.375*0.375
                    result[1][int(topping_i[2]) - 1] = result[1][int(topping_i[2]) - 1] + (np.pi*0.375*0.375) - area_smaller
                    result[0][int(topping_i[2]) - 1] = result[0][int(topping_i[2]) - 1] + area_smaller
                else:
                    small_angle_theta = min(theta_distance%(np.pi/4), ((30*np.pi)-theta_distance)%(np.pi/4))
                    phi = np.arcsin(distance_to_top*np.sin(small_angle_theta)/0.375)
                    area_smaller = (np.pi/2 - phi - (np.cos(phi)*np.sin(phi)))*0.375*0.375
                    result[1][int(topping_i[2]) - 1] = result[1][int(topping_i[2]) - 1] + area_smaller
                    result[0][int(topping_i[2]) - 1] = result[0][int(topping_i[2]) - 1] + (np.pi*0.375*0.375) - area_smaller
            else:      #If the topping falls in 3 or more regions. Honestly, this probability is so small (Likely one topping at max for a general distribution) that I am assuming the entire area in the maximum sector
                if (theta_distance*4//np.pi) %2 == 0:
                    result[1][int(topping_i[2]) - 1] = result[1][int(topping_i[2]) - 1] + (np.pi*0.375*0.375)
                else:
                    result[0][int(topping_i[2]) - 1] = result[0][int(topping_i[2]) - 1] + (np.pi*0.375*0.375)
        for i in range(num_toppings):
            result[0][i] = result[0][i]/(np.pi*0.375*0.375)
            result[1][i] = result[1][i]/(np.pi*0.375*0.375)
        return result
                    




    def clash_exists(x, y, pizza, topping_id):
        current_pizza = np.array(pizza)
        current_topping = np.array([x, y])
        current_distance = np.linalg.norm(current_topping)
        if current_distance + 0.375 > 6:
            return True
        if topping_id == 0:
            return False
        current_pizza = current_pizza[:topping_id]
        current_pizza = current_pizza[:, :2]
        current_topping = np.array([x, y])
        current_topping = np.tile(current_topping,(current_pizza.shape[0],1))
        distances = np.sqrt(np.sum((current_pizza- current_topping)**2,axis=1))
        min_distance = np.min(distances)
        if min_distance < 0.75:
            return True
        return False