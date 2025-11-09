from utils import AddressBook, Record, load_data, save_data

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Data is not valid. Please check"
        except IndexError:
            return "Enter the argument for the command"
        except KeyError:
            return "There is no such name in contacs."
        except AttributeError:
            return "There is no such name in contacs."

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Contact is changed."


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    return record.get_phones()


@input_error
def show_all(book: AddressBook):
    contacts_str = ''
    for user in book:
        contacts_str += f'{book[user]}\n'

    return contacts_str

@input_error
def add_birthday(args, book: AddressBook):
    name, date = args
    record = book.find(name)
    if (record):
        record.add_birthday(date)
        return "Contact is changed."
    else:
        return "Contact is missing"

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    return record.get_birthday()

@input_error
def birthdays(args, book: AddressBook):
    return book.get_upcoming_birthdays()


def main():
    contacts = load_data()
    
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(contacts)
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
