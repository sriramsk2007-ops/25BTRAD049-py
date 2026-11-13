# Recursive function to return the nth Fibonacci number
def recur_fibo(n):
    if n <= 1:
        return n
    return recur_fibo(n - 1) + recur_fibo(n - 2)

def generate_fibonacci_series(terms):
    if terms <= 0:
        print("Please enter a positive integer.")
    else:
        print(f"Generating Fibonacci series for {terms} terms:")
        fib_series = []
        for i in range(terms):
            fib_series.append(str(recur_fibo(i)))
        print(", ".join(fib_series))

if __name__ == "__main__":
    n_terms = 10
    generate_fibonacci_series(n_terms)
