import tkinter as tk
from tkinter import filedialog

try:
    from goit_project.main import PersonalAssistant,Record,Birthday,CleanFolder
    from goit_project.notes import NoteBook,Note,Path
except:
    from main import PersonalAssistant,Record,Birthday,CleanFolder
    from notes import NoteBook,Note,Path
from datetime import datetime
import customtkinter as ctk
import re
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
class App(ctk.CTk):

    # Generate naster form for App
    def __init__(self):
        super().__init__()
        
        # configure window
        self.title("GoIT_Project Group-13")
        self.geometry(f"{1100}x{580}")

        # configure grid layout
        self.grid_columnconfigure(0, weight=1,)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self)
        self.sidebar_frame.grid(row=0,column=0,rowspan=4,padx=0,pady=0,sticky='nsew')
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)


        # add sidebar functions
        self.sidebar_logo = ctk.CTkLabel(self.sidebar_frame, text='Functions',font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_logo.grid(row=0,column=0,padx=0,pady=(10,10),sticky='new')
        self.sidebar_addphone_button =ctk.CTkButton(self.sidebar_frame, text='Add new phone', command=self.generate_add_contact_frame)
        self.sidebar_addphone_button.grid(row=1,column=0,padx=0,pady=(0,10),sticky='new')
        self.sidebar_addnote_button = ctk.CTkButton(self.sidebar_frame, text='Add new note', command=self.generate_note_add_frame)
        self.sidebar_addnote_button.grid(row=2,column=0,padx=0,pady=(0,10),sticky='new')
        self.sidebar_clean_folder_button = ctk.CTkButton(self.sidebar_frame, text='Sort foldder', command=self.sort_folder)
        self.sidebar_clean_folder_button.grid(row=3,column=0,padx=0,pady=(0,10),sticky='new')
        


        # add logo
        self.logo_label = ctk.CTkLabel(self, text="ProjectX", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0,column=1,padx=0, pady=(10, 5),sticky='n')

        # create tabview
        self.tabview = ctk.CTkTabview(self,fg_color='transparent')
        self.tabview.grid(row=0, column=1, padx=(10,10), pady=(40, 10),sticky='nsew')
        self.tabview.add("Contacts")
        self.tabview.add("Notes")
        self.tabview.tab("Contacts").grid_columnconfigure((0,1,2,3,4), weight=1)
        self.tabview.tab("Notes").grid_columnconfigure((0,1,2,3,4), weight=1)
        self.generate_contact_list(assistant.contacts)
        self.generate_notes_list(nbook.data)
           
    # Generate main contact list with all contacts
    def generate_contact_list(self, list):
        # create search
        self.search_entry = ctk.CTkEntry(self.tabview.tab("Contacts"), placeholder_text="Search")
        self.search_entry.grid(row=0, column=0, columnspan=4, padx=(10, 0), pady=(10, 0), sticky="nsew")
        
        self.search_button = ctk.CTkButton(self.tabview.tab("Contacts"),text='Search', text_color=("gray10", "#DCE4EE"))
        self.search_button.configure(command=lambda: self.search_contact(self.search_entry.get()))
        self.search_button.grid(row=0, column=4, padx=(5, 10), pady=(10, 0), sticky="nsew")
        # create scrollable frame

        self.phones_list = ctk.CTkScrollableFrame(self.tabview.tab("Contacts"),height=350, label_text="Phone list", fg_color='black')
        self.phones_list.grid(row=1,column=0,columnspan=5, padx=0, pady=(5,0), sticky="ew")
        self.phones_list.grid_columnconfigure(0, weight=1)

        for r, contact in enumerate(list, start=1):
            self.phone_frame =  ctk.CTkFrame(self.phones_list)
            self.phone_frame.grid(row=r,column=0,padx=10,pady=(0,20),sticky='new')
            self.phone_frame.grid_columnconfigure(0, weight=1)
            self.phone_frame.grid_columnconfigure((1,2), weight=20)
            self.phone_frame.grid_columnconfigure(3,weight=1)
            self.name_label = ctk.CTkLabel(self.phone_frame, text= contact.name, font=ctk.CTkFont(size=18, weight="bold"))
            self.name_label.grid(row=0,column=1,rowspan=2,padx=0,pady=0, sticky='nsw')
            self.address_label = ctk.CTkLabel(self.phone_frame, text=contact.address, font=ctk.CTkFont(size=15, weight="bold"))
            self.address_label.grid(row=0,column=2,padx=0,pady=0,sticky='nse')
            try:
                self.birthday_label = ctk.CTkLabel(self.phone_frame, text=contact.birthday.value.strftime('%d.%m.%Y'),font=ctk.CTkFont(size=15, weight="bold"))
            except:
                self.birthday_label = ctk.CTkLabel(self.phone_frame, text=contact.birthday.value,font=ctk.CTkFont(size=15, weight="bold"))
            self.birthday_label.grid(row=1,column=2,padx=0,pady=0,sticky='nse')
            for i, number in enumerate(contact.phones):
                self.phone_label = ctk.CTkLabel(self.phone_frame, text= number,font=ctk.CTkFont(size=10, weight="bold"))
                self.phone_label.grid(row=3+i,column=1, padx=0,pady=1,sticky='ns')
            for i, mail in enumerate(contact.mails):
                self.mail_label = ctk.CTkLabel(self.phone_frame, text= mail,font=ctk.CTkFont(size=10, weight="bold"))
                self.mail_label.grid(row=3+i,column=2,padx=0,pady=1,sticky='ns')

            self.edit_button = ctk.CTkButton(self.phone_frame, text='Edit')
            self.edit_button.configure(command=lambda id=contact.id: self.generate_edit_contact_frame(id))
            self.edit_button.grid(row=0,column=3,padx=0,pady=0,sticky='nsew')
            self.delete_button = ctk.CTkButton(self.phone_frame, text='Delete')
            self.delete_button.configure(command=lambda id=contact.id: self.delete_contact(id))
            self.delete_button.grid(row=1,column=3,padx=0,pady=0,sticky='nsew')
    
    # Generate form with inputs for creating new contact
    def generate_add_contact_frame(self):
        form_phone_list = []
        form_mail_list = []
        input_form = ctk.CTkToplevel()
        self.attributes('-disabled', True)
        input_form.lift()
        input_form.focus_force()
        input_form.title('Add new contact')
        input_form.geometry('400x200')
        input_form.grid_columnconfigure(0, weight=1)
        input_form.grid_rowconfigure((0, 1, 2), weight=1)
        phone_frame =  ctk.CTkFrame(input_form)
        phone_frame.grid_columnconfigure((0,1,2), weight=1)
        phone_frame.grid(row=0,column=0,padx=10,pady=(10,0),sticky='nsew')
        name_label = ctk.CTkEntry(phone_frame,placeholder_text="Name",font=ctk.CTkFont(size=18, weight="bold"))
        name_label.grid(row=0,column=0,rowspan=2,padx=0,pady=0, sticky='nsw')
        address_label = ctk.CTkEntry(phone_frame, placeholder_text="Address",font=ctk.CTkFont(size=10, weight="bold"))
        address_label.grid(row=0,column=2,padx=0,pady=0,sticky='nse')
        birthday_label = ctk.CTkEntry(phone_frame,placeholder_text="Birthday(dd.mm.yyyy)",font=ctk.CTkFont(size=10, weight="bold"))
        birthday_label.bind("<Key>", lambda event: self.validate_date_input(event, birthday_label, submit_button))
        birthday_label.grid(row=1,column=2,padx=0,pady=0,sticky='nse')

        phone_label = ctk.CTkEntry(phone_frame,placeholder_text="Number:(+){5-13}",font=ctk.CTkFont(size=10, weight="bold"))
        phone_label.bind("<Key>", lambda event: self.validate_number_input(event, phone_label, submit_button))
        phone_label.grid(row=3,column=0,padx=0,pady=(5,0),sticky='ns')
        mail_label = ctk.CTkEntry(phone_frame,placeholder_text="Mail",font=ctk.CTkFont(size=10, weight="bold"))
        mail_label.bind("<Key>", lambda event: self.validate_mail_input(event, mail_label, submit_button))
        mail_label.grid(row=3,column=2,padx=0,pady=(5,0),sticky='ns')
        form_phone_list.append(phone_label)
        form_mail_list.append(mail_label)
        
        add_button = ctk.CTkButton(phone_frame, text='Add', command=lambda: self.add_entry(phone_frame,form_phone_list,form_mail_list, submit_button))
        add_button.grid(row=0, column=1, padx=5, pady=0, sticky='nswe')
        
        delete_button = ctk.CTkButton(phone_frame, text='Delete', command=lambda: self.delete_entry(form_phone_list, form_mail_list))
        delete_button.grid(row=1, column=1, padx=5, pady=0, sticky='nswe')

        submit_button = ctk.CTkButton(input_form, text='Submit', command=lambda: self.add_new_contact(name_label.get(),birthday_label.get(),address_label.get(),[phone.get() for phone in form_phone_list],[mail.get() for mail in form_mail_list]))
        submit_button.grid(row=1,column=0, columnspan=2,padx=0,pady=0, sticky='nwe')

        input_form.protocol("WM_DELETE_WINDOW", lambda: [self.attributes('-disabled', False), input_form.destroy()])
   
    def add_entry(self, phone_frame, form_phone_list, form_mail_list, submit_button):
        phone_label = ctk.CTkEntry(phone_frame, placeholder_text="Number:(+){5-13}", font=ctk.CTkFont(size=10, weight="bold"))
        phone_label.bind("<Key>", lambda event: self.validate_number_input(event, phone_label, submit_button))
        phone_label.grid(row=len(form_phone_list)+3, column=0, padx=0, pady=1, sticky='ns')
        mail_label = ctk.CTkEntry(phone_frame, placeholder_text="Mail", font=ctk.CTkFont(size=10, weight="bold"))
        mail_label.bind("<Key>", lambda event: self.validate_mail_input(event, mail_label, submit_button))
        mail_label.grid(row=len(form_mail_list)+3, column=2, padx=0, pady=1, sticky='ns')
        form_phone_list.append(phone_label)
        form_mail_list.append(mail_label)
    
    def delete_entry(self, form_phone_list, form_mail_list):
        if form_phone_list and form_mail_list:  # Check if there are entries to delete
            form_phone_list[-1].grid_forget()  # Remove last phone entry from grid
            form_mail_list[-1].grid_forget()  # Remove last mail entry from grid
            form_phone_list.pop()  # Remove last phone entry from list
            form_mail_list.pop()  # Remove last mail entry from list

    # Generate frame whith editable contact information
    def generate_edit_contact_frame(self, id):
        contact = assistant.contacts[id-1]
        form_phone_list = []
        form_mail_list = []
        input_form = ctk.CTkToplevel()
        self.attributes('-disabled', True)
        input_form.title('Edit contact')
        input_form.geometry('400x200')
        input_form.grid_columnconfigure(0, weight=1)
        input_form.grid_rowconfigure((0, 1, 2), weight=1)
        phone_frame =  ctk.CTkFrame(input_form)
        phone_frame.grid_columnconfigure((0,1,2), weight=1)
        phone_frame.grid(row=0,column=0,padx=10,pady=(10,0),sticky='nsew')
        name_label = ctk.CTkEntry(phone_frame,placeholder_text="Name",font=ctk.CTkFont(size=18, weight="bold"))
        name_label.insert(0, contact.name)
        name_label.grid(row=0,column=0,rowspan=2,padx=0,pady=(0, 5), sticky='nsw')
        address_label = ctk.CTkEntry(phone_frame, placeholder_text="Address",font=ctk.CTkFont(size=10, weight="bold"))
        if contact.address !='':
            address_label.insert(0, contact.address)
        address_label.grid(row=0,column=2,padx=0,pady=0,sticky='nse')
        birthday_label = ctk.CTkEntry(phone_frame,placeholder_text="Birthday(dd.mm.yyyy)",font=ctk.CTkFont(size=10, weight="bold"))
        birthday_label.bind("<Key>", lambda event: self.validate_date_input(event, birthday_label, submit_button))
        if contact.birthday.value != None:
            birthday_label.insert(0, contact.birthday.value.strftime('%d.%m.%Y'))
        birthday_label.grid(row=1,column=2,padx=0,pady=(0,5),sticky='nse')
        for r, phone in enumerate(contact.phones):
            phone_label = ctk.CTkEntry(phone_frame,placeholder_text="Number:(+){5-13}",font=ctk.CTkFont(size=10, weight="bold"))
            if phone != '':
                phone_label.insert(0, phone)
            phone_label.bind("<Key>", lambda event: self.validate_number_input(event, phone_label, submit_button))
            phone_label.grid(row=3+r,column=0,padx=0,pady=1,sticky='ns')
            form_phone_list.append(phone_label)
        for r, mail in enumerate(contact.mails):
            mail_label = ctk.CTkEntry(phone_frame,placeholder_text="Mail",font=ctk.CTkFont(size=10, weight="bold"))
            if mail !='':
                mail_label.insert(0, mail)
            mail_label.bind("<Key>", lambda event: self.validate_mail_input(event, mail_label, submit_button))
            mail_label.grid(row=3+r,column=2,padx=0,pady=1,sticky='ns')
            form_mail_list.append(mail_label)

        submit_button = ctk.CTkButton(input_form, text='Submit changes', command=lambda: self.edit_contact(id, name_label.get(),birthday_label.get(),address_label.get(),[phone.get() for phone in form_phone_list],[mail.get() for mail in form_mail_list]))
        submit_button.grid(row=1,column=0, columnspan=2,padx=0,pady=0, sticky='nwe')
        
        add_button = ctk.CTkButton(phone_frame, text='Add', command=self.add_entry(phone_frame,form_phone_list,form_mail_list, submit_button))
        add_button.grid(row=0, column=1, padx=5, pady=0, sticky='nswe')
        
        delete_button = ctk.CTkButton(phone_frame, text='Delete', command=self.delete_entry(form_phone_list, form_mail_list))
        delete_button.grid(row=1, column=1, padx=5, pady=0, sticky='nswe')

        input_form.protocol("WM_DELETE_WINDOW", lambda: [self.attributes('-disabled', False), input_form.destroy()])
    
    # Add new contact
    def add_new_contact(self, name, birthday, address, phones, mails):
        record = Record(name)
        if birthday != '':
            record.birthday = Birthday(birthday)

        record.address = address
        record.phones = phones
        record.mails = mails
        assistant.contacts.append(record)
        self.generate_contact_list(assistant.contacts)

    # Edit contact
    def edit_contact(self, id, name, birthday, address, phones, mails):
        contact = assistant.contacts[id-1]
        contact.name = name
        if birthday != '':
            contact.birthday = Birthday(birthday)
        contact.address = address
        contact.phones = phones
        contact.mails = mails
        self.generate_contact_list(assistant.contacts)
    
    # Delete contact
    def delete_contact(self, id):
        del assistant.contacts[id-1]
        record_id = 0
        for contact in assistant.contacts:
            record_id += 1
            contact.id = record_id
            Record._record_id = record_id
        self.generate_contact_list(assistant.contacts)
    
    # Search contact depends on serch input
    def search_contact(self, value):
        if value == '':
            self.generate_contact_list(assistant.contacts)
        else:
            search_list = []
            for contact in assistant.contacts:
                if value in contact.name:
                    search_list.append(contact)
                elif value in contact.address:
                    search_list.append(contact)
                elif value in ','.join(contact.phones):
                    search_list.append(contact)
                elif value in ','.join(contact.mails):
                    search_list.append(contact) 
            self.generate_contact_list(search_list)
    
    # Sort chosen folder
    def sort_folder(self):
        folder_selected = filedialog.askdirectory()  # Open the dialog box
        if folder_selected != '':
            CleanFolder.main(Path(folder_selected).resolve())

    # Generate notes list
    def generate_notes_list(self, list):
        # Create Search
        self.note_search_entry = ctk.CTkEntry(self.tabview.tab("Notes"), placeholder_text="Search")
        self.note_search_entry.grid(row=0, column=0, columnspan=4, padx=(10, 0), pady=(10, 0), sticky="nsew")
        
        self.note_search_button = ctk.CTkButton(self.tabview.tab("Notes"),text='Search', text_color=("gray10", "#DCE4EE"))
        self.note_search_button.configure(command=lambda: self.search_note(self.note_search_entry.get()))
        self.note_search_button.grid(row=0, column=4, padx=(5, 10), pady=(10, 0), sticky="nsew")

        # create scrollable frame
        self.notes_list = ctk.CTkScrollableFrame(self.tabview.tab("Notes"),height=350, label_text="Notes list", fg_color='black')
        self.notes_list.grid(row=1,column=0,columnspan=5, padx=0, pady=(5,0), sticky="ew")
        self.notes_list.grid_columnconfigure(0, weight=1)

        for r,Note in enumerate(list ,start= 1):
            self.note_frame =  ctk.CTkFrame(self.notes_list)
            self.note_frame.grid(row=r,column=0,padx=10,pady=(0,20),sticky='new')
            self.note_frame.grid_columnconfigure(0, weight=1)
            self.note_frame.grid_columnconfigure((1,2), weight=20)
            self.note_frame.grid_columnconfigure(3,weight=1)
            self.note_name_label = ctk.CTkLabel(self.note_frame, text= Note['name'], font=ctk.CTkFont(size=18, weight="bold"))
            self.note_name_label.grid(row=0,column=1,rowspan=2,padx=0,pady=0, sticky='nsw')
            self.note_tag_label = ctk.CTkLabel(self.note_frame, text=Note['tag'], font=ctk.CTkFont(size=15, weight="bold"))
            self.note_tag_label.grid(row=0,column=2,padx=0,pady=0,sticky='nse')
            self.note_date_label = ctk.CTkLabel(self.note_frame, text=Note['date'],font=ctk.CTkFont(size=15, weight="bold"))
            self.note_date_label.grid(row=1,column=2,padx=0,pady=0,sticky='nse')
            self.note_disc_label = ctk.CTkButton(self.note_frame, text=Note['desc'], font=ctk.CTkFont(size=15, weight="bold"),fg_color=("#212121"), state='disabled')
            self.note_disc_label._text_label.configure(wraplength=700)  # Adjust the wraplength as needed
            self.note_disc_label.grid(row=3, column=1, columnspan=2, padx=0, pady=1, sticky='ns')
            self.note_edit_button = ctk.CTkButton(self.note_frame, text='Edit')
            self.note_edit_button.configure(command=lambda id=Note['id']: self.generat_note_edit_frame(id))
            self.note_edit_button.grid(row=0,column=3,padx=0,pady=0,sticky='nsew')
            self.note_delete_button = ctk.CTkButton(self.note_frame, text='Delete')
            self.note_delete_button.configure(command=lambda id=Note['id']: self.delete_note(id))
            self.note_delete_button.grid(row=1,column=3,padx=0,pady=0,sticky='nsew')

    # Generate note add frame
    def generate_note_add_frame(self):
        notes_add_form = ctk.CTkToplevel()
        self.attributes('-disabled', True)
        notes_add_form.title('Add new note')
        notes_add_form.geometry('400x200')
        notes_add_form.grid_columnconfigure(0, weight=1)
        notes_add_form.grid_rowconfigure((0, 1, 2), weight=1)
        note_frame =  ctk.CTkFrame(notes_add_form)
        note_frame.grid_columnconfigure((0,1,2), weight=1)
        note_frame.grid_rowconfigure(1, weight=1)
        note_frame.grid(row=0,column=0,rowspan=3,padx=10,pady=(10,0),sticky='nsew')
        note_name_label = ctk.CTkEntry(note_frame,placeholder_text='Name',font=ctk.CTkFont(size=18, weight="bold"))
        note_name_label.grid(row=0,column=0,padx=0,pady=0, sticky='nsw')
        note_tag_label = ctk.CTkEntry(note_frame, placeholder_text='Tag',font=ctk.CTkFont(size=15, weight="bold"))
        note_tag_label.grid(row=0,column=2,padx=0,pady=0,sticky='nse')
        note_desc_label = ctk.CTkTextbox(note_frame, font=ctk.CTkFont(size=15, weight="bold"),border_width= 2, border_color='#565B5E')
        note_desc_label.insert('1.0', 'Description')
        note_desc_label.grid(row=1,column=0,columnspan=3,rowspan=1,padx=0,pady=(5,0),sticky='nsew')
        note_submit_button = ctk.CTkButton(notes_add_form, text='Submit changes')
        note_submit_button.configure(command=lambda: self.add_note(note_name_label.get(),note_tag_label.get(),note_desc_label.get("1.0", "end-1c")))
        note_submit_button.grid(row=3,column=0, columnspan=3,padx=0,pady=0, sticky='nwe')

        notes_add_form.protocol("WM_DELETE_WINDOW", lambda: [self.attributes('-disabled', False), notes_add_form.destroy()])

    # Generate notes edit frame
    def generat_note_edit_frame(self, id):
        note = nbook[id-1]
        notes_edit_form = ctk.CTkToplevel()
        self.attributes('-disabled', True)
        notes_edit_form.title('Add new note')
        notes_edit_form.geometry('400x200')
        notes_edit_form.grid_columnconfigure(0, weight=1)
        notes_edit_form.grid_rowconfigure((0, 1, 2), weight=1)
        note_frame =  ctk.CTkFrame(notes_edit_form)
        note_frame.grid_columnconfigure((0,1,2), weight=1)
        note_frame.grid_rowconfigure(1, weight=1)
        note_frame.grid(row=0,column=0,rowspan=3,padx=10,pady=(10,0),sticky='nsew')
        note_name_label = ctk.CTkEntry(note_frame,placeholder_text='Name',font=ctk.CTkFont(size=18, weight="bold"))
        note_name_label.insert(0, note['name'])
        note_name_label.grid(row=0,column=0,padx=0,pady=0, sticky='nsw')
        note_tag_label = ctk.CTkEntry(note_frame, placeholder_text='Tag',font=ctk.CTkFont(size=15, weight="bold"))
        note_tag_label.insert(0, note['tag'])
        note_tag_label.grid(row=0,column=2,padx=0,pady=0,sticky='nse')
        note_desc_label = ctk.CTkTextbox(note_frame, font=ctk.CTkFont(size=15, weight="bold"),border_width= 2, border_color='#565B5E')
        note_desc_label.insert('1.0', note['desc'])
        note_desc_label.grid(row=1,column=0,columnspan=3,rowspan=1,padx=0,pady=(5,0),sticky='nsew')
        note_submit_button = ctk.CTkButton(notes_edit_form, text='Submit changes')
        note_submit_button.configure(command=lambda: self.edit_note(id, note_name_label.get(),note_tag_label.get(),note_desc_label.get("1.0", "end-1c")))
        note_submit_button.grid(row=3,column=0, columnspan=3,padx=0,pady=0, sticky='nwe')

        notes_edit_form.protocol("WM_DELETE_WINDOW", lambda: [self.attributes('-disabled', False), notes_edit_form.destroy()])
        
    # Edit note
    def edit_note(self, id, name, tag, desc):
        note = nbook[id-1]
        note['name'] = name
        note['tag'] = tag
        note['desc'] = desc
        nbook.load_note()
        nbook.dump_note()
        self.generate_notes_list(nbook.data)

    # Add note
    def add_note(self, name, tag, desc):
        note_record = Note(name,desc,tag)
        note_dict = {'name': note_record.name, 'desc': note_record.desc, 'tag': note_record.tag, 'date': note_record.date}
        nbook.data.append(note_dict)
        nbook.load_note()
        nbook.dump_note()
        self.generate_notes_list(nbook.data)
        
    # Search note
    def search_note(self, value):
        if value == '':
            self.generate_notes_list(nbook.data)
        else:
            search_note_list = []
            for note in nbook.data:
                if value in note['name']:
                    search_note_list.append(note)
                elif value in note['tag']:
                    search_note_list.append(note)
                elif value in note['desc']:
                    search_note_list.append(note)
            self.generate_notes_list(search_note_list)

    # Delete note
    def delete_note(self, id):
        del nbook[id-1]
        nbook.load_note()
        nbook.dump_note()
        self.generate_notes_list(nbook.data)

    # Validate mail
    def validate_mail_input(self, event, mail_label, submit_button):
        value = mail_label.get()
        if not re.fullmatch(r'^[a-zA-Z0-9_.+-]*(@[a-zA-Z0-9-]*)?(\.[a-zA-Z0-9-.]*)?$', value) and len(value):
            # If input doesn't match the pattern, schedule the deletion of the last character
            mail_label.after_idle(lambda: mail_label.delete(len(value)-1))
            
    # Validate number
    def validate_number_input(self, event, phone_label, submit_button):
    # Schedule the validation to be performed after the new character is added
        phone_label.after_idle(lambda: self.check_number(phone_label, submit_button))

    # Check number
    def check_number(self, phone_label, submit_button):
        value = phone_label.get()
        if not re.fullmatch(r'(\+?\d{0,13}|\d{0,9})?', value) and len(value):
            # If input doesn't match the pattern, delete the last character
            phone_label.delete(len(value)-1)
        else:
            phone_label.configure(fg_color='#343638')
        
    # Validate birthday
    def validate_date_input(self, event, birthday_label, submit_button):
        birthday_label.after_idle(lambda: self.check_date_input(birthday_label, submit_button))
    
    
    def check_date_input(self, birthday_label, submit_button):
        value = birthday_label.get()
        if len(value) < 10 and len(value) != 0:
            birthday_label.after_idle(lambda: birthday_label.configure(fg_color='#343638'))
            birthday_label.after_idle(lambda: submit_button.configure(state='disabled'))
        if len(value) > 11:
            # If input exceeds 10 characters, schedule the deletion of the last character
            birthday_label.after_idle(lambda: birthday_label.delete(len(value)-1))
        elif len(value) == 0:
            birthday_label.after_idle(lambda: birthday_label.configure(fg_color='#343638'))
            birthday_label.after_idle(lambda: submit_button.configure(state='normal'))
        else:
            if not re.fullmatch(r'([0-2]?[0-9]?|3[0-1]?)(\.([0-0]?[1-9]?|1[0-2])?(\.[1-2]?[0-9]{0,3})?)?', value):
                # If input doesn't match the pattern and the last character is not '.', schedule the deletion of the last character
                birthday_label.after_idle(lambda: birthday_label.delete(len(value)-1))
            else:
                # If a full date has been entered, check if it's in the future
                birthday_label.after_idle(lambda: self.check_date(birthday_label, submit_button))
        
    # Check if the entered day is biger then todays day
    def check_date(self, birthday_label, submit_button):
        value = birthday_label.get()
        try:
            # If a full date has been entered, check if it's in the future
            if len(value) == 10:  # Check if a full date has been entered
                entered_date = datetime.strptime(value, '%d.%m.%Y')
                today = datetime.today()
                if entered_date.date() > today.date():
                    birthday_label.configure(fg_color='#B5001C')
                    submit_button.configure(state='disabled')
                else:
                    birthday_label.configure(fg_color='#343638')
                    submit_button.configure(state='normal')
        except:
            birthday_label.configure(fg_color='#343638')
            submit_button.configure(state='disabled')
        

def main():
    try:
        global nbook
        global assistant
        nbook = NoteBook()
        try:
            nbook.create_table()
        except:
            pass

        nbook.dump_note()
        assistant = PersonalAssistant()
        if len(assistant.contacts) > 0:
            Record._record_id = len(assistant.contacts)
        
        app = App()
        app.mainloop()
    finally:
        nbook.load_note()
        assistant.save_data_on_exit()

if __name__ == "__main__":
    main()