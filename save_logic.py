import json, os
from ship import Ship
from user_profile import Profile
from ascii_animations import *
import time
from colorama import *

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
PURPLE = '\033[95m'
MAGENTA = '\033[35m'
ENDCOLOR = '\033[0m'


def new_player(profile):
    '''Runs to initiate a new save game'''
    build_animation(solar_system)
    print(f"\n\n{PURPLE}Mostly Harmless Space Agency™ (MHSA){ENDCOLOR}\n{YELLOW}Onboarding Initializing...{ENDCOLOR}\n")
    time.sleep(2)
    print(f"> What is your name my fellow capitalist?")
    username = input()
    profile.name = username
    print(f"\n> Welcome to {PURPLE}MHSA™{ENDCOLOR}, Commander {profile.name}!")
    time.sleep(3)
    print("\n" * 50)


    build_animation(saturn)
    print("\n\n\n")
    print("=" * 30, "  TUTORIAL  ", "=" * 30)
    print(f"{YELLOW}Commander {username}, we need you to take tourists around our solar system.")
    print(f"{GREEN}- Successful expeditions give you cash $$$ and reputation.")
    print(f"- Higher reputation attracts more tourists to fill your spaceships.")
    print(f"- Cash can be used to upgrade or buy better spaceships.")
    print(f"- You've been given a basic spaceship to start off with, free of charge!{ENDCOLOR}")
    print("=" * 30, "  TUTORIAL  ", "=" * 30)
    print(f"Press {RED}ENTER{ENDCOLOR} to continue...")
    input()



def save_game(profile):
    """Save the current profile (and all ships) to <profile_name>.json."""
    # Serialize ships -> list of dicts
    ships_data = []
    for ship in getattr(profile, "ships", []):
        ships_data.append({
            "name": ship.name,
            "capacity": ship.capacity,
            "fuel_range": ship.fuel_range,
            "travel_speed": ship.travel_speed,
            "capacity_level": ship.capacity_level,
            "fuel_level": ship.fuel_level,
            "speed_level": ship.speed_level,
            "capacity_cost": getattr(ship, "capacity_cost", 100),
            "fuel_cost": getattr(ship, "fuel_cost", 100),
            "speed_cost": getattr(ship, "speed_cost", 100),
            "max_level": getattr(ship, "max_level", 10),
            "credits": getattr(ship, "credits", 0),
            "ship_cost": getattr(ship, "ship_cost", 0),
        })

    save_data = {
        "name": profile.name,
        "reputation": profile.reputation,
        "tourists": profile.tourists,
        "money": profile.money,
        "ships": ships_data,
    }

    os.makedirs("save_files", exist_ok=True)
    filename = os.path.join("save_files", f"{profile.name}.json")

    with open(filename, "w") as f:
        json.dump(save_data, f, indent=4)

    print(f"Game saved as {filename}")



def load_save():
    """Let the user pick a save file from save_files/ and return a loaded Profile."""
    files = [f for f in os.listdir("save_files") if f.endswith(".json")]
    if not files:
        return None

    print("\n" * 100)
    print("\nAvailable saves:")
    for i, fname in enumerate(files, start=1):
        print(f"{i}) {fname}")

    while True:
        choice = input("> ").strip()
        if not choice.isdigit():
            print("Please enter a number.")
            continue
        idx = int(choice)
        if 1 <= idx <= len(files):
            selected = files[idx - 1]
            break
        print("Invalid choice, try again.")

    filepath = os.path.join("save_files", selected)
    with open(filepath, "r") as f:
        data = json.load(f)

    # Rebuild ships list
    ships: list[Ship] = []
    for ship_data in data.get("ships", []):
        s = Ship(
            name=ship_data.get("name", "Ship"),
            capacity=ship_data.get("capacity", 10),
            fuel_range=ship_data.get("fuel_range", 250),
            travel_speed=ship_data.get("travel_speed", 5),
        )
        s.capacity_level = ship_data.get("capacity_level", 1)
        s.fuel_level = ship_data.get("fuel_level", 1)
        s.speed_level = ship_data.get("speed_level", 1)
        s.capacity_cost = ship_data.get("capacity_cost", 100)
        s.fuel_cost = ship_data.get("fuel_cost", 100)
        s.speed_cost = ship_data.get("speed_cost", 100)
        s.max_level = ship_data.get("max_level", 10)
        s.credits = ship_data.get("credits", 0)
        s.ship_cost = ship_data.get("ship_cost", 0)
        ships.append(s)

    # Rebuild Profile (using your existing signature)
        profile = Profile(
            data.get("name", ""),
            data.get("reputation", 1),
            data.get("tourists", 5),
            ships[0] if ships else None,
            data.get("money", 0),
        )

        # Ensure the full list is on the profile
        profile.ships = ships

        print(f"\nLoaded save for {profile.name}")
        return profile