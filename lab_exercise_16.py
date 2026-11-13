"""
Lab Exercise 16 : Dice Simulator using the random module
Concepts        : random.randint, random.seed, loops, dictionaries,
                  frequency analysis, probability, simulation
"""
 
import random
import sys
from collections import Counter
 
 
# ---------------------------------------------------------------
# Class Die : one fair die with a configurable number of sides
# ---------------------------------------------------------------
class Die:
    def __init__(self, sides=6):
        if sides < 2:
            raise ValueError("A die needs at least 2 sides.")
        self.sides = sides
 
    def roll(self):
        return random.randint(1, self.sides)      # both ends inclusive
 
 
# ---------------------------------------------------------------
# Simulator helpers
# ---------------------------------------------------------------
def roll_dice(num_dice=1, sides=6):
    """Roll num_dice dice once and return the list of faces."""
    dice = [Die(sides) for _ in range(num_dice)]
    return [d.roll() for d in dice]
 
 
def simulate(trials, num_dice=1, sides=6):
    """Roll the dice many times; return a Counter of the TOTAL of each roll."""
    return Counter(sum(roll_dice(num_dice, sides)) for _ in range(trials))
 
 
def expected_probability(total, num_dice=1, sides=6):
    """Exact theoretical probability of a total (by counting all outcomes)."""
    ways = {0: 1}
    for _ in range(num_dice):
        new = {}
        for s, w in ways.items():
            for face in range(1, sides + 1):
                new[s + face] = new.get(s + face, 0) + w
        ways = new
    return ways.get(total, 0) / (sides ** num_dice)
 
 
def show_frequency(counter, trials, num_dice=1, sides=6):
    """Print frequency table with a text histogram and theory comparison."""
    print(f"  {'Total':<7}{'Count':>7}{'Observed%':>11}{'Expected%':>11}   Histogram")
    print("  " + "-" * 70)
    for total in range(num_dice, num_dice * sides + 1):
        count = counter.get(total, 0)
        obs = 100 * count / trials
        exp = 100 * expected_probability(total, num_dice, sides)
        bar = "#" * round(obs * 2)
        print(f"  {total:<7}{count:>7}{obs:>10.2f}%{exp:>10.2f}%   {bar}")
 
 
# ---------------------------------------------------------------
# Optional interactive mode:  python ex16_dice.py --play
# ---------------------------------------------------------------
def play():
    print("DICE SIMULATOR  (type q to quit)")
    while True:
        cmd = input("How many dice to roll? ").strip().lower()
        if cmd == "q":
            break
        if not cmd.isdigit() or int(cmd) < 1:
            print("Please enter a positive whole number.")
            continue
        faces = roll_dice(int(cmd))
        print("You rolled:", faces, "| Total =", sum(faces))
 
 
# ---------------------------------------------------------------
# Demonstration run (seeded so the results can be reproduced)
# ---------------------------------------------------------------
def main():
    random.seed(2026)
 
    print("=" * 78)
    print(" 1. SINGLE DIE - TEN REPEATED ROLLS")
    print("=" * 78)
    rolls = [roll_dice()[0] for _ in range(10)]
    print("  Outcomes :", rolls)
    print("  Average  :", sum(rolls) / len(rolls), " (theoretical mean = 3.5)")
 
    print()
    print("=" * 78)
    print(" 2. TWO DICE - FIVE ROLLS (BOARD-GAME STYLE)")
    print("=" * 78)
    for turn in range(1, 6):
        d1, d2 = roll_dice(2)
        extra = "  <- DOUBLE! roll again" if d1 == d2 else ""
        print(f"  Turn {turn}: {d1} + {d2} = {d1 + d2}{extra}")
 
    print()
    print("=" * 78)
    print(" 3. FREQUENCY ANALYSIS - ONE DIE, DIFFERENT NUMBER OF TRIALS")
    print("=" * 78)
    for trials in (60, 600, 60000):
        print(f"\n  Trials = {trials}")
        show_frequency(simulate(trials), trials)
 
    print()
    print("=" * 78)
    print(" 4. FREQUENCY ANALYSIS - TWO DICE, 36000 TRIALS")
    print("=" * 78)
    trials = 36000
    show_frequency(simulate(trials, num_dice=2), trials, num_dice=2)
 
    print()
    print("=" * 78)
    print(" 5. PROBABILITY EXPERIMENT - GETTING A SIX / DOUBLE SIX")
    print("=" * 78)
    n = 100000
    sixes = sum(1 for _ in range(n) if roll_dice()[0] == 6)
    double6 = sum(1 for _ in range(n) if roll_dice(2) == [6, 6])
    print(f"  P(six)        observed = {sixes / n:.4f}   theory = {1 / 6:.4f}")
    print(f"  P(double six) observed = {double6 / n:.4f}   theory = {1 / 36:.4f}")
 
    print()
    print("=" * 78)
    print(" 6. BOARD GAME SIMULATION - RACE TO SQUARE 50")
    print("=" * 78)
    players = {"Sriram": 0, "Rahul": 0}
    turn = 0
    while max(players.values()) < 50:
        turn += 1
        for name in players:
            roll = roll_dice()[0]
            players[name] = min(50, players[name] + roll)
            if players[name] == 50:
                print(f"  Turn {turn:>2}: {name} rolled {roll} and reached square 50. {name} WINS!")
                break
        else:
            print(f"  Turn {turn:>2}: " + " | ".join(f"{k} at {v:>2}" for k, v in players.items()))
            continue
        break
 
 
if __name__ == "__main__":
    if "--play" in sys.argv:
        play()
    else:
        main()
