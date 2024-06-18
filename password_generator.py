import random
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import pyperclip

console = Console()

def yes_or_no(question):
    """Prompt the user with a yes or no question."""
    return Prompt.ask(question, choices=["Y", "N", "y", "n"], default="Y").strip().upper() == 'Y'

def generate_password(include_numbers, include_letters, include_special, include_both_cases, length):
    """Generate a password based on the specified criteria."""
    uppercase_letters = "QWERTYUIOPASDFGHJKLZXCVBNM"
    lowercase_letters = "qwertyuiopasdfghjklzxcvbnm"
    special_characters = "!@#$%^&*/-+."
    numbers = str(random.randint(0, 999999999))

    password_characters = ""
    if include_numbers:
        password_characters += numbers
    if include_special:
        password_characters += special_characters
    if include_letters:
        if include_both_cases:
            password_characters += uppercase_letters + lowercase_letters
        else:
            password_characters += lowercase_letters

    if not password_characters:
        return None

    password_parts = [random.choice(numbers) if include_numbers else '',
                      random.choice(special_characters) if include_special else '',
                      random.choice(uppercase_letters + lowercase_letters) if include_letters else '']

    remaining_length = max(0, length - len(''.join(password_parts)))
    remaining_characters = ''.join(random.choice(password_characters) for _ in range(remaining_length))
    final_password = ''.join(password_parts) + remaining_characters
    return final_password

def show_interface():
    table = Table(title="Password Generator", title_style="bold blue")
    table.add_column("Option", justify="right", style="bold cyan")
    table.add_column("Description", justify="left", style="bold green")

    table.add_row("1", "Generate a password")
    table.add_row("2", "Exit")
    table.add_row("3", "Generate multiple passwords")

    console.print(table)

def check_password_strength(password):
    password_length = len(password)
    strength = 0
    recommendations = []

    if any(char.isdigit() for char in password):
        strength += 1
    else:
        recommendations.append("Add a number.")

    if any(char.islower() for char in password):
        strength += 1
    else:
        recommendations.append("Add lowercase letters.")

    if any(char.isupper() for char in password):
        strength += 1
    else:
        recommendations.append("Add uppercase letters.")

    if any(char in "!@#$%^&*/-+." for char in password):
        strength += 1
    else:
        recommendations.append("Add special characters.")

    if password_length < 8:
        recommendations.append("Increase the password length to at least 8 characters.")

    if password_length >= 12 and strength >= 3:
        return "Strong password", "green", recommendations
    elif password_length >= 8 and strength >= 2:
        return "Medium password", "yellow", recommendations
    else:
        return "Weak password", "red", recommendations

def copy_to_clipboard(password):
    pyperclip.copy(password)
    console.print("Password copied to clipboard!", style="bold green")

def save_password(password, file_prefix="", appended=False):
    """Save the password to a file."""
    file_name = f"{file_prefix}passwords.txt" if file_prefix else "saved_password.txt"
    with open(file_name, "a") as file:
        file.write(password + "\n")
    if not appended:
        console.print(f"Password saved in {file_name}!", style="bold green")

def generate_and_save_multiple_passwords(count, include_numbers, include_letters, include_special, include_both_cases, length):
    passwords = []

    print("Generating passwords:", end=' ')
    for i in range(count):
        passwords.append(generate_password(include_numbers, include_letters, include_special, include_both_cases, length))
        
        progress = int((i + 1) / count * 50)
        print("\r[" + "#" * progress + " " * (50 - progress) + f"] {i + 1}/{count}", end='')
    print("\n")

    return passwords

def main():
    while True:
        show_interface()
        choice = Prompt.ask("Choose an action", choices=["1", "2", "3"])

        if choice == "2":
            console.print(Panel(Text("Goodbye, friend!", justify="center"), title="Goodbye!", border_style="red"))
            break

        console.print(Panel(Text("Generating password", justify="center"), title="Create", border_style="green"))

        include_numbers = yes_or_no("Do you want to include numbers?: ")
        include_letters = yes_or_no("Do you want to include letters?: ")
        include_special = yes_or_no("Do you want to include special characters?: ")

        include_both_cases = False
        length = 0  

        if include_letters:
            include_both_cases = yes_or_no("Do you want to include both uppercase and lowercase letters?: ")
            while True:
                try:
                    length = int(Prompt.ask("Enter the password length: ", default="16"))
                    break
                except ValueError:
                    console.print(Panel(Text("ERROR. Please enter a number.", justify="center"), title="Error", border_style="red", style="bold"))

        if choice == "1":
            password = generate_password(include_numbers, include_letters, include_special, include_both_cases, length)
            if password:
                strength, color, recommendations = check_password_strength(password)
                console.print(Panel(Text(f"{password}\nPassword strength: ", style=color) + Text(strength, style=color), title="Generated Password", border_style="green"))

                if recommendations:
                    recommendations_text = "\n".join(recommendations)
                    console.print(Panel(Text(recommendations_text), title="Recommendations", border_style="green", style="blue"))

                copy = yes_or_no("Do you want to copy the password to the clipboard?: ")
                if copy:
                    copy_to_clipboard(password)
                save = yes_or_no("Do you want to save the password?: ")
                if save:
                    save_password(password)
            else:
                console.print(Panel(Text("No settings selected.", justify="center"), title="Error", border_style="red"))

        elif choice == "3":
            num_passwords = int(Prompt.ask("Enter the number of passwords you want to generate: ", default="10"))
            passwords = generate_and_save_multiple_passwords(num_passwords, include_numbers, include_letters, include_special, include_both_cases, length)
            copy = yes_or_no("Do you want to copy the first password to the clipboard?: ")
            if copy:
                copy_to_clipboard(passwords[0])
            save_all = yes_or_no("Do you want to save all the passwords?: ")
            if save_all:
                appended = False
                for password in passwords:
                    save_password(password, file_prefix=f"{num_passwords}_", appended=appended)
                    appended = True 

if __name__ == "__main__":
    main()
