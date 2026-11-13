import random
import string

def generate_otp(length=6, alphanumeric=False):
    """Generate a numeric or alphanumeric one-time passcode."""
    if length <= 0:
        raise ValueError("OTP length must be positive.")

    if alphanumeric:
        char_pool = string.ascii_letters + string.digits
    else:
        char_pool = string.digits

    return "".join(random.choice(char_pool) for _ in range(length))

if __name__ == "__main__":
    print("--- OTP GENERATION EXPERIMENTS ---")
    numeric_6 = generate_otp(length=6, alphanumeric=False)
    print(f"[CASE 1] 6-Digit Numeric OTP:      {numeric_6}")

    numeric_4 = generate_otp(length=4, alphanumeric=False)
    print(f"[CASE 2] 4-Digit Numeric OTP:      {numeric_4}")

    alphanumeric_6 = generate_otp(length=6, alphanumeric=True)
    print(f"[CASE 3] 6-Char Alphanumeric OTP:  {alphanumeric_6}")

    alphanumeric_10 = generate_otp(length=10, alphanumeric=True)
    print(f"[CASE 4] 10-Char Security Key:    {alphanumeric_10}")
