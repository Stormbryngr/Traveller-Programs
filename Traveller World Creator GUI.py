import tkinter as tk
from tkinter import ttk, messagebox

import random
def roll_dice(num=1, sides=6):
    return sum(random.randint(1, sides) for _ in range(num))

def determine_starport(pop_code):
    # Determine DM based on population
    if pop_code <= 2:
        dm = -2
    elif pop_code in [3, 4]:
        dm = -1
    elif pop_code in [8, 9]:
        dm = 1
    elif pop_code >= 10:
        dm = 2
    else:
        dm = 0

    # Roll for Starport Class
    roll = roll_dice(2) + dm
    if roll <= 2:
        starport_class = "X"
    elif roll <= 4:
        starport_class = "E"
    elif roll <= 6:
        starport_class = "D"
    elif roll <= 8:
        starport_class = "C"
    elif roll <= 10:
        starport_class = "B"
    else:
        starport_class = "A"

    # Roll for Bases
    bases = []
    base_requirements = {
        "A": {"Military": 8, "Naval": 8, "Scout": 10},
        "B": {"Military": 8, "Naval": 8, "Scout": 9},
        "C": {"Military": 10, "Scout": 9},
        "D": {"Scout": 8, "Corsair": 12},
        "E": {"Corsair": 10},
        "X": {"Corsair": 10}
    }

    for base, requirement in base_requirements[starport_class].items():
        if roll_dice(2) >= requirement:
            bases.append(base)

    return starport_class, f"Class {starport_class}, Bases: {', '.join(bases) if bases else 'None'}"

def generate_government(population_code):
    roll = roll_dice(2) - 7 + population_code
    governments = [
        (0, "None"),
        (1, "Company/Corporation"),
        (2, "Participating Democracy"),
        (3, "Self-Perpetuating Oligarchy"),
        (4, "Representative Democracy"),
        (5, "Feudal Technocracy"),
        (6, "Captive Government"),
        (7, "Balkanization"),
        (8, "Civil Service Bureaucracy"),
        (9, "Impersonal Bureaucracy"),
        (10, "Charismatic Dictator"),
        (11, "Non-Charismatic Leader"),
        (12, "Charismatic Oligarchy"),
        (13, "Religious Dictatorship"),
        (14, "Religious Autocracy"),
        (15, "Totalitarian Oligarchy")
    ]

    for gov in governments:
        if roll == gov[0]:
            return {
                'Code': gov[0],
                'Type': gov[1]
            }

def generate_factions(government_code):
    dm = 0
    if 0 <= government_code <= 7:
        dm = 1
    elif government_code >= 10:
        dm = -1

    num_factions = roll_dice(1, 3) + dm
    factions = []

    for _ in range(num_factions):
        strength_roll = roll_dice(2)
        if strength_roll <= 3:
            factions.append("Obscure group")
        elif strength_roll <= 5:
            factions.append("Fringe group")
        elif strength_roll <= 7:
            factions.append("Minor group")
        elif strength_roll <= 9:
            factions.append("Notable group")
        elif strength_roll <= 11:
            factions.append("Significant group")
        else:
            factions.append("Overwhelming group")

    return factions

def determine_tech_level(starport_class, size_roll, atmosphere_roll, hydrographics, population_roll, government_code):
    # Starting with a roll of 1D
    tech_roll = roll_dice(1, 6)
    tech_modifiers = {
        'Starport': {
            'A': 6,
            'B': 4,
            'C': 2,
            'D': 1,
            'E': 1,
            'F': 1,
            'X': -4
        },
        'Size': {
            0: 2,
            1: 2,
            2: 1,
            3: 1,
            4: 1
        },
        'Atmosphere': {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            7: 2,
            9: 4,
            10: 2,
            11: 2,
            12: 2,
            13: 2,
            14: 2
        },
        'Hydrographics': {
            9: 1
        },
        'Population': {
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: 1,
            9: 2,
            10: 4,
            11: 4,
            12: 4
        },
        'Government': {
            0: 1,
            5: 1,
            7: 2,
            13: 1,
            14: 1
        }
    }

    # Modifying based on the starport class
    tech_roll += tech_modifiers['Starport'][starport_class]
    tech_roll += tech_modifiers['Size'].get(size_roll, 0)
    tech_roll += tech_modifiers['Atmosphere'].get(atmosphere_roll, 0)
    tech_roll += tech_modifiers['Hydrographics'].get(hydrographics, 0)
    tech_roll += tech_modifiers['Population'].get(population_roll, 0)
    tech_roll += tech_modifiers['Government'].get(government_code, 0)

    return tech_roll

def generate_world():
    # Roll for size (0-10)
    size_roll = roll_dice(2) - 2

    # Roll for atmosphere (0-15)
    atmosphere_roll = roll_dice(1) + size_roll

    atmosphere_descriptions = {
    0: {"Composition": "None (Moon)", "Pressure": "0.00", "Gear": "Vacc Suit"},
    1: {"Composition": "Trace (Mars)", "Pressure": "0.001 to 0.09", "Gear": "Vacc Suit"},
    2: {"Composition": "Very Thin, Tainted", "Pressure": "0.1 to 0.42", "Gear": "Respirator, Filter"},
    3: {"Composition": "Very Thin", "Pressure": "0.1 to 0.42", "Gear": "Respirator"},
    4: {"Composition": "Thin, Tainted", "Pressure": "0.43 to 0.7", "Gear": "Filter"},
    5: {"Composition": "Thin", "Pressure": "0.43 to 0.7", "Gear": None},
    6: {"Composition": "Standard (Earth)", "Pressure": "0.71-1.49", "Gear": None},
    7: {"Composition": "Standard, Tainted", "Pressure": "0.71-1.49", "Gear": "Filter"},
    8: {"Composition": "Dense", "Pressure": "1.5 to 2.49", "Gear": None},
    9: {"Composition": "Dense, Tainted", "Pressure": "1.5 to 2.49", "Gear": "Filter"},
    10: {"Composition": "Exotic", "Pressure": "Varies", "Gear": "Air Supply"},
    11: {"Composition": "Corrosive (Venus)", "Pressure": "Varies", "Gear": "Vacc Suit"},
    12: {"Composition": "Insidious", "Pressure": "Varies", "Gear": "Vacc Suit"},
    13: {"Composition": "Very Dense", "Pressure": "2.5+", "Gear": None},
    14: {"Composition": "Low", "Pressure": "0.5 or less", "Gear": None},
    15: {"Composition": "Unusual", "Pressure": "Varies", "Gear": "Varies"},
}


    # Roll for hydrographics (0-10)
    hydro = roll_dice(2) - 7 + atmosphere_roll
    hydro = max(0, min(hydro, 10))

    # Roll for population (0-12)
    pop_roll = roll_dice(2) - 2
    starport_class, starport_description = determine_starport(pop_roll)

    # Determine government type based on population
    government = generate_government(pop_roll)

    # Generate factions based on government
    factions = generate_factions(government['Code'])

    # Determine tech level
    tech_level = determine_tech_level(starport_class, size_roll, atmosphere_roll, hydro, pop_roll, government['Code'])

    atmosphere_description = atmosphere_descriptions[atmosphere_roll]
    atmosphere_summary = f"Atmosphere: {atmosphere_roll} ({atmosphere_description['Composition']}), " \
                         f"Pressure: {atmosphere_description['Pressure']}"
    if atmosphere_description["Gear"]:
        atmosphere_summary += f", Gear: {atmosphere_description['Gear']}"

    world_summary = f"""
    World Summary:
    Size: {size_roll}
    Atmosphere: {atmosphere_summary}
    Hydrographics: {hydro}0%
    Population: {pop_roll}
    Government: {government['Type']}
    Starport: {starport_description}
    Factions: {', '.join(factions) if factions else 'None'}
    Tech Level: {tech_level}
    """

    return world_summary.strip()

print(generate_world())

def on_generate_click():
    world = generate_world()
    result_text.config(state=tk.NORMAL)  # Enable editing
    result_text.delete(1.0, tk.END)      # Clear previous world info
    result_text.insert(tk.END, world)    # Insert new world info
    result_text.config(state=tk.DISABLED)  # Disable editing

app = tk.Tk()
app.title("World Generator")

frame = ttk.Frame(app, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

generate_btn = ttk.Button(frame, text="Generate World", command=on_generate_click)
generate_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

result_text = tk.Text(frame, width=100, height=15)
result_text.grid(row=1, column=0, sticky=(tk.W, tk.E))
result_text.config(state=tk.DISABLED)  # Disable editing by default

app.mainloop()