"""

1. Build an "expedition" class and create objects for every planet (including our moon for starter ships)m
planet name, distance, +rep which + how much money it gives + how many tourists to add to current profile

Moon -- planet_name == moon, distance, 500, cash_reward == 50, reputation_gain == 5050,  

"""

class Expedition:
    all_expeditions = []
    
    def __init__(self, planet_name, distance, cash_reward, reputation_gain, tourist_something):
           self.planet_name = planet_name
           self.distance = distance #in MHSA™ Distance Units
           self.cash_reward = cash_reward
           self.reputation_gain = reputation_gain
           self.tourist_something = tourist_something
           Expedition.all_expeditions.append(self)
           
    def __str__(self):
        return f" {self.planet_name}"
    
moon = Expedition(planet_name="Moon", distance=25, cash_reward=10, reputation_gain=1, tourist_something=25)
venus = Expedition(planet_name="Venus", distance=2800, cash_reward=10, reputation_gain=1, tourist_something=25)
mars = Expedition(planet_name="Mars", distance=5200, cash_reward=25, reputation_gain=3, tourist_something=25)
mercury = Expedition(planet_name="Mercury", distance=6100, cash_reward=25, reputation_gain=3, tourist_something=25)
asteroid_belt = Expedition(planet_name="Asteroid Belt", distance=15000, cash_reward=25, reputation_gain=3, tourist_something=25)
jupiter = Expedition(planet_name="Jupiter", distance=42000, cash_reward=50, reputation_gain=5, tourist_something=25)
saturn = Expedition(planet_name="Saturn", distance=85200, cash_reward=50, reputation_gain=5, tourist_something=25)
uranus = Expedition(planet_name="Uranus", distance=180200, cash_reward=50, reputation_gain=5, tourist_something=25)
neptune = Expedition(planet_name="Neptune", distance=290000, cash_reward=50, reputation_gain=5, tourist_something=25)
