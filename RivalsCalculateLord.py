import tkinter as tk
from tkinter import ttk, messagebox, font, colorchooser
import math
import json
import os

# Rank thresholds based on PDF (points needed to reach next rank from current)
RANK_THRESHOLDS = {
    "Agent": 500,
    "Knight": 1200,
    "Captain": 2000,
    "Centurion": 2400,
    "Lord": 0  # No further threshold
}

# Points per mission based on rank (from PDF)
POINTS_PER_MISSION = {
    "Agent": 10,
    "Knight": 25,
    "Captain": 40,
    "Centurion": 50,
    "Lord": 50  # Same as Centurion
}

class MarvelRivalsCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Marvel Rivals - Lord Rank Calculator v1.1 ~ Made by P13r")
        self.geometry("939x750")

        # Inputs
        self.current_rank_var = tk.StringVar(value="Agent")
        self.current_points_var = tk.StringVar(value="0")
        self.hours_played_var = tk.StringVar(value="0")

        # Mission data parsed from PDF
        self.mission_data = self.get_mission_data()

        # Role categorization for filter
        self.roles = {
            "Vanguard": ["Banner/Hulk", "Captain America", "Doctor Strange", "Groot", "Magneto", "Venom", "Emma Frost", "The Thing", "Peni Parker", "Angela", "Rogue"],
            "Duelist": ["Black Panther", "Black Widow", "Hawkeye", "Hela", "Iron Fist", "Iron Man", "Magik", "Moon Knight", "Namor", "Psylocke", "Scarlet Witch", "Spider-Man", "Squirrel Girl", "Star-Lord", "Storm", "The Punisher", "Winter Soldier", "Wolverine", "Blade", "Human Torch", "Phoenix", "Daredevil"],
            "Strategist": ["Adam Warlock", "Cloak & Dagger", "Invisible Woman", "Jeff The Land Shark", "Loki", "Luna Snow", "Mantis", "Mister Fantastic", "Rocket Raccoon", "Thor", "Ultron", "Gambit"]
        }

        # Character and rank selection
        self.current_character = tk.StringVar(value="")
        self.current_mission_rank = tk.StringVar(value="Agent")  # Separate from player rank

        # Checklist for completed characters and missions
        self.completed_data = self.load_completed()
        self.completed_characters = self.completed_data.get("characters", set())
        self.completed_missions = self.completed_data.get("missions", {})

        self._updating_combobox = False

        # Mission storage (loaded dynamically)
        self.characters = {}
        self.mission_requirements = {}

        # Customization variables
        self.bg_color = tk.StringVar(value="#ffffff")  # Default white
        self.fg_color = tk.StringVar(value="#000000")  # Default black
        self.text_color = tk.StringVar(value="#000000")  # Default black
        self.font_family = tk.StringVar(value="Consolas")
        self.font_size = tk.StringVar(value="12")

        self.filter_var = tk.StringVar(value="All")

        # Sort state
        self.sort_ascending = tk.BooleanVar(value=True)  # True for A-Z, False for Z-A

        self._build_ui()
        self.update_char_combobox()  # Initialize character list

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_completed(self):
        if os.path.exists("completed.json"):
            with open("completed.json", "r") as f:
                data = json.load(f)
                # Convert lists back to sets for completed characters
                data["characters"] = set(data.get("characters", []))
                # Convert mission lists back to sets
                missions = data.get("missions", {})
                for char in missions:
                    for rank in missions[char]:
                        missions[char][rank] = set(missions[char][rank])
                data["missions"] = missions
                return data
        return {"characters": set(), "missions": {}}

    def save_completed(self):
        # Convert sets to lists for JSON serialization
        serializable_missions = {}
        for char in self.completed_missions:
            serializable_missions[char] = {}
            for rank in self.completed_missions[char]:
                serializable_missions[char][rank] = list(self.completed_missions[char][rank])
        with open("completed.json", "w") as f:
            json.dump({
                "characters": list(self.completed_characters),
                "missions": serializable_missions
            }, f)

    def on_close(self):
        self.save_completed()
        self.destroy()

    def get_mission_data(self):
        data = {}

        # Adam Warlock
        data["Adam Warlock"] = {
            "Agent": {
                "Heal Damage": {"requirement": 10000},
                "KOs/Assists": {"requirement": 20},
                "Revive Allies with Karmic Revival": {"requirement": 5}
            },
            "Knight": {
                "Heal Damage": {"requirement": 25000},
                "KOs/Assists": {"requirement": 50},
                "Revive Allies with Karmic Revival": {"requirement": 12}
            },
            "Captain": {
                "Heal Damage": {"requirement": 42000},
                "KOs/Assists": {"requirement": 80},
                "Revive Allies with Karmic Revival": {"requirement": 20}
            },
            "Centurion": {
                "Heal Damage": {"requirement": 54000},
                "KOs/Assists": {"requirement": 100},
                "Revive Allies with Karmic Revival": {"requirement": 25}
            },
            "Lord": {
                "Heal Damage": {"requirement": 54000},
                "KOs/Assists": {"requirement": 100},
                "Revive Allies with Karmic Revival": {"requirement": 25}
            }
        }

        # Angela
        data["Angela"] = {
            "Agent": {
                "Block Damage": {"requirement": 15000},
                "KOs": {"requirement": 12},
                "Accumulate Attack Charge": {"requirement": 3000}
            },
            "Knight": {
                "Block Damage": {"requirement": 35000},
                "KOs": {"requirement": 30},
                "Accumulate Attack Charge": {"requirement": 7500}
            },
            "Captain": {
                "Block Damage": {"requirement": 60000},
                "KOs": {"requirement": 50},
                "Accumulate Attack Charge": {"requirement": 12000}
            },
            "Centurion": {
                "Block Damage": {"requirement": 75000},
                "KOs": {"requirement": 65},
                "Accumulate Attack Charge": {"requirement": 15000}
            },
            "Lord": {
                "Block Damage": {"requirement": 75000},
                "KOs": {"requirement": 65},
                "Accumulate Attack Charge": {"requirement": 15000}
            }
        }

        # Banner/Hulk
        data["Banner/Hulk"] = {
            "Agent": {
                "Block Damage": {"requirement": 21000},
                "KOs": {"requirement": 10},
                "Add Indestructible Guard to Allies": {"requirement": 20}
            },
            "Knight": {
                "Block Damage": {"requirement": 55000},
                "KOs": {"requirement": 25},
                "Add Indestructible Guard to Allies": {"requirement": 50}
            },
            "Captain": {
                "Block Damage": {"requirement": 85000},
                "KOs": {"requirement": 42},
                "Add Indestructible Guard to Allies": {"requirement": 80}
            },
            "Centurion": {
                "Block Damage": {"requirement": 110000},
                "KOs": {"requirement": 55},
                "Add Indestructible Guard to Allies": {"requirement": 100}
            },
            "Lord": {
                "Block Damage": {"requirement": 110000},
                "KOs": {"requirement": 55},
                "Add Indestructible Guard to Allies": {"requirement": 100}
            }
        }

        # Black Panther
        data["Black Panther"] = {
            "Agent": {
                "Deal Damage": {"requirement": 7500},
                "Final Hits": {"requirement": 10},
                "Use Spirit Road": {"requirement": 30}
            },
            "Knight": {
                "Deal Damage": {"requirement": 20000},
                "Final Hits": {"requirement": 25},
                "Use Spirit Road": {"requirement": 70}
            },
            "Captain": {
                "Deal Damage": {"requirement": 30000},
                "Final Hits": {"requirement": 40},
                "Use Spirit Road": {"requirement": 120}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 38000},
                "Final Hits": {"requirement": 50},
                "Use Spirit Road": {"requirement": 150}
            },
            "Lord": {
                "Deal Damage": {"requirement": 38000},
                "Final Hits": {"requirement": 50},
                "Use Spirit Road": {"requirement": 150}
            }
        }

        # Black Widow
        data["Black Widow"] = {
            "Agent": {
                "Deal Damage": {"requirement": 6000},
                "Land Final Hits": {"requirement": 10},
                "Achieve Critical Hits": {"requirement": 5}
            },
            "Knight": {
                "Deal Damage": {"requirement": 15000},
                "Land Final Hits": {"requirement": 25},
                "Achieve Critical Hits": {"requirement": 15}
            },
            "Captain": {
                "Deal Damage": {"requirement": 25000},
                "Land Final Hits": {"requirement": 40},
                "Achieve Critical Hits": {"requirement": 25}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 30000},
                "Land Final Hits": {"requirement": 50},
                "Achieve Critical Hits": {"requirement": 30}
            },
            "Lord": {
                "Deal Damage": {"requirement": 30000},
                "Land Final Hits": {"requirement": 50},
                "Achieve Critical Hits": {"requirement": 30}
            }
        }

        # Captain America
        data["Captain America"] = {
            "Agent": {
                "Block Damage": {"requirement": 20000},
                "KOs": {"requirement": 12},
                "Grant Bonus Health with Hero Charge": {"requirement": 3500}
            },
            "Knight": {
                "Block Damage": {"requirement": 45000},
                "KOs": {"requirement": 30},
                "Grant Bonus Health with Hero Charge": {"requirement": 9000}
            },
            "Captain": {
                "Block Damage": {"requirement": 70000},
                "KOs": {"requirement": 50},
                "Grant Bonus Health with Hero Charge": {"requirement": 14000}
            },
            "Centurion": {
                "Block Damage": {"requirement": 90000},
                "KOs": {"requirement": 65},
                "Grant Bonus Health with Hero Charge": {"requirement": 18000}
            },
            "Lord": {
                "Block Damage": {"requirement": 90000},
                "KOs": {"requirement": 65},
                "Grant Bonus Health with Hero Charge": {"requirement": 18000}
            }
        }

        # Cloak & Dagger
        data["Cloak & Dagger"] = {
            "Agent": {
                "Heal Damage": {"requirement": 10000},
                "KOs/Assists": {"requirement": 15},
                "Use Terror Cape to Hit Heroes": {"requirement": 10}
            },
            "Knight": {
                "Heal Damage": {"requirement": 25000},
                "KOs/Assists": {"requirement": 40},
                "Use Terror Cape to Hit Heroes": {"requirement": 24}
            },
            "Captain": {
                "Heal Damage": {"requirement": 42000},
                "KOs/Assists": {"requirement": 65},
                "Use Terror Cape to Hit Heroes": {"requirement": 36}
            },
            "Centurion": {
                "Heal Damage": {"requirement": 54000},
                "KOs/Assists": {"requirement": 80},
                "Use Terror Cape to Hit Heroes": {"requirement": 45}
            },
            "Lord": {
                "Heal Damage": {"requirement": 54000},
                "KOs/Assists": {"requirement": 80},
                "Use Terror Cape to Hit Heroes": {"requirement": 45}
            }
        }

        # Daredevil
        data["Daredevil"] = {
            "Agent": {
                "Deal Damage": {"requirement": 7500},
                "Land Final Hits": {"requirement": 10},
                "Accumulate Fury": {"requirement": 140}
            },
            "Knight": {
                "Deal Damage": {"requirement": 20000},
                "Land Final Hits": {"requirement": 25},
                "Accumulate Fury": {"requirement": 350}
            },
            "Captain": {
                "Deal Damage": {"requirement": 30000},
                "Land Final Hits": {"requirement": 40},
                "Accumulate Fury": {"requirement": 560}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 38000},
                "Land Final Hits": {"requirement": 50},
                "Accumulate Fury": {"requirement": 700}
            },
            "Lord": {
                "Deal Damage": {"requirement": 38000},
                "Land Final Hits": {"requirement": 10},
                "Accumulate Fury": {"requirement": 700}
            }
        }

        # Doctor Strange
        data["Doctor Strange"] = {
            "Agent": {
                "Block Damage": {"requirement": 21000},
                "KOs": {"requirement": 12},
                "Stun Enemies with Eye of Agamotto": {"requirement": 6}
            },
            "Knight": {
                "Block Damage": {"requirement": 55000},
                "KOs": {"requirement": 30},
                "Stun Enemies with Eye of Agamotto": {"requirement": 15}
            },
            "Captain": {
                "Block Damage": {"requirement": 85000},
                "KOs": {"requirement": 50},
                "Stun Enemies with Eye of Agamotto": {"requirement": 24}
            },
            "Centurion": {
                "Block Damage": {"requirement": 110000},
                "KOs": {"requirement": 65},
                "Stun Enemies with Eye of Agamotto": {"requirement": 30}
            },
            "Lord": {
                "Block Damage": {"requirement": 110000},
                "KOs": {"requirement": 65},
                "Stun Enemies with Eye of Agamotto": {"requirement": 30}
            }
        }

        # Gambit
        data["Gambit"] = {
            "Agent": {
                "Heal Damage": {"requirement": 9000},
                "KOs/Assists": {"requirement": 25},
                "Use Sleight of Hand Stacks": {"requirement": 50}
            },
            "Knight": {
                "Heal Damage": {"requirement": 23000},
                "KOs/Assists": {"requirement": 60},
                "Use Sleight of Hand Stacks": {"requirement": 125}
            },
            "Captain": {
                "Heal Damage": {"requirement": 35000},
                "KOs/Assists": {"requirement": 95},
                "Use Sleight of Hand Stacks": {"requirement": 200}
            },
            "Centurion": {
                "Heal Damage": {"requirement": 45000},
                "KOs/Assists": {"requirement": 120},
                "Use Sleight of Hand Stacks": {"requirement": 250}
            },
            "Lord": {
                "Heal Damage": {"requirement": 45000},
                "KOs/Assists": {"requirement": 120},
                "Use Sleight of Hand Stacks": {"requirement": 250}
            }
        }

        # Groot
        data["Groot"] = {
            "Agent": {
                "Block Damage": {"requirement": 27000},
                "KOs": {"requirement": 12},
                "Build Wooden Walls": {"requirement": 50}
            },
            "Knight": {
                "Block Damage": {"requirement": 70000},
                "KOs": {"requirement": 30},
                "Build Wooden Walls": {"requirement": 120}
            },
            "Captain": {
                "Block Damage": {"requirement": 110000},
                "KOs": {"requirement": 50},
                "Build Wooden Walls": {"requirement": 200}
            },
            "Centurion": {
                "Block Damage": {"requirement": 140000},
                "KOs": {"requirement": 65},
                "Build Wooden Walls": {"requirement": 250}
            },
            "Lord": {
                "Block Damage": {"requirement": 140000},
                "KOs": {"requirement": 65},
                "Build Wooden Walls": {"requirement": 250}
            }
        }

        # Hawkeye
        data["Hawkeye"] = {
            "Agent": {
                "Deal Damage": {"requirement": 10000},
                "Final Hits": {"requirement": 12},
                "Score Hits with Hypersonic Arrow": {"requirement": 40}
            },
            "Knight": {
                "Deal Damage": {"requirement": 25000},
                "Final Hits": {"requirement": 24},
                "Score Hits with Hypersonic Arrow": {"requirement": 100}
            },
            "Captain": {
                "Deal Damage": {"requirement": 40000},
                "Final Hits": {"requirement": 36},
                "Score Hits with Hypersonic Arrow": {"requirement": 150}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 50000},
                "Final Hits": {"requirement": 55},
                "Score Hits with Hypersonic Arrow": {"requirement": 180}
            },
            "Lord": {
                "Deal Damage": {"requirement": 50000},
                "Final Hits": {"requirement": 55},
                "Score Hits with Hypersonic Arrow": {"requirement": 180}
            }
        }

        # Hela
        data["Hela"] = {
            "Agent": {
                "Deal Damage": {"requirement": 11000},
                "Final Hits": {"requirement": 12},
                "Stun Enemies with Soul Drainer": {"requirement": 6}
            },
            "Knight": {
                "Deal Damage": {"requirement": 28000},
                "Final Hits": {"requirement": 30},
                "Stun Enemies with Soul Drainer": {"requirement": 15}
            },
            "Captain": {
                "Deal Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 50},
                "Stun Enemies with Soul Drainer": {"requirement": 25}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 55000},
                "Final Hits": {"requirement": 65},
                "Stun Enemies with Soul Drainer": {"requirement": 32}
            },
            "Lord": {
                "Deal Damage": {"requirement": 55000},
                "Final Hits": {"requirement": 65},
                "Stun Enemies with Soul Drainer": {"requirement": 32}
            }
        }

        # Invisible Woman
        data["Invisible Woman"] = {
            "Agent": {
                "Heal Damage": {"requirement": 10000},
                "KOs/Assists": {"requirement": 25},
                "Block Damage with Guardian Shield": {"requirement": 5000}
            },
            "Knight": {
                "Heal Damage": {"requirement": 25000},
                "KOs/Assists": {"requirement": 60},
                "Block Damage with Guardian Shield": {"requirement": 12500}
            },
            "Captain": {
                "Heal Damage": {"requirement": 42000},
                "KOs/Assists": {"requirement": 95},
                "Block Damage with Guardian Shield": {"requirement": 20000}
            },
            "Centurion": {
                "Heal Damage": {"requirement": 54000},
                "KOs/Assists": {"requirement": 120},
                "Block Damage with Guardian Shield": {"requirement": 25000}
            },
            "Lord": {
                "Heal Damage": {"requirement": 54000},
                "KOs/Assists": {"requirement": 120},
                "Block Damage with Guardian Shield": {"requirement": 25000}
            }
        }

        # Iron Fist
        data["Iron Fist"] = {
            "Agent": {
                "Deal Damage": {"requirement": 6000},
                "Final Hits": {"requirement": 8},
                "Gain Bonus Heals with Dragon's Defense": {"requirement": 1500}
            },
            "Knight": {
                "Deal Damage": {"requirement": 15000},
                "Final Hits": {"requirement": 25},
                "Gain Bonus Heals with Dragon's Defense": {"requirement": 3500}
            },
            "Captain": {
                "Deal Damage": {"requirement": 25000},
                "Final Hits": {"requirement": 35},
                "Gain Bonus Heals with Dragon's Defense": {"requirement": 6000}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 30000},
                "Final Hits": {"requirement": 45},
                "Gain Bonus Heals with Dragon's Defense": {"requirement": 7500}
            },
            "Lord": {
                "Deal Damage": {"requirement": 30000},
                "Final Hits": {"requirement": 45},
                "Gain Bonus Heals with Dragon's Defense": {"requirement": 7500}
            }
        }

        # Iron Man
        data["Iron Man"] = {
            "Agent": {
                "Deal Damage": {"requirement": 8000},
                "Final Hits": {"requirement": 8},
                "Directly Hit Enemies with Repulsor Blast": {"requirement": 50}
            },
            "Knight": {
                "Deal Damage": {"requirement": 20000},
                "Final Hits": {"requirement": 20},
                "Directly Hit Enemies with Repulsor Blast": {"requirement": 120}
            },
            "Captain": {
                "Deal Damage": {"requirement": 35000},
                "Final Hits": {"requirement": 35},
                "Directly Hit Enemies with Repulsor Blast": {"requirement": 200}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 40},
                "Directly Hit Enemies with Repulsor Blast": {"requirement": 250}
            },
            "Lord": {
                "Deal Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 40},
                "Directly Hit Enemies with Repulsor Blast": {"requirement": 250}
            }
        }

        # Jeff The Land Shark
        data["Jeff The Land Shark"] = {
            "Agent": {
                "Heal Damage": {"requirement": 10000},
                "KOs/Assists": {"requirement": 20},
                "Swallow Heroes with It's Jeff!": {"requirement": 4}
            },
            "Knight": {
                "Heal Damage": {"requirement": 25000},
                "KOs/Assists": {"requirement": 50},
                "Swallow Heroes with It's Jeff!": {"requirement": 10}
            },
            "Captain": {
                "Heal Damage": {"requirement": 42000},
                "KOs/Assists": {"requirement": 80},
                "Swallow Heroes with It's Jeff!": {"requirement": 16}
            },
            "Centurion": {
                "Heal Damage": {"requirement": 54000},
                "KOs/Assists": {"requirement": 100},
                "Swallow Heroes with It's Jeff!": {"requirement": 20}
            },
            "Lord": {
                "Heal Damage": {"requirement": 54000},
                "KOs/Assists": {"requirement": 100},
                "Swallow Heroes with It's Jeff!": {"requirement": 20}
            }
        }

        # Loki
        data["Loki"] = {
            "Agent": {
                "Heal Damage": {"requirement": 10000},
                "KOs/Assists": {"requirement": 25},
                "Conjure Illusions": {"requirement": 40}
            },
            "Knight": {
                "Heal Damage": {"requirement": 25000},
                "KOs/Assists": {"requirement": 60},
                "Conjure Illusions": {"requirement": 100}
            },
            "Captain": {
                "Heal Damage": {"requirement": 42000},
                "KOs/Assists": {"requirement": 95},
                "Conjure Illusions": {"requirement": 150}
            },
            "Centurion": {
                "Heal Damage": {"requirement": 54000},
                "KOs/Assists": {"requirement": 120},
                "Conjure Illusions": {"requirement": 180}
            },
            "Lord": {
                "Heal Damage": {"requirement": 54000},
                "KOs/Assists": {"requirement": 120},
                "Conjure Illusions": {"requirement": 180}
            }
        }

        # Luna Snow
        data["Luna Snow"] = {
            "Agent": {
                "Heal Damage": {"requirement": 12000},
                "KOs/Assists": {"requirement": 25},
                "Freeze Enemies with Absolute Zero": {"requirement": 4}
            },
            "Knight": {
                "Heal Damage": {"requirement": 30000},
                "KOs/Assists": {"requirement": 60},
                "Freeze Enemies with Absolute Zero": {"requirement": 4}
            },
            "Captain": {
                "Heal Damage": {"requirement": 50000},
                "KOs/Assists": {"requirement": 95},
                "Freeze Enemies with Absolute Zero": {"requirement": 16}
            },
            "Centurion": {
                "Heal Damage": {"requirement": 60000},
                "KOs/Assists": {"requirement": 120},
                "Freeze Enemies with Absolute Zero": {"requirement": 20}
            },
            "Lord": {
                "Heal Damage": {"requirement": 60000},
                "KOs/Assists": {"requirement": 120},
                "Freeze Enemies with Absolute Zero": {"requirement": 20}
            }
        }

        # Magik
        data["Magik"] = {
            "Agent": {
                "Deal Damage": {"requirement": 8000},
                "Final Hits": {"requirement": 10},
                "Gain Bonus Health with Limbo's Might": {"requirement": 2500}
            },
            "Knight": {
                "Deal Damage": {"requirement": 20000},
                "Final Hits": {"requirement": 25},
                "Gain Bonus Health with Limbo's Might": {"requirement": 6000}
            },
            "Captain": {
                "Deal Damage": {"requirement": 35000},
                "Final Hits": {"requirement": 40},
                "Gain Bonus Health with Limbo's Might": {"requirement": 10000}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 50},
                "Gain Bonus Health with Limbo's Might": {"requirement": 13000}
            },
            "Lord": {
                "Deal Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 50},
                "Gain Bonus Health with Limbo's Might": {"requirement": 13000}
            }
        }

        # Magneto
        data["Magneto"] = {
            "Agent": {
                "Block Damage": {"requirement": 20000},
                "KOs": {"requirement": 15},
                "Absorb Damage with Meteor M": {"requirement": 2000}
            },
            "Knight": {
                "Block Damage": {"requirement": 45000},
                "KOs": {"requirement": 35},
                "Absorb Damage with Meteor M": {"requirement": 5000}
            },
            "Captain": {
                "Block Damage": {"requirement": 70000},
                "KOs": {"requirement": 60},
                "Absorb Damage with Meteor M": {"requirement": 8000}
            },
            "Centurion": {
                "Block Damage": {"requirement": 90000},
                "KOs": {"requirement": 75},
                "Absorb Damage with Meteor M": {"requirement": 10000}
            },
            "Lord": {
                "Block Damage": {"requirement": 90000},
                "KOs": {"requirement": 75},
                "Absorb Damage with Meteor M": {"requirement": 10000}
            }
        }

        # Mantis
        data["Mantis"] = {
            "Agent": {
                "Heal Damage": {"requirement": 10000},
                "KOs/Assists": {"requirement": 25},
                "Sedate Enemies with Spore Slumber": {"requirement": 5}
            },
            "Knight": {
                "Heal Damage": {"requirement": 25000},
                "KOs/Assists": {"requirement": 65},
                "Sedate Enemies with Spore Slumber": {"requirement": 12}
            },
            "Captain": {
                "Heal Damage": {"requirement": 42000},
                "KOs/Assists": {"requirement": 100},
                "Sedate Enemies with Spore Slumber": {"requirement": 20}
            },
            "Centurion": {
                "Heal Damage": {"requirement": 54000},
                "KOs/Assists": {"requirement": 130},
                "Sedate Enemies with Spore Slumber": {"requirement": 25}
            },
            "Lord": {
                "Heal Damage": {"requirement": 54000},
                "KOs/Assists": {"requirement": 130},
                "Sedate Enemies with Spore Slumber": {"requirement": 25}
            }
        }

        # Mister Fantastic
        data["Mister Fantastic"] = {
            "Agent": {
                "Deal Damage": {"requirement": 10000},
                "Final Hits": {"requirement": 10},
                "Inflate": {"requirement": 15}
            },
            "Knight": {
                "Deal Damage": {"requirement": 25000},
                "Final Hits": {"requirement": 25},
                "Inflate": {"requirement": 35}
            },
            "Captain": {
                "Deal Damage": {"requirement": 40000},
                "Final Hits": {"requirement": 40},
                "Inflate": {"requirement": 60}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 50000},
                "Final Hits": {"requirement": 50},
                "Inflate": {"requirement": 75}
            },
            "Lord": {
                "Deal Damage": {"requirement": 50000},
                "Final Hits": {"requirement": 50},
                "Inflate": {"requirement": 75}
            }
        }

        # Moon Knight
        data["Moon Knight"] = {
            "Agent": {
                "Deal Damage": {"requirement": 8000},
                "Final Hits": {"requirement": 8},
                "Inflict Hits on Enemies with Ankhs": {"requirement": 400}
            },
            "Knight": {
                "Deal Damage": {"requirement": 20000},
                "Final Hits": {"requirement": 20},
                "Inflict Hits on Enemies with Ankhs": {"requirement": 1000}
            },
            "Captain": {
                "Deal Damage": {"requirement": 35000},
                "Final Hits": {"requirement": 35},
                "Inflict Hits on Enemies with Ankhs": {"requirement": 1500}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 40},
                "Inflict Hits on Enemies with Ankhs": {"requirement": 2000}
            },
            "Lord": {
                "Deal Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 40},
                "Inflict Hits on Enemies with Ankhs": {"requirement": 2000}
            }
        }

        # Namor
        data["Namor"] = {
            "Agent": {
                "Deal Damage": {"requirement": 10000},
                "Final Hits": {"requirement": 8},
                "Summon Monstro Spawns": {"requirement": 50}
            },
            "Knight": {
                "Deal Damage": {"requirement": 25000},
                "Final Hits": {"requirement": 20},
                "Summon Monstro Spawns": {"requirement": 120}
            },
            "Captain": {
                "Deal Damage": {"requirement": 40000},
                "Final Hits": {"requirement": 35},
                "Summon Monstro Spawns": {"requirement": 200}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 50000},
                "Final Hits": {"requirement": 40},
                "Summon Monstro Spawns": {"requirement": 250}
            },
            "Lord": {
                "Deal Damage": {"requirement": 50000},
                "Final Hits": {"requirement": 40},
                "Summon Monstro Spawns": {"requirement": 250}
            }
        }

        # Peni Parker
        data["Peni Parker"] = {
            "Agent": {
                "Block Damage": {"requirement": 15000},
                "KOs": {"requirement": 15},
                "Deal Damage with Arachno-Mines": {"requirement": 2500}
            },
            "Knight": {
                "Block Damage": {"requirement": 35000},
                "KOs": {"requirement": 35},
                "Deal Damage with Arachno-Mines": {"requirement": 6000}
            },
            "Captain": {
                "Block Damage": {"requirement": 60000},
                "KOs": {"requirement": 60},
                "Deal Damage with Arachno-Mines": {"requirement": 10000}
            },
            "Centurion": {
                "Block Damage": {"requirement": 75000},
                "KOs": {"requirement": 75},
                "Deal Damage with Arachno-Mines": {"requirement": 15000}
            },
            "Lord": {
                "Block Damage": {"requirement": 75000},
                "KOs": {"requirement": 75},
                "Deal Damage with Arachno-Mines": {"requirement": 15000}
            }
        }

        # Psylocke
        data["Psylocke"] = {
            "Agent": {
                "Deal Damage": {"requirement": 7500},
                "Final Hits": {"requirement": 10},
                "Be Invisible with Psychic Stealth": {"requirement": 40}
            },
            "Knight": {
                "Deal Damage": {"requirement": 20000},
                "Final Hits": {"requirement": 25},
                "Be Invisible with Psychic Stealth": {"requirement": 100}
            },
            "Captain": {
                "Deal Damage": {"requirement": 30000},
                "Final Hits": {"requirement": 40},
                "Be Invisible with Psychic Stealth": {"requirement": 160}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 38000},
                "Final Hits": {"requirement": 50},
                "Be Invisible with Psychic Stealth": {"requirement": 200}
            },
            "Lord": {
                "Deal Damage": {"requirement": 38000},
                "Final Hits": {"requirement": 50},
                "Be Invisible with Psychic Stealth": {"requirement": 200}
            }
        }

        # Rocket Raccoon
        data["Rocket Raccoon"] = {
            "Agent": {
                "Heal Damage": {"requirement": 10000},
                "KOs/Assists": {"requirement": 25},
                "Revive Allies with BRB": {"requirement": 6}
            },
            "Knight": {
                "Heal Damage": {"requirement": 25000},
                "KOs/Assists": {"requirement": 60},
                "Revive Allies with BRB": {"requirement": 15}
            },
            "Captain": {
                "Heal Damage": {"requirement": 42000},
                "KOs/Assists": {"requirement": 95},
                "Revive Allies with BRB": {"requirement": 25}
            },
            "Centurion": {
                "Heal Damage": {"requirement": 54000},
                "KOs/Assists": {"requirement": 120},
                "Revive Allies with BRB": {"requirement": 30}
            },
            "Lord": {
                "Heal Damage": {"requirement": 54000},
                "KOs/Assists": {"requirement": 120},
                "Revive Allies with BRB": {"requirement": 30}
            }
        }

        # Rogue
        data["Rogue"] = {
            "Agent": {
                "Block Damage": {"requirement": 20000},
                "KOs": {"requirement": 12},
                "Use Ability Absorption on heroes": {"requirement": 10}
            },
            "Knight": {
                "Block Damage": {"requirement": 45000},
                "KOs": {"requirement": 30},
                "Use Ability Absorption on heroes": {"requirement": 25}
            },
            "Captain": {
                "Block Damage": {"requirement": 70000},
                "KOs": {"requirement": 50},
                "Use Ability Absorption on heroes": {"requirement": 40}
            },
            "Centurion": {
                "Block Damage": {"requirement": 90000},
                "KOs": {"requirement": 65},
                "Use Ability Absorption on heroes": {"requirement": 50}
            },
            "Lord": {
                "Block Damage": {"requirement": 90000},
                "KOs": {"requirement": 65},
                "Use Ability Absorption on heroes": {"requirement": 50}
            }
        }

        # Scarlet Witch
        data["Scarlet Witch"] = {
            "Agent": {
                "Deal Damage": {"requirement": 7500},
                "Final Hits": {"requirement": 10},
                "Stun Enemies with Dark Seal": {"requirement": 6}
            },
            "Knight": {
                "Deal Damage": {"requirement": 20000},
                "Final Hits": {"requirement": 25},
                "Stun Enemies with Dark Seal": {"requirement": 15}
            },
            "Captain": {
                "Deal Damage": {"requirement": 30000},
                "Final Hits": {"requirement": 40},
                "Stun Enemies with Dark Seal": {"requirement": 25}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 38000},
                "Final Hits": {"requirement": 50},
                "Stun Enemies with Dark Seal": {"requirement": 35}
            },
            "Lord": {
                "Deal Damage": {"requirement": 38000},
                "Final Hits": {"requirement": 50},
                "Stun Enemies with Dark Seal": {"requirement": 35}
            }
        }

        # Spider-Man
        data["Spider-Man"] = {
            "Agent": {
                "Deal Damage": {"requirement": 6000},
                "Final Hits": {"requirement": 8},
                "Trigger Spider-Tracers": {"requirement": 40}
            },
            "Knight": {
                "Deal Damage": {"requirement": 15000},
                "Final Hits": {"requirement": 20},
                "Trigger Spider-Tracers": {"requirement": 100}
            },
            "Captain": {
                "Deal Damage": {"requirement": 25000},
                "Final Hits": {"requirement": 35},
                "Trigger Spider-Tracers": {"requirement": 160}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 30000},
                "Final Hits": {"requirement": 40},
                "Trigger Spider-Tracers": {"requirement": 200}
            },
            "Lord": {
                "Deal Damage": {"requirement": 30000},
                "Final Hits": {"requirement": 40},
                "Trigger Spider-Tracers": {"requirement": 200}
            }
        }

        # Squirrel Girl
        data["Squirrel Girl"] = {
            "Agent": {
                "Deal Damage": {"requirement": 10000},
                "Final Hits": {"requirement": 10},
                "Immobilize Enemies with Squirrel Blockade": {"requirement": 10}
            },
            "Knight": {
                "Deal Damage": {"requirement": 25000},
                "Final Hits": {"requirement": 25},
                "Immobilize Enemies with Squirrel Blockade": {"requirement": 28}
            },
            "Captain": {
                "Deal Damage": {"requirement": 40000},
                "Final Hits": {"requirement": 40},
                "Immobilize Enemies with Squirrel Blockade": {"requirement": 45}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 50000},
                "Final Hits": {"requirement": 50},
                "Immobilize Enemies with Squirrel Blockade": {"requirement": 55}
            },
            "Lord": {
                "Deal Damage": {"requirement": 50000},
                "Final Hits": {"requirement": 50},
                "Immobilize Enemies with Squirrel Blockade": {"requirement": 55}
            }
        }

        # Star-Lord
        data["Star-Lord"] = {
            "Agent": {
                "Deal Damage": {"requirement": 8000},
                "Final Hits": {"requirement": 10},
                "Reload Magazines with Stellar Shift": {"requirement": 1000}
            },
            "Knight": {
                "Deal Damage": {"requirement": 20000},
                "Final Hits": {"requirement": 25},
                "Reload Magazines with Stellar Shift": {"requirement": 2500}
            },
            "Captain": {
                "Deal Damage": {"requirement": 35000},
                "Final Hits": {"requirement": 40},
                "Reload Magazines with Stellar Shift": {"requirement": 4000}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 50},
                "Reload Magazines with Stellar Shift": {"requirement": 5000}
            },
            "Lord": {
                "Deal Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 50},
                "Reload Magazines with Stellar Shift": {"requirement": 5000}
            }
        }

        # Storm
        data["Storm"] = {
            "Agent": {
                "Deal Damage": {"requirement": 8000},
                "Final Hits": {"requirement": 10},
                "Use Goddess Boost on Heroes": {"requirement": 75}
            },
            "Knight": {
                "Deal Damage": {"requirement": 20000},
                "Final Hits": {"requirement": 25},
                "Use Goddess Boost on Heroes": {"requirement": 200}
            },
            "Captain": {
                "Deal Damage": {"requirement": 35000},
                "Final Hits": {"requirement": 40},
                "Use Goddess Boost on Heroes": {"requirement": 300}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 50},
                "Use Goddess Boost on Heroes": {"requirement": 370}
            },
            "Lord": {
                "Deal Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 50},
                "Use Goddess Boost on Heroes": {"requirement": 370}
            }
        }

        # The Punisher
        data["The Punisher"] = {
            "Agent": {
                "Deal Damage": {"requirement": 10000},
                "Final Hits": {"requirement": 10},
                "Envelop Enemies with Scourge Grenade": {"requirement": 20}
            },
            "Knight": {
                "Deal Damage": {"requirement": 25000},
                "Final Hits": {"requirement": 25},
                "Envelop Enemies with Scourge Grenade": {"requirement": 50}
            },
            "Captain": {
                "Deal Damage": {"requirement": 40000},
                "Final Hits": {"requirement": 40},
                "Envelop Enemies with Scourge Grenade": {"requirement": 80}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 50000},
                "Final Hits": {"requirement": 50},
                "Envelop Enemies with Scourge Grenade": {"requirement": 100}
            },
            "Lord": {
                "Deal Damage": {"requirement": 50000},
                "Final Hits": {"requirement": 50},
                "Envelop Enemies with Scourge Grenade": {"requirement": 100}
            }
        }

        # Thor
        data["Thor"] = {
            "Agent": {
                "Block Damage": {"requirement": 20000},
                "KOs": {"requirement": 12},
                "Accumulate Thorforce": {"requirement": 120}
            },
            "Knight": {
                "Block Damage": {"requirement": 45000},
                "KOs": {"requirement": 30},
                "Accumulate Thorforce": {"requirement": 300}
            },
            "Captain": {
                "Block Damage": {"requirement": 70000},
                "KOs": {"requirement": 50},
                "Accumulate Thorforce": {"requirement": 500}
            },
            "Centurion": {
                "Block Damage": {"requirement": 90000},
                "KOs": {"requirement": 65},
                "Accumulate Thorforce": {"requirement": 650}
            },
            "Lord": {
                "Block Damage": {"requirement": 90000},
                "KOs": {"requirement": 65},
                "Accumulate Thorforce": {"requirement": 650}
            }
        }

        # Venom
        data["Venom"] = {
            "Agent": {
                "Block Damage": {"requirement": 20000},
                "KOs": {"requirement": 12},
                "Gain Bonus Health with Symbiotic Resilience": {"requirement": 8000}
            },
            "Knight": {
                "Block Damage": {"requirement": 55000},
                "KOs": {"requirement": 30},
                "Gain Bonus Health with Symbiotic Resilience": {"requirement": 20000}
            },
            "Captain": {
                "Block Damage": {"requirement": 85000},
                "KOs": {"requirement": 50},
                "Gain Bonus Health with Symbiotic Resilience": {"requirement": 32000}
            },
            "Centurion": {
                "Block Damage": {"requirement": 100000},
                "KOs": {"requirement": 65},
                "Gain Bonus Health with Symbiotic Resilience": {"requirement": 40000}
            },
            "Lord": {
                "Block Damage": {"requirement": 100000},
                "KOs": {"requirement": 65},
                "Gain Bonus Health with Symbiotic Resilience": {"requirement": 40000}
            }
        }

        # Winter Soldier
        data["Winter Soldier"] = {
            "Agent": {
                "Deal Damage": {"requirement": 7500},
                "Final Hits": {"requirement": 8},
                "Grab Enemies with Bionic Hook": {"requirement": 15}
            },
            "Knight": {
                "Deal Damage": {"requirement": 20000},
                "Final Hits": {"requirement": 20},
                "Grab Enemies with Bionic Hook": {"requirement": 35}
            },
            "Captain": {
                "Deal Damage": {"requirement": 30000},
                "Final Hits": {"requirement": 35},
                "Grab Enemies with Bionic Hook": {"requirement": 60}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 38000},
                "Final Hits": {"requirement": 40},
                "Grab Enemies with Bionic Hook": {"requirement": 75}
            },
            "Lord": {
                "Deal Damage": {"requirement": 38000},
                "Final Hits": {"requirement": 40},
                "Grab Enemies with Bionic Hook": {"requirement": 75}
            }
        }

        # Wolverine
        data["Wolverine"] = {
            "Agent": {
                "Deal Damage": {"requirement": 8000},
                "Final Hits": {"requirement": 10},
                "Knock Down Enemies with Feral Leap": {"requirement": 10}
            },
            "Knight": {
                "Deal Damage": {"requirement": 20000},
                "Final Hits": {"requirement": 25},
                "Knock Down Enemies with Feral Leap": {"requirement": 25}
            },
            "Captain": {
                "Deal Damage": {"requirement": 35000},
                "Final Hits": {"requirement": 40},
                "Knock Down Enemies with Feral Leap": {"requirement": 40}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 50},
                "Knock Down Enemies with Feral Leap": {"requirement": 50}
            },
            "Lord": {
                "Deal Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 50},
                "Knock Down Enemies with Feral Leap": {"requirement": 50}
            }
        }

        # Ultron
        data["Ultron"] = {
            "Agent": {
                "Reach Healing": {"requirement": 10000},
                "Achieve KOs/Assists": {"requirement": 25},
                "Imperative: Firewall extra health": {"requirement": 4000}
            },
            "Knight": {
                "Reach Healing": {"requirement": 25000},
                "Achieve KOs/Assists": {"requirement": 65},
                "Imperative: Firewall extra health": {"requirement": 10000}
            },
            "Captain": {
                "Reach Healing": {"requirement": 42000},
                "Achieve KOs/Assists": {"requirement": 100},
                "Imperative: Firewall extra health": {"requirement": 16000}
            },
            "Centurion": {
                "Reach Healing": {"requirement": 54000},
                "Achieve KOs/Assists": {"requirement": 130},
                "Imperative: Firewall extra health": {"requirement": 20000}
            },
            "Lord": {
                "Reach Healing": {"requirement": 54000},
                "Achieve KOs/Assists": {"requirement": 130},
                "Imperative: Firewall extra health": {"requirement": 20000}
            }
        }

        # Emma Frost
        data["Emma Frost"] = {
            "Agent": {
                "Block Damage": {"requirement": 21000},
                "Achieve KOs": {"requirement": 15},
                "Seize control of sentiences with Psychic Spear": {"requirement": 6}
            },
            "Knight": {
                "Block Damage": {"requirement": 21000},
                "Achieve KOs": {"requirement": 35},
                "Seize control of sentiences with Psychic Spear": {"requirement": 15}
            },
            "Captain": {
                "Block Damage": {"requirement": 85000},
                "Achieve KOs": {"requirement": 60},
                "Seize control of sentiences with Psychic Spear": {"requirement": 24}
            },
            "Centurion": {
                "Block Damage": {"requirement": 110000},
                "Achieve KOs": {"requirement": 75},
                "Seize control of sentiences with Psychic Spear": {"requirement": 30}
            },
            "Lord": {
                "Block Damage": {"requirement": 110000},
                "Achieve KOs": {"requirement": 75},
                "Seize control of sentiences with Psychic Spear": {"requirement": 30}
            }
        }

        # Blade
        data["Blade"] = {
            "Agent": {
                "Reach Damage": {"requirement": 10000},
                "Achieve Final Hits": {"requirement": 10},
                "Lifesteal Health with Bloodline Awakening": {"requirement": 2500}
            },
            "Knight": {
                "Reach Damage": {"requirement": 25000},
                "Achieve Final Hits": {"requirement": 25},
                "Lifesteal Health with Bloodline Awakening": {"requirement": 6250}
            },
            "Captain": {
                "Reach Damage": {"requirement": 40000},
                "Achieve Final Hits": {"requirement": 40},
                "Lifesteal Health with Bloodline Awakening": {"requirement": 10000}
            },
            "Centurion": {
                "Reach Damage": {"requirement": 50000},
                "Achieve Final Hits": {"requirement": 50},
                "Lifesteal Health with Bloodline Awakening": {"requirement": 12500}
            },
            "Lord": {
                "Reach Damage": {"requirement": 50000},
                "Achieve Final Hits": {"requirement": 50},
                "Lifesteal Health with Bloodline Awakening": {"requirement": 12500}
            }
        }

        # Phoenix
        data["Phoenix"] = {
            "Agent": {
                "Deal Damage": {"requirement": 11000},
                "Final Hits": {"requirement": 12},
                "Trigger Spark Explosions": {"requirement": 80}
            },
            "Knight": {
                "Deal Damage": {"requirement": 28000},
                "Final Hits": {"requirement": 30},
                "Trigger Spark Explosions": {"requirement": 200}
            },
            "Captain": {
                "Deal Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 50},
                "Trigger Spark Explosions": {"requirement": 320}
            },
            "Centurion": {
                "Deal Damage": {"requirement": 55000},
                "Final Hits": {"requirement": 65},
                "Trigger Spark Explosions": {"requirement": 400}
            },
            "Lord": {
                "Deal Damage": {"requirement": 55000},
                "Final Hits": {"requirement": 65},
                "Trigger Spark Explosions": {"requirement": 400}
            }
        }

        # The Thing
        data["The Thing"] = {
            "Agent": {
                "Block Damage": {"requirement": 21000},
                "KOs": {"requirement": 15},
                "Hit enemies with Yancy Street Charge": {"requirement": 30}
            },
            "Knight": {
                "Block Damage": {"requirement": 25000},
                "KOs": {"requirement": 35},
                "Hit enemies with Yancy Street Charge": {"requirement": 75}
            },
            "Captain": {
                "Block Damage": {"requirement": 85000},
                "KOs": {"requirement": 60},
                "Hit enemies with Yancy Street Charge": {"requirement": 120}
            },
            "Centurion": {
                "Block Damage": {"requirement": 110000},
                "KOs": {"requirement": 75},
                "Hit enemies with Yancy Street Charge": {"requirement": 150}
            },
            "Lord": {
                "Block Damage": {"requirement": 110000},
                "KOs": {"requirement": 75},
                "Hit enemies with Yancy Street Charge": {"requirement": 150}
            }
        }

        # Human Torch
        data["Human Torch"] = {
            "Agent": {
                "Reach Damage": {"requirement": 8000},
                "Final Hits": {"requirement": 8},
                "Create flame fields with Blazing Blast": {"requirement": 200}
            },
            "Knight": {
                "Reach Damage": {"requirement": 20000},
                "Final Hits": {"requirement": 20},
                "Create flame fields with Blazing Blast": {"requirement": 500}
            },
            "Captain": {
                "Reach Damage": {"requirement": 35000},
                "Final Hits": {"requirement": 35},
                "Create flame fields with Blazing Blast": {"requirement": 800}
            },
            "Centurion": {
                "Reach Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 40},
                "Create flame fields with Blazing Blast": {"requirement": 1000}
            },
            "Lord": {
                "Reach Damage": {"requirement": 45000},
                "Final Hits": {"requirement": 40},
                "Create flame fields with Blazing Blast": {"requirement": 1000}
            }
        }

        # Set points for all missions based on rank
        for hero in data:
            for rank in data[hero]:
                for mission in data[hero][rank]:
                    data[hero][rank][mission]["points"] = POINTS_PER_MISSION[rank]

        return data

    def _build_ui(self):
        # Apply initial customization
        self.config(bg=self.bg_color.get())

        # Menubar for Settings and Help
        menubar = tk.Menu(self, bg=self.bg_color.get(), fg=self.text_color.get())
        self.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0, bg=self.bg_color.get(), fg=self.text_color.get())
        menubar.add_cascade(label="Settings", menu=settings_menu)

        settings_menu.add_command(label="Background Color", command=self.change_bg_color)
        settings_menu.add_command(label="Foreground Color", command=self.change_fg_color)
        settings_menu.add_command(label="Text Color", command=self.change_text_color)
        settings_menu.add_command(label="Font", command=self.change_font)
        settings_menu.add_command(label="Font Size", command=self.change_font_size)

        # Add Help menu to the right
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.bg_color.get(), fg=self.text_color.get())
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Help", command=self.show_help)

        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, weight=1)
        frame.columnconfigure(5, weight=1)
        frame.rowconfigure(11, weight=0)  # mission list (fixed height but scrollable)
        frame.rowconfigure(14, weight=1)  # output expands

        # Set font for frame
        self.custom_font = font.Font(family=self.font_family.get(), size=int(self.font_size.get()))
        style = ttk.Style()
        style.configure("TLabel", font=self.custom_font, foreground=self.text_color.get())
        style.configure("TButton", font=self.custom_font, foreground=self.text_color.get())
        style.configure("TCombobox", font=self.custom_font, foreground=self.text_color.get())
        style.configure("TEntry", font=self.custom_font, foreground=self.text_color.get())

        # Player rank inputs
        ttk.Label(frame, text="Your Current Rank:").grid(row=0, column=0, sticky="w")
        rank_menu = ttk.Combobox(frame, textvariable=self.current_rank_var,
                                 values=list(RANK_THRESHOLDS.keys()), state="readonly")
        rank_menu.grid(row=0, column=1)

        ttk.Label(frame, text="Your Current Points:").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.current_points_var, width=10).grid(row=1, column=1)

        ttk.Label(frame, text="Hours Played (60 points per hour):").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.hours_played_var, width=10).grid(row=2, column=1)

        # Character select (now searchable)
        ttk.Label(frame, text="Select Character:").grid(row=3, column=0, sticky="w")
        self.char_menu = ttk.Combobox(frame, textvariable=self.current_character,
                                      state="normal")  # ← "normal", non "readonly"
        self.char_menu.grid(row=3, column=1, columnspan=3, sticky="ew", padx=(5, 0))
        self.char_menu.bind("<<ComboboxSelected>>", self.on_character_selected)
        self.char_menu.bind("<KeyRelease>", self.on_char_search)

        # Sort button
        self.sort_button = ttk.Button(frame, text="Sort A-Z", command=self.toggle_sort)
        self.sort_button.grid(row=3, column=4, padx=(5, 0))

        # Filter by role (under)
        ttk.Label(frame, text="Filter Role:").grid(row=4, column=0, sticky="w")
        filter_menu = ttk.Combobox(frame, textvariable=self.filter_var,
                                   values=["All", "Vanguard", "Duelist", "Strategist"], state="readonly")
        filter_menu.grid(row=4, column=1, columnspan=2, sticky="w")
        filter_menu.bind("<<ComboboxSelected>>", self.on_filter_change)

        # Mission rank select
        ttk.Label(frame, text="Mission Rank:").grid(row=5, column=0, sticky="w")
        mission_rank_menu = ttk.Combobox(frame, textvariable=self.current_mission_rank,
                                         values=["Agent", "Knight", "Captain", "Centurion", "Lord"], state="readonly")
        mission_rank_menu.grid(row=5, column=1)
        mission_rank_menu.bind("<<ComboboxSelected>>", self.refresh_missions)

        # Checklist toggle for character
        ttk.Label(frame, text="Mark as Completed (Lord):").grid(row=6, column=0, sticky="w")
        self.completed_check = tk.BooleanVar(value=False)
        self.check_button = ttk.Checkbutton(frame, variable=self.completed_check, command=self.toggle_completed)
        self.check_button.grid(row=6, column=1)

        # Mission completion toggle
        ttk.Label(frame, text="Mark Selected Mission as Completed:").grid(row=7, column=0, sticky="w")
        self.mission_completed_check = tk.BooleanVar(value=False)
        self.mission_check_button = ttk.Checkbutton(frame, variable=self.mission_completed_check, command=self.toggle_mission_completed)
        self.mission_check_button.grid(row=7, column=1)

        # Mission section (for custom adds)
        ttk.Label(frame, text="\nAdd Custom Mission:").grid(row=8, column=0, sticky="w")

        ttk.Label(frame, text="Name").grid(row=9, column=0)
        self.mission_name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.mission_name_var, width=15).grid(row=10, column=0)

        ttk.Label(frame, text="Requirement").grid(row=9, column=1)
        self.mission_req_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.mission_req_var, width=10).grid(row=10, column=1)

        ttk.Label(frame, text="Points").grid(row=9, column=2)
        self.mission_points_var = tk.StringVar(value="40")
        ttk.Entry(frame, textvariable=self.mission_points_var, width=5).grid(row=10, column=2)

        ttk.Button(frame, text="Add Mission", command=self.add_mission).grid(row=10, column=3)
        ttk.Button(frame, text="Remove Selected Mission", command=self.remove_mission).grid(row=10, column=4, pady=5)

        # Mission list with horizontal and vertical scrollbars
        mission_frame = ttk.Frame(frame)
        mission_frame.grid(row=11, column=0, columnspan=6, pady=5, sticky="nsew")

        self.mission_list = tk.Listbox(
            mission_frame,
            height=6,
            width=90,
            font=self.custom_font,
            fg=self.text_color.get(),
            bg=self.bg_color.get(),
            exportselection=False  # optional, avoids deselection on focus loss
        )

        v_scroll_m = ttk.Scrollbar(mission_frame, orient="vertical", command=self.mission_list.yview)
        h_scroll_m = ttk.Scrollbar(mission_frame, orient="horizontal", command=self.mission_list.xview)
        self.mission_list.configure(yscrollcommand=v_scroll_m.set, xscrollcommand=h_scroll_m.set)

        self.mission_list.grid(row=0, column=0, sticky="nsew")
        v_scroll_m.grid(row=0, column=1, sticky="ns")
        h_scroll_m.grid(row=1, column=0, sticky="ew")

        mission_frame.columnconfigure(0, weight=1)
        mission_frame.rowconfigure(0, weight=1)

        self.mission_list.bind("<<ListboxSelect>>", self.update_mission_check)

        # Calculate button (centered)
        calc_frame = ttk.Frame(frame)
        calc_frame.grid(row=13, column=0, columnspan=6, pady=10)
        ttk.Button(calc_frame, text="Calculate", command=self.calculate).pack(anchor="center")

        # Output with horizontal and vertical scrollbars
        output_frame = ttk.Frame(frame)
        output_frame.grid(row=14, column=0, columnspan=6, pady=5, sticky="nsew")

        self.output = tk.Text(
            output_frame,
            height=15,
            width=90,
            wrap="none",  # ← IMPORTANTE: disabilita wrap per abilitare scroll orizzontale
            font=self.custom_font,
            fg=self.text_color.get(),
            bg=self.bg_color.get()
        )

        # Scrollbars
        v_scroll = ttk.Scrollbar(output_frame, orient="vertical", command=self.output.yview)
        h_scroll = ttk.Scrollbar(output_frame, orient="horizontal", command=self.output.xview)
        self.output.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # Layout
        self.output.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        # Make the Text widget expand
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

    def show_help(self):
        help_text = (
            "Welcome to the Marvel Rivals Lord Rank Calculator!\n\n"
            "This tool helps you track progress toward the Lord rank for each character in Marvel Rivals.\n\n"
            "How to Use:\n"
            "1. Enter your current rank, points, and hours played in the input fields.\n"
            "2. Select a character from the 'Select Character' dropdown. Use the search box, role filter (Vanguard, Duelist, Strategist), or Sort A-Z/Z-A button to find characters.\n"
            "3. Choose the mission rank (Agent, Knight, etc.) to view missions for that rank.\n"
            "4. Missions for the selected character and rank will appear in the list below. You can add custom missions or mark missions/characters as completed.\n"
            "5. Click 'Calculate' to see how many missions and points are needed to reach Lord rank.\n\n"
            "Calculating Lord Progress:\n"
            "- Points are earned from missions (varies by rank) and playtime (60 points per hour).\n"
            "- The calculator determines points needed to reach Lord rank based on your current rank and points.\n"
            "- It estimates the number of missions required, splitting them evenly across listed missions.\n"
            "- Completed characters and missions are marked with a ★ and saved when you close the app.\n\n"
            "Use the Settings menu to customize colors, font, and font size."
        )
        messagebox.showinfo("Help - Marvel Rivals Calculator", help_text)

    def change_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.bg_color.set(color)
            self.config(bg=color)
            self.mission_list.config(bg=color)
            self.output.config(bg=color)
            self.update()

    def change_fg_color(self):
        color = colorchooser.askcolor(title="Choose Foreground Color")[1]
        if color:
            self.fg_color.set(color)
            style = ttk.Style()
            style.configure("TButton", foreground=color)
            style.configure("TCombobox", foreground=color)
            self.update()

    def change_text_color(self):
        color = colorchooser.askcolor(title="Choose Text Color")[1]
        if color:
            self.text_color.set(color)
            style = ttk.Style()
            style.configure("TLabel", foreground=color)
            style.configure("TEntry", foreground=color)
            self.mission_list.config(fg=color)
            self.output.config(fg=color)
            self.update()

    def change_font(self):
        font_window = tk.Toplevel(self)
        font_window.title("Choose Font")
        font_window.geometry("300x100")

        ttk.Label(font_window, text="Select Font:").pack(pady=5)
        fonts = sorted(list(font.families()))
        font_var = tk.StringVar(value=self.font_family.get())
        font_menu = ttk.Combobox(font_window, textvariable=font_var, values=fonts, state="readonly")
        font_menu.pack(pady=5)

        def apply_font():
            selected_font = font_var.get()
            if selected_font:
                self.font_family.set(selected_font)
                self.custom_font.configure(family=selected_font)
                style = ttk.Style()
                style.configure("TLabel", font=self.custom_font)
                style.configure("TButton", font=self.custom_font)
                style.configure("TCombobox", font=self.custom_font)
                style.configure("TEntry", font=self.custom_font)
                self.mission_list.config(font=self.custom_font)
                self.output.config(font=self.custom_font)
                self.update()
                font_window.destroy()

        ttk.Button(font_window, text="Apply", command=apply_font).pack(pady=5)

    def change_font_size(self):
        font_size_window = tk.Toplevel(self)
        font_size_window.title("Choose Font Size")
        font_size_window.geometry("300x100")

        ttk.Label(font_size_window, text="Select Font Size:").pack(pady=5)
        sizes = [8, 10, 12, 14, 16, 18, 20, 22, 24]
        size_var = tk.StringVar(value=self.font_size.get())
        size_menu = ttk.Combobox(font_size_window, textvariable=size_var, values=sizes, state="readonly")
        size_menu.pack(pady=5)

        def apply_size():
            selected_size = size_var.get()
            if selected_size:
                self.font_size.set(selected_size)
                self.custom_font.configure(size=int(selected_size))
                style = ttk.Style()
                style.configure("TLabel", font=self.custom_font)
                style.configure("TButton", font=self.custom_font)
                style.configure("TCombobox", font=self.custom_font)
                style.configure("TEntry", font=self.custom_font)
                self.mission_list.config(font=self.custom_font)
                self.output.config(font=self.custom_font)
                self.update()
                font_size_window.destroy()

        ttk.Button(font_size_window, text="Apply", command=apply_size).pack(pady=5)

    def toggle_sort(self):
        # Toggle sort direction
        self.sort_ascending.set(not self.sort_ascending.get())
        # Update button text
        self.sort_button.config(text="Sort A-Z" if self.sort_ascending.get() else "Sort Z-A")
        # Update character list with new sort order
        self.update_char_combobox()

    def toggle_completed(self):
        char = self.current_character.get().replace(" ★", "")
        if self.completed_check.get():
            self.completed_characters.add(char)
        else:
            self.completed_characters.discard(char)
        self.update_char_combobox()  # Maintain current sort order
        self.save_completed()
        self.refresh_missions()

    def toggle_mission_completed(self):
        selection = self.mission_list.curselection()
        if not selection:
            return
        index = selection[0]
        mission_text = self.mission_list.get(index).replace(" ★", "")
        mission_name = mission_text.split(":")[0].strip()
        char = self.current_character.get().replace(" ★", "")
        rank = self.current_mission_rank.get()

        # Ensure mission completion dictionary structure
        if char not in self.completed_missions:
            self.completed_missions[char] = {}
        if rank not in self.completed_missions[char]:
            self.completed_missions[char][rank] = set()

        if self.mission_completed_check.get():
            self.completed_missions[char][rank].add(mission_name)
        else:
            self.completed_missions[char][rank].discard(mission_name)

        self.save_completed()
        self.refresh_missions()

    def update_mission_check(self, event=None):
        selection = self.mission_list.curselection()
        if not selection:
            self.mission_completed_check.set(False)
            return
        index = selection[0]
        mission_text = self.mission_list.get(index).replace(" ★", "")
        mission_name = mission_text.split(":")[0].strip()
        char = self.current_character.get().replace(" ★", "")
        rank = self.current_mission_rank.get()

        is_completed = (char in self.completed_missions and
                       rank in self.completed_missions[char] and
                       mission_name in self.completed_missions[char][rank])
        self.mission_completed_check.set(is_completed)

    def refresh_missions(self, event=None):
        char = self.current_character.get().replace(" ★", "")
        rank = self.current_mission_rank.get()
        self.mission_list.delete(0, tk.END)
        self.characters = {}
        self.mission_requirements = {}

        if char in self.mission_data and rank in self.mission_data[char]:
            for name, info in self.mission_data[char][rank].items():
                self.characters[name] = info["points"]
                self.mission_requirements[name] = {"requirement": info["requirement"]}
                is_completed = (char in self.completed_missions and
                               rank in self.completed_missions[char] and
                               name in self.completed_missions[char][rank])
                formatted_req = f"{info['requirement']:,}"  # Add comma to requirement
                formatted_points = f"{info['points']:,}"  # Add comma to points
                display_text = f"{name} ★: Req: {formatted_req} | {formatted_points} pts" if is_completed else f"{name}: Req: {formatted_req} | {formatted_points} pts"
                self.mission_list.insert(tk.END, display_text)

        # Update character checklist
        is_completed = char in self.completed_characters
        self.completed_check.set(is_completed)

    def add_mission(self):
        name = self.mission_name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Mission must have a name")
            return

        try:
            req = int(self.mission_req_var.get())
            points = int(self.mission_points_var.get())
        except ValueError:
            messagebox.showerror("Error", "Requirement and points must be numbers")
            return

        self.characters[name] = points
        self.mission_requirements[name] = {"requirement": req}

        formatted_req = f"{req:,}"  # Add comma to requirement
        formatted_points = f"{points:,}"  # Add comma to points
        self.mission_list.insert(tk.END, f"{name}: Req: {formatted_req} | {formatted_points} pts")

        # Clear inputs
        self.mission_name_var.set("")
        self.mission_req_var.set("")
        self.mission_points_var.set("40")

    def remove_mission(self):
        selection = self.mission_list.curselection()
        if not selection:
            return
        index = selection[0]
        mission_text = self.mission_list.get(index).replace(" ★", "")
        mission_name = mission_text.split(":")[0].strip()

        if mission_name in self.characters:
            del self.characters[mission_name]
        if mission_name in self.mission_requirements:
            del self.mission_requirements[mission_name]

        # Remove from completed missions
        char = self.current_character.get().replace(" ★", "")
        rank = self.current_mission_rank.get()
        if char in self.completed_missions and rank in self.completed_missions[char]:
            self.completed_missions[char][rank].discard(mission_name)
            self.save_completed()

        self.mission_list.delete(index)

    def calculate(self):
        try:
            current_rank = self.current_rank_var.get()
            current_points = int(self.current_points_var.get())
            hours_played = int(self.hours_played_var.get())
        except ValueError:
            messagebox.showerror("Error", "Points and hours must be numbers")
            return

        # Calculate points to Lord
        points_to_lord = 0
        found_rank = False
        ranks = list(RANK_THRESHOLDS.keys())
        for i, rank in enumerate(ranks):
            if rank == current_rank:
                found_rank = True
                points_to_lord += (RANK_THRESHOLDS[rank] - current_points)
            elif found_rank and rank != "Lord":
                points_to_lord += RANK_THRESHOLDS[rank]

        play_points = hours_played * 60
        remaining = max(0, points_to_lord - play_points)
        mission_points = POINTS_PER_MISSION[self.current_mission_rank.get()] if self.characters else 40
        total_missions = math.ceil(remaining / mission_points) if remaining > 0 else 0

        self.output.delete("1.0", tk.END)
        char = self.current_character.get().replace(" ★", "")
        star = "★" if char in self.completed_characters else ""
        self.output.insert(tk.END, f"Character: {char} {star}\n")
        self.output.insert(tk.END, f"Playtime points: {play_points:,}\n")  # Add comma
        self.output.insert(tk.END, f"Points still needed to Lord: {remaining:,}\n")  # Add comma
        self.output.insert(tk.END, f"Total missions required (at {mission_points:,} pts each): {total_missions:,}\n\n")  # Add comma

        if not self.characters:
            self.output.insert(tk.END, "No missions added yet.\n")
            return

        split = 1 / len(self.characters) if len(self.characters) > 0 else 0
        for name, points in self.characters.items():
            num_missions = math.ceil(total_missions * split)
            data = self.mission_requirements.get(name, {})
            req = data.get("requirement")
            is_completed = (char in self.completed_missions and
                           self.current_mission_rank.get() in self.completed_missions[char] and
                           name in self.completed_missions[char][self.current_mission_rank.get()])
            star = "★" if is_completed else ""
            formatted_points = f"{points * num_missions:,}"  # Add comma
            self.output.insert(tk.END, f"{name} {star}: {num_missions:,} missions ({formatted_points} pts)\n")  # Add comma
            if req:
                total_req = num_missions * req
                formatted_req = f"{total_req:,}"  # Add comma
                self.output.insert(tk.END, f"  → {formatted_req} required\n")
            self.output.insert(tk.END, "\n")

    def on_filter_change(self, event=None):
        """Ricarica la lista completa quando si cambia il filtro ruolo."""
        self._full_character_list = None  # Resetta cache
        self.update_char_combobox()

    def on_char_search(self, event=None):
        if event and event.keysym in ("Up", "Down", "Return", "Escape", "Tab", "Shift_L", "Shift_R", "Control_L",
                                      "Control_R", "BackSpace", "Delete", "Home", "End", "Left", "Right"):
            return
        if self._updating_combobox:
            return

        current_text = self.current_character.get().lower().strip()
        self.update_char_combobox(search_term=current_text)

        #
        self.after(300, lambda: self._open_combobox_popup())

    def _open_combobox_popup(self):
        if not self.char_menu.winfo_viewable():
            return
        try:
            # cross-platform way to open the dropdown
            self.char_menu.event_generate("<Button-1>")
            self.char_menu.event_generate("<ButtonRelease-1>")
        except Exception:
            pass

    def on_character_selected(self, event=None):
        """Quando un personaggio viene selezionato, aggiorna le missioni."""
        char = self.current_character.get().replace(" ★", "")
        # Assicurati che sia un personaggio valido (non testo casuale)
        if char in self._get_all_characters():
            self.refresh_missions()
            self.char_menu.select_clear()
        else:
            # Se digita qualcosa di non valido, non fare nulla (o resetta)
            pass

    def _get_all_characters(self):
        """Restituisce tutti i personaggi (piatti) dalla categorizzazione."""
        chars = []
        for role in self.roles.values():
            chars.extend(role)
        return set(chars)

    def update_char_combobox(self, search_term=""):
        if self._updating_combobox:
            return
        self._updating_combobox = True

        filter_role = self.filter_var.get()
        characters = []

        for role, heros in self.roles.items():
            if filter_role == "All" or filter_role == role:
                characters.extend(heros)

        if search_term:
            characters = [c for c in characters if search_term in c.lower()]

        characters.sort(reverse=not self.sort_ascending.get())

        display_chars = []
        for char in characters:
            if char in self.completed_characters:
                display_chars.append(f"{char} ★")
            else:
                display_chars.append(char)

        current_input = self.current_character.get()
        self.char_menu["values"] = display_chars
        self.current_character.set(current_input)
        self.char_menu.icursor(tk.END)

        self._updating_combobox = False

if __name__ == "__main__":
    app = MarvelRivalsCalculator()
    app.mainloop()