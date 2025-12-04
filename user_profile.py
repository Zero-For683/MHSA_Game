'''
3. Build a "Profile" class that will update as you get more "reputation" (more reputation == more tourists on each expidition)
We can try saving this to a file so we can save game-state
name, rep, current money, ship assigned, default tourist count.


attributes: profile name, reputation, tourist count, current ship, money
'''

from ship import Ship

class Profile:
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

        print(f"Purchased {ship.name} for {cost} credits.")
        print(f"Remaining credits: {self.money}")
        return True



# The ship attribute will be a list, because I plan on allowing the user to buy multiple ships

player_ship = Ship(name="Starter", capacity=50, fuel_range=2000, travel_speed=8000)
user_profile = Profile(name=str(input()), reputation=1, tourists=5, ship=player_ship, money=100)