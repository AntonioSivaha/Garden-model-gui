import os
import time

from Master import Master
from utils.OS_color_them_detecter import detect_dark_mode

try:
    import colorama
except ImportError as err:
    print(err)
    colorama = None


def submenu(master, position):
    """Additional menu to detail show statistics and
    manipulation with gardenbed."""
    while True:
        os.system("cls" if os.name in ["nt", "dos"] else "clear")
        print(detect_dark_mode() +
              '''Select an action:
                1.Grow plant.
                2.Show details static.
                3.Cut plant.
                4.Weed.
                5.Water the plant.
                0.Exit\n\n'''
              )
        try:
            selected_point: int = int(input(">>> "))
        except TypeError as err:
            print(err)
            time.sleep(5)
            continue
        except ValueError as err:
            print(err)
            time.sleep(5)
            continue

        match selected_point:
            case 1:
                master.grow_plant(inp_gardenbed_place=position)
            case 2:
                master.show_gardenbed_info(position)
                try:
                    choose: int = int(input("\n\nInput 0 to exit.\n>>>"))
                except TypeError as err:
                    print(err)
                    time.sleep(5)
                    return
                except ValueError as err:
                    print(err)
                    time.sleep(5)
                    continue
                if choose == 0:
                    continue
            case 3:
                master.delete_plant(position)
            case 4:
                master.weed(position)
            case 5:
                master.water(position)
            case 0:
                break


def main_menu(master):
    """Main menu with your garden, warehouse, avg
    statistics and sorting."""
    while True:
        os.system("cls" if os.name in ["nt", "dos"] else "clear")
        print(detect_dark_mode() + "Plants:")
        master.show_plants_short()
        print("\nSeeds:")
        master.show_warehouse_info()
        print("\nAVG statistics:")
        master.avg_statistics()
        print("\n6.Filter")
        selected_point = input("\n\nSelect gardenbed or do step: ")
        if selected_point == "":
            master.step()
            continue
        try:
            selected_point = int(selected_point)
        except TypeError as err:
            print(err)
            time.sleep(5)
            continue
        if 1 <= selected_point <= 5:
            submenu(master, selected_point - 1)
        if selected_point == 6:
            try:
                sort_by = str(input("Input filter: "))
            except TypeError as err:
                print(err)
                time.sleep(5)
                continue
            except ValueError as err:
                print(err)
                time.sleep(5)
                continue
            if sort_by not in ["Name", "Harvest", "Live", "Immunity", "Ills"]:
                print("This filter is unavailable.")
                time.sleep(5)
                continue
            master.sort_elements(sort_by)
            input("Input something to continue: ")
            continue
        if selected_point == 0:
            exit()


def menu(inp_master=None):
    master = inp_master
    if not inp_master:
        master = Master()
    main_menu(master)
