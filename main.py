#############################################################################################
'''
YOU CAN INSTALL THIS AT GITHUB:
https://github.com/Zero-For683/MHSA_Game

'''






from user_profile import user_profile, Profile
from ship import Ship
from expedition import *
from ascii_animations import *
from save_logic import *
from core_game_logic import *


import time
import os
import json

#########################################################################################



def main():
    print("\n" * 100)
    profile = user_profile

    try:
        os.mkdir("save_files")
    except FileExistsError:
        pass

    if any(os.path.isfile(os.path.join("save_files", f)) for f in os.listdir("save_files")):
        print("Would you like to create a new save, or load an existing playthrough?")
        print("1) Load save")
        print("2) Create new save")
        save = int(input("> "))

        if save == 1:
            loaded = load_save()
            if loaded is not None:
                profile = loaded
        elif save == 2:
            new_player(profile)
    else:
        # No save files found
        new_player(profile)





    # Main game loop
    while True:
        choice = main_menu(profile)

        if choice == "1":
            choose_ship = choose_owned_ship(profile)
            if choose_ship is not None:
                expedition = choose_destination(choose_ship)
                run_mission(profile, choose_ship, expedition)
        elif choice == "2":
            ship_to_upgrade = choose_owned_ship(profile)
            if ship_to_upgrade is not None:
                shop_menu(profile, ship_to_upgrade)
        elif choice == "0":
            save_game(profile)
            print("Saving game, see you later Commander...")
            break
        else:
            print("Invalid option, please try again")


if __name__ == "__main__":

    main()
