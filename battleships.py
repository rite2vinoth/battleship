# see the readme.md file for description and data
import sys
import copy
import random as r
import time
#import extension as ext    Uncomment if we want to run visualisation from this program


def get_coordinates(ship):
    ''' returns coordinates (i.e squares) occupied by the ship. It may be assumed that a legal arrangement of ship is passed '''

    row_head, col_head, horiz, length = ship[0], ship[1], ship[2], ship[3]
    coord_set = set()
    for i in range(length):
        # If ship is horizontal, we keep row index same and increment column
        if horiz:
            coord_set.add((row_head, col_head+i))
        # If ship is vertical, we keep col index same and increment row index
        else:
            coord_set.add((row_head+i, col_head))
    return coord_set


def get_never_shot_set(shots_set):
    ''' returns a set of coordinates that have never been shot at '''
    never_shot_set = set()
    ocean_set = {(i, j) for j in range(0, 10) for i in range(0, 10)}
    never_shot_set = ocean_set.difference(shots_set)
    return never_shot_set


def get_shot_not_hit_set(fleet, shots_set):
    ''' returns a set of coordinates that have been shot at, but not resulted in a hit(nothing was there)'''
    shot_not_hit_set = set()
    current_fleet_hit_set = get_fleet_hit_set(fleet)
    shot_not_hit_set = shots_set.difference(current_fleet_hit_set)
    return shot_not_hit_set


def get_fleet_hit_set(fleet):
    ''' returns coordinates (i.e squares) occupied by all ships in fleet. It may be assumed that a legal arrangement of ship is passed '''
    fleet_hit_set = set()
    for ship in fleet:
        fleet_hit_set.update(get_coordinates(ship))
    return fleet_hit_set


def get_hit_not_sunk_set(fleet):
    ''' returns coordinates (i.e squares) occupied by ships that have been hit, but not yet sunk'''
    hit_not_sunk_set = set()
    for ship in fleet:
        if not is_sunk(ship):
            hit_not_sunk_set.update(ship[4])
    return hit_not_sunk_set


def get_sunk_ships_coord_dict(fleet):
    '''returns a dictionary containing coordinates of sunk ships and ship type'''
    sunk_ships_coord_dict = dict()
    ship_type_small_dict = {'submarine': 'S',
                            'destroyer': 'D', 'cruiser': 'C', 'battleship': 'B'}
    for ship in fleet:
        if is_sunk(ship):
            for each_hit in ship[4]:
                sunk_ships_coord_dict[each_hit] = ship_type_small_dict[ship_type(
                    ship)]
    return sunk_ships_coord_dict


def is_sunk(ship):
    ''' returns Boolean value, which is True if ship is sunk and False otherwise
    simple Check: There should be as many hits as the length of the ship and
    complete check: Check hit coordinates and verify if those are coordinates occupied by ship
    and returns True only if both satisfy'''

    length, hits = ship[3], ship[4]
    return (length == len(hits) and get_coordinates(ship) == hits)


def ship_type(ship):
    ''' returns one of the strings "batleshup","cruiser","destroyer", or "submarine" identifying the type of ship '''
    ship_type_dict = {1: 'submarine', 2: 'destroyer',
                      3: 'cruiser', 4: 'battleship'}
    return (ship_type_dict[ship[3]])


def is_open_sea(row, column, fleet):
    '''checks if the square given by `row` and `column` neither contains nor is adjacent (horizontally, vertically, or diagonally)
       to some ship in `fleet`. Returns Boolean `True` if so and `False` otherwise'''
    # obtain adjacent and own squares occupied by ships and testing given row, column iteratively
    # loop through each ship in the fleet
    for ship in fleet:
        # find each ship's coordinates
        coord_set = get_coordinates(ship)
        # obtain individual coordinate tuple individually
        for coord in coord_set:
            row_index, col_index = coord[0], coord[1]
            x_list = [x for x in range(row_index-1, row_index+2)]
            y_list = [y for y in range(col_index-1, col_index+2)]
            # create a set to hold occupied and adjacent coordinates
            occ_coord = set()
            for i in range(len(x_list)):
                for j in range(len(y_list)):
                    # check the fringe coordinates for out of ocean test
                    if not (y_list[j] in [-1, 10] or x_list[i] in [-1, 10]):
                        occ_coord.add((x_list[i], y_list[j]))
                        # check if supplied row, column is present in occupied / adjacent coordinates set
                        if {(row, column)}.issubset(occ_coord):
                            return False

    return True


def ok_to_place_ship_at(row, column, horizontal, length, fleet):
    '''checks if addition of a ship, specified by `row, column, horizontal`, and `length` as in `ship` representation above,
       to the `fleet` results in a legal arrangement'''
    # all coordinates of the ship specified by row,column should be open sea
    # first we construct the ship and pass it to get coordinates using get coordinates function
    ship = (row, column, horizontal, length, set())
    coord_set = get_coordinates(ship)
    # use the coordinates iteratively to get all coordinates
    # iteratively check coordinates using is_open_sea function
    for each_coord in coord_set:
        # check if any of the coordinates will go outside of the ocean, if so return False immediately
        if (each_coord[0] in [-1, 10] or each_coord[1] in [-1, 10]):
            return False
        else:
            # check if any of the coordinates are illegal, if so return False immediately
            if not (is_open_sea(each_coord[0], each_coord[1], fleet)):
                return False
    return True


def place_ship_at(row, column, horizontal, length, fleet):
    '''returns a new fleet that is the result of adding a ship, specified by `row, column, horizontal`, and `length` as in `ship`
       representation above, to `fleet`. It may be assumed that the resulting arrangement of the new fleet is legal'''
    # create the ship from parameters and append it to the deep copy of the supplied fleet
    ship = (row, column, horizontal, length, set())
    fleet1 = copy.deepcopy(fleet)
    fleet1.append(ship)
    return fleet1


def randomly_place_all_ships():
    '''returns a fleet that is a result of a random legal arrangement of the 10 ships in the ocean.
       This function makes use of the functions `ok_to_place_ship_at` and `place_ship_at` '''
    fleet = []
    # placing biggest ship first - i.e battleship. First ship can be placed anywhere, hence no need for 'ok_to_place_ship_at'
    fleet = place_ship_at(r.randint(0, 9), r.randint(
        0, 9), r.choice([True, False]), 4, fleet)

    # placing the two cruisers next
    cruiser_count = 0
    while cruiser_count < 2:
        row, col, horiz = r.randint(0, 9), r.randint(
            0, 9), r.choice([True, False])
        if ok_to_place_ship_at(row, col, horiz, 3, fleet):
            fleet = place_ship_at(row, col, horiz, 3, fleet)
            cruiser_count += 1

    # placing the three destroyers next
    destroyer_count = 0
    while destroyer_count < 3:
        row, col, horiz = r.randint(0, 9), r.randint(
            0, 9), r.choice([True, False])
        if ok_to_place_ship_at(row, col, horiz, 2, fleet):
            fleet = place_ship_at(row, col, horiz, 2, fleet)
            destroyer_count += 1

    # placing the four submarines finally
    sub_count = 0
    while sub_count < 4:
        row, col, horiz = r.randint(0, 9), r.randint(
            0, 9), r.choice([True, False])
        if ok_to_place_ship_at(row, col, horiz, 1, fleet):
            fleet = place_ship_at(row, col, horiz, 1, fleet)
            sub_count += 1

    return fleet


def check_if_hits(row, column, fleet):
    '''returns Boolean value, which is `True` if the shot of the human player
       at the square represented by `row` and `column` hits any of the ships of `fleet`, and `False` otherwise'''

    hit_set = {(row, column)}
    # loop through each ship in fleet
    for ship in fleet:
        # loop through each ship's coordinates using the get_coordinate function
        # if hit_set is subset of any of the ship's coordinates in the fleet return True
        if hit_set.issubset(get_coordinates(ship)):
            break
    # The ship that got hit is the ship just before the break statement

    return hit_set.issubset(get_coordinates(ship))


def hit(row, column, fleet):
    '''returns a tuple `(fleet1, ship)` where `ship` is the ship from the fleet `fleet` that receives a hit by the shot at the #
    square represented by `row` and `column`, and `fleet1` is the fleet resulting from this hit.
    It may be assumed that shooting at the square `row, column` results in hitting of some ship in `fleet` '''

    hit_set = {(row, column)}
    # making a deep copy of the original fleet so not to disturb the original fleet
    fleet1 = copy.deepcopy(fleet)

    # loop through each ship in fleet

    for ship in fleet:
        # loop through each ship's coordinates using the get_coordinate function
        # if hit_set is subset of any of the ship's coordinates in the fleet return the ship that was hit
        if hit_set.issubset(get_coordinates(ship)):
            break
    # Out of the loop 'ship' is the ship that got hit. Finding its index in fleet1
    # ship now refers to the ship in the original fleet
    index = fleet1.index(ship)
    # finding the ship in the new list and updating its hit coordinates
    fleet1[index][4].update(hit_set)

    return(fleet1, fleet1[index])


def are_unsunk_ships_left(fleet):
    '''returns Boolean value, which is `True` if there are ships in the fleet that are still not sunk, and `False` otherwise'''
    unsunk_count = 0
    for ship in fleet:
        if not is_sunk(ship):
            unsunk_count += 1

    if unsunk_count != 0:
        return True
    else:
        return False


def main():
    ''' main function to start the game '''
    current_fleet = randomly_place_all_ships()

    print("WELCOME TO THE BATTLESHIP GAME. \n  Ships are randomly placed. \n  Game starts now. \n  Good Luck !\n")

    game_over = False
    shots = 0
    shots_set = set()

    while not game_over:
        try:
            loc_str = input(
                "Enter row and column to shoot (separted by space). Enter 'quit' at any time to quit the game: ")
            # check if user enters quit and exit the game with message else proceed with the game
            if loc_str.lower() == 'quit':
                sys.exit("Game Ended! \nThanks for playing Battleship!")
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
                # uncomment the below if you want to visualise
                #ext.visualise(current_fleet, shots_set)

        except ValueError:
            print(
                "Invalid Entry. If you want to quit, enter 'quit' else enter valid coordinates.")
    print("Game over! You required", shots, "shots.")


if __name__ == '__main__':  # keep this in
    main()
