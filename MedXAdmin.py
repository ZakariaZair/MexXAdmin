from tkinter import PhotoImage
from typing import Optional, Tuple, Union
import customtkinter as ctk
import firebase_admin
from firebase_admin import credentials, db
from PIL import Image, ImageTk


# Initialize Firebase


ctk.set_default_color_theme("green")

class admin():
    cred: str
    def __init__(self):
        self.cred = credentials.Certificate("./medxnote-63104-firebase-adminsdk-5mup6-ecb75519dc.json")
        firebase_admin.initialize_app(self.cred, {
            'databaseURL': 'https://medxnote-63104-default-rtdb.firebaseio.com/'
        })
    
    def send(self, text_field: ctk.CTkEntry, key: str):
        value = text_field.get()
        ref = db.reference('messages')
        new_message_ref = ref.child(key)
        new_message_ref.set({"Page": value})
    
    def receive(self):
        ref = db.reference('Systems')
        snapshot = ref.get()
        if snapshot:
            for key, value in snapshot.items():
                print(f"System: {key}")
                for key, value2 in value.items():
                    print(f"Maladie: {key}, Contenu: {value2}")
        return snapshot
    
    

class MedXAdmin(ctk.CTk):
    user = admin()
    tabView: ctk.CTkTabview
    sickness: list[ctk.CTkFrame] = []
    sidebar: ctk.CTkFrame
    screen_width: int
    screen_height: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setUp()
    
    def setUp(self):
        self.title("MedXAdmin")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry(f"{self.screen_width-100}x{self.screen_height-400}+0+0")
        
        self.sidebar = ctk.CTkFrame(self, width=200, height=600, border_width=2, fg_color="transparent")
        self.sidebar.pack_propagate(False)
        self.tabView = ctk.CTkTabview(self)

        # bg_label = ctk.CTkLabel(
        #     self.tabView,
        #     image=ctk.CTkImage(
        #         light_image=Image.open("polygon_wall.jpeg"),
        #         dark_image=Image.open("polygon_wall.jpeg"), size=(self.screen_width, self.screen_height)
        #     )
        #     , text=""
        # )
        # bg_label.place(relwidth=1, relheight=1)
        
        index: int = 0
        for key, maladies in self.user.receive().items():
            self.tabView.add(key)
            btn = ctk.CTkButton(self.sidebar, text=key, command=lambda i=key: self.changeTab(i), corner_radius=0)
            btn.grid(row=index, column=1, sticky='nsew', padx=15, pady=15)
            self.sickness.append(self.sidebar)
            index += 1
            currentTab = self.tabView.tab(key)
            for maladie, rawText in maladies.items():
                maladieFrame = ctk.CTkFrame(currentTab, width=self.screen_width, height=self.screen_height/4, border_width=2)
                ctk.CTkLabel(maladieFrame, text=maladie, font=('Roboto', 25), bg_color="transparent").pack(pady=10)
                rawTextBox = ctk.CTkTextbox(maladieFrame, width=1000, height=100)
                rawTextBox.insert(0.0, rawText)
                rawTextBox.pack(pady=10)
                maladieFrame.pack(fill="both", padx=70, pady=10)
        

        

        
        btn = ctk.CTkButton(self.sidebar, text="(---+---)", command=self.addSystem, corner_radius=0)
        btn.grid(row=index, column=1, sticky='nsew', padx=15, pady=15)
        self.sidebar.pack(side='left', fill='both', padx=10, pady=10)
        self.tabView.pack(fill='both', expand=True)

    def addSystem(self):
        dialog = ctk.CTkInputDialog(text="Type system name:", title="Add")
        print("Input:", dialog.get_input())   

    def addMaladie():
        pass
        

    def changeTab(self, tab):
        self.tabView.set(tab)
        


# # Create a button
# button = ctk.CTkButton(root, text="Send to Firebase", command= lambda: send_to_firebase(text_field))
# button.pack()

def main(): 
    app = MedXAdmin()
    app.mainloop()

main()