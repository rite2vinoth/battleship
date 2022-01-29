import sys
from battleships import *


def visualise(fleet, shots_set):
    ''' provides visualisation showing state of ocean and fleet after every shoot from user '''
    never_shot_set = get_never_shot_set(shots_set)
    shot_not_hit_set = get_shot_not_hit_set(fleet, shots_set)
    hit_not_sunk_set = get_hit_not_sunk_set(fleet)
    sunk_ships_coord_dict = get_sunk_ships_coord_dict(fleet)

    print("||", end='\t')
    for i in range(10):
        print(i, end='\t')
    print()
    print("----------------------------------------------------------------------------------", end="\n")
    for r in range(10):
        print(r, end='\t')
        for c in range(10):
            if(r, c) in hit_not_sunk_set:
                print("*", end='\t')
            elif (r, c) in shot_not_hit_set:
                print("-", end='\t')
            elif (r, c) in sunk_ships_coord_dict:
                print(sunk_ships_coord_dict[(r, c)], end='\t')
            else:
                print(".", end='\t')
        print("\n")
    print("Legend: \n '.' \t\t    squares never been shot \n '-' \t\t    squares shot but not resulted in hit  \n '*' \t\t    squares containing a ship that has been hit but not yet sunk \n 'S or D or C or B' ships that were sunk and their type")


def extension():
    ''' extension function to start the game '''
    current_fleet = randomly_place_all_ships()
    print("WELCOME TO THE BATTLESHIP GAME. \n  Ships are randomly placed. \n  Game starts now. \n  Good Luck !\n")

    game_over = False
    shots = 0
    shots_set = set()

    while not game_over:
        try:
            loc_str = input(
                "\n Enter row and column to shoot (separted by space). Enter 'quit' at any time to quit the game: ")
            # check if user enters quit and exit the game with message else proceed with the game
            if loc_str.lower() == 'quit':
                sys.exit("Game Ended!\nThanks for playing Battleship!")
            else:
                (r, c) = loc_str.split()
                current_row = int(r)
                current_column = int(c)
                # check if user enters coordinates outside of the ocean boundary
                if(current_row < 0 or current_row > 9 or current_column < 0 or current_column > 9):
                    raise ValueError
                current_shot = (current_row, current_column)
                shots += 1
                if current_shot not in shots_set:
                    shots_set.add(current_shot)
                    if check_if_hits(current_row, current_column, current_fleet):
                        print("You have a hit!")
                        (current_fleet, ship_hit) = hit(
                            current_row, current_column, current_fleet)
                        if is_sunk(ship_hit):
                            print("You sank a " + ship_type(ship_hit) + "!")
                    else:
                        print("You missed!")
                    if not are_unsunk_ships_left(current_fleet):
                        game_over = True
                else:
                    print("You already entered this coordinate. You missed!")
                # calling these functions to update so can be used in extension for display
                visualise(current_fleet, shots_set)

        except ValueError:
            print(
                "Invalid Entry. If you want to quit, enter 'quit' else enter valid coordinates.")
    print("Game over! You required", shots, "shots.")


if __name__ == '__main__':  # keep this in
    extension()
