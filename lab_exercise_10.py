"""
Lab Exercise 10 : Frequency Counter using Dictionaries
Core idea
---------
A dictionary maps each distinct item to the number of times it appears:
    freq = {item: count}
For every item we either start a new key at 1 or add 1 to the existing key:
    freq[item] = freq.get(item, 0) + 1
"""
import string
STOP_WORDS = {"a", "an", "the", "is", "are", "was", "were", "and", "or", "of", "to",
              "in", "on", "at", "it", "this", "that", "for", "with", "i", "we", "very"}
# -------------------------------------------------------------------
# Counting
# -------------------------------------------------------------------
def clean_words(text, remove_stop_words=False):
    """Lower-case the text, strip punctuation and split into a list of words."""
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")
    table = str.maketrans("", "", string.punctuation)
    words = text.lower().translate(table).split()
    if remove_stop_words:
        words = [w for w in words if w not in STOP_WORDS]
    return words
def count_items(items):
    """Count how many times each element occurs in a list (or any iterable)."""
    freq = {}
    for item in items:
        freq[item] = freq.get(item, 0) + 1
    return freq
def word_frequency(text, remove_stop_words=False):
    return count_items(clean_words(text, remove_stop_words))
def element_frequency(items, ignore_case=False):
    if not isinstance(items, (list, tuple)):
        raise TypeError("Input must be a list or tuple.")
    if ignore_case:
        items = [i.strip().lower() if isinstance(i, str) else i for i in items]
    return count_items(items)
# -------------------------------------------------------------------
# Analysis
# -------------------------------------------------------------------
def sorted_frequency(freq):
    """List of (item, count) sorted by count (high to low), then by item."""
    return sorted(freq.items(), key=lambda pair: (-pair[1], str(pair[0])))
def most_common(freq):
    """All items that share the highest count (handles ties)."""
    if not freq:
        return []
    top = max(freq.values())
    return sorted((k for k, v in freq.items() if v == top), key=str)
def least_common(freq):
    if not freq:
        return []
    low = min(freq.values())
    return sorted((k for k, v in freq.items() if v == low), key=str)
def top_n(freq, n):
    return sorted_frequency(freq)[:n]
def percentages(freq):
    total = sum(freq.values())
    return {k: round(v / total * 100, 1) for k, v in freq.items()} if total else {}
def average_of_numeric(freq):
    """Weighted mean when the keys are numbers (e.g. rating -> number of votes)."""
    total = sum(freq.values())
    return round(sum(k * v for k, v in freq.items()) / total, 2) if total else 0.0
# -------------------------------------------------------------------
# Display
# -------------------------------------------------------------------
def display_frequency(freq, title="Frequency table", bar_char="#"):
    if not freq:
        print("No data to display.")
        return
    total = sum(freq.values())
    width = max(len(str(k)) for k in freq) + 2
    print(title)
    print("-" * (width + 28))
    print(f"{'Item':<{width}}{'Count':>6}{'%':>8}  Bar")
    for item, count in sorted_frequency(freq):
        print(f"{str(item):<{width}}{count:>6}{count / total * 100:>7.1f}%  {bar_char * count}")
    print("-" * (width + 28))
    print(f"{'Total':<{width}}{total:>6}{'100.0%':>8}   ({len(freq)} distinct)")
# -------------------------------------------------------------------
# Menu driven program
# -------------------------------------------------------------------
def menu():
    options = """
===== FREQUENCY COUNTER =====
1. Count words in a sentence
2. Count elements in a list (comma separated)
3. Exit
"""
    while True:
        print(options)
        choice = input("Enter choice: ").strip()
        try:
            if choice == "1":
                text = input("Enter a sentence: ")
                skip = input("Ignore common words? (y/n): ").strip().lower() == "y"
                display_frequency(word_frequency(text, skip), "Word frequency")
            elif choice == "2":
                raw = input("Enter items separated by commas: ")
                items = [x.strip() for x in raw.split(",") if x.strip()]
                display_frequency(element_frequency(items, ignore_case=True), "Element frequency")
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except TypeError as err:
            print("Error:", err)
if __name__ == "__main__":
    menu()
