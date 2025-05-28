class Coords:
    def __init__(self, left, upper, right, lower):
        self.left = left
        self.upper = upper
        self.right = right
        self.lower = lower



def build_set_coords_map() :
    base_coords = Coords(525, 437, 582, 474)
    gym_coords = Coords(525, 437, 582, 474)
    neo_coords = Coords(525, 437, 582, 474)

    ex_coords = Coords(540, 790, 582, 820)

    e_card_coords = Coords(530, 720, 575, 760)

    diamond_pearl_coords = Coords(550, 780, 590, 810)
    heart_gold_soul_silver_coords = Coords(550, 780, 590, 810)
    x_y_coords = Coords(550, 780, 590, 810)
    platinum_coords = Coords(550, 780, 590, 810)
    black_white_coords = Coords(550, 780, 590, 810)

    sun_moon_coords = Coords(50, 950, 125, 985)
    sword_shield_coords = Coords(50, 950, 125, 985)

    scarlet_violet_coords = Coords(550, 780, 590, 810)

    # Promos? 
    np_coords = Coords(540, 790, 582, 820)

    pop_coords = Coords(550, 780, 590, 810)

    other_coords = Coords(550, 780, 590, 810)

    series_coords_map = {}
    series_coords_map["Base"] = base_coords
    series_coords_map["Gym"] = gym_coords
    series_coords_map["Neo"] = neo_coords

    series_coords_map["EX"] = ex_coords

    series_coords_map["E-Card"] = e_card_coords

    series_coords_map["Diamond & Pearl"] = diamond_pearl_coords

    series_coords_map["HeartGold & SoulSilver"] = heart_gold_soul_silver_coords
    series_coords_map["XY"] = x_y_coords
    series_coords_map["Scarlet & Violet"] = scarlet_violet_coords
    series_coords_map["Sword & Shield"] = sword_shield_coords
    series_coords_map["Platinum"] = platinum_coords
    series_coords_map["NP"] = np_coords
    series_coords_map["Sun & Moon"] = sun_moon_coords
    series_coords_map["POP"] = pop_coords
    series_coords_map["Black & White"] = black_white_coords
    series_coords_map["Other"] = other_coords

    return series_coords_map