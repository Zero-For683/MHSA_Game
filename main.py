'''
Program idea:

New users get small amount of money and a starter ship. 
The user picks a destination to take tourists to for money (moon, mercery, venus, etc)

Expiditions to those destinations give you money, which you can shop for better parts, or better ships

More expeditions give you more rep, which give you more tourists


-----------------------------------------------------------------


DELEGATIONS:
1. Build an "expedition" class and create objects for every planet (including our moon for starter ships)m
planet name, distance, +rep which = how many tourists to add to current profile, - czedrik got this 

2. Build a "ship" class that has some basic stat attributes that you can upgrade with methods
default name, fuel cap, speed, capacity
add method to upgrade fuel, speed and capacity
fuel capacity * speed = range / tourist capacity /

3. Build a "Profile" class that will update as you get more "reputation" (more reputation == more tourists on each expidition)
We can try saving this to a file so we can save game-state
name, rep, current money, ship assigned, default tourist count.

4. Build a while loop for game-state (we'll build this last to determine the flow of the game, and build ASCII art)
while option != 0
if option 1 = Begin mission -> pick destination -> passengers -> launch -> award money -> loop back to main menu?
elif option 2 = Upgrade Ship -> pick part -> update player_ship -> loop back to main menu
elif option 3 = Save Game -> save state
elif option 4 = New Game? -> confirm -> wipe memory
else invalid option

'''


from profile import user_profile, Profile
from ship import ship1, ship2, ship3, Ship
from expedition import moon, mars, jupiter, Expedition # Add in more planets as necessary
import time
import os

DESTINATIONS = {
    "1": moon,
    "2": mars,
    "3": jupiter
}

def new_player(profile):
    '''Determines if there is a new player and gives them the rundown'''
    print(f"Hello, what is your name?\n")
    username = input()
    profile.name = username
    print(f"I hope you're ready for an exciting adventure {profile.name}")
    print(f"What ship would you like to have to start your business off?")




def main_menu(profile):
    """Show the main menu and return the player's choice."""
    print("\n================================")
    print(f"Commander:   {profile.name}")
    print(f"Money:       {profile.money}")
    print(f"Reputation:  {profile.reputation}")
    print(f"Tourists:    {profile.tourists}")
    print("================================")
    print("1) Choose mission")
    print("2) Upgrade ship")
    print("0) Save & Quit")
    choice = input("Choose an option: ")
    return choice.strip()

def choose_destination():
    '''When called, you get the option to choose the available missions -- Czedrik Draft'''   
    print("Available Destinations:")
    for i, obj in enumerate(Expedition._expedition, start=1):
        print(f"{1}. {obj.planet_name}")

    while True:
        try:
            choice = int(input("\nEnter the number of your choice: "))
            if 1 <= choice <= len(Expedition._expedition):
                selected_destination = Expedition._expedition[choice - 1]
                print(f"Destination Selected: {selected_destination.planet_name}")
                return selected_destination
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid. Please enter a number.")  


def run_mission(profile, ship, expedition):
    """Runs the chosen mission."""
    if expedition is None:
        print("Invalid destination. Mission aborted.")
        return

    # Simple range check: can this ship make a round trip?
    if ship.capacity * ship.travel_speed < expedition.distance * 2:
        print(
            "Your ship isn't strong enough for this expedition. "
            "Say goodbye to your tourists and prized ship..."
        )
        # We can add penalties here if we want to for random button mashing
        return

    print(f"\nYou order your captain to embark on a journey to {expedition.planet_name} with the tourists!")
    print(f"Rewards:\n  Money:       {expedition.cash_reward}\n  Reputation:  {expedition.reputation_gain}")

    profile.money += expedition.cash_reward
    profile.reputation += expedition.reputation_gain
    profile.tourists += expedition.tourist_something   # if you want rep -> more tourists


def upgrade_ship(profile_ship):
    while True:

        print(f"Which ship component would you like to upgrade?")
        print(f"Enter 1 to check your current ship status")
        print(f"Enter 2 to upgrade your ships holding capacity")
        print(f"Enter 3 to upgrade your ships fuel range")
        print(f"Enter 4 to upgrade your ships speed")
        print(f"Enter 0 to go back to main menu")
        pick = int(input("Pick an option: "))

        if pick < 0 or pick > 4:
          print("Invalid option. Please choose between 0 and 4.")
          continue

        if pick == 1:
            profile_ship.get_status()
        elif pick == 2:
            profile_ship.upgrade_capacity()
        elif pick == 3:
            profile_ship.upgrade_fuel()
            
        elif pick == 4:
            profile_ship.upgrade_speed()
        elif pick == 0:
            break
    

def main():
    profile = user_profile

    player_ship = Ship(name="Starter", capacity=50, fuel_range=2000, travel_speed=8000)
    profile.ship = player_ship

    new_player(profile)

    # Main game loop
    while True:
        choice = main_menu(profile)

        if choice == "1":
            expedition = choose_destination()
            run_mission(profile, player_ship, expedition)
        elif choice == "2":
            upgrade_ship(player_ship)
        elif choice == "0":
            print("Saving game (NOT IMPLEMENTED YET) and quitting, Goodbye Commander")
            break
        else:
            print("Invalid option, please try again")


if __name__ == "__main__":
    main()