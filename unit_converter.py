# MINI PROJECT 1: UNIT CONVERTER

# Length conversions
def km_to_miles(km):
    return km * 0.621371

def miles_to_km(miles):
    return miles / 0.621371

def meters_to_feet(m):
    return m * 3.28084

def feet_to_meters(feet):
    return feet / 3.28084

# Weight conversions
def kg_to_pounds(kg):
    return kg * 2.20462

def pounds_to_kg(pounds):
    return pounds / 2.20462

# Temperature conversions
def celsius_to_fahrenheit(c):
    return (c * 9 / 5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9

def celsius_to_kelvin(c):
    return c + 273.15

if __name__ == "__main__":
    print("=" * 50)
    print("UNIT CONVERTER".center(50))
    print("=" * 50)

    print("\n-- Length --")
    km = 15
    print(f"{km} km = {km_to_miles(km):.2f} miles")
    miles = 10
    print(f"{miles} miles = {miles_to_km(miles):.2f} km")
    meters = 250
    print(f"{meters} meters = {meters_to_feet(meters):.2f} feet")
    feet = 100
    print(f"{feet} feet = {feet_to_meters(feet):.2f} meters")

    print("\n-- Weight --")
    kg = 70
    print(f"{kg} kg = {kg_to_pounds(kg):.2f} pounds")
    pounds = 150
    print(f"{pounds} pounds = {pounds_to_kg(pounds):.2f} kg")

    print("\n-- Temperature --")
    temp_c = 37
    print(f"{temp_c} C = {celsius_to_fahrenheit(temp_c):.2f} F")
    print(f"{temp_c} C = {celsius_to_kelvin(temp_c):.2f} K")
    temp_f = 98.6
    print(f"{temp_f} F = {fahrenheit_to_celsius(temp_f):.2f} C")

    print("\n" + "=" * 50)
