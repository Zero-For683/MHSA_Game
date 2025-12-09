# -*- coding: utf-8 -*-
"""
Ship Class
"""

class Ship:
    def __init__(self, name: str, capacity: int, fuel_range: int, travel_speed: int):
        self.name = name

        # base values (read_only)
        self.__capacity = capacity
        self.__fuel_range = fuel_range
        self.__travel_speed = travel_speed

        self.capacity = capacity
        self.fuel_range = fuel_range
        self.travel_speed = travel_speed

        

        self.ship_cost = capacity * (travel_speed + fuel_range)
        self.base_cost = self.ship_cost

        # Upgrade levels
        self.capacity_level = 1 
        self.fuel_level = 1
        self.travel_speed_level = 1

        # Max level for each stat
        self.max_level = 3 
    
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
        return int(0.65 * self.ship_cost * level)
                        
    def upgrade_fuel(self):
        if self.fuel_level > self.max_level:
            print("Fuel range already maxed!")
            return

        # Apply upgrade
        percent = self.get_upgrade_percent(self.fuel_level)
        self.fuel_range = int(self.__fuel_range * (1 + percent))
        self.fuel_level += 1

        print(f"Fuel Upgraded to Level {self.fuel_level-1}")
        print(f"New Fuel Range: {self.fuel_range}")
        print(f"Next upgrade cost: ${self.get_upgrade_cost(self.fuel_level) if self.fuel_level <= 3 else 'MAX':,.2f}")

    def upgrade_speed(self):
        if self.travel_speed_level > self.max_level:
            print("Speed already maxed!")
            return

        # Apply upgrade
        percent = self.get_upgrade_percent(self.travel_speed_level)
        self.travel_speed = int(self.__travel_speed * (1 + percent))
        self.travel_speed_level += 1

        print(f"Speed Upgraded to Level {self.travel_speed_level-1}")
        print(f"New Speed: {self.travel_speed}")
        print(f"Next upgrade cost: ${self.get_upgrade_cost(self.travel_speed_level) if self.travel_speed_level <= 3 else 'MAX':,.2f}")

    def upgrade_capacity(self):
        if self.capacity_level > self.max_level:
            print("Capacity already maxed!")
            return
        # Apply upgrade
        percent = self.get_upgrade_percent(self.capacity_level)
        self.capacity = int(self.__capacity * (1 + percent))
        self.capacity_level += 1

        print(f"Capacity Upgraded to Level {self.capacity_level-1}")
        print(f"New Capacity: {self.capacity}")
        print(f"Next upgrade cost: ${self.get_upgrade_cost(self.capacity_level) if self.capacity_level <= 3 else 'MAX':,.2f}")




Hella = Ship("Hella",  20,  300,  575) # Starter
Omega = Ship("Omega",  50,  575,  850) # Beginner
Alpha = Ship("Alpha",  200,  1250,  2500) # Intermediate
Sigma = Ship("Sigma",  500,  2000, 6000) # End-game

ship_shop = [Hella, Omega, Alpha, Sigma]
