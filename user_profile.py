'''
3. Build a "Profile" class that will update as you get more "reputation" (more reputation == more tourists on each expidition)
We can try saving this to a file so we can save game-state
name, rep, current money, ship assigned, default tourist count.


attributes: profile name, reputation, tourist count, current ship, money
'''

import math
import random
from ship import Ship
from enum import Enum

class Profile:
    class Reputation_Tier(Enum):
        """Rep Tier RNG Min,Max Range to determine # tourists attracted to a ship's capacity"""
        LOW = (10, 40) #25% average
        MEDIUM = (30, 75) #50% average
        HIGH = (50, 100) #75% average

        @property
        def min_rng(self):
            return self.value[0]
        
        @property
        def max_rng(self):
            return self.value[1]
        

    def __init__(self, name: str, reputation: float, tourists: int,
                 ship: Ship | None, money: int) -> None:
        self.name = name
        self.reputation = reputation
        self.tourists = tourists
        self.money = money

        # initialize ships list correctly
        self.ships: list[Ship] = []
        if ship is not None:
            self.ships.append(ship)

    def buy_ship(self, ship: Ship) -> bool:
        """Try to buy a ship using this profile's credits."""
        cost = ship.ship_cost

        if self.money < cost:
            print(f"Not enough credits to buy {ship.name}. "
                  f"Cost: {cost}, you have: {self.money}")
            return False

        self.money -= cost

        if not hasattr(self, "ships"):
            self.ships = []
        self.ships.append(ship)

        print(f"\nPurchased {ship.name} for ${cost:,.2f}")
        print(f"Remaining Credits: ${self.money:,.2f}\n")
        return True
    
    
    def get_reputation_level(self):
        """Reputation Level: High = 70~100% , Medium = 25~69%, Low <24%"""
        if (self.reputation > 70):
            return self.Reputation_Tier.HIGH
        elif (self.reputation >= 25 and self.reputation <= 69):
            return self.Reputation_Tier.MEDIUM
        else:
            return self.Reputation_Tier.LOW
        
    def increase_reputation(self, tourist_count):
        """reputation increases based on number of tourist onboard in the mission"""
        
        # this is flat percent added to reputation. All reputation is less than 1%
        flat_increase = 0.0
        bonus_max_multiplier = 0.0

        if self.get_reputation_level().name == 'HIGH':
            flat_increase = 0.25
            bonus_max_multiplier = 5
        elif self.get_reputation_level().name == 'MEDIUM': 
            flat_increase = 0.75
            bonus_max_multiplier = 10
        else: # LOW
            flat_increase = 1.25
            bonus_max_multiplier = 25
 

        # current reputation + flat increase + bonus reputation. See details below
        #
        # REPUTATION GAIN TABLE:
        # LOW: Up to 25% of tourist onboard
        # MEDIUM: Up to 10% of tourist onboard
        # HIGH: Up to 5% of tourist onboard
        gain = round(flat_increase + random.uniform(0, bonus_max_multiplier/100 * tourist_count), 2)
        self.reputation = min(self.reputation + gain, 100) # limits the reputation to 100 by using mininum function
        return gain
    
    def increase_money(self, expedition_distance, tourist_count):
        """Gain money based on tourist count * distance of expedition"""
        gain = tourist_count * (expedition_distance / 100)
        
        self.money += gain
        return gain
    

        
# The ship attribute will be a list, because I plan on allowing the user to buy multiple ships
player_ship = Ship(name="Starter", capacity=20, fuel_range=300, travel_speed=575)
user_profile = Profile(name=str(input()), reputation=1, tourists=0, ship=player_ship, money=1000)

#TODO: Ensure default Starter Ship and Profile is uncommented above. Delete debugging lines below.
# player_ship = Ship(name="DEBUGGER", capacity=200, fuel_range=2500, travel_speed=5000)
# user_profile = Profile(name=str(input()), reputation=35, tourists=0, ship=player_ship, money=1000000000)
