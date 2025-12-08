# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 13:05:18 2025

@author: krive
"""

class Ship:
    def __init__(self, name="New Ship", capacity=10, fuel_range=250, travel_speed=5):
        self.name = name
        self.capacity = capacity
        self.fuel_range = fuel_range
        self.travel_speed = travel_speed
        self.ship_cost = capacity * (travel_speed + fuel_range) #TODO Czedrik will need to Balance more
        self.base_cost = self.ship_cost

        # Upgrade levels
        self.capacity_level = 1 
        self.fuel_level = 1
        self.speed_level = 1

        # Upgrade costs
        self.capacity_cost = 100
        self.fuel_cost = 100
        self.speed_cost = 100

        # Max level for each stat
        self.max_level = 3 

        # Player credits (money) 
        self.credits = 100
    
    def get_status(self):
        print(f"{self.name} current stats are capacity is {self.capacity}, fuel range is {self.fuel_range} and speed is {self.travel_speed}")
    
    def rename_ship(self, new_name):
        self.name = new_name
        print(f"Ship renamed to {self.name}")    

    def get_upgrade_percent(self, level):
            if level == 1:
                return 0.25
            elif level == 2:
                return 0.50
            elif level == 3:
                return 1.00

    def get_upgrade_cost(self, level):
        return int(0.65 * self.base_cost * level)
                        
    def upgrade_fuel(self):
        if self.fuel_level >= self.max_level:
            print("Fuel range already maxed!")
            return

        cost = self.get_upgrade_cost(self.fuel_level)
        if self.credits < cost:
            print("Not enough credits!")
            return
        
        # Pay cost
        self.credits -= cost

        # Apply upgrade
        percent = self.get_upgrade_percent(self.fuel_level)
        self.fuel_range = int(self.base_fuel_range * (1 + percent))
        self.fuel_level += 1

        print(f"Fuel upgraded to Level {self.fuel_level-1}")
        print(f"New Fuel Range: {self.fuel_range}")
        print(f"Credits left: {self.credits}")
        print(f"Next upgrade cost: {self.get_upgrade_cost(self.fuel_level) if self.fuel_level <= 3 else 'MAX'}")

    def upgrade_speed(self):
        if self.speed_level >= self.max_level:
            print("Speed already maxed!")
            return

        cost = self.get_upgrade_cost(self.speed_level)
        if self.credits < cost:
            print("Not enough credits!")
            return

        # Pay cost
        self.credits -= cost

        # Apply upgrade
        percent = self.get_upgrade_percent(self.speed_level)
        self.travel_speed = int(self.base_speed * (1 + percent))
        self.speed_level += 1

        print(f"Speed upgraded to Level {self.speed_level-1}")
        print(f"New Speed: {self.travel_speed}")
        print(f"Credits left: {self.credits}")
        print(f"Next upgrade cost: {self.get_upgrade_cost(self.speed_level) if self.speed_level <= 3 else 'MAX'}")

    def upgrade_capacity(self):
        if self.capacity_level >= self.max_level:
            print("Capacity already maxed!")
            return
        
        cost = self.get_upgrade_cost(self.capacity_level)
        if self.credits < cost:
            print("Not enough credits!")
            return

        # Pay cost
        self.credits -= cost

        # Apply upgrade
        percent = self.get_upgrade_percent(self.capacity_level)
        self.capacity = int(self.base_capacity * (1 + percent))
        self.capacity_level += 1

        print(f"Capacity upgraded to Level {self.capacity_level-1}")
        print(f"New Capacity: {self.capacity}")
        print(f"Credits left: {self.credits}")
        print(f"Next upgrade cost: {self.get_upgrade_cost(self.capacity_level) if self.capacity_level <= 3 else 'MAX'}")




Hella = Ship("Hella",  10,   250,  500) # Starter
Omega = Ship("Omega",  50,  500,  1500) # Beginner
Alpha = Ship("Alpha",  200,  1000,  3000) # Intermediate
Sigma = Ship("Sigma",  500,  2000, 6000) # End-game

ship_shop = [Hella, Omega, Alpha, Sigma]
