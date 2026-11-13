# Part A: Prime Number Checker
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Part B: Iterative Factorial Calculator
def factorial(n):
    if n < 0:
        return "Undefined for negative numbers"
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

if __name__ == "__main__":
    print("--- Part A: Prime Checker ---")
    test_numbers = [17, 12]
    for num in test_numbers:
        if is_prime(num):
            print(f"{num} is a prime number.")
        else:
            print(f"{num} is not a prime number.")

    print("\n--- Part B: Factorial ---")
    num_fact = 5
    print(f"Factorial of {num_fact} is: {factorial(num_fact)}")
