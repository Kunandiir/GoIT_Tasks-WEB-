
from datetime import datetime,timedelta
import re
from pathlib import Path
import shutil
import sys
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
#pip install prompt_toolkit
import os
import atexit
import pickle


from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table, Column
try:
    from goit_project.notes import NoteBook
except: from notes import NoteBook


email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

class Field():
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value

# class Birthday validate birthday entered by user
class Birthday(Field):

    @Field.value.setter
    def value(self, value):
        if value != None:
            if datetime.today().date() >= datetime.strptime(value, "%d.%m.%Y").date():
                self._value = datetime.strptime(value, "%d.%m.%Y").date()
            else:
                print(f"Incorect birthday date, use format dd.mm.yy")

# class Record stores all contacts information
class Record():
    _record_id = 0
    def __init__(self, name, birthday = None, address = None) -> None:
        Record._record_id += 1
        self.id = Record._record_id
        self.name = name
        self.phones = []
        self.mails = []
        self.address = address
        self.birthday = Birthday(birthday)

    # to see what Record contains
    def __str__(self) -> str:
        return f"ID:{self.id},Name: {self.name}, Phones: {[phone for phone in self.phones]}, Mails: {[mail for mail in self.mails]}, Birthday: {self.birthday.value}, Address: {self.address}"
    

class PersonalAssistant:
    def __init__(self):
        self.contacts = []
        self.notes = []
        self.file_path = Path.home() / "personal_assistant_data.pkl"
        self.load_data()
        if len(self.contacts) > 0:
            Record._record_id = len(self.contacts)
        atexit.register(self.save_data_on_exit)  # Register the function for atexit
        self.console = Console()

    def load_data(self):
        if self.file_path.exists():
            with open(self.file_path, "rb") as file:
                saved_data = pickle.load(file)
                self.contacts = saved_data.get("contacts", [])
                self.notes = saved_data.get("notes", [])

    def save_data(self):
        data_to_save = {"contacts": self.contacts, "notes": self.notes}
        with open(self.file_path, "wb") as file:
            pickle.dump(data_to_save, file)

    def save_data_on_exit(self):
        self.save_data()
        self.console.print("[green]Data saved before exiting.[/]")

    def add_contact(self):
        
        inputs = input('Enter name [Example: Name]: ')
        record = Record(inputs)

        while True:
            inputs = input('Enter phone number [Example: +00000000]: ')
            if inputs !='':
                if not re.match(r'^\+\d{1,4}\d{6,}$', inputs):
                    self.console.print("[red]Invalid phone number.[/]")
                else:
                    record.phones.append(inputs)
                    break

        while True:
            inputs = input('Enter maill [Example: mail@ua.com]: ')
            if inputs !='':
                if not inputs or not re.match(email_regex, inputs):
                    self.console.print("[red]Invalid email. Please provide a valid email address.[/]")
                else:
                    record.mails.append(inputs)
                    break

        while True:
            new_birthday = input('Enter new birthday [Example: 11.11.1111]: ')
            if new_birthday != '':
                try:
                    birthday_date = datetime.strptime(new_birthday, '%d.%m.%Y')
                    if birthday_date > datetime.now():
                        self.console.print("[red]Entered birthday is in the future. Please enter a valid date.[/]")
                    else:
                        record.birthday = Birthday(new_birthday)
                        break
                except ValueError:
                    self.console.print("[red]Incorrect birthday date format. Use the format dd.mm.yyyy.[/]")

        inputs = input('Enter address [Example: address]: ')
        if inputs != '':
            record.address = inputs
            self.contacts.append(record)

    def restor_id(self):
        record_id = 0
        for contact in self.contacts:
            record_id += 1
            contact.id = record_id
            Record._record_id = record_id

    def show_contacts(self, table_adressbook):
        for contact in self.contacts:
            table_adressbook.add_row(contact.name, ",".join(contact.phones), ",".join(contact.mails), str(contact.birthday.value), contact.address)
        self.console.print(table_adressbook)

    # task_2/ return a list of contacts whose birthday is after a specified number of days from the current date
    def get_birthdays(self, table_adressbook):
        days = int(input('Enter amount of days: '))
        today = datetime.today()
        next_birthday = today.date() + timedelta(days=days)
        for user in self.contacts:
            ignor_year = user.birthday.value.replace(year=today.year) #to ignore year
            if ignor_year < today.date():
                ignor_year = ignor_year.replace(year = today.year +1)
            if today.date() <= ignor_year <= next_birthday:
                table_adressbook.add_row(user.name, ",".join(user.phones), ",".join(user.mails), str(user.birthday.value), user.address)
        self.console.print(table_adressbook)


    # task 4
    def search_contact(self, name, table_adressbook):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                table_adressbook.add_row(contact.name, ",".join(contact.phones), ",".join(contact.mails), str(contact.birthday.value), contact.address)
                self.console.print(table_adressbook)
                return contact    
        self.console.print(f'[red]Contact {name} not found.[/]')
                
        

    # task 5
    def edit_contact(self, name, table_adressbook):
        contact = self.search_contact(name, table_adressbook) # проходимся по контактах
        if contact:
            print('Enter new information: ')
            new_name = input('Enter new name: ')
            if new_name != '':
                contact.name = new_name
            while True:
                new_phones = input('Enter phone number [Example: +00000000]: ')
                if new_phones !='':
                    new_phones = new_phones.replace(',', '')  # Remove commas
                    if not re.match(r'^\+\d{1,4}\d{6,}$', new_phones):
                        self.console.print("[red]Invalid phone number.[/]")
                    else:
                        contact.phones = [new_phones]
                        break
                else:
                    break
            while True:
                new_mails = input('Enter maill [Example: mail@ua.com]: ')
                if new_mails != '':
                    if not new_mails or not re.match(email_regex, new_mails):
                        self.console.print("[red]Invalid email. Please provide a valid email address.[/]")
                    else:
                        contact.mails = [new_mails]
                        break
                else:
                    break
            while True:
                new_birthday = input('Enter new birthday [Example: 11.11.1111]: ')
                if new_birthday != '':
                    try:
                        birthday_date = datetime.strptime(new_birthday, '%d.%m.%Y')
                        if birthday_date > datetime.now():
                            self.console.print("[red]Entered birthday is in the future. Please enter a valid date.[/]")
                        else:
                            contact.birthday = Birthday(new_birthday)
                            break
                    except ValueError:
                        self.console.print("[red]Incorrect birthday date format. Use the format dd.mm.yyyy.[/]")
                else:
                    break

            new_address = input('Enter new address: ')
            if new_address != '':
                contact.address = new_address
            self.console.print(f'[green]Contact {name} redactioned successfully.[/]')

    def delete_contact(self, name, table_adressbook):
        
        contact = self.search_contact(name, table_adressbook) #проходимся по контактах
        if contact:
            self.contacts.remove(contact)
            self.console.print(f'[green]Contact {name} deleted successfully.[/]')
        
        self.restor_id()


#    task_11(self):

class CleanFolder():
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    trans = dict()

    for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        trans[ord(cyrillic)] = latin
        trans[ord(cyrillic.upper())] = latin.upper()
        
    def normalize(name: str) -> str:
        translate_name = re.sub(r'\W', '_', name.translate(CleanFolder.trans))
        translate_name = ".".join(translate_name.rsplit("_",1))
        return translate_name

    #--------------------------------------------------
    JPEG_IMAGES = []
    PNG_IMAGES=[]
    JPG_IMAGES = []
    SVG_IMAGES = []
    AVI_VIDEO = []
    MP4_VIDEO = []
    MOV_VIDEO = []
    MKV_VIDEO = []
    DOC_DOCUMENTS = []
    DOCX_DOCUMENTS = []
    TXT_DOCUMENTS = []
    PDF_DOCUMENTS = []
    XLSX_DOCUMENTS = []
    PPTX_DOCUMENTS = []
    MP3_AUDIO = []
    OGG_AUDIO = []
    WAV_AUDIO = []
    AMR_AUDIO = []
    ARCHIVES = []
    MY_OTHERS = []

    REGISTER_EXTENSION = {
        'JPEG': JPEG_IMAGES,
        'PNG': PNG_IMAGES,
        'JPG': JPG_IMAGES,
        'SVG': SVG_IMAGES,
        'AVI': AVI_VIDEO,
        'MP4': MP4_VIDEO,
        'MOV': MOV_VIDEO,
        'MKV': MKV_VIDEO,
        'DOC': DOC_DOCUMENTS,
        'DOCX': DOCX_DOCUMENTS,
        'TXT': TXT_DOCUMENTS,
        'PDF': PDF_DOCUMENTS,
        'XLSX': XLSX_DOCUMENTS,
        'PPTX': PPTX_DOCUMENTS,
        'MP3': MP3_AUDIO,
        'OGG': OGG_AUDIO,
        'WAV': WAV_AUDIO,
        'AMR': AMR_AUDIO,
        'ZIP': ARCHIVES,
        'GZ': ARCHIVES,
        'TAR': ARCHIVES,
    }

    FOLDERS = []
    EXTENSIONS = set()
    UNKNOWN = set()

    def get_extension(name: str) -> str:
        return Path(name).suffix[1:].upper()

    def scan(folder: Path):
        for item in folder.iterdir():
            # Робота з папкою
            if item.is_dir():  # перевіріямо чи обєкт папка
                if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                    CleanFolder.FOLDERS.append(item)
                    CleanFolder.scan(item)
                continue
            
            # Робота з файлами                    
            extension = CleanFolder.get_extension(item.name) # беремо розширення файлу
            full_name = folder / item.name # беремо повний шлях до файлу
            if not extension:
                CleanFolder.MY_OTHERS.append(full_name)
            else:
                try:
                    ext_reg = CleanFolder.REGISTER_EXTENSION[extension]
                    ext_reg.append(full_name)
                    CleanFolder.EXTENSIONS.add(extension)
                except KeyError:
                    CleanFolder.UNKNOWN.add(extension)
                    CleanFolder.MY_OTHERS.append(full_name)


    def handle_media(file_name: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        file_name.replace(target_folder / CleanFolder.normalize(file_name.name))
        
    def handle_documents(file_name: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        file_name.replace(target_folder / CleanFolder.normalize(file_name.name))
        
    def handle_archive(file_name: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        folder_for_file = target_folder / CleanFolder.normalize(file_name.name.replace(file_name.suffix, ''))
        folder_for_file.mkdir(exist_ok=True, parents=True)
        try:
            shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
        except shutil.ReadError:
            folder_for_file.rmdir()
            return
        file_name.unlink()

    def main(folder: Path):
        CleanFolder.scan(folder)
        for file in CleanFolder.JPEG_IMAGES:
            CleanFolder.handle_media(file, folder / 'images' / 'JPEG')
        for file in CleanFolder.JPG_IMAGES:
            CleanFolder.handle_media(file, folder / 'images' / 'JPG')  
        for file in CleanFolder.PNG_IMAGES:
            CleanFolder.handle_media(file, folder / 'images' / 'PNG')
        for file in CleanFolder.SVG_IMAGES:
            CleanFolder.handle_media(file, folder / 'images' / 'SVG') 
        for file in CleanFolder.AVI_VIDEO:
            CleanFolder.handle_media(file, folder / 'video' / 'AVI')
        for file in CleanFolder.MP4_VIDEO:
            CleanFolder.handle_media(file, folder / 'video' / 'MP4')
        for file in CleanFolder.MOV_VIDEO:
            CleanFolder.handle_media(file, folder / 'video' / 'MOV')
        for file in CleanFolder.MKV_VIDEO:
            CleanFolder.handle_media(file, folder / 'video' / 'MKV')
        for file in CleanFolder.DOC_DOCUMENTS:
            CleanFolder.handle_documents(file, folder / 'documents' / 'DOC')
        for file in CleanFolder.DOCX_DOCUMENTS:
            CleanFolder.handle_documents(file, folder / 'documents' / 'DOCX')
        for file in CleanFolder.TXT_DOCUMENTS:
            CleanFolder.handle_documents(file, folder / 'documents' / 'TXT')
        for file in CleanFolder.PDF_DOCUMENTS:
            CleanFolder.handle_documents(file, folder / 'documents' / 'PDF') 
        for file in CleanFolder.XLSX_DOCUMENTS:
            CleanFolder.handle_documents(file, folder / 'documents' / 'XLSX')
        for file in CleanFolder.PPTX_DOCUMENTS:
            CleanFolder.handle_documents(file, folder / 'documents' / 'PPTX')
        for file in CleanFolder.MP3_AUDIO:
            CleanFolder.handle_media(file, folder / 'audio' / 'MP3')
        for file in CleanFolder.OGG_AUDIO:
            CleanFolder.handle_media(file, folder / 'audio' / 'OGG')
        for file in CleanFolder.WAV_AUDIO:
            CleanFolder.handle_media(file, folder / 'audio' / 'WAV')
        for file in CleanFolder.AMR_AUDIO:
            CleanFolder.handle_media(file, folder / 'audio' / 'AMR') 
        for file in CleanFolder.MY_OTHERS:
            CleanFolder.handle_media(file, folder / 'MY_OTHER')   
                
        for file in CleanFolder.ARCHIVES:
            CleanFolder.handle_archive(file, folder / 'ARCHIVES') 
        
        for folder in CleanFolder.FOLDERS[::-1]:
            # видаляємо пусті папки після сортування
            try:
                folder.rmdir()
            except OSError:
                print(f'Error during remove: {folder}')
  





def main():
    nbook = NoteBook()
    
    try:
        nbook.create_table()
    except:
        pass

    assistant = PersonalAssistant()
    commands = ['add_contact','show_contacts', "birthday_day", 'help', 'search_contact',
                'edit_contact', 'delete_contact', 'clean', 'exit','add_note', 'all_note','sort_note',
                'find_note','change_note','delete_note']
    completer = WordCompleter(commands, ignore_case=True)

    while True:
        print("\nEnter the command (For a list of available commands, enter 'help'):")
        command = prompt("> ", completer=completer).lower()

        try:
            nbook.dump_note()
            table_adressbook = Table(
                    Column("Name", justify="center"),
                    Column("Phones", justify="center"),
                    Column("Mails", justify="center"),
                    Column("Birthday", justify="center"),
                    Column("Address", justify="center"),
                    title='Adress Book',
                    show_lines=True
                )
            table = Table(
                    Column(header='Name', justify='center'),
                    Column(header='Description', justify='center'),
                    Column(header='Tag', justify='center'),
                    Column(header='Date', justify='center'),
                    title='NoteBook',
                    show_lines=True
                )
            if command == 'help':
                print(f"Available commands: {', '.join(commands)}")
            elif command == 'add_contact':
                assistant.add_contact()
            elif command == 'show_contacts':
                assistant.show_contacts(table_adressbook)
            elif command == "birthday_day":
                assistant.get_birthdays(table_adressbook)
            elif command == 'search_contact':
                name = input('Enter name to search: ')
                assistant.search_contact(name, table_adressbook)
            elif command == 'edit_contact':
                name = input('Enter contact name to edit: ')
                assistant.edit_contact(name, table_adressbook)
            elif command == 'delete_contact':
                name = input('Enter contact name to delete: ')
                assistant.delete_contact(name, table_adressbook)
            elif command.lower() == 'clean':
                path = input("Write a path: ")

                if Path(path).exists():
                    folder_process = Path(path).resolve()
                    CleanFolder.main(folder_process)
                    print("Done")
                else:
                    print("You wrote a wrong directory")
            elif command == 'add_note':
                nbook.add_note(table)
            elif command == 'all_note':
                nbook.all_note(table)
            elif command == 'sort_note':
                nbook.sort_note(table)
            elif command == 'find_note':
                nbook.find_note(table)
            elif command == 'change_note':
                nbook.change_note(table)
            elif command == 'delete_note':
                nbook.delete_note(table)
            elif command == 'exit':
                print("Goodbye!")
                break
            else:
                print("Unknown command. Type 'help' for a list of available commands")
        finally:
            nbook.load_note()

if __name__ == "__main__":
    main()