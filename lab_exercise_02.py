# Create the student_info dictionary
student_info = {
    "name": "Sriram Satvik       ",
    "age": 19,
    "major": "Computer Science - Artificial Intelligence & Data Engineering",
    "university": "Jain University, Bangalore"
}

# Print some initial details
print("Name:", student_info["name"])
print("Age:", student_info["age"])

# Add a new key
student_info["email"] = "09Sriram Satvik @gmail.com"

# Update an existing key
student_info["age"] = 19

# Remove a key
del student_info["major"]

# Print the final dictionary
print(student_info)
