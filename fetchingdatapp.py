import customtkinter
from CTkTable import *
from customtkinter import CTkEntry
from PIL import Image
import os
import pyodbc
import time
import json



"""server ismini akılda tutması için"""
#def save_data( a, filename='data.json'):
#    with open(filename, 'w') as file:
#        json.dump(a, file)
#
#
#def load_data(filename='data.json'):
#
#    try:
#        with open(filename, 'r') as file:
#            return json.load(file)
#    except FileNotFoundError:
#        return {}


def fetch_data():

    global select_station
    i = select_station[8]
    select_station = "Station " + i
    table_name = 'Table_ST' + i
    print(select_station)


    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        query = 'SELECT * FROM ' + table_name
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        conn.close()
        return rows, columns
    except pyodbc.Error as e:
        print("Veritabanı bağlantı hatası:", e)
        return [], []


def display_data(rows, columns):
    

    header_frame = customtkinter.CTkFrame(root)
    header_frame.pack(fill='x')

    global progressbar
    progressbar = customtkinter.CTkProgressBar(master=header_frame, mode="determinate", determinate_speed=.5)
    progressbar.pack(padx=20, pady=10)
    progressbar.configure(width=200, height=5, )
    progressbar.set(0)


    for deger in range(1201):
        yazi = deger / 1200.0
        progressbar.set(yazi)
        print(deger)
        root.update()
        time.sleep(0.00000000001)


    column_widths = [max(len(col) for col in columns)] * len(columns)
    for col in columns:
        header = customtkinter.CTkLabel(header_frame, text=col, width=column_widths[columns.index(col)] * 10.5)
        header.pack(side='left', padx=5, anchor='w')


    for row in rows:
        row_frame = customtkinter.CTkFrame(root)
        row_frame.pack(fill='x')
        for i, item in enumerate(row):
            cell_width = column_widths[i] * 10
            cell = customtkinter.CTkLabel(row_frame, text=str(item), width=cell_width)
            cell.pack(side='left', padx=5, anchor='w')


def sqldatafetch():

    title_label = customtkinter.CTkLabel(root, text=select_station, font=("Arial", 24))
    title_label.pack(pady=20)


    rows, columns = fetch_data()
    if rows:
        display_data(rows, columns)
    else:

        no_data_label = customtkinter.CTkLabel(root, text="No data available")
        no_data_label.pack(pady=5)

        



def login():

    username = "H. Volkan Akkoc"  #entry1.get()
    password = "novi"  #entry2.get()
    server = "DESKTOP-63BCPVP\\WINCC"   #entry3.get()
    database = 'deneme'
    global conn_str
    conn_str = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=' + server + ';'
                                 'DATABASE=' + database + ';'
                                                          'Trusted_Connection=yes;'
                                                          'TrustServerCertificate=yes;'
    )

    if username == "H. Volkan Akkoc" and password == "novi":
        for widget in frame.winfo_children():
            widget.destroy()

        label2 = customtkinter.CTkLabel(master=frame, text="Assembly Line", font=("Futura", 26))
        label2.pack(pady=30, padx=10)

        combobox_var = customtkinter.StringVar(value="Station 1")

        def combobox_callback(choice):
            global select_station
            print("Combobox dropdown clicked:", choice)
            select_station = combobox.get()
            print("selected :", select_station)
        combobox_frame = customtkinter.CTkFrame(master=frame)
        combobox_frame.pack(pady=12, padx=10, anchor="w")

        global combobox
        combobox = customtkinter.CTkComboBox(master=combobox_frame,
                                             values=["Station 1", "Station 2", "Station 3", "Station 4", "Station 5",
                                                     "Station 6", "Station 7", "Station 8", "Station 9"],
                                             command=combobox_callback,
                                             variable=combobox_var)
        combobox.grid(row=0, column=0, padx=5)

        check_button = customtkinter.CTkButton(master=combobox_frame, text="Test Results", command=sqldatafetch)
        check_button.grid(row=0, column=1, padx=5)
    else:
        print("Invalid credentials")






customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

root = customtkinter.CTk()
root.geometry("700x600")
root.title("Fetch.Data")
my_image = customtkinter.CTkImage(dark_image=Image.open("C:/Users/HP/Desktop/file (1).png"), size=(300, 150))


frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=15, padx=15, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Login System", font=("Roboto", 24))
label.pack(pady=20, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

"""server ismini akılda tutması için"""
#entry3 = customtkinter.CTkEntry(master=frame,placeholder_text="SQL SERVER", width=200, height=28,
#                                border_width=10)
#entry3.pack(pady=12, padx=10)
#a = entry3.get()
#checkboxforserver= customtkinter.CTkCheckBox(master=frame, text="Remember Server",command=save_data(a))
#checkboxforserver.pack(pady=12, padx=10)


checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
checkbox.pack(pady=12, padx=10)

label3 = customtkinter.CTkLabel(master=frame, text="", image=my_image)
label3.pack(pady=30, padx=10)

button = customtkinter.CTkButton(master=frame, text="Login", command=login)
button.pack(pady=12, padx=10)


root.mainloop()
