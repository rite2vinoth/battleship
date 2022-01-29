import pytest
from battleships import *

# declare global variables for ships and fleet
s1 = (1, 1, True, 3, set())
s2 = (1, 6, False, 2, set())
s3 = (3, 0, True, 1, set())
s4 = (3, 2, True, 3, set())
s5 = (2, 9, False, 2, set())
s6 = (5, 1, True, 2, set())
s7 = (5, 4, True, 1, set())
s8 = (5, 7, True, 1, set())
s9 = (9, 0, True, 1, set())
s10 = (6, 9, False, 4, set())
fleet = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
fleet2 = [(1, 1, True, 3, set()), (1, 6, False, 2, {(1, 6)}), (2, 9, False, 2, set()), (3, 0, True, 1, set()),
          (3, 2, True, 3, {(3, 3), (3, 4)}), (5, 1, True, 2, {(5, 2)}), (5, 4, True, 1, set()), (5, 7, True, 1, set()), (6, 9, False, 4, set()), (9, 0, True, 1, set())]


def test_get_coordinates1():
    actual = get_coordinates(s1)
    expected = {(1, 1), (1, 2), (1, 3)}
    assert actual == expected


def test_get_coordinates2():
    actual = get_coordinates(s3)
    expected = {(3, 0)}
    assert actual == expected


def test_get_coordinates3():
    actual = get_coordinates(s10)
    expected = {(6, 9), (7, 9), (8, 9), (9, 9)}
    assert actual == expected


def test_get_coordinates4():
    actual = get_coordinates(s5)
    expected = {(2, 9), (3, 9)}
    assert actual == expected


def test_get_coordinates5():
    actual = get_coordinates(s4)
    expected = {(3, 2), (3, 3), (3, 4)}
    assert actual == expected


def test_is_sunk1():
    s = (2, 3, False, 3, {(2, 3), (3, 3), (4, 3)})
    assert is_sunk(s) == True


def test_is_sunk2():
    s = (6, 7, True, 2, {(6, 6)})
    assert is_sunk(s) == False


def test_is_sunk3():
    s = (9, 0, True, 1, {(9, 0)})
    assert is_sunk(s) == True


def test_is_sunk4():
    s = (5, 4, True, 4, {(5, 4), (5, 6)})
    assert is_sunk(s) == False


def test_is_sunk5():
    s = (1, 1, True, 3, {(1, 1), (1, 2), (1, 3)})
    assert is_sunk(s) == True


def test_ship_type1():
    s = (5, 4, True, 4, {(5, 4), (5, 6)})
    assert ship_type(s) == "battleship"


def test_ship_type2():
    s = (7, 5, False, 2, {(8, 5)})
    assert ship_type(s) == "destroyer"


def test_ship_type3():
    s = (9, 0, True, 1, set())
    assert ship_type(s) == "submarine"


def test_ship_type4():
    s = (1, 1, True, 3, {(1, 1)})
    assert ship_type(s) == "cruiser"


def test_ship_type5():
    s = (3, 2, True, 3, set())
    assert ship_type(s) == "cruiser"


def test_is_open_sea1():
    assert is_open_sea(7, 6, fleet) == True


def test_is_open_sea2():
    assert is_open_sea(5, 8, fleet) == False


def test_is_open_sea3():
    assert is_open_sea(6, 3, fleet) == False


def test_is_open_sea4():
    assert is_open_sea(8, 2, fleet) == True


def test_is_open_sea5():
    assert is_open_sea(0, 4, fleet) == False


def test_ok_to_place_ship_at1():
    assert ok_to_place_ship_at(5, 6, True, 3, fleet) == False


def test_ok_to_place_ship_at2():
    assert ok_to_place_ship_at(7, 5, True, 2, fleet) == True


def test_ok_to_place_ship_at3():
    assert ok_to_place_ship_at(
        8, 2, False, 1, fleet) == True


def test_ok_to_place_ship_at4():
    assert ok_to_place_ship_at(1, 4, False, 4, fleet) == False


def test_ok_to_place_ship_at5():
    assert ok_to_place_ship_at(6, 8, True, 2, fleet) == False


f1 = [s1, s2]
f2 = [s2, s3, s4]
f3 = [s9, s10]
f4 = [s5]
f5 = [s1, s2, s3, s4, s5, s6, s8, s9, s10]


def test_place_ship_at1():
    actual = place_ship_at(6, 9, False, 4, f1)
    actual.sort()
    expected = [s1, s2, (6, 9, False, 4, set())]
    expected.sort()
    assert expected == actual


def test_place_ship_at2():
    actual = place_ship_at(1, 1, True, 3, f2)
    actual.sort()
    expected = [s2, s3, s4, (1, 1, True, 3, set())]
    expected.sort()
    assert expected == actual


def test_place_ship_at3():
    actual = place_ship_at(1, 6, False, 2, f3)
    actual.sort()
    expected = [s9, s10, (1, 6, False, 2, set())]
    expected.sort()
    assert expected == actual


def test_place_ship_at4():
    actual = place_ship_at(9, 0, True, 1, f4)
    actual.sort()
    expected = [s5, (9, 0, True, 1, set())]
    expected.sort()
    assert expected == actual


def test_place_ship_at5():
    actual = place_ship_at(5, 4, True, 1, f5)
    actual.sort()
    expected = [s1, s2, s3, s4, s5, s6, s8, s9, s10, (5, 4, True, 1, set())]
    expected.sort()
    assert expected == actual


def test_check_if_hits1():
    assert check_if_hits(5, 7, fleet) == True
    # provide at least four tests in total for check_if_hits by the project submission deadline


def test_check_if_hits2():
    assert check_if_hits(7, 7, fleet) == False


def test_check_if_hits3():
    assert check_if_hits(6, 9, fleet) == True


def test_check_if_hits4():
    assert check_if_hits(0, 4, fleet) == False


def test_check_if_hits5():
    assert check_if_hits(8, 6, fleet) == False


def test_hit1():
    (actual, s) = hit(5, 1, fleet)
    actual.sort()
    expected = [s1, s2, s3, s4, s5,
                (5, 1, True, 2, {(5, 1)}), s7, s8, s9, s10]
    expected.sort()
    assert (actual, s) == (expected, (5, 1, True, 2, {(5, 1)}))


def test_hit2():
    (actual, s) = hit(5, 4, fleet)
    actual.sort()
    expected = [s1, s2, s3, s4, s5,
                s6, (5, 4, True, 1, {(5, 4)}), s8, s9, s10]
    expected.sort()
    assert (actual, s) == (expected, (5, 4, True, 1, {(5, 4)}))


def test_hit3():
    (actual, s) = hit(7, 9, fleet)
    actual.sort()
    expected = [s1, s2, s3, s4, s5,
                s6, s7, s8, s9, (6, 9, False, 4, {(7, 9)})]
    expected.sort()
    assert (actual, s) == (expected, (6, 9, False, 4, {(7, 9)}))

# for the next two tests we use fleet2 (same fleet with hits already) to test if new hit coordinates are getting added


def test_hit4():
    (actual, s) = hit(3, 2, fleet2)
    actual.sort()
    expected = [(1, 1, True, 3, set()), (1, 6, False, 2, {(1, 6)}), (2, 9, False, 2, set()), (3, 0, True, 1, set()),
                (3, 2, True, 3, {(3, 3), (3, 4), (3, 2)}), (5, 1, True, 2, {(5, 2)}), (5, 4, True, 1, set()), (5, 7, True, 1, set()), (6, 9, False, 4, set()), (9, 0, True, 1, set())]
    expected.sort()
    assert (actual, s) == (expected, (3, 2, True, 3, {(3, 3), (3, 4), (3, 2)}))


def test_hit5():
    (actual, s) = hit(2, 6, fleet2)
    actual.sort()
    expected = [(1, 1, True, 3, set()), (1, 6, False, 2, {(1, 6), (2, 6)}), (2, 9, False, 2, set()), (3, 0, True, 1, set()),
                (3, 2, True, 3, {(3, 3), (3, 4)}), (5, 1, True, 2, {(5, 2)}), (5, 4, True, 1, set()), (5, 7, True, 1, set()), (6, 9, False, 4, set()), (9, 0, True, 1, set())]
    expected.sort()
    assert (actual, s) == (expected, (1, 6, False, 2, {(1, 6), (2, 6)}))


fleet_all_sunk = [(1, 1, True, 3, {(1, 1), (1, 2), (1, 3)}), (1, 6, False, 2, {(1, 6), (2, 6)}), (2, 9, False, 2, {(2, 9), (3, 9)}), (3, 0, True, 1, {(3, 0)}),
                  (3, 2, True, 3, {(3, 3), (3, 4), (3, 2)}), (5, 1, True, 2, {
                      (5, 2), (5, 1)}), (5, 4, True, 1, {(5, 4)}),
                  (5, 7, True, 1, {(5, 7)}), (6, 9, False, 4, {(6, 9), (7, 9), (8, 9), (9, 9)}), (9, 0, True, 1, {(9, 0)})]

fleet_all_sunk2 = [(1, 1, True, 3, {(1, 1), (1, 2), (1, 3)}), (1, 6, False, 2, {(1, 6), (2, 6)}), (2, 9, False, 2, {(2, 9), (3, 9)}), (3, 0, True, 1, {(3, 0)}),
                   (3, 2, True, 3, {(3, 3), (3, 4), (3, 2)}), (5, 1, True, 2, {
                       (5, 2), (5, 1)}), (5, 4, True, 1, {(5, 4)}),
                   (5, 7, True, 1, {(5, 7)}), (9, 4, True, 4, {(9, 4), (9, 5), (9, 6), (9, 7)}), (7, 7, True, 1, {(7, 7)})]


def test_are_unsunk_ships_left1():
    assert are_unsunk_ships_left(fleet) == True


def test_are_unsunk_ships_left2():
    assert are_unsunk_ships_left(fleet_all_sunk) == False


def test_are_unsunk_ships_left3():
    assert are_unsunk_ships_left(fleet2) == True


def test_are_unsunk_ships_left4():
    assert are_unsunk_ships_left(fleet_all_sunk2) == False


def test_are_unsunk_ships_left5():
    assert are_unsunk_ships_left(fleet2) == True
