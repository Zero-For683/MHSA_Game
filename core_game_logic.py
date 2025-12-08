import math
from random import randint
from ascii_animations import *
import time
from expedition import Expedition
from ship import *
from user_profile import Profile
import threading
import time

def main_menu(profile):
    """Show the main menu and return the player's choice."""
    print("\n" * 100)
    build_animation(winter_home)
    print("=" * 30, "  MAIN MENU  ", "=" * 30)
    print(f"Commander:        {profile.name}")
    print(f"Money:            {profile.money}")
    print(f"Reputation:       {profile.reputation}")
    print(f"Tourist Serviced: {profile.tourists}\n\n")
    print("1) Choose mission")
    print("2) Upgrade ship")
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
                print(f"Destination Selected: {selected_destination.planet_name}")
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
    if ship.fuel_range * ship.travel_speed < expedition.distance * 2:
        print(
            "Your ship isn't strong enough for this expedition. "
            "Say goodbye to your tourists and prized ship..."
        )
        # We can add penalties here if we want to for random button mashing
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

    import threading
    import time

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

        input("Press Enter to return to the menu...")
        return

    # Normal preflight check
    if not is_preflight_check_pass(ship, expedition):
        return

    # Determine how many passengers board
    tourist_onboard = calc_passenger_onboard(profile, ship)
    print(
        f"\nBased on your reputation, {tourist_onboard} decided to join this mission. "
        f"You had {ship.capacity - tourist_onboard} seats left open."
    )
    input("\nPress Enter to launch the mission... ")

    # Compute a rough mission duration based on distance and ship speed
    # travel_units grows with distance and shrinks with speed
    travel_units = expedition.distance / max(1, ship.travel_speed)
    # Clamp to something reasonable in real seconds
    mission_duration = max(10, min(120, int(travel_units / 5)))

    # Mark ship as "away"
    ship._mission_active = True
    ship._mission_destination = expedition.planet_name
    ship._mission_eta = time.time() + mission_duration

    print(f"\nYou order your captain to embark on a journey to {expedition.planet_name} with the tourists!")
    print(f"{ship.name} will be away for about {mission_duration} seconds (round trip).")
    print("You can visit the shop or main menu while the mission runs in the background.\n")

    def mission_worker():
        spinner = "|/-\\"
        i = 0

        # Tiny background animation loop while the mission is in flight
        while time.time() < ship._mission_eta and getattr(ship, "_mission_active", False):
            remaining = max(0, int(ship._mission_eta - time.time()))
            frame = spinner[i % len(spinner)]
            # One-line status that will occasionally interleave with menu output
            print(
                f"\r[{frame}] {ship.name} en route to {expedition.planet_name} | ETA: {remaining:2d}s ",
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
        print(f"Tourists delivered: {tourist_onboard}")
        print(f"Rewards:\n  Money:       +{gained_money}\n  Reputation:  +{gained_reputation}\n")

    # Start the background mission thread and immediately return control to main loop
    mission_thread = threading.Thread(target=mission_worker, daemon=True)
    ship._mission_thread = mission_thread
    mission_thread.start()

    input("Press Enter to return to the menu while your ship is on mission...")





def open_ship_shop(profile, ship_list):
    """Display a ship shop, let the player buy ships from ship_list."""
    while True:
        print("\n" * 50)
        print("=" * 30, "SHIPYARD", "=" * 30)
        print(f"Your credits: {profile.money}")
        print()

        for idx, ship in enumerate(ship_list, start=1):
            print(f"{idx}) {ship.name}")
            art = SHIP_ART.get(ship.name, "")
            if art:
                print(art)
            print(f"   Capacity:    {ship.capacity}")
            print(f"   Fuel range:  {ship.fuel_range}")
            print(f"   Speed:       {ship.travel_speed}")
            print(f"   Price:       {ship.ship_cost} credits")
            print("-" * 60)

        print("0) Leave shipyard")
        choice = input("Choose a ship number to buy (or 0 to exit): ").strip()

        if choice == "0":
            break

        if not choice.isdigit():
            print("Please enter a number.")
            input("Press Enter to continue...")
            continue

        idx = int(choice)
        if not (1 <= idx <= len(ship_list)):
            print("Invalid choice.")
            input("Press Enter to continue...")
            continue

        selected_ship = ship_list[idx - 1]

        # Attempt purchase via Profile method
        success = profile.buy_ship(selected_ship)
        if success:
            print(f"{selected_ship.name} has been added to your fleet.")
        input("Press Enter to continue...")

def choose_owned_ship(profile):
    """Let the player pick one of their owned ships. Returns a Ship or None."""
    if not getattr(profile, "ships", []):
        print("You don't own any ships yet.")
        return None

    print("\n" * 100)
    print("=" * 30, "YOUR FLEET", "=" * 30)
    for i, ship in enumerate(profile.ships, start=1):
        print(f"{i}) {ship.name} "
              f"(Cap: {ship.capacity}, Fuel: {ship.fuel_range}, Speed: {ship.travel_speed})")

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


def shop_menu(profile, profile_ship):
    while True:
        print("\n" * 100)
        build_animation(spaceship)
        print("=" * 30, "  SHIP UPGRADE MENU  ", "=" * 30)

        print("Which ship component would you like to upgrade?\n")
        print("1) check your current ship status\n")
        print("2) upgrade your ships holding capacity")
        print("3) upgrade your ships fuel range")
        print("4) upgrade your ships speed")
        print("5) Buy a new ship")
        print("\n0) to go back to main menu")
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

        # from here down, your existing logic:
        if pick == 1:
            profile_ship.check_stats()
            time.sleep(5)
        elif pick == 2:
            profile_ship.upgrade_capacity()
            time.sleep(5)
        elif pick == 3:
            profile_ship.upgrade_fuel()
            time.sleep(5)
        elif pick == 4:
            profile_ship.upgrade_speed()
            time.sleep(5)
        elif pick == 5:
            open_ship_shop(profile, ship_shop)
        elif pick == 0:
            break
        else:
            print("Invalid option BOZO. Pick again")