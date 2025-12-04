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
        
        # Upgrade levels
        self.capacity_level = 1
        self.fuel_level = 1
        self.speed_level = 1

        # Upgrade costs
        self.capacity_cost = 100
        self.fuel_cost = 100
        self.speed_cost = 100

        # Max level for each stat
        self.max_level = 10

        # Player credits (money) 
        self.credits = 100
    
    def get_status(self):
        print(f"{self.name} current stats are capacity is {self.capacity}, fuel range is {self.fuel_range} and speed is {self.travel_speed}")
    
    def rename_ship(self, new_name):
        self.name = new_name
        print(f"Ship renamed to {self.name}")    
        
    def upgrade_fuel(self):
        if self.fuel_level >= self.max_level:
            print("Fuel range is already max level!")
            return

        if self.credits < self.fuel_cost:
            print("Not enough credits!")
            return

        # Deduct cost
        self.credits -= self.fuel_cost

        # Upgrade stat
        self.fuel_level += 1
        self.fuel_range += 750

        # Increase next upgrade cost
        self.fuel_cost = int(self.fuel_cost * 1.5)

        print(f"{self.name}'s fuel range upgraded to Level {self.fuel_level}.")
        print(f"New fuel range: {self.fuel_range}")
        print(f"Credits remaining: {self.credits}")
        print(f"Next upgrade cost: {self.fuel_cost}")

    def upgrade_speed(self):
        if self.speed_level >= self.max_level:
            print("Speed is already max level!")
            return

        if self.credits < self.speed_cost:
            print("Not enough credits!")
            return

        self.credits -= self.speed_cost
        self.speed_level += 1
        self.travel_speed += 15
        self.speed_cost = int(self.speed_cost * 1.5)

        print(f"{self.name}'s speed upgraded to Level {self.speed_level}.")
        print(f"New speed: {self.travel_speed}")
        print(f"Credits remaining: {self.credits}")
        print(f"Next speed cost: {self.speed_cost}")

    def upgrade_capacity(self):
        if self.capacity_level >= self.max_level:
            print("Capacity is already max level!")
            return

        if self.credits < self.capacity_cost:
            print("Not enough credits!")
            return

        self.credits -= self.capacity_cost
        self.capacity_level += 1
        self.capacity += 10
        self.capacity_cost = int(self.capacity_cost * 1.5)

        print(f"{self.name}'s capacity upgraded to Level {self.capacity_level}.")
        print(f"New capacity: {self.capacity}")
        print(f"Credits remaining: {self.credits}")
        print(f"Next capacity cost: {self.capacity_cost}")

ship1 = Ship("Hella", 50, 2000, 8000)

ship1.upgrade_capacity()
ship1.upgrade_fuel()
ship1.upgrade_speed()        
ship1.get_status()        
    