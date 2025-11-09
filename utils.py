from collections import UserDict
from datetime import datetime, timedelta
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Birthday(Field):
    def __init__(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        if (len(phone) == 10 and phone.isdigit()):
            self.value = phone
        else:
            raise ValueError('Wrong number, expect 10 digits')

    def update_phone(self, value):
        if (len(value) == 10 and value.isdigit()):
            self.value = value
        else:
            raise ValueError('Wrong number, expect 10 digits')


class Record():
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone = self.find_phone(phone)
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)
        phone.update_phone(new_phone)

    def get_birthday(self):
        return self.birthday

    def find_phone(self, f_phone) -> Phone:
        phone = list(filter(lambda phone: phone.value == f_phone, self.phones))
        if (not phone):
            return None

        return phone[0]
    
    def get_phones(self):
        if (not len(self.phones)):
            return None

        return [p.value for p in self.phones]

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value if self.birthday else 'None'}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name) -> Record:
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        users = self.data.values()
        users_to_congratulate = []
        today_date = datetime.today()
        endDate = today_date.date() + timedelta(days=7)

        for user in users:
            if not user.birthday:
                continue

            user_birthday_in_2025 = user.birthday.value.replace(year=today_date.year)

            if (user_birthday_in_2025.date() < today_date.date()):
                user_birthday_in_2025 = user_birthday_in_2025.replace(year=today_date.year + 1)

            if (today_date.date() <= user_birthday_in_2025.date() <= endDate):
                user_birthday_weekday = user_birthday_in_2025.weekday()
                congratulation_date = user_birthday_in_2025

                if (user_birthday_weekday == 5 or user_birthday_weekday == 6):
                    congratulation_date = user_birthday_in_2025 + timedelta(days= (7 - user_birthday_weekday))

                users_to_congratulate.append({
                    'name': user.name.value,
                    'congratulation_date': datetime.strftime(congratulation_date, '%Y.%m.%d')
                })

        return users_to_congratulate
    

def save_data(book, filename="addressbook.pkl"):
    print('book', book)
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
            return data
    except FileNotFoundError:
        return AddressBook()