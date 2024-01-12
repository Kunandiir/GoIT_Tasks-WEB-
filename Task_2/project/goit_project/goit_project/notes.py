from collections import UserList
from datetime import datetime
import sqlite3
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table, Column


class Note:
    def __init__(self, name, desc, tag) -> None:
        self.name = name
        self.desc = desc
        self.tag = tag
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self) -> str:
        return f'Name: {self.name}\nDesc: {self.desc}\nTag: {self.tag}\nDate: {self.date}'
    

class NoteBook(UserList):
    def __init__(self):
        self.console = Console()
        self.db = sqlite3.connect(f'{Path.home()}/notes.db')
        self.cursor = self.db.cursor()
        super().__init__()
    
    
    def create_table(self):
        self.cursor.execute(
                '''CREATE TABLE cls_notes (
                id INTEGER PRIMARY KEY,
                name TEXT,
                desc STR,
                tag STR,
                date DATE)'''
            )
        self.db.commit()
        
      
    def add_note(self, table: Table):
        while True:
            record = Note(input('Enter name: '), input('Enter desc: '), input('Enter tag: '))
            if (record.name and record.desc and record.tag) and (record.name != ' ' and record.desc != ' ' and record.tag != ' '):
                dict_record = {'name': record.name, 'desc': record.desc, 'tag': record.tag, 'date': record.date}
                self.data.append(dict_record)
                table.add_row(dict_record['name'], dict_record['desc'], dict_record['tag'], dict_record['date'])
                self.console.print(table)
                break
            else:
                self.console.print('[red]Try again[/]')
        
    
    def all_note(self, table: Table):
        if self.data:
            for note in self.data:
                table.add_row(note['name'], note['desc'], note['tag'], note['date'])
            self.console.print(table)
        else:
            self.console.print('[bold red]Notes are empty[/]')
    
    
    def sort_note(self, table: Table):
        if self.data:
            self.cursor.execute("SELECT * FROM cls_notes ORDER BY tag")
            for note in self.cursor.fetchall():
                table.add_row(str(note[1]), str(note[2]), str(note[3]), str(note[4]))
            self.console.print(table)
        else:
            self.console.print('[bold red]Notes are empty[/]')
        

    def find_note(self, table: Table):
        if self.data:
            key = Prompt.ask('Enter a parameter to search for', choices=['name', 'desc', 'tag'])
            value = input('Enter the value: ')
            for note in self.data:
                if value in note[key]:
                    table.add_row(note['name'], note['desc'], note['tag'], note['date'])
                    self.console.print(table)
                    return note
            self.console.print(f'[red]Notes with parameter "{key}" and value "{value}" not found.[/]')
        else:
            self.console.print('[bold red]Notes are empty[/]')


    def change_note(self, table: Table):
        while True:
            note = self.find_note(table)
            if not note:
                continue
            yn = Prompt.ask(f'Is this the note you wanted to find?', choices=['y','n'])
            if yn == 'y':
                key = Prompt.ask('Enter the parameter you want to change', choices=['name', 'desc', 'tag'])
                value = input('Enter the value: ')
                note[key] = value
                table.add_row(note['name'], note['desc'], note['tag'], note['date'])
                self.console.print(table)
                break


    def delete_note(self, table: Table):
        while True:
            note = self.find_note(table)
            if not note:
                continue
            yn = Prompt.ask(f'Is this the note you want to delete?', choices=['y','n'])
            if yn == 'y':           
                self.data.remove(note)
                self.console.print('[green]Succsessfully deleted[/]')
                break

    
    def load_note(self):
        self.cursor.execute(f"DELETE FROM cls_notes")
        self.db.commit()
        for note in self.data:
            self.cursor.execute("INSERT INTO cls_notes (name, desc, tag, date) VALUES (?, ?, ?, ?)",
                (note['name'], note['desc'], note['tag'], note['date']))
        self.db.commit()
        # print('Load')

    def dump_note(self):
        self.cursor.execute("SELECT * FROM cls_notes")
        self.data = []
        for note in self.cursor.fetchall():
            dict_note = {'id': note[0], 'name': str(note[1]), 'desc': str(note[2]), 'tag': str(note[3]), 'date': str(note[4])}
            self.data.append(dict_note)    
        # print('Dump')

    def bye(self):
        self.console.print('[green]Good bye![/]❤️')
        return exit()



def main():
    nbook = NoteBook()
    
    try:
        nbook.create_table()
    except:
        pass
    
    while True:
        try:
            nbook.dump_note()
            table = Table(
                    Column(header='Name', justify='center'),
                    Column(header='Description', justify='center'),
                    Column(header='Tag', justify='center'),
                    Column(header='Date', justify='center'),
                    title='NoteBook',
                    show_lines=True
                    )
            enter = Prompt.ask('[blue]Enter command[/]').lower().strip()
            if enter == 'add-note':
                nbook.add_note(table)
            elif enter == 'all-note':
                nbook.all_note(table)
            elif enter == 'sort-note':
                nbook.sort_note(table)
            elif enter == 'find-note':
                nbook.find_note(table)
            elif enter == 'change-note':
                nbook.change_note(table)
            elif enter == 'delete-note':
                nbook.delete_note(table)
            elif enter in ['close', 'exit', 'good bye']:
                nbook.bye()
            else:
                print('Wrong command(')
        finally:
            nbook.load_note()
        
if __name__ == '__main__':
    main()
