import click
import json

from menu import menu
from Master import Master
# from menu_gui import 


master = Master()


@click.group()
def main():
    pass


@main.command()
def new_garden():
    """Clean all autosave json files."""
    with open("autosave_warehouse.json", "w") as autosave_file:
        json.dump("", autosave_file)
    with open("autosave_garden.json", "w") as autosave_file:
        json.dump("", autosave_file)


@main.command()
@click.option(
    "--plant-name", type=click.Choice([
        "Rose", "Poppy", "Violet", "Pineapple",
        "Apple", "Orange", "Cactus", "Oak",
        "Pine", "Carrot", "Potato", "Tomato"
    ], case_sensitive=False),
    help="Plant name."
)
@click.option("-n", "--number", default=1, help="Gardenbed number.")
def plant(plant_name, number):
    """Grow plant in gardenbed by name and key."""
    master.grow_plant(plant_name, number - 1)


@main.command()
def short_show():
    """Print all plants in short mode."""
    master.show_plants_short()


@main.command()
@click.option("-n", "--number", type=int, default=1, help="Weeding gardenbed by number.")
def weed_gardenbed(number):
    """Weeding gardenbed."""
    master.weed(number)


@main.command()
@click.option("-n", "--number", type=int, default=1, help="Watering gardenbed by number.")
def watering(number):
    """Watering gardenbed."""
    master.water(number)


@main.command()
@click.option("-s", "--show", type=int, default=1, help="Print plants based on input gardenbed.")
def show_details(show):
    """Print plants based on input gardenbed."""
    master.show_gardenbed_info(show - 1)


@main.command()
def show_seeds():
    """Print all seeds in warehouse."""
    master.show_warehouse_info()


@main.command()
@click.option("-gbn", "--gardenbed-number", type=int, help="Number of gardenbed.")
@click.option("-p", "position", type=int, help="Number of plant in gardenbed.")
def delete_plant(gardenbed_number, position):
    """Delete plant from gardenbed by number of gardenbed and number of gardenbed plant."""
    master.delete_plant(gardenbed_number, position)


@main.command()
def run_menu():
    """Load this app in simple console interface."""
    menu(master)


@main.command()
@click.option("--sort-by", default="Name", type=click.Choice([
    "Name", "Harvest", "Live", "Immunity", "Ills"
], case_sensitive=False), help="Sort items by key.")
def sort_elements(sort_by: str):
    """Sort items by key."""
    master.sort_elements(sort_by)


@main.command()
def avg():
    """Show avg statistics."""
    master.avg_statistics()


@main.command()
@click.option("--step", default=1, help="Produces x steps.")
def do_step(step):
    """Produce step and change params in plants."""
    master.step(count=step)


if __name__ == "__main__":
    main()
