'''
3. Build a "Profile" class that will update as you get more "reputation" (more reputation == more tourists on each expidition)
We can try saving this to a file so we can save game-state
name, rep, current money, ship assigned, default tourist count.


attributes: profile name, reputation, tourist count, current ship, money
'''

class Profile():
    def __init__(self, name, reputation, tourists, ship, money):
        self.name = name 
        self.reputation = reputation
        self.tourists = tourists
        self.ship = ship
        self.money = money
        
user_profile = Profile(name=str(input()), reputation=1, tourists=5, ship="Default", money=100)

