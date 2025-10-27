import re
from typing import Callable
from functools import wraps

"""Parse user input and return command and arguments."""
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

"""Decorator to handle input errors for command functions."""
def input_error(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Error: Missing arguments"
        except KeyError as e:
            return "Error: Contact not found: " + str(e)
        except ValueError as e:
            return "Error: Invalid value: " + str(e)
    return wrapper

"""Add a new contact to the contacts dictionary."""
@input_error
def add_contact(args, contacts):
    name = args[0]
    phone = args[1]

    if not re.match(r"^[\d\+\-\(\)\s]+$", phone) or len(phone) < 5: #Match one or more characters that are digits, plus signs, hyphens, parentheses, or whitespace
        raise ValueError("phone number should contain only digits, spaces, and these symbols: + - ( )")
    if name in contacts:
        return "Contact already exists, for update use the 'change' command."

    contacts[name] = phone
    return "Contact added."

"""Change an existing contact's phone number."""
@input_error
def change_contact(args, contacts):
    name = args[0]
    phone = args[1]
    contacts[name] = phone
    return "Contact updated."

"""Show phone number for a specific contact."""
@input_error
def show_phone(args, contacts):
    name = args[0]
    return contacts[name]

"""Show all contacts."""
def show_all(contacts):
    if not contacts:
        return "No contacts saved."
    result = []
    for name, phone in contacts.items():
        result.append(f"{name}: {phone}")
    return "\n".join(result)


"""Main function to run the bot assistant for managing contacts."""
def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    print("Here you can manage your contacts. Available commands:")
    print(" command | parameters     | description                   |")
    print("---------|----------------|-------------------------------|")
    print(" add     | <name> <phone> | adds a new contact            |")
    print(" change  | <name> <phone> | changes an existing contact   |")
    print(" phone   | <name>         | shows a contact's phone number|")
    print(" all     |                | shows all contacts            |")
    print(" exit    |                | closes the bot                |")

    while True:
        user_input = input("Enter a command: ").strip()
        
        if not user_input:
            continue
            
        command, *args = parse_input(user_input)
        
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()


