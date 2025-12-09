"""

1. Build an "expedition" class and create objects for every planet (including our moon for starter ships)m
planet name, distance, +rep which + how much money it gives + how many tourists to add to current profile

Moon -- planet_name == moon, distance, 500, cash_reward == 50, reputation_gain == 5050,  

"""

class Expedition:
    all_expeditions = []
    
    def __init__(self, planet_name, distance):
           self.planet_name = planet_name
           self.distance = distance #in MH™ Distance Units (Earth to Destination in AU x 200,000)
           Expedition.all_expeditions.append(self)
           
    def __str__(self):
        return f" {self.planet_name}"
    
moon = Expedition(planet_name="Moon", distance=500)
venus = Expedition(planet_name="Venus", distance=56000)
mars = Expedition(planet_name="Mars", distance=104000)
mercury = Expedition(planet_name="Mercury", distance=122000)
asteroid_belt = Expedition(planet_name="Asteroid Belt", distance=300000)
jupiter = Expedition(planet_name="Jupiter", distance=840000)
saturn = Expedition(planet_name="Saturn", distance=1704000)
uranus = Expedition(planet_name="Uranus", distance=3604000)
neptune = Expedition(planet_name="Neptune", distance=5800000)
