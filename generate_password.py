import random
import string

def generate_password(length=30, include_uppercase=True, include_numbers=True, include_symbols=True):
    """Generates a random password with customizable options.

    Args:
        length (int, optional): The desired length of the password. Defaults to 12.
        include_uppercase (bool, optional): Whether to include uppercase letters. Defaults to True.
        include_numbers (bool, optional): Whether to include numbers. Defaults to True.
        include_symbols (bool, optional): Whether to include symbols. Defaults to True.

    Returns:
        str: The generated password.
    """

    characters = string.ascii_lowercase
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_numbers:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def main():
    # Example usage:
    password = generate_password()
    print(password)  # Output: a random password with default options

    password_without_symbols = generate_password(include_symbols=False)
    print(password_without_symbols)  # Output: a random password without symbols

if __name__ == "__main__":
    main()
    