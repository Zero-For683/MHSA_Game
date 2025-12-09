import math
import threading
import time
from random import randint
from typing import Callable
from ascii_animations import *
from expedition import Expedition
from ship import *
from user_profile import Profile
from colorama import *
from save_logic import *

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
PURPLE = '\033[95m'
MAGENTA = '\033[35m'
ENDCOLOR = '\033[0m'

def main_menu(profile):
    """Show the main menu and return the player's choice."""
    print("\n" * 50)
    build_animation(winter_home)
    print("=" * 30, "  MAIN MENU  ", "=" * 30)
    print(f"{YELLOW}Commander:        {profile.name}{ENDCOLOR}")
    print(f"{GREEN}Credits:          ${profile.money:,.2f}{ENDCOLOR}")
    print(f"{CYAN}Reputation:       {profile.reputation:.2f}%{ENDCOLOR}")
    print(f"Tourist Serviced: {profile.tourists}\n\n")
    print("1) Choose Mission")
    print("2) Upgrade Ship")
    print("0) Save & Quit")
    print("=" * 30, "  MAIN MENU  ", "=" * 30)
    choice = input("Choose an option: ")
    return choice.strip()

def choose_destination():
    '''When called, you get the option to choose the available missions'''   
    print("\n" * 100)
    print("=" * 30, "  MISSION SELECTOR  ", "=" * 30)
    build_animation(solar_system_big)
    print("Available Destinations:")
    for i, obj in enumerate(Expedition.all_expeditions):
        print(f"{i + 1}. {obj.planet_name}")

    while True:
        try:
            choice = int(input("\nEnter the number of your destination or [0] to return to main menu: "))
            if choice == 0:
                break
            if 1 <= choice <= len(Expedition.all_expeditions):
                selected_destination = Expedition.all_expeditions[choice - 1]
                print(f"Destination Selected: {RED}{selected_destination.planet_name}{ENDCOLOR}")
                return selected_destination
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid. Please enter a number.")  


def is_preflight_check_pass(ship, expedition):
    if expedition is None:
        print("Invalid destination. Mission aborted.")
        return False

    # Simple range check: can this ship make a round trip?
    if (ship.fuel_range * ship.travel_speed) < (expedition.distance * 2):
        print(
            "Your ship isn't strong enough for this expedition. "
        )
        input(f"\nPress {RED}ENTER{ENDCOLOR} return to the menu...")
        return False
    return True

def calc_passenger_onboard(profile: Profile, ship: Ship) -> int:
    """Determine how many passengers got onboard based on current player's reputation"""
    
    rep_level = profile.get_reputation_level()
    
    # use math ceiling because we want at least 1 passenger if rng of min capacity returns zero
    min_capacity = math.ceil(ship.capacity * (rep_level.min_rng / 100)) 
    max_capacity = math.floor(ship.capacity * (rep_level.max_rng / 100))

    return randint(min_capacity, max_capacity)


def run_mission(profile: Profile, ship: Ship, expedition: Expedition):
    """Runs the chosen mission asynchronously with a tiny in-terminal animation."""

    # If no destination was actually selected, just bail.
    if expedition is None:
        print("No destination selected. Mission aborted.")
        return

    # If this ship is already away, show a tiny status animation and block sending it again.
    if getattr(ship, "_mission_active", False):
        dest = getattr(ship, "_mission_destination", "somewhere")
        eta = getattr(ship, "_mission_eta", None)

        print(f"\n{ship.name} is already on a mission to {dest}.")

        spinner = "|/-\\"
        if eta is not None:
            # Quick, non-blocking style status check (~6 seconds max)
            for i in range(12):
                remaining = max(0, int(eta - time.time()))
                frame = spinner[i % len(spinner)]
                print(
                    f"\r[{frame}] Mission in progress... approx {remaining:2d}s remaining ",
                    end="",
                    flush=True,
                )
                time.sleep(0.5)
            print()
        else:
            print("Mission in progress...")

        input(f"Press {RED}ENTER{ENDCOLOR} return to the menu...")
        return

    # Normal preflight check
    if not is_preflight_check_pass(ship, expedition):
        return

    # Determine how many passengers board
    tourist_onboard = calc_passenger_onboard(profile, ship)
    print(
        f"\nBased on your reputation, {YELLOW}[{tourist_onboard}] tourists joined this expedition{ENDCOLOR}."
        f" You had {ship.capacity - tourist_onboard} seats left open."
        
    )
    input(f"\nPress {RED}ENTER{ENDCOLOR} to launch the mission... ")

    # Compute a rough mission duration based on distance and ship speed
    # travel_units grows with distance and shrinks with speed
    travel_units = expedition.distance / max(1, ship.travel_speed)
    # Clamp to something reasonable in real seconds
    mission_duration = max(10, min(120, int(travel_units / 5)))

    # Mark ship as "away"
    ship._mission_active = True
    ship._mission_destination = expedition.planet_name
    ship._mission_eta = time.time() + mission_duration

    print(f"\nCommander initiates {expedition.planet_name} expedition for the tourists!")
    print(f"\t{ship.name} will be away for about {mission_duration} seconds...")
    print("\tYou can visit the shop or main menu while the mission runs in the background.\n")

    def mission_worker():
        spinner = "|/-\\"
        i = 0

        # Tiny background animation loop while the mission is in flight
        while time.time() < ship._mission_eta and getattr(ship, "_mission_active", False):
            remaining = max(0, int(ship._mission_eta - time.time()))

            # Only draw the spinner if it's enabled
            if getattr(ship, "_mission_show_spinner", True):
                frame = spinner[i % len(spinner)]
                print(
                    f"\r{MAGENTA}[{frame}] {ship.name} en route to {expedition.planet_name} | ETA: {remaining:2d}s {ENDCOLOR}",
                    end="",
                    flush=True,
                )
                i += 1

            time.sleep(0.5)

        # Clean up the animation line
        print("\r", end="")


        # If something else cancelled the mission, don't apply rewards
        if not getattr(ship, "_mission_active", False):
            return

        # Apply rewards when the mission actually completes
        gained_reputation = profile.increase_reputation(tourist_onboard)
        gained_money = profile.increase_money(expedition.distance, tourist_onboard)
        profile.tourists += tourist_onboard

        # Clear mission state
        ship._mission_active = False
        ship._mission_eta = None
        ship._mission_destination = None

        # Final mission summary
        print(f"\n\nMission complete! {ship.name} has returned from {expedition.planet_name}.")
        print(f"Tourists Delivered: {tourist_onboard}")
        print(f"{YELLOW}Rewards:{ENDCOLOR}\n  {GREEN}Money:       +${gained_money:,.2f}{ENDCOLOR}\n  {CYAN}Reputation:  +{gained_reputation:.2f}%{ENDCOLOR}\n")
       
    ship._mission_show_spinner = True
    mission_thread = threading.Thread(target=mission_worker, daemon=True)
    ship._mission_thread = mission_thread
    mission_thread.start()

    # This prompt is still on the mission screen
    input(f"\nPress {RED}ENTER{ENDCOLOR} return to the menu...")

    # Once we leave the mission screen, stop drawing the spinner so it
    # doesn't interfere with menu input while the mission continues running
    ship._mission_show_spinner = False
    # Optional: wipe the spinner line
    print("\r" + " " * 80 + "\r", end="")



def open_ship_shop(profile, ship_list):
    """Display a ship shop, let the player buy ships from ship_list."""
    while True:
        print("\n" * 50)
        print("=" * 30, "SHIPYARD", "=" * 30)
        print(f"Your Credits: {GREEN}${profile.money:,.2f}{ENDCOLOR}")
        print()

        for idx, ship in enumerate(ship_list, start=1):
            print(f"{idx}) {ship.name}")
            art = SHIP_ART.get(ship.name, "")
            if art:
                print(art)
            print(f"   Capacity:    {ship.capacity}")
            print(f"   Fuel range:  {ship.fuel_range}")
            print(f"   Speed:       {ship.travel_speed}")
            print(f"   Price:       {GREEN}${ship.ship_cost:,.2f}{ENDCOLOR}")
            print("-" * 60)

        print("0) Leave shipyard")
        choice = input("Choose a ship number to buy (or 0 to exit): ").strip()

        if choice == "0":
            break

        if not choice.isdigit():
            print("Please enter a number.")
            input(f"Press {RED}ENTER{ENDCOLOR} continue...")
            continue

        idx = int(choice)
        if not (1 <= idx <= len(ship_list)):
            print("Invalid choice.")
            input(f"Press {RED}ENTER{ENDCOLOR} continue...")
            continue

        selected_ship = ship_list[idx - 1]

        # Attempt purchase via Profile method
        success = profile.buy_ship(selected_ship)
        if success:
            print(f"{selected_ship.name} has been added to your fleet.")
        input(f"Press {RED}ENTER{ENDCOLOR} continue...")


def choose_owned_ship(profile):
    """Let the player pick one of their owned ships. Returns a Ship or None."""
    if not getattr(profile, "ships", []):
        print("You don't own any ships yet.")
        return None

    print("\n" * 100)
    print("=" * 30, "YOUR FLEET", "=" * 30)
    for i, ship in enumerate(profile.ships, start=1):
        print(f"{i}) {ship.name} "
              f"(Capacity: {ship.capacity}, Fuel: {ship.fuel_range}, Speed: {ship.travel_speed})")

    print("0) Cancel")

    while True:
        choice = input("Choose a ship: ").strip()
        if choice == "0":
            return None
        if not choice.isdigit():
            print("Please enter a number.")
            continue

        idx = int(choice)
        if 1 <= idx <= len(profile.ships):
            return profile.ships[idx - 1]

        print("Invalid choice, try again.")


def shop_menu(profile: Profile, ship: Ship):
    while True:
        print("\n" * 100)
        build_animation(spaceship)
        print("=" * 30, "  SHIP UPGRADE MENU  ", "=" * 30)

        print("Which ship component would you like to upgrade?\n")
        print("1) Check This Ship's Current Stats\n")
        print("2) Upgrade Passenger Capacity")
        print("3) Upgrade Fuel Range")
        print("4) Upgrade Speed")
        print("5) Buy a New Ship")
        print("\n0) Back to Main Menu")
        print("=" * 30, "  SHIP UPGRADE MENU  ", "=" * 30, "\n")

        # Safely read input
        while True:
            choice_str = input("Pick an option: ").strip()
            if choice_str == "":
                # Treat blank enter as "do nothing, re-show prompt"
                print("Please enter a number from the menu.")
                continue
            try:
                pick = int(choice_str)
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

        # Created a inner function for readability
        def upgrade_ship(ship_upgrade_cb: Callable[[], None], level: int):
            """helper function for checking profile money and executing ship upgrade function"""
            if profile.money >= ship.get_upgrade_cost(level):
                ship_upgrade_cb()
                profile.money -= ship.get_upgrade_cost(level)
                print(f"\n${profile.money:,.2f} Credits Left")
            else:
                print("Not enough credits")
            time.sleep(5)


        # from here down, your existing logic:
        if pick == 1:
            ship.get_status()
            time.sleep(5)
        elif pick == 2:
            upgrade_ship(ship.upgrade_capacity, ship.capacity_level)
        elif pick == 3:
            upgrade_ship(ship.upgrade_fuel, ship.fuel_level)
        elif pick == 4:
            upgrade_ship(ship.upgrade_speed, ship.travel_speed_level)
        elif pick == 5:
            open_ship_shop(profile, ship_shop)
        elif pick == 0:
            break
        else:
            print("Invalid option BOZO. Pick again")