from classes import AddressBook, Record, Birthday, Phone, Name, Field
import pickle


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError as e:
            return f"Key {e} not found, try again."
        except IndexError:
            return "Index not found, write again."
        except AttributeError as e:
            return f"Attribute error: {e}"
    return inner

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
    
@input_error
def parse_input(user_input):
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args  

@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."
    
    record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)

    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Contact {name} updated."
    else:
        return f"Contact {name} not found."

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return f"{name}: {', '.join(p.value for p in record.phones)}"
    else:
        return f"Contact {name} not found."

@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts found."

    result = []
    for name, record in book.data.items():
        phones = ', '.join(p.value for p in record.phones)
        birthday = record.birthday.value if record.birthday else "No birthday"
        result.append(f"{name}: Phones: {phones}, Birthday: {birthday}")

    return "\n".join(result)

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)

    if record:
        record.birthday = Birthday(birthday)
        return f"Birthday for {name} added: {birthday}"
    else:
        return "Contact not found."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)

    if record and record.birthday:
        return f"Birthday {name}: {record.birthday.value.strftime('%d.%m.%Y')}"
    else:
        return "Contact not found or birthday not set."

@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No greetings for next week."
    
    result = "Greetings for next week:\n"
    for item in upcoming:
        result += f"{item['name']}: {item['birthday']}\n"

    return result.strip()

def main():
    book = load_data()
    print("Welcome to the assistance bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()