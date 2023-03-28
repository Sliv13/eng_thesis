import tkinter
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from mysql.connector import errorcode
from time import strftime
from time import sleep
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfile
from tkVideoPlayer import TkinterVideo
import sys
import os
import requests as req
import re
import datetime
import serial.tools.list_ports
import time
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib as plt
from matplotlib import pyplot as plt
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from tkinter import filedialog as fd

#główna klasa odpowiadająca za mechanikę aplikacji
class App(tk.Tk):
    szerokość= 1200
    wysokość= 700
    konto={

            "login" : "",
            "haslo" : "",
            "nr_pacjenta": ""
    }


    def __init__(self):
        super().__init__()

        self.title("Physiolimb")
        self.geometry(f"{App.szerokość}x{App.wysokość}")
        self.resizable(width=False, height=False)

        #self.configure(bg="#2d2e2e")
        global otwarcie
        otwarcie = ImageTk.PhotoImage(Image.open('ikony/otworz.png'))
        global zamkniecie
        zamkniecie =ImageTk.PhotoImage(Image.open('ikony/zamknij.png'))
        global folder
        folder = ImageTk.PhotoImage(Image.open('ikony/folder.png'))
        global wlacz
        wlacz = ImageTk.PhotoImage(Image.open('ikony/wlacz.png'))
        global stop
        stop = ImageTk.PhotoImage(Image.open('/ikonystop.png'))
        global pauza
        pauza = ImageTk.PhotoImage(Image.open('ikony/pauza.png'))


        kontener_stron=tk.Frame(self, bg="#2d2e2e")
        kontener_stron.configure(bg="#2d2e2e")
        kontener_stron.pack(side="top",fill="both",expand=True)
        kontener_stron.rowconfigure(0,weight=1)
        kontener_stron.columnconfigure(0,weight=1)


        self.frames = {}
        self.Wybor_profilu = Wybor_profilu
        self.Logowanie_Fizjo = Logowanie_Fizjo
        self.Logowanie_Pacjent = Logowanie_Pacjent
        self.Zalogowano_Pacjent = Zalogowano_Pacjent
        self.Testy = Testy
        self.Testy_Ugiecia= Testy_Ugiecia
        self.Testy_Nacisku = Testy_Nacisku
        self.Cwiczenia=Cwiczenia
        self.Zalogowano_Fizjo=Zalogowano_Fizjo
        self.Wgraj_Filmy=Wgraj_Filmy
        self.Przypisz_Ćwiczenia=Przypisz_Ćwiczenia
        self.Odbierz_Wyniki=Odbierz_Wyniki
        self.Zarejestruj_Pacjenta=Zarejestruj_Pacjenta
        self.Historia=Historia
        self.Pomoc=Pomoc


        for F in {Wybor_profilu,Logowanie_Fizjo,Logowanie_Pacjent, Zalogowano_Pacjent,Testy,Testy_Ugiecia,Testy_Nacisku,Cwiczenia,Zalogowano_Fizjo,Wgraj_Filmy,Przypisz_Ćwiczenia,Odbierz_Wyniki,Zarejestruj_Pacjenta,Historia,Pomoc}:
            frame = F(self, kontener_stron)
            self.frames[F]= frame
            frame.grid(row=0,column=0,sticky="nsew")



        self.show_frame(Wybor_profilu)

    def show_frame(self, cont):

        frame = self.frames[cont]
       # menubar = frame.create_menubar(self)
        #self.configure(menu=menubar)
        frame.tkraise()

    def czas(self):
        format = strftime("%H:%M:%S \n %d.%m.%Y")
        self.zegar.config(text=format)
        self.zegar.after(1000, self.czas)

class Wybor_profilu(Frame,App):

        def __init__(self, aplikacja, kontener_stron):
            super().__init__(kontener_stron)

            self.configure(bg="#2d2e2e")
            self.columnconfigure(index=1, weight=3)

            napis_profil1 = Label(self, text="Wybierz profil dostępu", fg="white", bg="#2d2e2e", font=('Arial', 30, 'bold'))
            napis_profil1.grid(row=1, column=1, columnspan=1, padx=(0), pady=(80,75))
            przycisk_fizjo = Button(self, text="Fizjoterapeuta", fg="white", bg="#01786F", width=15, height=2,
                                    font=('Arial', 15), activebackground="#319177", activeforeground="white",cursor="hand2",command=lambda: aplikacja.show_frame(aplikacja.Logowanie_Fizjo))
            przycisk_fizjo.grid(row=2, column=0, columnspan=1, padx=(50,0), pady=(215,75))
            przycisk_pacjent = Button(self, text="Pacjent", fg="white", bg="#01786F", width=15, height=2,
                                      font=('Arial', 15), activebackground="#319177", activeforeground="white",cursor="hand2",command=lambda: aplikacja.show_frame(aplikacja.Logowanie_Pacjent))
            przycisk_pacjent.grid(row=2, column=2, columnspan=1, padx=(0,50), pady=(215,75))

            ramka_zegar = Frame(self, highlightthickness=2, highlightbackground="#606060",
                                highlightcolor="#606060")
            self.zegar = Label(ramka_zegar, bg="#2d2e2e", fg="white", font=('Arial', 12, 'bold'))
            ramka_zegar.grid(row=0, column=2, padx=(0, 27),sticky="ne", pady=25)
            self.zegar.grid(row=1, column=2)
            
            print(link2)


            self.czas()


class Logowanie_Fizjo(Frame,App):
            def __init__(self, aplikacja, kontener_stron):
                super().__init__(kontener_stron)

                self.configure(bg="#2d2e2e")
                self.columnconfigure(index=1,weight=2)


                napis_fizjo = Label(self, text="Fizjoterapeuta", fg="white", bg="#606060", width=35, height=2,
                                    font=('Arial', 18, 'bold'))  # ALBO PACJENT!!!
                napis_fizjo.grid(row=1, column=1, columnspan=1,sticky="NSEW",padx=(120),  pady=90)  # trzeba wysrodkowac napis!
                napis_login = Label(self, text="Wprowadź login", fg="white", bg="#2d2e2e", width=35, height=0,
                                    font=('Arial', 17))
                napis_login.grid(row=2, column=1, columnspan=1, padx=(291.25,291.25), pady=10)  # trzeba wysrodkowac napis!
                okno_login = Entry(self, width=25, font=('Arial', 15))
                okno_login.grid(row=3, column=1, columnspan=1, padx=250, pady=10,sticky="nsew")  # trzeba wysrodkowac napis!
                napis_haslo = Label(self, text="Wprowadź hasło", fg="white", bg="#2d2e2e", width=35, height=0,
                                    font=('Arial', 17))
                napis_haslo.grid(row=4, column=1, columnspan=1, padx=200, pady=10,sticky="nsew")  # trzeba wysrodkowac napis!
                okno_haslo = Entry(self, width=25, font=('Arial', 15),show="*")
                okno_haslo.grid(row=5, column=1, columnspan=1, padx=250,
                                pady=10,sticky="nsew")  # trzeba wysrodkowac napis! i zagwiazdkowac haslo

                przycisk_cofnij = Button(self, text="Cofnij", fg="white", bg="#01786F", width=15, height=2,
                                         font=('Arial', 15), activebackground="#319177", activeforeground="white",cursor="hand2",command=lambda: aplikacja.show_frame(aplikacja.Wybor_profilu) )
                przycisk_cofnij.grid(row=6, column=0, columnspan=1, padx=(50,0), pady=75,sticky="SW")
                przycisk_zaloguj = Button(self, text="Zaloguj", fg="white", bg="#01786F", width=15, height=2,
                                          font=('Arial', 15), activebackground="#319177", activeforeground="white",cursor="hand2",command=lambda: [self.baza(str(okno_login.get()),str(okno_haslo.get()),aplikacja),okno_login.delete(0, END),okno_haslo.delete(0, END)])
                przycisk_zaloguj.grid(row=6, column=2, columnspan=1, padx=(0,50), pady=75,sticky="SE")
                ramka_zegar = Frame(self, highlightthickness=2, highlightbackground="#606060",
                                    highlightcolor="#606060")
                self.zegar = Label(ramka_zegar, bg="#2d2e2e", fg="white", font=('Arial', 12, 'bold'))
                ramka_zegar.grid(row=1, column=2, padx=(0, 27), sticky="ne", pady=25)
                self.zegar.grid(row=1, column=2)
                wartosc = IntVar(value=0)
                def pokaz_haslo():
                    if (wartosc.get() == 1):
                        okno_haslo.config(show='')
                    else:
                        okno_haslo.config(show='*')

                widok_hasla = Checkbutton(self, text='Pokaż hasło', variable=wartosc,
                                          onvalue=1, offvalue=0, command=pokaz_haslo, bg="#2d2e2e", fg="white",
                                          font=("Arial", 10), activebackground="#2d2e2e", activeforeground='white',
                                          selectcolor="#282828")
                widok_hasla.grid(row=5, column=1, padx=(360, 0), pady=(0, 0))

                self.czas()

            def baza(self, login_fizjo, haslo_fizjo, aplikacja):
                try:
                    mysqldb = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="login")
                    mycursor = mysqldb.cursor()
                    sql = "SELECT * from logowanie_fizjo where login_fizjo= %s and haslo_fizjo= %s"
                    mycursor.execute(sql, [login_fizjo, haslo_fizjo])
                    results = mycursor.fetchall()
                    if results:
                        App.konto["login"] = login_fizjo
                        App.konto["haslo"] = haslo_fizjo
                        aplikacja.show_frame(aplikacja.Zalogowano_Fizjo)
                        mysqldb.close()

                    else:
                        messagebox.showinfo("", "Nieprawidłowy login lub hasło")

                except mysql.connector.Error:
                    messagebox.showinfo("", "Błąd przy połączeniu")
                except:
                    messagebox.showinfo("", "Błąd")
                else:
                    mysqldb.close()



class Logowanie_Pacjent(Frame,App):
    login=""
    haslo=""
    def __init__(self, aplikacja, kontener_stron):
        super().__init__(kontener_stron)

        self.configure(bg="#2d2e2e")
        self.columnconfigure(index=1, weight=2)

        napis_fizjo = Label(self, text="Pacjent", fg="white", bg="#606060", width=35, height=2,
                            font=('Arial', 18, 'bold'))  # ALBO PACJENT!!!
        napis_fizjo.grid(row=1, column=1, columnspan=1, sticky="NSEW", padx=(120), pady=90)  # trzeba wysrodkowac napis!
        napis_login = Label(self, text="Wprowadź login", fg="white", bg="#2d2e2e", width=35, height=0,
                            font=('Arial', 17))
        napis_login.grid(row=2, column=1, columnspan=1, padx=(291.25, 291.25), pady=10)  # trzeba wysrodkowac napis!
        okno_login = Entry(self, width=25, font=('Arial', 15))
        okno_login.grid(row=3, column=1, columnspan=1, padx=250, pady=10, sticky="nsew")  # trzeba wysrodkowac napis!
        napis_haslo = Label(self, text="Wprowadź hasło", fg="white", bg="#2d2e2e", width=35, height=0,
                            font=('Arial', 17))
        napis_haslo.grid(row=4, column=1, columnspan=1, padx=200, pady=10, sticky="nsew")  # trzeba wysrodkowac napis!
        okno_haslo = Entry(self, width=25, font=('Arial', 15), show="*")
        okno_haslo.grid(row=5, column=1, columnspan=1, padx=250,
                        pady=10, sticky="nsew")  # trzeba wysrodkowac napis! i zagwiazdkowac haslo

        przycisk_cofnij = Button(self, text="Cofnij", fg="white", bg="#01786F", width=15, height=2,
                                 font=('Arial', 15), activebackground="#319177", activeforeground="white",cursor="hand2",
                                 command=lambda: aplikacja.show_frame(aplikacja.Wybor_profilu))
        przycisk_cofnij.grid(row=6, column=0, columnspan=1, padx=(50, 0), pady=75, sticky="SW")
        przycisk_zaloguj = Button(self, text="Zaloguj", fg="white", bg="#01786F", width=15, height=2,
                                  font=('Arial', 15), activebackground="#319177",
                                  activeforeground="white",cursor="hand2",
                                  command=lambda: [self.baza(str(okno_login.get()),str(okno_haslo.get()),aplikacja),okno_login.delete(0, END),okno_haslo.delete(0, END)])
        przycisk_zaloguj.grid(row=6, column=2, columnspan=1, padx=(0, 50), pady=75, sticky="SE")


        ramka_zegar = Frame(self, highlightthickness=2, highlightbackground="#606060",
                            highlightcolor="#606060")
        self.zegar = Label(ramka_zegar, bg="#2d2e2e", fg="white", font=('Arial', 12, 'bold'))
        ramka_zegar.grid(row=1, column=2, padx=(0, 27), sticky="ne", pady=25)
        self.zegar.grid(row=1, column=2)
        wartosc = IntVar(value=0)

        def pokaz_haslo():
            if (wartosc.get() == 1):
                okno_haslo.config(show='')
            else:
                okno_haslo.config(show='*')

        widok_hasla = Checkbutton(self, text='Pokaż hasło', variable=wartosc,
                                  onvalue=1, offvalue=0, command=pokaz_haslo, bg="#2d2e2e", fg="white",
                                  font=("Arial", 10), activebackground="#2d2e2e", activeforeground='white',
                                  selectcolor="#282828")
        widok_hasla.grid(row=5, column=1, padx=(360, 0), pady=(0, 0))
        self.czas()

    def baza(self,login_pacjent,haslo_pacjent,aplikacja):
        try:
            mysqldb=mysql.connector.connect(host="localhost",user="root",passwd="1234",database="login")
            print(mysqldb.connection_id)
            mycursor=mysqldb.cursor()
            sql="SELECT * from logowanie where login= %s and haslo= %s"
            mycursor.execute(sql,[login_pacjent,haslo_pacjent])
            results=mycursor.fetchall()
            dane=results[0]
            if results:
                str(results).strip("()")
                App.konto["login"]=login_pacjent
                App.konto["haslo"]=haslo_pacjent
                App.konto["nr_pacjenta"]=dane[0]
                print(dane[0])
                aplikacja.show_frame(aplikacja.Zalogowano_Pacjent)

            else:
                messagebox.showinfo("","Nieprawidłowy login lub hasło")

        except mysql.connector.Error:
            messagebox.showinfo("", "Błąd przy połączeniu")
        except:
            messagebox.showinfo("", "Błąd")
        else:
            mysqldb.close()



class Zalogowano_Pacjent(Frame,App):
    def __init__(self, aplikacja, kontener_stron):
        super().__init__(kontener_stron)
        #
        self.configure(bg="#2d2e2e")
        self.columnconfigure(index=1, weight=2)
        napis = Label(self, text='''Zalogowano pomyślnie.
        Witaj na twoim koncie pacjenta.''', fg="white",bg="#2d2e2e",  width=35, height=2,font=('Arial', 18))  # ALBO PACJENT!!!
        napis.grid(row=1, column=1, columnspan=1, sticky="NSEW", padx=130, pady=90)  # trzeba wysrodkowac napis!

        wiadomosc=Text(self)

        def pokaz_wiadomosc():
            message=str(self.baza_wiadomosc()).strip("[('',)]")
            if message != "":
                wiadomosc.insert(INSERT, message)
                wiadomosc.grid(row=3, column=1, padx=(300, 200), pady=(30, 30))
                wiadomosc.configure(state=DISABLED,  width=150, height=7, fg="black", bg="white", font=('Arial', 14))
            else:
                messagebox.showinfo("","brak wiadomości od fizjoterapeuty")


        wiadomosc_przycisk = Button(self, text="Załaduj wiadomość od fizjoterapeuty",fg="white", bg="#01786F", width=32,
                                  font=('Arial', 15), activebackground="#319177", activeforeground="white",cursor="hand2",command=lambda:[pokaz_wiadomosc()])
        wiadomosc_przycisk.grid(row=2, column=1, padx=(110,0))
        ramka_zegar = Frame(self, highlightthickness=2, highlightbackground="#606060",
                            highlightcolor="#606060")
        self.zegar = Label(ramka_zegar, bg="#2d2e2e", fg="white", font=('Arial', 12, 'bold'))
        ramka_zegar.grid(row=1, column=2, padx=(0, 27), sticky="ne", pady=25)
        self.zegar.grid(row=1, column=2)



        global otwarcie

        global zamkniecie

        global b2
        b2 = Button(self,
                    image=otwarcie,
                    command=lambda :[self.lista_menu(aplikacja),print(App.konto["login"])],
                    border=0,
                    bg='#2d2e2e',
                    activebackground='#2d2e2e',
                    cursor = "hand2")
        b2.place(x=5, y=8)
        self.czas()

    def lista_menu(self,aplikacja):

        f1 = Frame(self, width=250, height=700, bg='#01786F')
        f1.place(x=0, y=0)
        b2.place(x=5, y=8)

        def przycisk_menu(x, y, tekst, bcolor, fcolor, komenda):

            przycisk_m = Button(f1, text=tekst,
                                width=27,
                                height=2,
                                fg='white',
                                border=0,
                                bg=fcolor,
                                activeforeground='white',
                                activebackground=bcolor,
                                font=('Arial', 13),
                                cursor="hand2",
                                command=komenda)
            przycisk_m.place(x=x, y=y)

        przycisk_menu(0, 140, 'Wykonaj testy', '#319177', '#01786F', lambda : [f1.destroy(),aplikacja.show_frame(aplikacja.Testy)])
        przycisk_menu(0, 240, 'Wykonaj ćwiczenia', '#319177', '#01786F', lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Cwiczenia)])
        przycisk_menu(0, 340, 'Historia', '#319177', '#01786F', lambda : [f1.destroy(),aplikacja.show_frame(aplikacja.Historia)])
        przycisk_menu(0, 440, 'Pomoc', '#319177', '#01786F', lambda : [f1.destroy(),aplikacja.show_frame(aplikacja.Pomoc)])
        przycisk_menu(0, 540, 'Wyloguj', '#319177', '#01786F', lambda:wyloguj())

        def zamknij():
            f1.destroy()

        def wyloguj():
            f1.destroy()
            pytanie = messagebox.askyesno('Wylogowywanie', 'Czy chcesz się wylogować?')
            if pytanie == True:
                messagebox.showinfo('Wylogowywanie', 'Pomyślnie wylogowano.')
                aplikacja.show_frame(aplikacja.Wybor_profilu)


        Button(f1,
               image=zamkniecie,
               border=0,
               command=zamknij,
               bg='#01786F',
               cursor="hand2",
               activebackground='#01786F').place(x=5, y=10)

    #metoda klasy "Zalogowano_Pacjent" odpowiedzialna
    # za załadowanie najnowszej wiadomości przesłanej przez fizjoterapeutę do pacjenta:
    def baza_wiadomosc(self):
        login_pacjent = App.konto["login"]
        try:
            # wprowadzenie danych używanej bazy danych i otwarcie jej:
            mysqldb5 = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="login")
            # tworzenie zmiennej tymczasowej użwyanej do pobrania wyniku zapytania do bazy danych:
            mycursor5 = mysqldb5.cursor()
            # zapytanie(kwerenda) sql wprowadzające dane do bazy:
            sql = "SELECT komentarz from pacjenci_dane where login= %s"
            # wykonanie zapytania sql do bazy danych:
            mycursor5.execute(sql, [login_pacjent])
            # zatwierdzenie pobrania danych z bazy:
            results = mycursor5.fetchall()
            if results:

                return results

            else:
                #obsługa błędów
                messagebox.showinfo("", "Nieprawidłowy login lub hasło")

        except mysql.connector.Error:
            messagebox.showinfo("", "Błąd przy połączeniu")
        except:
            messagebox.showinfo("", "Błąd")
        else:
            #zamknięcie otwartej bazy
            mysqldb5.close()

class Testy(Frame,App):
    def __init__(self, aplikacja, kontener_stron):
        super().__init__(kontener_stron)


        self.configure(bg="#2d2e2e")

        l2 = Label(self, text='Wybierz rodzaj testu: ', fg='white', bg='#2d2e2e')
        l2.config(font=('Arial', 20))
        l2.place(x=593, y=150)
        przycisk_ugiecie = Button(self, text="Test ugięcia palców", fg="white", bg="#01786F", width=17, height=2,
                                  font=('Arial', 15),
                                  activebackground="#319177", activeforeground="white",cursor="hand2", command=lambda: aplikacja.show_frame(aplikacja.Testy_Ugiecia))
        przycisk_ugiecie.grid(row=2, column=1, columnspan=1, padx=(400, 125), pady=(250, 100), sticky=SW)
        przycisk_nacisk = Button(self, text="Test siły nacisku", fg="white", bg="#01786F", width=17, height=2,
                                 font=('Arial', 15),
                                 activebackground="#319177", activeforeground="white",cursor="hand2", command=lambda: aplikacja.show_frame(aplikacja.Testy_Nacisku))
        przycisk_nacisk.grid(row=2, column=2, columnspan=1, padx=(135, 400), pady=(250, 100), sticky=SE)

        global otwarcie
        global zamkniecie

        global b2
        b2 = Button(self,
                    image=otwarcie,
                    command=lambda :self.lista_menu(aplikacja),
                    border=0,
                    bg='#2d2e2e',
                    cursor="hand2",
                    activebackground='#2d2e2e')
        b2.place(x=5, y=8)


    def lista_menu(self,aplikacja):


        f1 = Frame(self, width=250, height=700, bg='#01786F')

        f1.place(x=0, y=0)
        b2.place(x=5, y=8)

        def przycisk_menu(x, y, tekst, bcolor, fcolor, komenda):

            przycisk_m = Button(f1, text=tekst,
                                width=27,
                                height=2,
                                fg='white',
                                border=0,
                                bg=fcolor,
                                activeforeground='white',
                                activebackground=bcolor,
                                font=('Arial', 13),
                                cursor="hand2",
                                command=komenda)
            przycisk_m.place(x=x, y=y)
        przycisk_menu(0, 140, 'Strona Główna', '#319177', '#01786F', lambda: [aplikacja.show_frame(aplikacja.Zalogowano_Pacjent),f1.destroy()])
        przycisk_menu(0, 240, 'Wykonaj ćwiczenia', '#319177', '#01786F', lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Cwiczenia)])
        przycisk_menu(0, 340, 'Historia', '#319177', '#01786F', lambda : [f1.destroy(),aplikacja.show_frame(aplikacja.Historia)])
        przycisk_menu(0, 440, 'Pomoc', '#319177', '#01786F', lambda : [f1.destroy(),aplikacja.show_frame(aplikacja.Pomoc)])
        przycisk_menu(0, 540, 'Wyloguj', '#319177', '#01786F', lambda:wyloguj())

        def zamknij():
            f1.destroy()

        def wyloguj():
            f1.destroy()
            pytanie = messagebox.askyesno('Wylogowywanie', 'Czy chcesz się wylogować?')
            if pytanie == True:
                messagebox.showinfo('Wylogowywanie', 'Pomyślnie wylogowano.')
                aplikacja.show_frame(aplikacja.Wybor_profilu)


        Button(f1,
               image=zamkniecie,
               border=0,
               command=zamknij,
               bg='#01786F',
               cursor="hand2",
               activebackground='#01786F').place(x=5, y=10)

class Testy_Ugiecia(Frame, App):
    def __init__(self, aplikacja, kontener_stron):
        super().__init__(kontener_stron)


        self.configure(bg="#2d2e2e")

        napis_test_ugiecia = Label(self, text="TEST UGIĘCIA PALCÓW", width=20, font=("Arial", 15, 'bold'), fg="white",
                                   bg="#2d2e2e")
        napis_test_ugiecia.grid(column=1, row=0, padx=480, pady=(25, 0))

        napis_port = Label(self, text="Wybierz port :", width=11, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_port.grid(column=1, row=2, padx=(0, 200), pady=(10, 0))

        wybrany_port = StringVar()
        wybor_portu = ttk.Combobox(self, width=20, textvariable=wybrany_port, font=("Arial", 11))


        przycisk_port = Button(self, text="Załaduj  listę dostępnych portów COM", fg="white", bg="#01786F", width=32, height=1,
                               font=('Arial', 12), activebackground="#319177", activeforeground="white",
                               cursor="hand2",command=lambda:[wybor_portu.configure(values=self.wyborport()),pierwszy_port(wybor_portu)] )
        przycisk_port.grid(row=1, column=1, columnspan=1, padx=(0, 0), pady=10)

        wybor_portu.grid(column=1, row=2, padx=(115, 0), pady=(10, 0))
        wybor_portu.current()

        przycisk_port2 = Button(self, text="Testuj połączenie z portem", fg="white", bg="#01786F", width=24, height=1,
                               font=('Arial', 12), activebackground="#319177", activeforeground="white",cursor="hand2",command=lambda:self.portconnect_and_test(str(wybrany_port.get()),1))
        przycisk_port2.grid(row=3, column=1, columnspan=1, padx=(0, 0), pady=10)

        napis_testy = Label(self, text="Aby zmierzyć kąt ugięcia palców, kliknij poniższy przycisk :", width=45,
                            font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_testy.grid(column=1, row=4, padx=(0, 0), pady=(25, 0))

        przycisk_testy = Button(self, text="Wykonaj testy", fg="white", bg="#01786F", width=13, height=1,
                                font=('Arial', 12), activebackground="#319177", activeforeground="white",cursor="hand2",command=lambda:[kasowanie(),self.portconnect_and_test(str(wybrany_port.get()),2)])
        przycisk_testy.grid(row=5, column=1, columnspan=1, padx=(0, 0), pady=20)

        wyniki = Label(self, text="Wyniki pomiarów :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        wyniki.grid(column=1, row=6, padx=(0, 0), pady=(25, 0))

        napis_kciuk = Label(self, text="Kciuk :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_kciuk.grid(column=1, row=7, padx=(0, 180), pady=(15, 0))
        global okna
        okno_kciuk = Entry(self, width=12, font=('Arial', 12))
        okno_kciuk.grid(row=7, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))

        napis_wskazujacy = Label(self, text="Wskazujący :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_wskazujacy.grid(column=1, row=8, padx=(0, 180), pady=(15, 0))

        okno_wskazujacy = Entry(self, width=12, font=('Arial', 12))
        okno_wskazujacy.grid(row=8, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))
        napis_srodkowy = Label(self, text="Środkowy :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_srodkowy.grid(column=1, row=9, padx=(0, 180), pady=(15, 0))
        okno_srodkowy = Entry(self, width=12, font=('Arial', 12))
        okno_srodkowy.grid(row=9, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))
        napis_serdeczny = Label(self, text="Serdeczny :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_serdeczny.grid(column=1, row=10, padx=(0, 180), pady=(15, 0))
        okno_serdeczny = Entry(self, width=12, font=('Arial', 12))
        okno_serdeczny.grid(row=10, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))
        napis_maly = Label(self, text="Mały :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_maly.grid(column=1, row=11, padx=(0, 180), pady=(15, 0))
        okno_maly = Entry(self, width=12, font=('Arial', 12))
        okno_maly.grid(row=11, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))
        okna=(okno_kciuk,okno_wskazujacy,okno_srodkowy,okno_serdeczny,okno_maly)

        przycisk_zapisz = Button(self, text="Zapisz wyniki", fg="white", bg="#01786F", width=12,
                                 height=1,
                                 font=('Arial', 12), activebackground="#319177",
                                 activeforeground="white", cursor="hand2",command=lambda:zapis())
        przycisk_zapisz.grid(row=12, column=1, columnspan=1, padx=(0, 0), pady=(20, 20))

        przycisk_cofnij_2 = Button(self, text="Cofnij", fg="white", bg="#01786F", width=13, height=1,
                                   font=('Arial', 15), activebackground="#319177", activeforeground="white",cursor="hand2",command=lambda: [aplikacja.show_frame(aplikacja.Testy),kasowanie()])
        przycisk_cofnij_2.grid(row=13, column=1, columnspan=1, padx=(0, 950), pady=(15, 0))
        def pierwszy_port(pierwszy):
            try:
                pierwszy.current(0)
            except:
                messagebox.showinfo("","Brak dostępnych portów")

        #metoda pozwalająca na zapisanie wyników testu
        # na dysku komputera pacjenta, w bazie danych i w archiwum:
        def zapis():
            #pobranie aktualnej daty
            data1 = datetime.date.today()
            data2=datetime.datetime.now()
            #linie 593-610 pozwalają na zapis danych w pliku na dysku komputera pacjenta:
            path_and_name = "testy/" + str(data1) + "-" + str(App.konto["nr_pacjenta"]) + "-ugiecie.txt"
            #otwarcie pliku
            file = open(path_and_name, mode='w')
            tablica_z_danymi_do_bd=list()
            try:
                for palec in okna:
                    #pobranie wyniku testu
                    zapis=palec.get()
                    #wpisanie wyniku do pliku
                    file.write(str(zapis).strip("'") + "\n")
                    tablica_z_danymi_do_bd.append(str(zapis).strip("'") + "\n")
                messagebox.showinfo("", "Wyniki zostały zapisane na dysku")
            except:
                #obsługa błędów
                messagebox.showinfo("Niepowodzenie w zapisie wyników na dysku")
            else:
                #zamknięcie pliku po zapisie
                file.close()
            #linie 612-628 pozwalają na wysłanie wyników testów do archiwum
            try:
                # linie odpowiedzialne za autoryzację dostępu do dysku Google przez API Google Drive:
                gauth = GoogleAuth()
                drive = GoogleDrive(gauth)
                # utworzenie nowego pliku na dysku Google:
                gfile = drive.CreateFile(
                    {'title': str(data2) + "-" + str(App.konto["nr_pacjenta"]) + "-ugiecie.txt",
                     'parents': [{'id': '1ok5Glz4vepxv1_Ys3QXouYxDOlA1DZq7'}]})
                # wgranie zawartości pliku z komputera pacjenta do archiwum:
                gfile.SetContentFile(path_and_name)
                gfile.Upload()
            except:
                #obsługa błędów
                messagebox.showinfo("", "Niepowodzenie w przesyłaniu wyników")
            else:
                #zamknięcie pliku po zapisie
                file.close()
            #linie 630-666 pozwalają na wgranie wyników testu do bazy danych
            try:
                #otwarcie pliku z dysku pacjenta w którym zapisane są dane
                file=open(path_and_name,mode='r')
                #odczyt danych z pliku
                dane=file.read()
                # wprowadzenie danych używanej bazy danych i otwarcie jej:
                mysqldb4 = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="login")
                # sprawdzenie połączenia:
                print(mysqldb4.connection_id)
                # tworzenie zmiennej tymczasowej użwyanej do pobrania wyniku zapytania do bazy danych:
                mycursor4 = mysqldb4.cursor()
                # zapytanie(kwerenda) sql aktualizujące dane w bazie:
                sql = "UPDATE pacjenci_dane SET test_ugiecia = %s WHERE nr = %s"
                # wartości wysyłane do bazy danych:
                val = (str(dane), App.konto["nr_pacjenta"])
                # wykonanie zapytania sql do bazy danych:
                mycursor4.execute(sql, val)

                try:
                    # zatwierdzenie zmian dokonanych przez zapytanie SQL:
                    mysqldb4.commit()

                    messagebox.showinfo("", "Wyniki zostały przesłane do fizjoterapeuty")

                except:
                    #obsługa błędów:
                    messagebox.showinfo("", "Niepowodzenie w przesyłaniu wyników")

            except mysql.connector.Error:
                messagebox.showinfo("", "Błąd przy połączeniu")
            except:
                messagebox.showinfo("", "Błąd")
            else:
                # zamknięcie otwartej bazy danych:
                mysqldb4.close()
                #zamknięcie pliku po zapisie
                file.close()

        def kasowanie():
            for palec in okna:
                palec.delete(0,END)
    #metoda klasy Testy_Ugiecia pozwalająca na załadowanie listy portów dostępnych na komputerze pacjenta:
    def wyborport(self):
        #linie 673-680 odpowiedzialne są za wyświetlenie listy dostępnych portów COM
        ports = serial.tools.list_ports.comports()
        portList = []

        for onePort in ports:
            portList.append(str(onePort))
            print(str(onePort))
        return portList
    #metoda klasy Testy_ugiecia pozwalająca na połączenie się z urządzeniem
    #i wykonanie testów ugięcia palców:
    def portconnect_and_test(self,port,tryb):
        wybrany_port="COM"+port[3]
        self.tryb=tryb
        packet = list()
        #ustawienie parametrów do połącznia się z portem
        serialInst = serial.Serial()
        serialInst.baudrate = 9600
        serialInst.port = wybrany_port
        #linie 692-700 pozwalają na sprawdzenie połącznia się z portem
        if self.tryb==1:
            try:
                serialInst.open()
                messagebox.showinfo("","Nastąpiło prawidłowe połącznie z portem")
                print(serialInst.is_open)

            except:
                #obsługa błędów:
                messagebox.showinfo("","Błąd podczas łączenia z portem. Upewnij się, że urządzenie jest prawidłowo połączone")
        #linie 702-720 pozwalają na wykonanie testów ugięcia palców pacjenta:
        if self.tryb==2:
            try:
                #otwarcie połączenia z portem
                serialInst.open()
                print(serialInst.is_open)
                while True:
                    #sprawdzenie czy przez port nadawane są dane:
                    if serialInst.in_waiting:
                        for i in range(0, 5):
                            #zapisanie odebranych danych do tymczaswowej listy packet:
                            wynik = serialInst.readline()
                            wynik = wynik.replace(b'\n', b'').replace(b'\r', b'')
                            packet.append(str(wynik).lstrip("b").strip("'"))
                        #wypisanie wyników na ekranie pacjenta:
                        global okna
                        for j in range(0,5):
                            okna[j].insert(0,packet[j])
                        else:
                            break

                for w in packet:
                    print(w)
            except:
                #obsługa błędów
                messagebox.showinfo("","Błąd podczas łączenia z portem. Upewnij się, że urządzenie jest prawidłowo połączone")
            #zamknięcie otwartego portu
            finally:
                serialInst.close()



class Testy_Nacisku(Frame, App):
    def __init__(self, aplikacja, kontener_stron):
        super().__init__(kontener_stron)


        self.configure(bg="#2d2e2e")
        napis_test_ugiecia = Label(self, text="TEST SIŁY NACISKU", width=20, font=("Arial", 15, 'bold'), fg="white",
                                   bg="#2d2e2e")
        napis_test_ugiecia.grid(column=1, row=0, padx=480, pady=(25, 0))

        napis_port = Label(self, text="Wybierz port :", width=11, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_port.grid(column=1, row=2, padx=(0, 170), pady=(25, 0))

        wybrany_port = StringVar()
        wybor_portu = ttk.Combobox(self, width=20, textvariable=wybrany_port, font=("Arial", 11))

        wybor_portu.grid(column=1, row=2, padx=(115, 0), pady=(25, 0))
        wybor_portu.current()

        przycisk_port = Button(self, text="Załaduj  listę dostępnych portów COM", fg="white", bg="#01786F", width=32,
                               height=1,
                               font=('Arial', 12), activebackground="#319177", activeforeground="white",
                               cursor="hand2", command=lambda: [wybor_portu.configure(values=self.wyborport()),pierwszy_port(wybor_portu)])
        przycisk_port.grid(row=1, column=1, columnspan=1, padx=(0, 0), pady=10)
        przycisk_port2 = Button(self, text="Testuj połączenie z portem", fg="white", bg="#01786F", width=24, height=1,
                                font=('Arial', 12), activebackground="#319177", activeforeground="white",
                                cursor="hand2", command=lambda: self.portconnect_and_test(str(wybrany_port.get()), 1))
        przycisk_port2.grid(row=3, column=1, columnspan=1, padx=(0, 0), pady=10)




        napis_testy = Label(self, text="Aby zmierzyć siłę nacisku, kliknij poniższy przycisk :", width=41,
                            font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_testy.grid(row=4, column=1, columnspan=1, padx=(0, 0), pady=(0,0))


        przycisk_testy = Button(self, text="Wykonaj test", fg="white", bg="#01786F", width=12, height=1,
                                font=('Arial', 12), activebackground="#319177", activeforeground="white",
                                cursor="hand2", command=lambda: [kasowanie(),self.portconnect_and_test(str(wybrany_port.get()), 2)])
        przycisk_testy.grid(row=5, column=1, columnspan=1, padx=(0, 0), pady=10)



        wyniki = Label(self, text="Wynik pomiaru :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        wyniki.grid(column=1, row=6, padx=(0, 0), pady=(10,10))
        global okno_nacisk
        okno_nacisk = Entry(self, width=12, font=('Arial', 12))
        okno_nacisk.grid(row=7, column=1, columnspan=1, padx=(0, 0), pady=(0,0))


        przycisk_zapisz = Button(self, text="Zapisz wynik", fg="white", bg="#01786F", width=11, height=1,
                                 font=('Arial', 12), activebackground="#319177", activeforeground="white",cursor="hand2",command=lambda:zapis())
        przycisk_zapisz.grid(row=8, column=1, columnspan=1, padx=(0, 0), pady=(10, 0))

        przycisk_cofnij_3 = Button(self, text="Cofnij", fg="white", bg="#01786F", width=13, height=1,
                                   font=('Arial', 15), activebackground="#319177", activeforeground="white",cursor="hand2",command=lambda  : [kasowanie(),aplikacja.show_frame(aplikacja.Testy)])
        przycisk_cofnij_3.grid(row=9, column=1, columnspan=1, padx=(0, 950), pady=(190, 0))
        def pierwszy_port(pierwszy):
            try:
                pierwszy.current(0)
            except:
                messagebox.showinfo("","Brak dostępnych portów")

        # metoda pozwalająca na zapisanie wyników testu
        # na dysku komputera pacjenta, w bazie danych i w archiwum:
        def zapis():
            #pobranie aktualnej daty
            data1 = datetime.date.today()
            data2 = datetime.datetime.now()
            # linie 803-819 pozwalają na zapis danych w pliku na dysku komputera pacjenta:
            path_and_name = "testy/" + str(data1) + "-" + str(App.konto["nr_pacjenta"]) + "nacisk.txt"
            try:
                #otwarcie pliku:
                file = open(path_and_name, mode='w')
                #pobranie wyniku testu
                zapis = okno_nacisk.get()
                #wypisanie wyników
                file.write(str(zapis).strip("'") + "\n")
                messagebox.showinfo("", "Wyniki zostały zapisane na dysku")
            except:
                # obsługa błędów
                messagebox.showinfo("Niepowodzenie w zapisie wyników na dysku")

            else:
                # zamknięcie pliku po zapisie
                file.close()

            # linie 822-832 pozwalają na wysłanie wyników testów do archiwum
            try:
                # linie odpowiedzialne za autoryzację dostępu do dysku Google przez API Google Drive:
                gauth = GoogleAuth()
                drive = GoogleDrive(gauth)
                # utworzenie nowego pliku na dysku Google:
                gfile = drive.CreateFile(
                    {'title': str(data2) + "-" + str(App.konto["nr_pacjenta"])
                              + "-nacisk.txt", 'parents': [{'id': '1pKp-OoLbrWApdstm9bIcmFLGQWAJkfL9'}]})
                # wgranie zawartości pliku z komputera pacjenta do archiwum:
                gfile.SetContentFile(path_and_name)
                gfile.Upload()
            except:
                #obsługa błędu
                messagebox.showinfo("", "Niepowodzenie w przesyłaniu wyników")
            # linie 837-870 pozwalają na wgranie wyników testu do bazy danych
            try:
                #otwarcie pliku z dysku pacjenta w którym zapisane są dane
                file=open(path_and_name,mode='r')
                # odczyt danych z pliku
                dane=file.read()
                # wprowadzenie danych używanej bazy danych i otwarcie jej:
                mysqldb4 = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="login")
                # sprawdzenie połączenia:
                print(mysqldb4.connection_id)
                # tworzenie zmiennej tymczasowej użwyanej do pobrania wyniku zapytania do bazy danych:
                mycursor4 = mysqldb4.cursor()
                # zapytanie(kwerenda) sql aktualizujące dane w bazie:
                sql = "UPDATE pacjenci_dane SET test_nacisku = %s WHERE nr = %s"
                # wartości wysyłane do bazy danych:
                val = (str(dane), App.konto["nr_pacjenta"])
                # wykonanie zapytania sql do bazy danych:
                mycursor4.execute(sql, val)

                try:
                    # zatwierdzenie zmian dokonanych przez zapytanie SQL:
                    mysqldb4.commit()
                    messagebox.showinfo("", "Wyniki zostały przesłane do fizjoterapeuty")

                except:
                    #obsługa błędów
                    messagebox.showinfo("", "Niepowodzenie w przesyłaniu wyników")

            except mysql.connector.Error:
                messagebox.showinfo("", "Błąd przy połączeniu")
            except:
                messagebox.showinfo("", "Błąd")
            else:
                # zamknięcie otwartej bazy danych:
                mysqldb4.close()
                #zamknięcie pliku po zapisie
                file.close()

        def kasowanie():
            for palec in okna:
                palec.delete(0, END)

    # metoda klasy Testy_Nacisku pozwalająca na wybór portu com do którego podłączone jest urządzenie:
    def wyborport(self):
        # linie 881-886 odpowiedzialne są za wyświetlenie listy dostępnych portów COM
        ports = serial.tools.list_ports.comports()
        portList = []
        for onePort in ports:
            portList.append(str(onePort))
            print(str(onePort))
        return portList

    # metoda klasy Testy_Nacisku pozwalająca na połączenie się z urządzeniem
    # i wykonanie testów siły nacisku dłoni:
    def portconnect_and_test(self, port, tryb):
        wybrany_port = "COM" + port[3]
        self.tryb = tryb
        packet = list()
        serialInst = serial.Serial()
        serialInst.baudrate = 9600
        serialInst.port = wybrany_port
        # linie 898-906 pozwalają na sprawdzenie połącznia portem
        if self.tryb == 1:
            try:
                serialInst.open()
                messagebox.showinfo("", "Nastąpiło prawidłowe połącznie z portem")
                print(serialInst.is_open)

            except:
                # obsługa błędów:
                messagebox.showinfo("","Błąd podczas łączenia z portem. Upewnij się, że urządzenie jest prawidłowo połączone")
        # linie 907-927 pozwalają na wykonanie testów nacisku dłoni pacjenta:
        if self.tryb == 2:

            try:
                # otwarcie połączenia z portem
                serialInst.open()
                # sprawdzenie czy przez port nadawane są dane:
                print(serialInst.is_open)
                while True:
                    if serialInst.in_waiting:
                        for i in range(0,6):
                            # zapisanie odebranych danych do tymczaswowej listy packet:
                            wynik = serialInst.readline()
                            wynik = wynik.replace(b'\n', b'').replace(b'\r', b'')
                            packet.append(str(wynik).lstrip("b").strip("'"))
                            # wypisanie wyników na ekranie pacjenta:
                        global okno_nacisk
                        for j in range(0,1):
                            okno_nacisk.insert(0, packet[5])
                        else:
                            break

                #for w in packet:
                print(packet[5])

            except:
                # obsługa błędów
                messagebox.showinfo("","Błąd podczas łączenia z portem. Upewnij się, że urządzenie jest prawidłowo połączone")
            # zamknięcie otwartego portu
            finally:
                serialInst.close()



class Cwiczenia(Frame, App):
    def __init__(self, aplikacja, kontener_stron):
        super().__init__(kontener_stron)

        self.configure(bg="#2d2e2e")
        global folder
        global wlacz
        global stop
        global pauza

        lbl1 = Label(self, text="WYBÓR ĆWICZENIA",
                     fg="white", bg="#2d2e2e", font=("Arial", 15,'bold'))

        lbl1.pack(pady=(25,0))
        lbl2 = Label(self, text="Proszę wybrać z poniższej listy ćwiczenie zalecone przez specjalistę:", fg="white",
                     bg="#2d2e2e", font=("Arial", 12))
        lbl2.pack()
        wybrane_cwicznie = StringVar()
        wybor_cwiczenia = ttk.Combobox(self, width=21, textvariable=wybrane_cwicznie, font=("Arial", 11))
        wybrany_port = StringVar()
        wybor_portu_cw = ttk.Combobox(self, width=20, textvariable=wybrany_port, font=("Arial", 11))
        przycisk_port = Button(self, text="Załaduj  listę dostępnych portów COM", fg="white", bg="#01786F", width=30,
                               height=1,
                               font=('Arial', 12), activebackground="#319177", activeforeground="white",
                               cursor="hand2",
                               command=lambda: [wybor_portu_cw.configure(values=self.wyborport()), pierwszy_port(wybor_portu_cw)])
        przycisk_port.pack()

        wybor_portu_cw.pack()
        wybor_portu_cw.current()

        wybor_cwiczenia['values'] = ()
        wybor_cwiczenia.configure(state=DISABLED)
        f2 = Frame(self, width=1200, height=200, bg="#2d2e2e")
        f2.pack(side=BOTTOM, fill="x")
        f3=Frame(self, width=200, height=700, bg="#2d2e2e")
        f3.pack(side=LEFT, fill="y")
        f4=Frame(self, width=200, height=700, bg="#2d2e2e")
        f4.pack(side=RIGHT, fill="y")
        playbtn = Button(f2, state=DISABLED, image=wlacz, bg="#2d2e2e", activebackground='#2d2e2e', border=0, cursor="hand2",
                         command=lambda: [self.playAgain(), print(App.konto)])
        playbtn.grid(column=2, row=0, padx=(50, 50))

        stopbtn = Button(f2,state=DISABLED, image=stop, bg="#2d2e2e", activebackground='#2d2e2e', border=0, cursor="hand2",
                         command=lambda: [self.StopVideo(), playbtn.configure(state=DISABLED),stopbtn.configure(state=DISABLED),pausebtn.configure(state=DISABLED)])
        stopbtn.grid(column=1, row=0, padx=(240, 0))

        pausebtn = Button(f2,state=DISABLED, image=pauza, bg="#2d2e2e", activebackground='#2d2e2e', border=0, cursor="hand2",
                          command=lambda: self.PauseVideo())
        pausebtn.grid(column=3, row=0)
        testuj=Button(f2,fg="white",bg="#2d2e2e",  width=25,text="Wykonaj ćwiczenie",
                               height=1,
                               font=('Arial', 12), activebackground="#319177", activeforeground="white",
                               cursor="hand2",state=DISABLED,
                               command=lambda: [self.portconnect_and_test(wybrany_port.get(),2),self.open_popup(wyniki_cwiczen,wybrane_cwicznie.get())])
        testuj.grid(column=5,row=0,padx=(250,0))
        komentarz = Button(f2, fg="white", bg="#2d2e2e", width=30, text="Sprawdź komentarz do ćwiczenia",
                        height=1,
                        font=('Arial', 12), activebackground="#319177", activeforeground="white",
                        cursor="hand2",state=DISABLED,
                        command=lambda: [self.open_popup_komentarz(self.baza2(wybrane_cwicznie.get(),2))])
        komentarz.grid(column=0,row=0)
        global przycisk_zatwierdz
        global przycisk_zaladuj
        przycisk_zatwierdz = Button(self, text="Zatwierdź ćwiczenie", fg="white", bg="#01786F", width=20, height=1,
                                    font=('Arial', 12), activebackground="#319177", activeforeground="white",
                                    cursor="hand2", command=lambda: [przycisk_zatwierdz.configure(state=DISABLED, background="#2d2e2e", text="Zatwierdź ćwiczenie",
                                        width=20), self.open_file(wybrane_cwicznie.get(),str(wybrany_port),2),przycisk_zaladuj.configure(state=DISABLED, background="#2d2e2e"),playbtn.configure(state=NORMAL),stopbtn.configure(state=NORMAL),pausebtn.configure(state=NORMAL),testuj.configure(state=NORMAL,bg="#01786F"),])
        przycisk_zatwierdz.configure(state=DISABLED,background="#2d2e2e")
        przycisk_zaladuj = Button(self, text="Załaduj listę ćwiczeń", fg="white", bg="#01786F", width=20, height=1,
                                    font=('Arial', 12), activebackground="#319177", activeforeground="white",
                                    cursor="hand2",
                                    command=lambda: [wybor_cwiczenia.configure(state=NORMAL,values=str((self.baza(App.konto["login"]))).strip("[(]),'_").replace(","," ").lstrip("[(]),'_")),wybor_cwiczenia.current(0),print(str(self.baza(App.konto["login"]))),przycisk_zatwierdz.configure(state=NORMAL,bg="#01786F"),komentarz.configure(state=NORMAL,bg="#01786F")])


        przycisk_zaladuj.pack(pady=(5,5))
        wybor_cwiczenia.pack(pady=(5,5))


        global numerfilmu

        numerfilmu = wybor_cwiczenia.current()

        przycisk_zatwierdz.pack(pady=(5,5))
        global wyniki_cwiczen
        kciuk=list()
        wskazujacy=list()
        srodkowy=list()
        serdeczny=list()
        maly=list()
        nacisk=list()
        wyniki_cwiczen=(kciuk,wskazujacy,srodkowy,serdeczny,maly,nacisk)

        global otwarcie

        global zamkniecie

        global b2
        b2 = Button(self,
                    image=otwarcie,
                    command=lambda: self.lista_menu(aplikacja),
                    border=0,
                    bg='#2d2e2e',
                    cursor="hand2",
                    activebackground='#2d2e2e')
        b2.place(x=5, y=8)
        def pierwszy_port(pierwszy):
            try:
                pierwszy.current(0)
            except:
                messagebox.showinfo("","Brak dostępnych portów")
    def lista_menu(self,aplikacja):

        global f1

        f1 = Frame(self, width=250, height=700, bg='#01786F')
        f1.place(x=0, y=0)
        b2.place(x=5, y=8)

        def przycisk_menu(x, y, tekst, bcolor, fcolor, komenda):

            przycisk_m = Button(f1, text=tekst,
                                width=27,
                                height=2,
                                fg='white',
                                border=0,
                                bg=fcolor,
                                activeforeground='white',
                                activebackground=bcolor,
                                font=('Arial', 13),
                                cursor="hand2",
                                command=komenda)
            przycisk_m.place(x=x, y=y)
        przycisk_menu(0, 140, 'Wykonaj testy', '#319177', '#01786F', lambda : [f1.destroy(),aplikacja.show_frame(aplikacja.Testy)])
        przycisk_menu(0, 240, 'Strona Główna', '#319177', '#01786F', lambda : [f1.destroy(),aplikacja.show_frame(aplikacja.Zalogowano_Pacjent)])
        przycisk_menu(0, 340, 'Historia', '#319177', '#01786F', lambda : [f1.destroy(),aplikacja.show_frame(aplikacja.Historia)])
        przycisk_menu(0, 440, 'Pomoc', '#319177', '#01786F', lambda : [f1.destroy(),aplikacja.show_frame(aplikacja.Pomoc)])
        przycisk_menu(0, 540, 'Wyloguj', '#319177', '#01786F', lambda:wyloguj())

        def zamknij():
            f1.destroy()

        def wyloguj():
            f1.destroy()
            pytanie = messagebox.askyesno('Wylogowywanie', 'Czy chcesz się wylogować?')
            if pytanie == True:
                messagebox.showinfo('Wylogowywanie', 'Pomyślnie wylogowano.')
                aplikacja.show_frame(aplikacja.Wybor_profilu)


        Button(f1,
               image=zamkniecie,
               border=0,
               command=zamknij,
               bg='#01786F',
               cursor="hand2",
               activebackground='#01786F').place(x=5, y=10)

    #metoda klasy Cwiczenia powzwalająca na pobranie informacji
    # o przepisanych pacjentowi ćwiczeń do wykonywania
    def baza(self,login):
        login_pacjent=App.konto["login"]
        try:
            # wprowadzenie danych używanej bazy danych i otwarcie jej:
            mysqldb1=mysql.connector.connect(host="localhost",user="root",passwd="1234",database="login")
            # tworzenie zmiennej tymczasowej użwyanej do pobrania wyniku zapytania do bazy danych:
            mycursor=mysqldb1.cursor()
            # zapytanie(kwerenda) sql wprowadzające dane do bazy:
            sql="SELECT przypisane_cwiczenia from pacjenci_dane where login= %s"
            # wykonanie zapytania sql do bazy danych:
            mycursor.execute(sql,[login_pacjent])
            # zatwierdzenie pobrania danych z bazy:
            results=mycursor.fetchall()
            if results:
                return results
            else:
                #obsługa błędó
                messagebox.showinfo("","Nieprawidłowy login lub hasło")

        except mysql.connector.Error:
            messagebox.showinfo("", "Błąd przy połączeniu")
        except:
            messagebox.showinfo("", "Błąd")
        else:
            #zamknięcie otwartej bazy
            mysqldb1.close()

    #metoda klasy Cwiczenia pozwalająca na otwarcie materiału wideo ćwiczenia,
    #mogąca wywołać pobieranie go z dysku google
    def open_file(self,nazwa,port,tryb):

        global videoplayer
        global f2
        #stworzenie odtwarzacza wideo przy użyciu konstruktora TkinterVideo z biblioteki TkVideoPlayer:
        videoplayer = TkinterVideo(master=self, scaled=True)
        videoplayer.pack(expand=True, fill="both")



        #ścieżka do filmu na dysku komputera pacjenta
        film=nazwa
        file = "filmy/"+str(film)+".mp4"
        #sprawdzenie czy pacjent ma pobrany plik:
        if os.path.isfile(file):
            #załadowanie i odtworzenie filmu:
            videoplayer.load(r"{}".format(file))
            videoplayer.play()
        else:
            #jeśli pacjent nie ma pobranego pliku następuje wywołanie pobrania go z Dysku Google
            videoplayer.destroy()
            print(f"Unable to open ")
            self.pob = Label(self, text="Trwa_pobieranie", fg="white")
            self.przycisk = Button(self,text="Pobierz ten film",fg="white", bg="#01786F", width=20, height=1,
                                        font=('Arial', 12), activebackground="#319177", activeforeground="white",
                                        cursor="hand2", command=lambda:[self.pobieranie(film,self.przycisk,przycisk_zatwierdz)])
            self.przycisk.pack(pady=(5,5))

            przycisk_zatwierdz.configure(state=NORMAL,fg="white", bg="#01786F")


    #metoda klasy Cwiczenia wywoływana przez metodę open_file
    # w razie potrzeby pobrania filmu z dysku Google
    def pobieranie(self,nazwa,przycisk,przycisk_z):
        self.przycisk = przycisk
        przycisk.configure(text="Trwa pobieranie")

        try:

            # linie odpowiedzialne za autoryzację dostępu do dysku Google przez API Google Drive:
            gauth = GoogleAuth()
            drive = GoogleDrive(gauth)
            #linie 1174-1181 pozwalają na pobranie pożądanego filmu z dysku Google
            #załadowanie i posortowanie listy dostępnych filmów do pobrania:
            file_list = drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format('1E_nQtJc0UyrtyYvkz04pA-pyVR5ZRjKs')}).GetList()
            for i, file in enumerate(sorted(file_list, key=lambda x: x['title']), start=1):
                #sprawdzenie czy film do wybranego ćwiczenia znajduje się na dysku Google:
                if file['title']==nazwa+'.mp4':
                    path='filmy/'
                    #pobranie filmu z dysku Google na dysk komputera pacjenta:
                    file.GetContentFile(path+file['title'])

            self.przycisk.destroy()
            przycisk_z.configure(state=NORMAL, background="#01786F",
                             text="Pobrano plik. Kliknij, by zatwierdzić ćwiczenie.", width=37)
        except:
            self.przycisk.destroy()




    def playAgain(self):

        try:
                videoplayer.play()
        except TclError:
                messagebox.showinfo("", "Proszę załadować film")
        except:

                messagebox.showinfo("","Proszę załadować film")



    def StopVideo(self):
        try:
            videoplayer.stop()

            przycisk_zatwierdz.configure(state=NORMAL, background="#01786F")
            przycisk_zaladuj.configure(state=NORMAL,background="#01786F")
            videoplayer.destroy()
        except TclError:
            messagebox.showinfo("", "Proszę załadować film")
        except:
            messagebox.showinfo("", "Proszę załadować film")

    def PauseVideo(self):
        try:
            videoplayer.pause()
        except TclError:
            messagebox.showinfo("", "Proszę załadować film")
        except:
            messagebox.showinfo("", "Proszę załadować film")

    def wyborport(self):
        ports = serial.tools.list_ports.comports()


        portList = []

        for onePort in ports:
            portList.append(str(onePort))
            print(str(onePort))
        return portList
    #metoda klasy Cwiczenia pozwalająca na połączenie się z wybranym portem COM
    # i odbieranie danych pomiarowych z czyjników z wykonywanych ćwiczeń przez pacjenta
    def portconnect_and_test(self,port,tryb):
        global wyniki_cwiczen
        # wyczyszczenie tablicy zawierającej poprzednie dane pomiarowe
        for i in range(0, 6):
            wyniki_cwiczen[i].clear()
        try:
            wybrany_port="COM"+port[3]
            self.tryb=tryb
            packet = list()
            # ustawienie parametrów do połącznia się z portem:
            serialInst = serial.Serial()
            serialInst.baudrate = 9600
            serialInst.port = wybrany_port
            global videoplayer
            if serialInst.is_open:
                serialInst.close()
            #sprawdzenie połączenia z portem
            print(serialInst.is_open)
            #ustalenie czasu pomiaru przy wykonywaniu ćwiczenia:
            print(videoplayer.current_duration())
            timeout=time.time()+videoplayer.current_duration()
            # otwarcie połączenia z portem
            serialInst.open()
            # linie 1261-1280 pozwalają na wykonanie odpowiednich pomiarów
            # pracy dłoni pacjenta podczas wykonywania ćwiczeń:
            while True:
                #przerwanie pobierania danych pomiarowych po wyznaczonym czasie:
                if time.time()>timeout:
                    serialInst.close()
                    break
                # sprawdzenie czy przez port nadawane są dane:
                if serialInst.in_waiting:
                    for i in range(0,6):
                            #odczyt danych przesyłanych przez port COM
                            wynik = serialInst.readline()
                            #linie 1273-1275 odpowiadają za zapewnienie poprawnego odczytu danych z portu
                            # przy wystąpieniu przerwy w przesylanych danych:
                            while wynik=="":
                                serialInst.cancel_read()
                                wynik = serialInst.readline()

                            else:
                                #linie 1322-1323 odpowiadają za zapisanie w tablicy wyniki_cwiczen danych pomiarowych
                                wynik = wynik.replace(b'\n', b'').replace(b'\r', b'')
                                wyniki_cwiczen[i].append(str(wynik).lstrip("b").strip("'").strip("stopni").strip("g"))


                for w in packet:
                    print(w)
                print("kciuk=")
                print(wyniki_cwiczen[0])
                print("wskazujacy=")
                print(wyniki_cwiczen[1])
                print("srodkowy=")
                print(wyniki_cwiczen[2])
                print("serdeczny=")
                print(wyniki_cwiczen[3])
                print("maly=")
                print(wyniki_cwiczen[4])
                print("nacisk")
                print(wyniki_cwiczen[5])




        except:
            messagebox.showinfo("","Błąd podczas łączenia z portem. Upewnij się, że urządzenie jest prawidłowo połączone")
        finally:
                serialInst.close()

    def open_popup(self,wyniki,nazwa_cwiczenia):
        data = datetime.date.today()
        data2 = datetime.datetime.now()
        top=Toplevel()

        top.geometry("1200x700")
        top.configure( bg= "#2d2e2e")
        top.resizable(width=False,height=False)
        wybrany_palec_lub_sila=StringVar()
        wykresy_katow_i_sily = ttk.Combobox(top, width=20, textvariable=wybrany_palec_lub_sila, font=("Arial", 11),
                                            values=["kciuk", "wskazujący", "środkowy", "serdeczny", "mały",
                                                    "siła_nacisku"])

        przycisk_pokaz_wykresy = Button(top, text="Załaduj wykres",
                                               fg="white", bg="#01786F", width=14, height=1,
                                               font=('Arial', 12), activebackground="#319177",
                                               activeforeground="white",
                                               cursor="hand2",
                                               command=lambda: [
                                                   wykres(wyniki[wykresy_katow_i_sily.current()],wykresy_katow_i_sily.current())])
        wykresy_katow_i_sily.grid(row=2, column=1, padx=(450, 0), pady=(15, 0))

        przycisk_pokaz_wykresy.grid(row=3, column=1, padx=(450, 0), pady=(10, 20))



        czas_i_wynik = list()
        czas_i_wynik.append(videoplayer.current_duration())
        czas_i_wynik.append(wyniki)
        print(nazwa_cwiczenia)
        #fragment kodu metody open_popup klasy Cwiczenia
        # pozwalający na zapisy danych pomiarowych z wykonywanych ćwiczeń do pliku:
        #utworzenie pliku mającego przechować dane w wyznaczonej śćieżce dostepu:
        path_and_name = "testy/" + str(data) + "-" + str(App.konto["nr_pacjenta"]) +str(nazwa_cwiczenia) +".txt"
        file = open(path_and_name, mode='w')
        try:
            #linie1343-1353 odpowiadają za zapisanie pliku z danymi na dysk komputera pacjenta:
            file.write(str(videoplayer.current_duration()) + "\n")
            for wy in wyniki:
                zapis = wy
                file.write(str(zapis) + "\n")
            messagebox.showinfo("", "Wyniki zostały zapisane na dysku")
        except:
            #obsluga błędów
            messagebox.showinfo("Niepowodzenie w zapisie wyników na dysku")
        else:
            #zamknięcie pliku po wykonaniu zapisu
            file.close()
        # fragment kodu metody open_popup klasy Cwiczenia
        # pozwalający na zapisy danych pomiarowych z wykonywanych ćwiczeń do archiwum:
        # linie odpowiadające za autoryzację dostępu do dysku Google przez API Google Drive:
        gauth = GoogleAuth()
        drive = GoogleDrive(gauth)
        # utworzenie nowego pliku na dysku Google:
        file1 = drive.CreateFile({'parents': [{'id': '1MH62rnEyI0vkZFo3Ii2oMGJ3UrJHbGRG'}],
                                  'title': str(nazwa_cwiczenia)+str(data2)+"-"+str(App.konto['nr_pacjenta'])+"-.txt"})
        # wgranie zawartości pliku z komputera fizjoterapeuty na dysk Google:
        file1.SetContentFile(str(path_and_name))
        file1.Upload()

        #metoda zagnieżdżona w metodzie open_popup klasy Cwiczenia
        # pozwalająca na narysowanie wykresów przedstawiających dane z wykonanego ćwiczenia przez pacjenta:
        def wykres(wyniki,tryb):
            global videoplayer
            wyn=list()
            for w in wyniki:
                try:
                    wyn.append(float(w))
                except:
                    pass
            try:
                # stworzenie nowego wykresu:
                fig = Figure(figsize=(6,5))
                # skonfigurowanie osi czasu na wykresie:
                t=np.arange(0,videoplayer.current_duration(),videoplayer.current_duration()/len(wyn))
                # linie 1383-1394 odpowiadają za wyrysowanie wykresu,
                # a także za ustawienie etykiet osi:
                ax=fig.add_subplot()
                ax.plot(t, wyn)
                ax.set_xlabel('czas [s]')
                #zmiana etykiety osi y w zależności od wybranego wykresu:
                if tryb in range(0,5):
                    ax.set_ylabel('kąt ugięcia [°]')
                elif tryb==5:
                    ax.set_ylabel('siła nacisku [g]')
                # linie 1392-1394 odpowiadają za umieszczenie wykresu w oknie wyświetlającym wykresy:
                canvas = FigureCanvasTkAgg(fig, master=top)  # A tk.DrawingArea.
                canvas.draw()
                canvas.get_tk_widget().grid(column=1,columnspan=3,row=4,rowspan=3, padx=(280,0), pady=5)
            except:
                #obsługa błędów
                messagebox.showerror("","Brak danych, sprawdź połączenie z urządzeniem.")
                top.destroy()
    #metoda klasy Cwiczenia pozwalajaca na pobranie komentarza do wybranego ćwiczenia:
    def baza2(self, nazwa_cwiczenia, tryb):
        login_pacjent = App.konto["login"]
        try:
            # wprowadzenie danych używanej bazy danych i otwarcie jej:
            mysqldb1 = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="login")
            # tworzenie zmiennej tymczasowej użwyanej do pobrania wyniku zapytania do bazy danych:
            mycursor = mysqldb1.cursor()
            # zapytanie(kwerenda) sql wprowadzające dane do bazy:
            sql = "SELECT komentarz from cwiczenia where nazwa_cwiczenia= %s"
            # wykonanie zapytania sql do bazy danych:
            mycursor.execute(sql, [nazwa_cwiczenia])
            #podtwierdzenie pobrania komentarza z bazy
            results = mycursor.fetchall()
            if results:
                return results

            else:
                #obsługa błędów
                messagebox.showinfo("", "Nie znaleziono komentarza do ćwiczenia")

        except mysql.connector.Error:
            messagebox.showinfo("", "Błąd przy połączeniu")
        except:
            messagebox.showinfo("", "Błąd")
        else:
            #zamknięcie otwartej bazy danych
            mysqldb1.close()

    #metoda klasy Cwiczenia pozwalająca na przeczytanie wskazówek fizjoterapeuty
    def open_popup_komentarz(self,komentarz):
        top2=Toplevel()
        top2.geometry("700x700")
        top2.configure( bg= "#2d2e2e")
        do_usuniecia='\\n'
        napis_komentarz=Label(top2,text="Komentarz do ćwiczenia dodany przez fizjoterapeutę:",
                              fg="white", bg="#2d2e2e", font=("Arial", 15,'bold'))
        napis_komentarz.pack(pady=20)
        okno_komentarz=Text(top2,height=10)
        #wyświetlenie komentarza po wywołaniu metody klasy Cwiczenia pobierającej go(baza_2)
        okno_komentarz.insert(INSERT,str(komentarz).strip("{()}[],'").replace(do_usuniecia,""))
        okno_komentarz.configure(state=NORMAL)
        okno_komentarz.pack(pady=30)


class Historia(Frame,App):
    def __init__(self, aplikacja, kontener_stron):
        super().__init__(kontener_stron)
        self.configure(bg="#2d2e2e")
        l2 = Label(self, text='Przejrzyj historię wyników: ', fg='white', bg='#2d2e2e')
        l2.config(font=('Arial', 20))
        l2.place(x=593, y=150)
        Ostanie=Button(self,text="Poprzednie wyniki testów",fg="white", bg="#01786F", width=23, height=2,
                                  font=('Arial', 13),
                                  activebackground="#319177", activeforeground="white", cursor="hand2", command=lambda:self.open_popup_poprzednie_wyniki())
        Ostanie.place(x=290,y=300)
        his_kat = Button(self, text="Historia kątów ugięć palców i siły nacisku",fg="white", bg="#01786F", width=36, height=2,
                                  font=('Arial', 13),
                                  activebackground="#319177", activeforeground="white", cursor="hand2", command=lambda:self.open_popup_historia())
        his_kat.place(x=544,y=300)
        wykresy = Button(self, text="Historia wykresów z ćwiczeń",fg="white", bg="#01786F", width=26, height=2,
                                  font=('Arial', 13),
                                  activebackground="#319177", activeforeground="white", cursor="hand2", command=lambda:self.open_popup_wykr())
        wykresy.place(x=915,y=300)



        global otwarcie
       # otwarcie =ImageTk.PhotoImage(Image.open('otworz.png'))

        global zamkniecie
        #zamkniecie = ImageTk.PhotoImage(Image.open('zamknij.png'))

        global b2
        b2 = Button(self,
                    image=otwarcie,
                    command=lambda :self.lista_menu(aplikacja),
                    border=0,
                    bg='#2d2e2e',
                    cursor="hand2",
                    activebackground='#2d2e2e')
        b2.place(x=5, y=8)


    def lista_menu(self,aplikacja):


        f1 = Frame(self, width=250, height=700, bg='#01786F')

        f1.place(x=0, y=0)
        b2.place(x=5, y=8)

        def przycisk_menu(x, y, tekst, bcolor, fcolor, komenda):

            przycisk_m = Button(f1, text=tekst,
                                width=27,
                                height=2,
                                fg='white',
                                border=0,
                                bg=fcolor,
                                activeforeground='white',
                                activebackground=bcolor,
                                font=('Arial', 13),
                                cursor="hand2",
                                command=komenda)
            przycisk_m.place(x=x, y=y)
        przycisk_menu(0, 140, 'Wykonaj Testy', '#319177', '#01786F', lambda: [aplikacja.show_frame(aplikacja.Testy),f1.destroy()])
        przycisk_menu(0, 240, 'Wykonaj ćwiczenia', '#319177', '#01786F', lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Cwiczenia)])
        przycisk_menu(0, 340, 'Strona Główna', '#319177', '#01786F', lambda: [aplikacja.show_frame(aplikacja.Zalogowano_Pacjent),f1.destroy()])
        przycisk_menu(0, 440, 'Pomoc', '#319177', '#01786F',lambda : [f1.destroy(),aplikacja.show_frame(aplikacja.Pomoc)])
        przycisk_menu(0, 540, 'Wyloguj', '#319177', '#01786F', lambda:wyloguj())

        def zamknij():
            f1.destroy()

        def wyloguj():
            f1.destroy()
            pytanie = messagebox.askyesno('Wylogowywanie', 'Czy chcesz się wylogować?')
            if pytanie == True:
                messagebox.showinfo('Wylogowywanie', 'Pomyślnie wylogowano.')
                aplikacja.show_frame(aplikacja.Wybor_profilu)


        Button(f1,
               image=zamkniecie,
               border=0,
               command=zamknij,
               bg='#01786F',
               cursor="hand2",
               activebackground='#01786F').place(x=5, y=10)

    def open_popup_poprzednie_wyniki(self):
        top3=Toplevel()
        top3.geometry("1200x700")
        top3.configure( bg= "#2d2e2e")
        top3.resizable(width=False, height=False)

        napis_poprzedni = Label(top3, text="WYŚWIETLENIE OSTATNICH WYNIKÓW POMIARU", width=40,
                                 font=("Arial", 15, 'bold'),
                                 fg="white",
                                 bg="#2d2e2e")
        napis_poprzedni.grid(column=1, row=2, padx=350, pady=(25, 0))

        przycisk_odbierz_wyniki = Button(top3, text="Wyświetl wyniki", fg="white", bg="#01786F", width=13, height=1,
                                         font=('Arial', 12), activebackground="#319177", activeforeground="white",
                                         cursor="hand2",
                                         command=lambda: [wyswietlenie_wynikow(self.baza_odb_poprzednie(App.konto['nr_pacjenta']))])
        przycisk_odbierz_wyniki.grid(row=3, column=1, columnspan=1, padx=(0, 0), pady=20)
        wyniki_1 = Label(top3, text="Wyniki pomiarów :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        wyniki_1.grid(column=1, row=4, padx=(0, 0), pady=(25, 0))

        napis_kciuk_1 = Label(top3, text="Kciuk :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_kciuk_1.grid(column=1, row=5, padx=(0, 180), pady=(15, 0))
        okno_kciuk_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_kciuk_1.grid(row=5, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))
        napis_wskazujacy_1 = Label(top3, text="Wskazujący :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_wskazujacy_1.grid(column=1, row=6, padx=(0, 180), pady=(15, 0))
        okno_wskazujacy_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_wskazujacy_1.grid(row=6, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))
        napis_srodkowy_1 = Label(top3, text="Środkowy :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_srodkowy_1.grid(column=1, row=7, padx=(0, 180), pady=(15, 0))
        okno_srodkowy_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_srodkowy_1.grid(row=7, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))
        napis_serdeczny_1 = Label(top3, text="Serdeczny :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_serdeczny_1.grid(column=1, row=8, padx=(0, 180), pady=(15, 0))
        okno_serdeczny_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_serdeczny_1.grid(row=8, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))
        napis_maly_1 = Label(top3, text="Mały :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_maly_1.grid(column=1, row=9, padx=(0, 180), pady=(15, 0))
        okno_maly_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_maly_1.grid(row=9, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))
        napis_sila_nacisku_1 = Label(top3, text="Siła nacisku :", width=14, font=("Arial", 12), fg="white",
                                     bg="#2d2e2e")
        napis_sila_nacisku_1.grid(column=1, row=10, padx=(0, 180), pady=(15, 0))
        okno_sila_nacisku_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_sila_nacisku_1.grid(row=10, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))

        # metoda zagnieżdżona w metodzie open_popup_poprzednie_wyniki klasy Historia do wyświetlania wyników:
        def wyswietlenie_wynikow(wyniki):
            wynik = wyniki[0]
            ugiecie = wynik[0]
            # w linijkach 1583-1590 następuje obróbka i wpisanie w odpowiednie okienka danych
            # z najnowszych wyników testów pacjenta,
            # które zostały uprzednio pobrane z bazy danych
            ugiecie_oddzielone = ugiecie.splitlines(True)
            nacisk = wynik[1]
            okno_kciuk_1.insert(0, ugiecie_oddzielone[0])
            okno_wskazujacy_1.insert(0, ugiecie_oddzielone[1])
            okno_srodkowy_1.insert(0, ugiecie_oddzielone[2])
            okno_serdeczny_1.insert(0, ugiecie_oddzielone[3])
            okno_maly_1.insert(0, ugiecie_oddzielone[4])
            okno_sila_nacisku_1.insert(0, nacisk)


    def open_popup_historia(self):
        top3=Toplevel()
        top3.geometry("1200x700")
        top3.configure( bg= "#2d2e2e")
        top3.resizable(width=False, height=False)
        wybrane_hist_ugiecie = StringVar()
        historyczne_ugiecia = ttk.Combobox(top3, width=21, textvariable=wybrane_hist_ugiecie, font=("Arial", 11))
        wybrany_hist_nacisk = StringVar()
        historyczne_naciski = ttk.Combobox(top3, width=20, textvariable=wybrany_hist_nacisk, font=("Arial", 11))
        przycisk_odbierz_hist_wyniki_ugiecie = Button(top3, text="Załaduj historyczne wyniki testów ugięcia", fg="white", bg="#01786F", width=32, height=1,
                                         font=('Arial', 12), activebackground="#319177", activeforeground="white",
                                         cursor="hand2",
                                         command=lambda: [historyczne_ugiecia.configure(values=lista_his_ug()),historyczne_ugiecia.current(0)])
        przycisk_odbierz_hist_wyniki_nacisk = Button(top3, text="Załaduj historyczne wyniki testów nacisku", fg="white",
                                         bg="#01786F", width=32, height=1,
                                         font=('Arial', 12), activebackground="#319177", activeforeground="white",
                                         cursor="hand2",
                                         command=lambda: [historyczne_naciski.configure(values=lista_his_nac()),historyczne_naciski.current(0)])


        wyniki_1 = Label(top3, text="PRZEGLĄD HISTORII POMIARÓW", width=28, font=("Arial", 15, 'bold'), fg="white", bg="#2d2e2e")
        wyniki_1.grid(column=1, row=2, padx=(400, 0), pady=(25, 0))


        przycisk_odbierz_hist_wyniki_ugiecie.grid(row=3, column=1, columnspan=1, padx=(400, 0), pady=(20,5))
        historyczne_ugiecia.grid(column=1, row=4, padx=(400,0))
        przycisk_zatw_ug = Button(top3, text="Zatwierdź",
                                                      fg="white", bg="#01786F", width=11, height=1,
                                                      font=('Arial', 12), activebackground="#319177",
                                                      activeforeground="white",
                                                      cursor="hand2",
                                                      command=lambda:[wyswietlenie_wynikow_ug(wybrane_hist_ugiecie.get())])
        przycisk_zatw_nac = Button(top3, text="Zatwierdź",
                                  fg="white", bg="#01786F", width=11, height=1,
                                  font=('Arial', 12), activebackground="#319177",
                                  activeforeground="white",
                                  cursor="hand2",
                                  command=lambda: [wyswietlenie_wynikow_nac(wybrany_hist_nacisk.get())])
        przycisk_zatw_ug.grid(column=1,row=5, padx=(400,0), pady=(10,0))

        napis_kciuk_1 = Label(top3, text="Kciuk :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_kciuk_1.grid(column=1, row=6, padx=(365, 180), pady=(15, 0))
        okno_kciuk_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_kciuk_1.grid(row=6, column=1, columnspan=1, padx=(450, 0), pady=(10, 0))
        napis_wskazujacy_1 = Label(top3, text="Wskazujący :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_wskazujacy_1.grid(column=1, row=7, padx=(355, 180), pady=(15, 0))
        okno_wskazujacy_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_wskazujacy_1.grid(row=7, column=1, columnspan=1, padx=(450, 0), pady=(10, 0))
        napis_srodkowy_1 = Label(top3, text="Środkowy :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_srodkowy_1.grid(column=1, row=8, padx=(355, 180), pady=(15, 0))
        okno_srodkowy_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_srodkowy_1.grid(row=8, column=1, columnspan=1, padx=(450, 0), pady=(10, 0))
        napis_serdeczny_1 = Label(top3, text="Serdeczny :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_serdeczny_1.grid(column=1, row=9, padx=(355, 180), pady=(15, 0))
        okno_serdeczny_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_serdeczny_1.grid(row=9, column=1, columnspan=1, padx=(450, 0), pady=(10, 0))
        napis_maly_1 = Label(top3, text="Mały :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_maly_1.grid(column=1, row=10, padx=(365, 180), pady=(15, 0))
        okno_maly_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_maly_1.grid(row=10, column=1, columnspan=1, padx=(450, 0), pady=(10, 0))
        napis_sila_nacisku_1 = Label(top3, text="Siła nacisku :", width=14, font=("Arial", 12), fg="white",
                                     bg="#2d2e2e")
        przycisk_odbierz_hist_wyniki_nacisk.grid(row=11, column=1, columnspan=1, padx=(400, 0), pady=(30,5))
        historyczne_naciski.grid(column=1, row=12, padx=(400, 0))
        przycisk_zatw_nac.grid(column=1, row=13, padx=(400, 0), pady=(10,0))
        napis_sila_nacisku_1.grid(column=1, row=14, padx=(355, 180), pady=(15, 0))
        okno_sila_nacisku_1 = Entry(top3, width=18, font=('Arial', 13))
        okno_sila_nacisku_1.grid(row=14, column=1, columnspan=1, padx=(450, 0), pady=(10, 0))

        # metoda zagnieżdzona w metodzie open_popup_historia klasy Odbierz_wyniki
        # odpowiedzialna za wyświetlenie archiwum testów ugięcia palców pacjenta:
        def lista_his_ug():
            # linie odpowiadające za autoryzację dostępu do dysku Google przez API Google Drive:
            gauth = GoogleAuth()
            drive = GoogleDrive(gauth)
            # linie 1669-1676 odpowiadają za pobranie i wyświetlenie listy testów ugięcia palców z archiwum
            lista_ugiec=list()
            file_list = drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format('1ok5Glz4vepxv1_Ys3QXouYxDOlA1DZq7')}).GetList()
            for file in file_list:
                if str(App.konto['nr_pacjenta']) in file['title']:
                    print('title: %s, id: %s' % (file['title'], file['id']))
                    lista_ugiec.append(file['title'])
            return lista_ugiec

        # metoda zagnieżdzona w metodzie open_popup_historia klasy Historia
        # odpowiedzialna za wyświetlenie archiwum testów siły nacisku dłoni pacjenta:
        def lista_his_nac():
            # linie odpowiedzialne za autoryzację dostępu do dysku Google przez API Google Drive:
            gauth = GoogleAuth()
            drive = GoogleDrive(gauth)
            # linie 1685-1692 odpowiadają za pobranie i wyświetlenie listy testów siły nacisku dłoni z archiwum
            lista_naciskow=list()
            file_list = drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format('1pKp-OoLbrWApdstm9bIcmFLGQWAJkfL9')}).GetList()
            for file in file_list:
                if str(App.konto['nr_pacjenta']) in file['title']:
                    print('title: %s, id: %s' % (file['title'], file['id']))
                    lista_naciskow.append(file['title'])
            return lista_naciskow

        # metoda zagnieżdzona w metodzie open_popup_historia klasy Historia
        # odpowiedzialna za pobranie z archiwum i wyświetlenie wybranych przez pacjenta
        # wyników ugięcia palców:
        def wyswietlenie_wynikow_ug(plik):
            # linie odpowiedzialne za autoryzację dostępu do dysku Google przez API Google Drive:
            gauth = GoogleAuth()
            drive = GoogleDrive(gauth)
            # linie 1704-1716 odpowiadają za pobranie z archiwum i wyświetlenie
            # wybranych przez pacjenta
            # wyników ugięcia palców:
            file_list = drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format('1ok5Glz4vepxv1_Ys3QXouYxDOlA1DZq7')}).GetList()
            for file in file_list:
                if file['title']==plik:
                    file2 = drive.CreateFile({'id': file['id']})

                    ugiecia=file2.GetContentString(file2).splitlines(True)
                    print(ugiecia)
                    okno_kciuk_1.insert(0, ugiecia[0])
                    okno_wskazujacy_1.insert(0, ugiecia[1])
                    okno_srodkowy_1.insert(0, ugiecia[2])
                    okno_serdeczny_1.insert(0, ugiecia[3])
                    okno_maly_1.insert(0, ugiecia[4])

        # metoda zagnieżdzona w metodzie open_popup_historia klasy Odbierz_wyniki
        # odpowiedzialna za pobranie z archiwum i wyświetlenie wybranych przez pacjenta
        # wyników siły nacisku dłoni:
        def wyswietlenie_wynikow_nac(plik):
            # linie odpowiedzialne za autoryzację dostępu do dysku Google przez API Google Drive:
            gauth = GoogleAuth()
            drive = GoogleDrive(gauth)
            # linie 1728-1734 odpowiadają za pobranie z archiwum i wyświetlenie
            # wybranych przez pacjenta
            # wyników siły nacisku dłoni:
            file_list = drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format('1pKp-OoLbrWApdstm9bIcmFLGQWAJkfL9')}).GetList()
            for file in file_list:
                if file['title']==plik:
                    file2 = drive.CreateFile({'id': file['id']})
                    nacisk=file2.GetContentString(file2)
                    okno_sila_nacisku_1.insert(0, nacisk+",")

    # metoda klasy Odbierz_wyniki odpowiadająca za pobranie najnowyszch wyników testów pacjenta z BD
    def baza_odb_poprzednie(self,indeks):

        ind=str(indeks)
        try:
            # wprowadzenie danych używanej bazy danych i otwarcie jej:
            mysqldb_odb=mysql.connector.connect(host="localhost",user="root",passwd="1234",database="login")
            # tworzenie zmiennej tymczasowej użwyanej do pobrania wyniku zapytania do bazy danych:
            mycursor_odb=mysqldb_odb.cursor()
            # zapytanie(kwerenda) sql pobierające pożądane dane z bazy:
            sql="SELECT test_ugiecia,test_nacisku from pacjenci_dane where nr= %s"
            # wykonanie zapytania sql do bazy danych:
            mycursor_odb.execute(sql,[ind])
            # zatwierdzenie pobrania danych z bazy:
            results=mycursor_odb.fetchall()
            if results:
                print(results)
                return results

            else:
                # obsługa błędów:
                messagebox.showinfo("","Nieprawidłowy login lub hasło")

        except mysql.connector.Error:
            messagebox.showinfo("", "Błąd przy połączeniu")
        except:
            messagebox.showinfo("", "Błąd")
        else:
            #zamknięcie otwartej bazy
            mysqldb_odb.close()
    def open_popup_wykr(self):
        data = datetime.date.today()

        top4=Toplevel()

        top4.geometry("1200x700")
        top4.configure( bg= "#2d2e2e")
        top4.resizable(width=False, height=False)
        wybrany_hist_wykres = StringVar()
        historyczne_wykresy = ttk.Combobox(top4, width=20, textvariable=wybrany_hist_wykres, font=("Arial", 11))
        przycisk_odbierz_hist_wykresy = Button(top4, text="Załaduj historyczne wyniki testów",
                                                      fg="white", bg="#01786F", width=27, height=1,
                                                      font=('Arial', 12), activebackground="#319177",
                                                      activeforeground="white",
                                                      cursor="hand2",
                                                      command=lambda: [
                                                          historyczne_wykresy.configure(values=lista_his_wykr()),
                                                          historyczne_wykresy.current(0)])
        global pobrane_wyniki
        pobrane_wyniki=list()
        czas=list()
        global pomiary
        pomiary=""
        wyniki_1 = Label(top4, text="PRZEGLĄD HISTORII WYKRESÓW", width=28, font=("Arial", 15, 'bold'), fg="white",
                         bg="#2d2e2e")
        wyniki_1.grid(column=1, row=2, padx=(400, 0), pady=(25, 10))
        przycisk_odbierz_hist_wykresy.grid(row=3, column=1, columnspan=1, padx=(400, 0), pady=5)
        historyczne_wykresy.grid(column=1, row=4, padx=(400, 0))
        przycisk_zatw_wykr = Button(top4, text="Zatwierdź",
                                  fg="white", bg="#01786F", width=11, height=1,
                                  font=('Arial', 12), activebackground="#319177",
                                  activeforeground="white",
                                  cursor="hand2",
                                  command=lambda: [pobrano(),czas.append(pobrane_wyniki[0].lstrip("[")),print(czas[0]),print(pobrane_wyniki[0]),print(pobrane_wyniki[1])])
        przycisk_zatw_wykr.grid(row=5,column=1, padx=(400, 0), pady=(5,0))

        wybrany_palec_lub_sila = StringVar()
        wykresy_katow_i_sily = ttk.Combobox(top4, width=20, textvariable=wybrany_palec_lub_sila, font=("Arial", 11),
                                            values=["kciuk", "wskazujący", "środkowy", "serdeczny", "mały",
                                                    "siła_nacisku"])

        przycisk_odbierz_hist_wykresy = Button(top4, text="Załaduj wykres",
                                               fg="white", bg="#01786F", width=14, height=1,
                                               font=('Arial', 12), activebackground="#319177",
                                               activeforeground="white",
                                               cursor="hand2",
                                               command=lambda: [
                                                   wykres(czas[0], pobrane_wyniki[wykresy_katow_i_sily.current() + 1],wykresy_katow_i_sily.current())])
        wykresy_katow_i_sily.grid(row=6, column=1, padx=(400, 0), pady=(5, 0))

        przycisk_odbierz_hist_wykresy.grid(row=7, column=1, padx=(400, 0), pady=(5, 30))

        # metoda zagnieżdzona w metodzie open_popup_wykr klasy Historia
        # odpowiedzialna za wyświetlenie archiwum wykresów ukazujących przebieg ćwiczeń
        # wykonywanych przez pacjenta:
        def lista_his_wykr():
            # linie odpowiadające za autoryzację dostępu do dysku Google przez API Google Drive:
            gauth = GoogleAuth()
            drive = GoogleDrive(gauth)
            # linie 1827-1833 odpowiadają za pobranie i wyświetlenie
            # listy archiwalnych wykresów z ćwiczeń wykonywanych przez pacjenta:
            lista_wykr=list()
            file_list = drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format('1MH62rnEyI0vkZFo3Ii2oMGJ3UrJHbGRG')}).GetList()
            for file in file_list:
                print('title: %s, id: %s' % (file['title'], file['id']))
                lista_wykr.append(file['title'])
            return lista_wykr

        # metoda zagnieżdzona w metodzie open_popup_wykr klasy Historia
        # odpowiedzialna za pobranie z archiwum i wyświetlenie wybranych przez pacjenta
        # wykresów z ćwiczeń:
        def pobranie_wykresów(plik):
            # linie odpowiadające za autoryzację dostępu do dysku Google przez API Google Drive:
            gauth = GoogleAuth()
            drive = GoogleDrive(gauth)
            # linie 1844-1854 odpowiadają za pobranie i wyświetlenie
            # listy archiwalnych wykresów z ćwiczeń wykonywanych przez pacjenta:
            file_list = drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format('1MH62rnEyI0vkZFo3Ii2oMGJ3UrJHbGRG')}).GetList()
            for file in file_list:
                if file['title']==plik:
                    file2 = drive.CreateFile({'id': file['id']})

                    dane=file2.GetContentString(file2).splitlines(True)
                    return dane
        def pobrano():
            global pobrane_wyniki
            pobrane_wyniki=pobranie_wykresów(wybrany_hist_wykres.get())

        # metoda zagnieżdzona w metodzie open_popup_wykr klasy Historia
        # odpowiedzialna za pobranie danych i narysowanie wykresów pobranych z archiwum:
        def wykres(czas,wyniki,tryb):
            # linie 1861-1869 odpowiadają za obróbkę pobranych danych
            wyniki2=wyniki.strip("['']")
            wyniki3=wyniki2.replace("', '"," ")
            wyniki4=wyniki3.split(" ")
            wyn = list()

            for w in wyniki4:
                try:
                    wyn.append(float(w))
                except:
                    pass
            print(wyn)
            try:
                # stworzenie nowego wykresu:
                fig = Figure(figsize=(6,4))
                # skonfigurowanie osi czasu na wykresie:
                t=np.arange(0,float(czas),float(czas)/len(wyn))
                # linie 1878-1889 odpowiadają za wyrysowanie wykresu,
                # a także za ustawienie etykiet osi:
                ax = fig.add_subplot()
                ax.plot(t, wyn)
                ax.set_xlabel('czas [s]')
                # zmiana etykiety osi y w zależności od wybranego wykresu:
                if tryb in range(0, 5):
                    ax.set_ylabel('kąt ugięcia [°]')
                elif tryb == 5:
                    ax.set_ylabel('siła nacisku [g]')
                # linie 1886-1889 odpowiadają za umieszczenie wykresu w oknie z przeglądarką archiwum:
                canvas = FigureCanvasTkAgg(fig, master=top4)  # A tk.DrawingArea.
                canvas.draw()
                canvas.get_tk_widget().grid(column=1, columnspan=3, row=8, rowspan=3, padx=(280, 0), pady=5)
            except:
                # obsługa błędów:
                messagebox.showerror("","Brak danych, sprawdź połączenie z urządzeniem.")
                top4.destroy()



class Pomoc(Frame,App):
    def __init__(self, aplikacja, kontener_stron):
        super().__init__(kontener_stron)

        self.configure(bg="#2d2e2e")

        napis_pomoc = Label(self, text="SKRÓCONA INSTRUKCJA UŻYTKOWANIA APLIKACJI", width=43, font=("Arial", 15, 'bold'),
                             fg="white",
                             bg="#2d2e2e")
        napis_pomoc.grid(column=1, row=2, padx=480, pady=(25, 0))


        napis_pomoc_glowna = Label(self, text="STRONA GŁÓWNA", width=15, font=("Arial", 12), fg="white",
                                bg="#2d2e2e")
        napis_pomoc_glowna.grid(column=1, row=3, padx=(0,780), pady=(15, 0))
        tekst_pomoc_glowna = Label(self, text="To pierwsza strona po zalogowaniu do aplikacji. Można na niej odczytać wiadomość od fizjoterapeuty.", width=77, font=("Arial", 12), fg="white",
                                   bg="#2d2e2e")
        tekst_pomoc_glowna.grid(column=1, row=4, padx=(0, 220), pady=(2, 0))

        napis_pomoc_testy = Label(self, text="WYKONAJ TESTY", width=14, font=("Arial", 12), fg="white",
                                   bg="#2d2e2e")
        napis_pomoc_testy.grid(column=1, row=5, padx=(0, 785), pady=(15, 0))
        tekst_pomoc_testy = Label(self,
                                   text="W tym oknie występuje możliwość wykonania testu ugięcia palców lub siły nacisku dłoni. Do przeprowadzenia testu potrzebna",
                                   width=100, font=("Arial", 12), fg="white",
                                   bg="#2d2e2e")
        tekst_pomoc_testy.grid(column=1, row=6, padx=(0, 55), pady=(2, 0))
        tekst_pomoc_testy1 = Label(self,
                                  text="jest rękawica z czujnikami, którą pacjent wypożycza od fizjoterapeuty i zakłada przed wciśnięciem przycisku “Wykonaj testy”.",
                                  width=100, font=("Arial", 12), fg="white",
                                  bg="#2d2e2e")
        tekst_pomoc_testy1.grid(column=1, row=7, padx=(0, 65), pady=(2, 0))

        napis_pomoc_cwiczenia = Label(self, text="WYKONAJ ĆWICZENIA", width=19, font=("Arial", 12), fg="white",
                                  bg="#2d2e2e")
        napis_pomoc_cwiczenia.grid(column=1, row=8, padx=(0, 753), pady=(15, 0))
        tekst_pomoc_cwiczenia = Label(self,
                                  text="Tutaj pacjent może wykonać ćwiczenia przypisane przez fizjoterapeutę, korzystając z rękawicy. Pacjent wybiera dane ćwiczenie,",
                                  width=100, font=("Arial", 12), fg="white",
                                  bg="#2d2e2e")
        tekst_pomoc_cwiczenia.grid(column=1, row=9, padx=(0, 50), pady=(2, 0))
        tekst_pomoc_cwiczenia1 = Label(self,
                                      text="ogląda film instruktażowy, odczytuje komentarz o sposobie poprawnego wykonania i po założeniu rękawicy wykonuje ćwiczenie.",
                                      width=100, font=("Arial", 12), fg="white",
                                      bg="#2d2e2e")
        tekst_pomoc_cwiczenia1.grid(column=1, row=10, padx=(0, 45), pady=(2, 0))

        napis_pomoc_historia = Label(self, text="HISTORIA", width=10, font=("Arial", 12), fg="white",
                                      bg="#2d2e2e")
        napis_pomoc_historia.grid(column=1, row=11, padx=(0, 840), pady=(15, 0))
        tekst_pomoc_historia = Label(self,
                                      text="W “Historii” można przejrzeć archiwizowane wyniki pomiarów. Występują trzy historie: “Poprzednie wyniki testów” (wyniki",
                                      width=100, font=("Arial", 12), fg="white",
                                      bg="#2d2e2e")
        tekst_pomoc_historia.grid(column=1, row=12, padx=(0, 87), pady=(2, 0))
        tekst_pomoc_historia1 = Label(self,
                                     text="ostatnio wykonanego pomiaru), “Historia kątów ugięć palców i siły nacisku” (wyniki wybranego pomiaru z archiwum), “Historia",
                                     width=100, font=("Arial", 12), fg="white",
                                     bg="#2d2e2e")
        tekst_pomoc_historia1.grid(column=1, row=13, padx=(0, 53), pady=(2, 0))
        tekst_pomoc_historia2 = Label(self,
                                      text="wykresów z ćwiczeń” (wykresy wygenerowane na podstawie danych wyjściowych z czujników rękawicy podczas wykonywania",
                                      width=100, font=("Arial", 12), fg="white",
                                      bg="#2d2e2e")
        tekst_pomoc_historia2.grid(column=1, row=14, padx=(0, 55), pady=(2, 0))
        tekst_pomoc_historia3 = Label(self,
                                      text="danego ćwiczenia).",
                                      width=22, font=("Arial", 12), fg="white",
                                      bg="#2d2e2e")
        tekst_pomoc_historia3.grid(column=1, row=15, padx=(0, 780), pady=(2, 0))

        napis_pomoc_pomoc = Label(self, text="POMOC", width=8, font=("Arial", 12), fg="white",
                                     bg="#2d2e2e")
        napis_pomoc_pomoc.grid(column=1, row=16, padx=(0, 855), pady=(15, 0))
        tekst_pomoc_pomoc = Label(self,
                                     text="Najważniejsze informacje odnośnie obsługi aplikacji oraz dane kontaktowe do fizjoterapeuty.",
                                     width=80, font=("Arial", 12), fg="white",
                                     bg="#2d2e2e")
        tekst_pomoc_pomoc.grid(column=1, row=17, padx=(0, 280), pady=(2, 0))

        napis_pomoc_wyloguj = Label(self, text="WYLOGUJ", width=11, font=("Arial", 12), fg="white",
                                  bg="#2d2e2e")
        napis_pomoc_wyloguj.grid(column=1, row=18, padx=(0, 840), pady=(15, 0))
        tekst_pomoc_wyloguj = Label(self,
                                  text="Okno wylogowania się z aplikacji.",
                                  width=38, font=("Arial", 12), fg="white",
                                  bg="#2d2e2e")
        tekst_pomoc_wyloguj.grid(column=1, row=19, padx=(0, 685), pady=(2, 0))

        napis_pomoc_kontakt = Label(self, text="DANE KONTAKTOWE", width=18, font=("Arial", 10, 'bold'), fg="white",
                                    bg="#2d2e2e")
        napis_pomoc_kontakt.grid(column=1, row=20, padx=(710, 0), pady=(5, 0))
        tekst_pomoc_kontakt = Label(self,
                                    text="Fizjoterapeuta: Jan Kowalski",
                                    width=35, font=("Arial", 10), fg="white",
                                    bg="#2d2e2e")
        tekst_pomoc_kontakt.grid(column=1, row=21, padx=(675, 0), pady=(1, 0))
        tekst_pomoc_kontakt1 = Label(self,
                                    text="Numer telefonu: 123 456 789",
                                    width=32, font=("Arial", 10), fg="white",
                                    bg="#2d2e2e")
        tekst_pomoc_kontakt1.grid(column=1, row=22, padx=(677, 0), pady=(1, 0))
        tekst_pomoc_kontakt2 = Label(self,
                                     text="Adres e-mail: jkowalski@fizjo.com.pl",
                                     width=35, font=("Arial", 10), fg="white",
                                     bg="#2d2e2e")
        tekst_pomoc_kontakt2.grid(column=1, row=23, padx=(635, 0), pady=(1, 0))
        tekst_pomoc_kontakt3 = Label(self,
                                     text="Adres: ul. Rehabilitacyjna 1, 80-402 Gdańsk",
                                     width=40, font=("Arial", 10), fg="white",
                                     bg="#2d2e2e")
        tekst_pomoc_kontakt3.grid(column=1, row=24, padx=(595, 0), pady=(1, 0))


        global otwarcie

        global zamkniecie

        global b2
        b2 = Button(self,
                    image=otwarcie,
                    command=lambda :self.lista_menu(aplikacja),
                    border=0,
                    bg='#2d2e2e',
                    cursor="hand2",
                    activebackground='#2d2e2e')
        b2.place(x=5, y=8)


    def lista_menu(self,aplikacja):


        f1 = Frame(self, width=250, height=700, bg='#01786F')

        f1.place(x=0, y=0)
        b2.place(x=5, y=8)

        def przycisk_menu(x, y, tekst, bcolor, fcolor, komenda):

            przycisk_m = Button(f1, text=tekst,
                                width=27,
                                height=2,
                                fg='white',
                                border=0,
                                bg=fcolor,
                                activeforeground='white',
                                activebackground=bcolor,
                                font=('Arial', 13),
                                cursor="hand2",
                                command=komenda)
            przycisk_m.place(x=x, y=y)
        przycisk_menu(0, 140, 'Wykonaj Testy', '#319177', '#01786F', lambda: [aplikacja.show_frame(aplikacja.Testy),f1.destroy()])
        przycisk_menu(0, 240, 'Wykonaj ćwiczenia', '#319177', '#01786F', lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Cwiczenia)])
        przycisk_menu(0, 340, 'Historia', '#319177', '#01786F', lambda: [aplikacja.show_frame(aplikacja.Historia),f1.destroy()])
        przycisk_menu(0, 440, 'Strona Główna', '#319177', '#01786F', lambda: [aplikacja.show_frame(aplikacja.Zalogowano_Pacjent),f1.destroy()])
        przycisk_menu(0, 540, 'Wyloguj', '#319177', '#01786F', lambda:wyloguj())

        def zamknij():
            f1.destroy()

        def wyloguj():
            f1.destroy()
            pytanie = messagebox.askyesno('Wylogowywanie', 'Czy chcesz się wylogować?')
            if pytanie == True:
                messagebox.showinfo('Wylogowywanie', 'Pomyślnie wylogowano.')
                aplikacja.show_frame(aplikacja.Wybor_profilu)


        Button(f1,
               image=zamkniecie,
               border=0,
               command=zamknij,
               bg='#01786F',
               cursor="hand2",
               activebackground='#01786F').place(x=5, y=10)

class Zalogowano_Fizjo(Frame,App):
    def __init__(self, aplikacja, kontener_stron):
        super().__init__(kontener_stron)

        self.configure(bg="#2d2e2e")
        self.columnconfigure(index=1, weight=2)
        napis = Label(self, text='''Zalogowano pomyślnie.
        Witaj na twoim koncie fizjoterapeuty.''', fg="white",bg="#2d2e2e",  width=35, height=2,font=('Arial', 18))  # ALBO PACJENT!!!
        napis.grid(row=1, column=1, columnspan=1, sticky="NSEW", padx=(100), pady=90)  # trzeba wysrodkowac napis!

        ramka_zegar = Frame(self, highlightthickness=2, highlightbackground="#606060",
                            highlightcolor="#606060")
        self.zegar = Label(ramka_zegar, bg="#2d2e2e", fg="white", font=('Arial', 12, 'bold'))
        ramka_zegar.grid(row=1, column=2, padx=(0, 27), sticky="ne", pady=25)
        self.zegar.grid(row=1, column=2)

        global otwarcie

        global zamkniecie

        global b2
        b2 = Button(self,
                    image=otwarcie,
                    command=lambda :[self.lista_menu(aplikacja),print(App.konto["login"])],
                    border=0,
                    bg='#2d2e2e',
                    activebackground='#2d2e2e',
                    cursor = "hand2")
        b2.place(x=5, y=8)
        self.czas()
    def lista_menu(self,aplikacja):

        f1 = Frame(self, width=250, height=700, bg='#01786F')
        f1.place(x=0, y=0)
        b2.place(x=5, y=8)

        def przycisk_menu(x, y, tekst, bcolor, fcolor, komenda):

            przycisk_m = Button(f1, text=tekst,
                                width=27,
                                height=2,
                                fg='white',
                                border=0,
                                bg=fcolor,
                                activeforeground='white',
                                activebackground=bcolor,
                                font=('Arial', 13),
                                cursor="hand2",
                                command=komenda)
            przycisk_m.place(x=x, y=y)

        przycisk_menu(0, 140, 'Wgraj filmy ','#319177', '#01786F', lambda : [f1.destroy(),aplikacja.show_frame(aplikacja.Wgraj_Filmy)])
        przycisk_menu(0, 240, 'Przypisz ćwiczenia', '#319177', '#01786F', lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Przypisz_Ćwiczenia)])
        przycisk_menu(0, 340, 'Odbierz wyniki', '#319177', '#01786F', lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Odbierz_Wyniki)])
        przycisk_menu(0, 440, 'Zarejestruj pacjenta', '#319177', '#01786F', lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Zarejestruj_Pacjenta)])
        przycisk_menu(0, 540, 'Wyloguj', '#319177', '#01786F', lambda:wyloguj())

        def zamknij():
            f1.destroy()

        def wyloguj():
            f1.destroy()
            pytanie = messagebox.askyesno('Wylogowywanie', 'Czy chcesz się wylogować?')
            if pytanie == True:
                messagebox.showinfo('Wylogowywanie', 'Pomyślnie wylogowano.')
                aplikacja.show_frame(aplikacja.Wybor_profilu)


        Button(f1,
               image=zamkniecie,
               border=0,
               command=zamknij,
               bg='#01786F',
               cursor="hand2",
               activebackground='#01786F').place(x=5, y=10)

class Wgraj_Filmy(Frame,App):
    def __init__(self, aplikacja, kontener_stron):
        super().__init__(kontener_stron)

        self.configure(bg="#2d2e2e")
        napis_filmik = Label(self, text="WGRYWANIE FILMU INSTRUKTAŻOWEGO", width=34, font=("Arial", 15, 'bold'),
                             fg="white",
                             bg="#2d2e2e")
        napis_filmik.grid(column=1, row=2, padx=500, pady=(25, 0))

        napis_komentarz = Label(self, text="Dodaj komentarz dla pacjentów:", width=27, font=("Arial", 12), fg="white",
                               bg="#2d2e2e")
        napis_komentarz.grid(column=1, row=6, padx=(0, 0), pady=(25, 0))

        okno_komentarz = Text(self, font=('Arial', 14))
        okno_komentarz.grid(row=7, column=1, columnspan=1, padx=(20, 20), pady=(10, 10))
        okno_komentarz.configure(state=NORMAL, width=50, height=7, fg='black', bg='white')

        napis_cwiczenie = Label(self, text="Wprowadź nazwę ćwiczenia:", width=22, font=("Arial", 12), fg="white",
                                bg="#2d2e2e")
        napis_cwiczenie.grid(column=1, row=3, padx=(0, 0), pady=(15, 0))

        napis_cwiczenie_2 = Label(self,
                                  text="( Jeśli nazwa jest kilkuczłonowa, oddziel poszczególne słowa symbolem: _ )",
                                  width=55, font=("Arial", 10), fg="white",
                                  bg="#2d2e2e")
        napis_cwiczenie_2.grid(column=1, row=4, padx=(0, 0), pady=(0, 0))

        okno_cwiczenie = Entry(self, width=35, font=('Arial', 12))
        okno_cwiczenie.grid(row=5, column=1, columnspan=1, padx=(0, 0), pady=(10, 0))



        przycisk_wgraj_film = Button(self, text="Wgraj do bazy danych", fg="white", bg="#01786F", width=18, height=1,
                                     font=('Arial', 12), activebackground="#319177", activeforeground="white",
                                     cursor="hand2",command=lambda:[self.baza_wgrywanie(str(okno_cwiczenie.get()),str(okno_komentarz.get("1.0",'end-1c'))),self.wgranie_filmu(str(okno_cwiczenie.get()))])
        przycisk_wgraj_film.grid(row=10, column=1, columnspan=1, padx=(0, 0), pady=20)

        global otwarcie

        global zamkniecie

        global b2
        b2 = Button(self,
                    image=otwarcie,
                    command=lambda :self.lista_menu(aplikacja),
                    border=0,
                    bg='#2d2e2e',
                    cursor="hand2",
                    activebackground='#2d2e2e')
        b2.place(x=5, y=8)

    # metoda klasy Wgraj_filmy odpowiadająca za przesłanie przesłanie nowego filmu na dysk google:
    def wgranie_filmu(self,nazwa_cwiczenia):
        # linijka ta wywołuje okno dialogowe wyboru filmu z komputera fizjoterapeuty:
        file = fd.askopenfilename()
        # linie odpowiedzialne za autoryzację dostępu do dysku Google przez API Google Drive:
        gauth = GoogleAuth()
        drive = GoogleDrive(gauth)
        # utworzenie nowego pliku na dysku Google:
        gfile = drive.CreateFile({'title':nazwa_cwiczenia+".mp4",'parents': [{'id': '1E_nQtJc0UyrtyYvkz04pA-pyVR5ZRjKs'}]})
        # wgranie zawartości pliku z komputera fizjoterapeuty na dysk Google:
        gfile.SetContentFile(file)
        gfile.Upload()

    def lista_menu(self, aplikacja):
        # global f1

        f1 = Frame(self, width=250, height=700, bg='#01786F')
        f1.place(x=0, y=0)
        b2.place(x=5, y=8)

        def przycisk_menu(x, y, tekst, bcolor, fcolor, komenda):
            przycisk_m = Button(f1, text=tekst,
                                width=27,
                                height=2,
                                fg='white',
                                border=0,
                                bg=fcolor,
                                activeforeground='white',
                                activebackground=bcolor,
                                font=('Arial', 13),
                                cursor="hand2",
                                command=komenda)
            przycisk_m.place(x=x, y=y)

        przycisk_menu(0, 140, 'Strona Główna ', '#319177', '#01786F',
                      lambda: [f1.destroy(), aplikacja.show_frame(aplikacja.Zalogowano_Fizjo)])
        przycisk_menu(0, 240, 'Przypisz ćwiczenia', '#319177', '#01786F',
                      lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Przypisz_Ćwiczenia)])
        przycisk_menu(0, 340, 'Odbierz wyniki', '#319177', '#01786F',
                      lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Odbierz_Wyniki)])
        przycisk_menu(0, 440, 'Zarejestruj pacjenta', '#319177', '#01786F',
                      lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Zarejestruj_Pacjenta)])
        przycisk_menu(0, 540, 'Wyloguj', '#319177', '#01786F',
                      lambda: wyloguj())

        def zamknij():
            f1.destroy()

        def wyloguj():
            f1.destroy()
            pytanie = messagebox.askyesno('Wylogowywanie', 'Czy chcesz się wylogować?')
            if pytanie == True:
                messagebox.showinfo('Wylogowywanie', 'Pomyślnie wylogowano.')
                aplikacja.show_frame(aplikacja.Wybor_profilu)


        Button(f1,
               image=zamkniecie,
               border=0,
               command=zamknij,
               bg='#01786F',
               cursor="hand2",
               activebackground='#01786F').place(x=5, y=10)

    # metoda klasy Wgraj_filmy odpowiadająca za przesłanie danych do nowego filmu do ćwiczenia:
    def baza_wgrywanie(self,nazwa_cwiczenia,kom):
            try:
                # wprowadzenie danych używanej bazy danych i otwarcie jej:
                mysqldb2 = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="login")
                # sprawdzenie połączenia:
                print(mysqldb2.connection_id)
                # tworzenie zmiennej tymczasowej użwyanej do pobrania wyniku zapytania do bazy danych:
                mycursor2 = mysqldb2.cursor()
                # zapytanie(kwerenda) sql wprowadzające dane do bazy:
                sql = "INSERT into cwiczenia (nazwa_cwiczenia, komentarz) VALUES (%s,%s) "
                # wartości wysyłane do bazy danych:
                val=(nazwa_cwiczenia,kom)
                # wykonanie zapytania sql do bazy danych:
                mycursor2.execute(sql,val)
                try:
                    # zatwierdzenie zmian dokonanych przez zapytanie SQL:
                    mysqldb2.commit()
                    print("Nowe ćwiczenie i film dodano pomyślnie")
                except:
                       #obsługa błędów:
                       messagebox.showinfo("", "Niepowodzenie w dodaniu filmu")
            except mysql.connector.Error:
                messagebox.showinfo("", "Błąd przy połączeniu")
            except:
                messagebox.showinfo("", "Błąd")
            else:
                # zamknięcie otwartej bazy danych:
                mysqldb2.close()

class Przypisz_Ćwiczenia(Frame,App):
    def __init__(self, aplikacja, kontener_stron):
        super().__init__(kontener_stron)

        self.configure(bg="#2d2e2e")
        napis_przypisanie = Label(self, text="PRZYPISANIE ĆWICZENIA PACJENTOWI", width=32, font=("Arial", 15, 'bold'),
                                  fg="white",
                                  bg="#2d2e2e")
        napis_przypisanie.grid(column=1, row=2, padx=520, pady=(25, 0))



        napis_cwiczenie_3 = Label(self, text="Wprowadź nazwę ćwiczenia:", width=22, font=("Arial", 12), fg="white",
                                  bg="#2d2e2e")
        napis_cwiczenie_3.grid(column=1, row=5, padx=(0, 0), pady=(15, 0))

        napis_cwiczenie_4 = Label(self,
                                  text="( Jeśli nazwa jest kilkuczłonowa, oddziel poszczególne słowa symbolem: _ )",
                                  width=55, font=("Arial", 10), fg="white",
                                  bg="#2d2e2e")
        napis_cwiczenie_4.grid(column=1, row=6, padx=(0, 0), pady=(0, 0))

        okno_cwiczenie_1 = Entry(self, width=35, font=('Arial', 12))
        okno_cwiczenie_1.grid(row=7, column=1, columnspan=1, padx=(0, 0), pady=(10, 0))

        napis_indeks = Label(self, text="Podaj indeks pacjenta:", width=18, font=("Arial", 12), fg="white",
                             bg="#2d2e2e")
        napis_indeks.grid(column=1, row=8, padx=(0, 0), pady=(15, 0))

        okno_indeks = Entry(self, width=12, font=('Arial', 12))
        okno_indeks.grid(row=9, column=1, columnspan=1, padx=(0, 0), pady=(10, 0))

        napis_komentarz = Label(self, text="Dodaj komentarz dla pacjenta:", width=23, font=("Arial", 12), fg="white",
                                bg="#2d2e2e")
        napis_komentarz.grid(column=1, row=10, padx=(0, 0), pady=(15, 0))

        napis_komentarz_2 = Label(self, text="( Pole nieobowiązkowe )",
                                  width=17, font=("Arial", 10), fg="white",
                                  bg="#2d2e2e")
        napis_komentarz_2.grid(column=1, row=11, padx=(0, 0), pady=(0, 0))

        okno_komentarz = Entry(self, width=55, font=('Arial', 12))
        okno_komentarz.grid(row=12, column=1, columnspan=1, padx=(0, 0), pady=(10, 0))

        przycisk_wyslij_pacjentowi = Button(self, text="Wyślij do pacjenta", fg="white", bg="#01786F", width=15,
                                            height=1,
                                            font=('Arial', 12), activebackground="#319177", activeforeground="white",
                                            cursor="hand2",command=lambda:self.baza_przypisanie(str(okno_cwiczenie_1.get()),str(okno_indeks.get()),str(okno_komentarz.get())))
        przycisk_wyslij_pacjentowi.grid(row=13, column=1, columnspan=1, padx=(0, 0), pady=20)

        global otwarcie

        global zamkniecie

        global b2
        b2 = Button(self,
                    image=otwarcie,
                    command=lambda :self.lista_menu(aplikacja),
                    border=0,
                    bg='#2d2e2e',
                    cursor="hand2",
                    activebackground='#2d2e2e')
        b2.place(x=5, y=8)

    def lista_menu(self, aplikacja):

        f1 = Frame(self, width=250, height=700, bg='#01786F')
        f1.place(x=0, y=0)
        b2.place(x=5, y=8)

        def przycisk_menu(x, y, tekst, bcolor, fcolor, komenda):
            przycisk_m = Button(f1, text=tekst,
                                width=27,
                                height=2,
                                fg='white',
                                border=0,
                                bg=fcolor,
                                activeforeground='white',
                                activebackground=bcolor,
                                font=('Arial', 13),
                                cursor="hand2",
                                command=komenda)
            przycisk_m.place(x=x, y=y)

        przycisk_menu(0, 140, 'Wgraj filmy ', '#319177', '#01786F',
                      lambda: [f1.destroy(), aplikacja.show_frame(aplikacja.Wgraj_Filmy)])
        przycisk_menu(0, 240, 'Strona Główna', '#319177', '#01786F',
                      lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Zalogowano_Fizjo)])
        przycisk_menu(0, 340, 'Odbierz wyniki', '#319177', '#01786F',
                      lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Odbierz_Wyniki)])
        przycisk_menu(0, 440, 'Zarejestruj pacjenta', '#319177', '#01786F',
                      lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Zarejestruj_Pacjenta)])
        przycisk_menu(0, 540, 'Wyloguj', '#319177', '#01786F',
                      lambda: wyloguj())

        def zamknij():
            f1.destroy()

        def wyloguj():
            f1.destroy()
            pytanie = messagebox.askyesno('Wylogowywanie', 'Czy chcesz się wylogować?')
            if pytanie == True:
                messagebox.showinfo('Wylogowywanie', 'Pomyślnie wylogowano.')
                aplikacja.show_frame(aplikacja.Wybor_profilu)


        Button(f1,
               image=zamkniecie,
               border=0,
               command=zamknij,
               bg='#01786F',
               cursor="hand2",
               activebackground='#01786F').place(x=5, y=10)

    # metoda klasy Przypisz_Ćwicznenia odpowiadająca za przypisanie pacjentowi wskazanych ćwiczeń:
    def baza_przypisanie(self, nazwa, login_pacjent,kom):
        nazwa_cw = nazwa
        login = login_pacjent
        try:
            # wprowadzenie danych używanej bazy danych i otwarcie jej:
            mysqldb3 = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="login")
            # sprawdzenie połączenia:
            print(mysqldb3.connection_id)
            # tworzenie zmiennej tymczasowej użwyanej do pobrania wyniku zapytania do bazy danych:
            mycursor3 = mysqldb3.cursor()
            # zapytanie(kwerenda) sql aktualizujące dane w bazie:
            sql = "UPDATE pacjenci_dane SET przypisane_cwiczenia = %s, komentarz=%s WHERE nr = %s"
            # wartości wysyłane do bazy danych:
            val = (nazwa_cw,kom ,login)
            # wykonanie zapytania sql do bazy danych:
            mycursor3.execute(sql, val)
            try:
                # zatwierdzenie zmian dokonanych przez zapytanie SQL:
                mysqldb3.commit()
                messagebox.showinfo("","Przypisano ćwiczenia do pacjenta")
            except:
                # obsługa błędów:
                messagebox.showinfo("", "Niepowodzenie w przypisywaniu ćwiczeń")
        except mysql.connector.Error:
            messagebox.showinfo("", "Błąd przy połączeniu")
        except:
            messagebox.showinfo("", "Błąd")
        else:
            # zamknięcie otwartej bazy danych:
            mysqldb3.close()

class Odbierz_Wyniki(Frame,App):
    def __init__(self, aplikacja, kontener_stron):
        super().__init__(kontener_stron)

        self.configure(bg="#2d2e2e")
        napis_odebranie = Label(self, text="ODEBRANIE WYNIKÓW POMIARÓW OD PACJENTA", width=41,
                                font=("Arial", 15, 'bold'),
                                fg="white",
                                bg="#2d2e2e")
        napis_odebranie.grid(column=1, row=2, padx=480, pady=(25, 0))

        napis_indeks_1 = Label(self, text="Podaj indeks pacjenta:", width=18, font=("Arial", 12), fg="white",
                               bg="#2d2e2e")
        napis_indeks_1.grid(column=1, row=3, padx=(0, 0), pady=(15, 0))

        okno_indeks_1 = Entry(self, width=12, font=('Arial', 12))
        okno_indeks_1.grid(row=4, column=1, columnspan=1, padx=(0, 0), pady=(10, 0))
        wyniki=list()
        Ostatnie=Button(self,text="Poprzednie wyniki testów", fg="white", bg="#01786F", width=23, height=2,
                         font=('Arial', 13),
                         activebackground="#319177", activeforeground="white", cursor="hand2", command=lambda:pobranie_indeksu_ostatnie())
        Ostatnie.place(x=290, y=300)
        his_kat = Button(self, text="Historia kątów ugięć palców i siły nacisku", fg="white", bg="#01786F", width=36,
                         height=2,
                         font=('Arial', 13),
                         activebackground="#319177", activeforeground="white", cursor="hand2", command=lambda:pobranie_indeksu_his_kat())
        his_kat.place(x=544, y=300)
        wykresy = Button(self, text="Historia wykresów z ćwiczeń", fg="white", bg="#01786F", width=26, height=2,
                         font=('Arial', 13),
                         activebackground="#319177", activeforeground="white", cursor="hand2", command=lambda:pobranie_indeksu_wykresy())
        wykresy.place(x=915, y=300)

        def pobranie_indeksu_ostatnie():
            indeks_pacjenta=okno_indeks_1.get()
            if indeks_pacjenta=="":
                messagebox.showinfo("","Proszę o podanie indeksu pacjenta")
            else:
                self.open_popup_poprzednie_wyniki(indeks_pacjenta)
        def pobranie_indeksu_his_kat():
            indeks_pacjenta=okno_indeks_1.get()
            if indeks_pacjenta=="":
                messagebox.showinfo("","Proszę o podanie indeksu pacjenta")
            else:
                self.open_popup_historia(indeks_pacjenta)
        def pobranie_indeksu_wykresy():
            indeks_pacjenta=okno_indeks_1.get()
            if indeks_pacjenta=="":
                messagebox.showinfo("","Proszę o podanie indeksu pacjenta")
            else:
                self.open_popup_wykr(indeks_pacjenta)
        global otwarcie

        global zamkniecie

        global b2
        b2 = Button(self,
                    image=otwarcie,
                    command=lambda :self.lista_menu(aplikacja),
                    border=0,
                    bg='#2d2e2e',
                    cursor="hand2",
                    activebackground='#2d2e2e')
        b2.place(x=5, y=8)


    def lista_menu(self, aplikacja):

        f1 = Frame(self, width=250, height=700, bg='#01786F')
        f1.place(x=0, y=0)
        b2.place(x=5, y=8)

        def przycisk_menu(x, y, tekst, bcolor, fcolor, komenda):
            przycisk_m = Button(f1, text=tekst,
                                width=27,
                                height=2,
                                fg='white',
                                border=0,
                                bg=fcolor,
                                activeforeground='white',
                                activebackground=bcolor,
                                font=('Arial', 13),
                                cursor="hand2",
                                command=komenda)
            przycisk_m.place(x=x, y=y)

        przycisk_menu(0, 140, 'Wgraj filmy ', '#319177', '#01786F',
                      lambda: [f1.destroy(), aplikacja.show_frame(aplikacja.Wgraj_Filmy)])
        przycisk_menu(0, 240, 'Przypisz ćwiczenia', '#319177', '#01786F',
                      lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Przypisz_Ćwiczenia)])
        przycisk_menu(0, 340, 'Strona Główna', '#319177', '#01786F',
                      lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Zalogowano_Fizjo)])
        przycisk_menu(0, 440, 'Zarejestruj pacjenta', '#319177', '#01786F',
                      lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Zarejestruj_Pacjenta)])
        przycisk_menu(0, 540, 'Wyloguj', '#319177', '#01786F',
                      lambda: wyloguj())

        def zamknij():
            f1.destroy()

        def wyloguj():
            f1.destroy()
            pytanie = messagebox.askyesno('Wylogowywanie', 'Czy chcesz się wylogować?')
            if pytanie == True:
                messagebox.showinfo('Wylogowywanie', 'Pomyślnie wylogowano.')
                aplikacja.show_frame(aplikacja.Wybor_profilu)


        Button(f1,
               image=zamkniecie,
               border=0,
               command=zamknij,
               bg='#01786F',
               cursor="hand2",
               activebackground='#01786F').place(x=5, y=10)

    def open_popup_poprzednie_wyniki(self,indeks):
        top3=Toplevel()
        top3.geometry("1200x700")
        top3.configure( bg= "#2d2e2e")
        top3.resizable(width=False, height=False)
        self.indeks=indeks

        napis_poprzednie = Label(top3, text="ODEBRANIE NAJNOWSZYCH WYNIKÓW POMIARU OD PACJENTA", width=53,
                                font=("Arial", 15, 'bold'),
                                fg="white",
                                bg="#2d2e2e")
        napis_poprzednie.grid(column=1, row=2, padx=290, pady=(25, 0))


        przycisk_odbierz_wyniki = Button(top3, text="Odbierz wyniki", fg="white", bg="#01786F", width=13, height=1,
                                         font=('Arial', 12), activebackground="#319177", activeforeground="white",
                                         cursor="hand2",
                                         command=lambda: [wyswietlenie_wynikow(self.baza_odb_poprzednie(self.indeks))])
        przycisk_odbierz_wyniki.grid(row=3, column=1, columnspan=1, padx=(0, 0), pady=20)
        wyniki_1 = Label(top3, text="Wyniki pomiarów :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        wyniki_1.grid(column=1, row=4, padx=(0, 0), pady=(25, 0))

        napis_kciuk_1 = Label(top3, text="Kciuk :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_kciuk_1.grid(column=1, row=5, padx=(0, 180), pady=(15, 0))
        okno_kciuk_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_kciuk_1.grid(row=5, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))
        # tu insert?
        napis_wskazujacy_1 = Label(top3, text="Wskazujący :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_wskazujacy_1.grid(column=1, row=6, padx=(0, 180), pady=(15, 0))
        okno_wskazujacy_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_wskazujacy_1.grid(row=6, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))
        napis_srodkowy_1 = Label(top3, text="Środkowy :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_srodkowy_1.grid(column=1, row=7, padx=(0, 180), pady=(15, 0))
        okno_srodkowy_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_srodkowy_1.grid(row=7, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))
        napis_serdeczny_1 = Label(top3, text="Serdeczny :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_serdeczny_1.grid(column=1, row=8, padx=(0, 180), pady=(15, 0))
        okno_serdeczny_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_serdeczny_1.grid(row=8, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))
        napis_maly_1 = Label(top3, text="Mały :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_maly_1.grid(column=1, row=9, padx=(0, 180), pady=(15, 0))
        okno_maly_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_maly_1.grid(row=9, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))
        napis_sila_nacisku_1 = Label(top3, text="Siła nacisku :", width=14, font=("Arial", 12), fg="white",
                                     bg="#2d2e2e")
        napis_sila_nacisku_1.grid(column=1, row=10, padx=(0, 180), pady=(15, 0))
        okno_sila_nacisku_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_sila_nacisku_1.grid(row=10, column=1, columnspan=1, padx=(100, 0), pady=(10, 0))

        #metoda zagnieżdżona w metodzie open_popup_poprzednie_wyniki klasy Odbierz_wyniki
        def wyswietlenie_wynikow(wyniki):
            wynik = wyniki[0]
            print(wynik)
            ugiecie = wynik[0]
            #w linijkach 2610-2620 następuje obróbka i wpisanie w odpowiednie okienka danych
            # z najnowszych wyników testów pacjenta,
            #które zostały uprzednio pobrane z bazy danych
            ugiecie_oddzielone = ugiecie.splitlines(True)
            nacisk = wynik[1]
            okno_kciuk_1.insert(0, ugiecie_oddzielone[0])
            okno_wskazujacy_1.insert(0, ugiecie_oddzielone[1])
            okno_srodkowy_1.insert(0, ugiecie_oddzielone[2])
            okno_serdeczny_1.insert(0, ugiecie_oddzielone[3])
            okno_maly_1.insert(0, ugiecie_oddzielone[4])
            okno_sila_nacisku_1.insert(0, nacisk)

    def open_popup_historia(self,indeks):
        top3=Toplevel()
        top3.geometry("1200x700")
        top3.configure( bg= "#2d2e2e")
        top3.resizable(width=False, height=False)
        self.indeks = indeks
        wybrane_hist_ugiecie = StringVar()
        historyczne_ugiecia = ttk.Combobox(top3, width=21, textvariable=wybrane_hist_ugiecie, font=("Arial", 11))
        wybrany_hist_nacisk = StringVar()
        historyczne_naciski = ttk.Combobox(top3, width=20, textvariable=wybrany_hist_nacisk, font=("Arial", 11))
        przycisk_odbierz_hist_wyniki_ugiecie = Button(top3, text="Załaduj historyczne wyniki testów ugięcia", fg="white", bg="#01786F", width=32, height=1,
                                         font=('Arial', 12), activebackground="#319177", activeforeground="white",
                                         cursor="hand2",
                                         command=lambda: [historyczne_ugiecia.configure(values=lista_his_ug()),historyczne_ugiecia.current(0)])
        przycisk_odbierz_hist_wyniki_nacisk = Button(top3, text="Załaduj historyczne wyniki testów nacisku", fg="white",
                                         bg="#01786F", width=32, height=1,
                                         font=('Arial', 12), activebackground="#319177", activeforeground="white",
                                         cursor="hand2",
                                         command=lambda: [historyczne_naciski.configure(values=lista_his_nac()),historyczne_naciski.current(0)])





        wyniki_1 = Label(top3, text="PRZEGLĄD HISTORII POMIARÓW", width=28, font=("Arial", 15, 'bold'), fg="white", bg="#2d2e2e")
        wyniki_1.grid(column=1, row=2, padx=(400, 0), pady=(25, 0))
        przycisk_odbierz_hist_wyniki_ugiecie.grid(row=3, column=1, columnspan=1, padx=(400, 0), pady=(20,5))
        historyczne_ugiecia.grid(column=1, row=4, padx=(400,0))
        przycisk_zatw_ug = Button(top3, text="Zatwierdź",
                                                      fg="white", bg="#01786F", width=11, height=1,
                                                      font=('Arial', 12), activebackground="#319177",
                                                      activeforeground="white",
                                                      cursor="hand2",
                                                      command=lambda:[wyswietlenie_wynikow_ug(wybrane_hist_ugiecie.get())])
        przycisk_zatw_nac = Button(top3, text="Zatwierdź",
                                  fg="white", bg="#01786F", width=11, height=1,
                                  font=('Arial', 12), activebackground="#319177",
                                  activeforeground="white",
                                  cursor="hand2",
                                  command=lambda: [wyswietlenie_wynikow_nac(wybrany_hist_nacisk.get())])
        przycisk_zatw_ug.grid(column=1, row=5, padx=(400, 0), pady=(10,0))

        napis_kciuk_1 = Label(top3, text="Kciuk :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_kciuk_1.grid(column=1, row=6, padx=(365, 180), pady=(15, 0))
        okno_kciuk_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_kciuk_1.grid(row=6, column=1, columnspan=1, padx=(450, 0), pady=(10, 0))
        napis_wskazujacy_1 = Label(top3, text="Wskazujący :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_wskazujacy_1.grid(column=1, row=7, padx=(355, 180), pady=(15, 0))
        okno_wskazujacy_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_wskazujacy_1.grid(row=7, column=1, columnspan=1, padx=(450, 0), pady=(10, 0))
        napis_srodkowy_1 = Label(top3, text="Środkowy :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_srodkowy_1.grid(column=1, row=8, padx=(355, 180), pady=(15, 0))
        okno_srodkowy_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_srodkowy_1.grid(row=8, column=1, columnspan=1, padx=(450, 0), pady=(10, 0))
        napis_serdeczny_1 = Label(top3, text="Serdeczny :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_serdeczny_1.grid(column=1, row=9, padx=(355, 180), pady=(15, 0))
        okno_serdeczny_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_serdeczny_1.grid(row=9, column=1, columnspan=1, padx=(450, 0), pady=(10, 0))
        napis_maly_1 = Label(top3, text="Mały :", width=14, font=("Arial", 12), fg="white", bg="#2d2e2e")
        napis_maly_1.grid(column=1, row=10, padx=(365, 180), pady=(15, 0))
        okno_maly_1 = Entry(top3, width=18, font=('Arial', 12))
        okno_maly_1.grid(row=10, column=1, columnspan=1, padx=(450, 0), pady=(10, 0))
        napis_sila_nacisku_1 = Label(top3, text="Siła nacisku :", width=14, font=("Arial", 12), fg="white",
                                     bg="#2d2e2e")
        przycisk_odbierz_hist_wyniki_nacisk.grid(row=11, column=1, columnspan=1, padx=(400, 0), pady=(30,5))
        historyczne_naciski.grid(column=1, row=12, padx=(400,0))
        przycisk_zatw_nac.grid(column=1, row=13, padx=(400,0), pady=(10,0))
        napis_sila_nacisku_1.grid(column=1, row=14, padx=(355, 180), pady=(15, 0))
        okno_sila_nacisku_1 = Entry(top3, width=18, font=('Arial', 13))
        okno_sila_nacisku_1.grid(row=14, column=1, columnspan=1, padx=(450, 0), pady=(10, 0))
        #metoda zagnieżdzona w metodzie open_popup_historia klasy Odbierz_wyniki
        # odpowiedzialna za wyświetlenie archiwum testów ugięcia palców pacjenta:
        def lista_his_ug():
            #linie odpowiadające za autoryzację dostępu do dysku Google przez API Google Drive:
            gauth = GoogleAuth()
            drive = GoogleDrive(gauth)
            # linie 2699-2706 odpowiadają za pobranie i wyświetlenie listy testów ugięcia palców z archiwum
            lista_ugiec=list()
            file_list = drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format('1ok5Glz4vepxv1_Ys3QXouYxDOlA1DZq7')}).GetList()
            for file in file_list:
                if str(self.indeks) in file['title']:
                    print('title: %s, id: %s' % (file['title'], file['id']))
                    lista_ugiec.append(file['title'])
            return lista_ugiec

        # metoda zagnieżdzona w metodzie open_popup_historia klasy Odbierz_wyniki
        # odpowiedzialna za wyświetlenie archiwum testów siły nacisku dłoni pacjenta:
        def lista_his_nac():
            # linie odpowiedzialne za autoryzację dostępu do dysku Google przez API Google Drive:
            gauth = GoogleAuth()
            drive = GoogleDrive(gauth)
            #linie 2715-2722 odpowiadają za pobranie i wyświetlenie listy testów siły nacisku dłoni z archiwum
            lista_naciskow=list()
            file_list = drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format('1pKp-OoLbrWApdstm9bIcmFLGQWAJkfL9')}).GetList()
            for file in file_list:
                if str(self.indeks) in file['title']:
                    print('title: %s, id: %s' % (file['title'], file['id']))
                    lista_naciskow.append(file['title'])
            return lista_naciskow

        # metoda zagnieżdzona w metodzie open_popup_historia klasy Odbierz_wyniki
        # odpowiedzialna za pobranie z archiwum i wyświetlenie wybranych przez fizjoterapeutę
        # wyników ugięcia palców pacjenta:
        def wyswietlenie_wynikow_ug(plik):
            # linie odpowiedzialne za autoryzację dostępu do dysku Google przez API Google Drive:
            gauth = GoogleAuth()
            drive = GoogleDrive(gauth)
            #linie 2734-2746 odpowiadają za pobranie z archiwum i wyświetlenie
            # wybranych przez fizjoterapeutę
            #wyników ugięcia palców:
            file_list = drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format('1ok5Glz4vepxv1_Ys3QXouYxDOlA1DZq7')}).GetList()
            for file in file_list:
                if file['title']==plik:
                    file2 = drive.CreateFile({'id': file['id']})

                    ugiecia=file2.GetContentString(file2).splitlines(True)
                    print(ugiecia)
                    okno_kciuk_1.insert(0, ugiecia[0]+",")
                    okno_wskazujacy_1.insert(0, ugiecia[1]+",")
                    okno_srodkowy_1.insert(0, ugiecia[2]+",")
                    okno_serdeczny_1.insert(0, ugiecia[3]+",")
                    okno_maly_1.insert(0, ugiecia[4]+",")

        # metoda zagnieżdzona w metodzie open_popup_historia klasy Odbierz_wyniki
        # odpowiedzialna za pobranie z archiwum i wyświetlenie wybranych przez fizjoterapeutę
        # wyników siły nacisku dłoni pacjenta:
        def wyswietlenie_wynikow_nac(plik):
            # linie odpowiedzialne za autoryzację dostępu do dysku Google przez API Google Drive:
            gauth = GoogleAuth()
            drive = GoogleDrive(gauth)
            # linie 2758-2764 odpowiadają za pobranie z archiwum i wyświetlenie
            # wybranych przez fizjoterapeutę
            # wyników siły nacisku dłoni:
            file_list = drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format('1pKp-OoLbrWApdstm9bIcmFLGQWAJkfL9')}).GetList()
            for file in file_list:
                if file['title']==plik:
                    file2 = drive.CreateFile({'id': file['id']})
                    nacisk=file2.GetContentString(file2)
                    okno_sila_nacisku_1.insert(0, nacisk+",")

    #metoda klasy Odbierz_wyniki odpowiadająca za pobranie najnowyszch wyników testów pacjenta z BD
    def baza_odb_poprzednie(self,indeks):
        ind=str(indeks)
        try:
            # wprowadzenie danych używanej bazy danych i otwarcie jej:
            mysqldb_odb=mysql.connector.connect(host="localhost",user="root",passwd="1234",database="login")
            # tworzenie zmiennej tymczasowej użwyanej do pobrania wyniku zapytania do bazy danych:
            mycursor_odb=mysqldb_odb.cursor()
            # zapytanie(kwerenda) sql pobierające pożądane dane z bazy:
            sql="SELECT test_ugiecia,test_nacisku from pacjenci_dane where nr= %s"
            # wykonanie zapytania sql do bazy danych:
            mycursor_odb.execute(sql,[ind])
            #zatwierdzenie pobrania danych z bazy:
            results=mycursor_odb.fetchall()
            if results:
                print(results)
                return results

            else:
                #obsługa błędów:
                messagebox.showinfo("","Nieprawidłowy login lub hasło")

        except mysql.connector.Error:
            messagebox.showinfo("", "Błąd przy połączeniu")
        except:
            messagebox.showinfo("", "Błąd")
        else:
            # zamknięcie otwartej bazy danych:
            mysqldb_odb.close()

    def open_popup_wykr(self,indeks):
        data = datetime.date.today()

        top4=Toplevel()
        top4.geometry("1200x700")
        top4.configure( bg= "#2d2e2e")
        top4.resizable(width=False, height=False)
        self.indeks=indeks
        wybrany_hist_wykres = StringVar()
        historyczne_wykresy = ttk.Combobox(top4, width=20, textvariable=wybrany_hist_wykres, font=("Arial", 11))
        przycisk_odbierz_hist_wykresy = Button(top4, text="Załaduj historyczne wyniki testów",
                                                      fg="white", bg="#01786F", width=27, height=1,
                                                      font=('Arial', 12), activebackground="#319177",
                                                      activeforeground="white",
                                                      cursor="hand2",
                                                      command=lambda: [
                                                          historyczne_wykresy.configure(values=lista_his_wykr()),
                                                          historyczne_wykresy.current(0)])
        global pobrane_wyniki
        pobrane_wyniki=list()
        czas=list()
        global pomiary
        pomiary=""
        wyniki_1 = Label(top4, text="PRZEGLĄD HISTORII WYKRESÓW", width=28, font=("Arial", 15, 'bold'), fg="white",
                         bg="#2d2e2e")
        wyniki_1.grid(column=1, row=2, padx=(400, 0), pady=(25, 10))
        przycisk_odbierz_hist_wykresy.grid(row=3, column=1, columnspan=1, padx=(400, 0), pady=5)
        historyczne_wykresy.grid(column=1, row=4, padx=(400, 0))
        przycisk_zatw_wykr = Button(top4, text="Zatwierdź",
                                  fg="white", bg="#01786F", width=11, height=1,
                                  font=('Arial', 12), activebackground="#319177",
                                  activeforeground="white",
                                  cursor="hand2",
                                  command=lambda: [pobrano(),czas.append(pobrane_wyniki[0].lstrip("[")),print(czas[0]),print(pobrane_wyniki[0]),print(pobrane_wyniki[1])])
        przycisk_zatw_wykr.grid(row=5,column=1, padx=(400, 0), pady=(5,0))

        wybrany_palec_lub_sila = StringVar()
        wykresy_katow_i_sily = ttk.Combobox(top4, width=20, textvariable=wybrany_palec_lub_sila, font=("Arial", 11),values=["kciuk", "wskazujący", "środkowy", "serdeczny", "mały", "siła_nacisku"])

        przycisk_odbierz_hist_wykresy = Button(top4, text="Załaduj wykres",
                                               fg="white", bg="#01786F", width=14, height=1,
                                               font=('Arial', 12), activebackground="#319177",
                                               activeforeground="white",
                                               cursor="hand2",
                                               command=lambda:[wykres(czas[0],pobrane_wyniki[wykresy_katow_i_sily.current()+1],wykresy_katow_i_sily.current())])
        wykresy_katow_i_sily.grid(row=6,column=1,padx=(400, 0), pady=(5,0) )

        przycisk_odbierz_hist_wykresy.grid(row=7,column=1, padx=(400, 0), pady=(5,30))


        # metoda zagnieżdzona w metodzie open_popup_wykr klasy Odbierz_wyniki
        # odpowiedzialna za wyświetlenie archiwum wykresów ukazujących przebieg ćwiczeń
        # wykonywanych przez pacjenta:
        def lista_his_wykr():
            # linie odpowiadające za autoryzację dostępu do dysku Google przez API Google Drive:
            gauth = GoogleAuth()
            drive = GoogleDrive(gauth)
            # linie 2855-2862 odpowiadają za pobranie i wyświetlenie
            # listy archiwalnych wykresów z ćwiczeń wykonywanych przez pacjenta:
            lista_wykr=list()
            file_list = drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format('1MH62rnEyI0vkZFo3Ii2oMGJ3UrJHbGRG')}).GetList()
            for file in file_list:
                if str(self.indeks) in file['title']:
                    print('title: %s, id: %s' % (file['title'], file['id']))
                    lista_wykr.append(file['title'])
            return lista_wykr

        # metoda zagnieżdzona w metodzie open_popup_wykr klasy Odbierz_wyniki
        # odpowiedzialna za pobranie z archiwum i wyświetlenie wybranych przez fizjoterapeutę
        # wykresów z ćwiczeń pacjenta:
        def pobranie_wykresów(plik):
            # linie odpowiadające za autoryzację dostępu do dysku Google przez API Google Drive:
            gauth = GoogleAuth()
            drive = GoogleDrive(gauth)
            # linie 2873-2880 odpowiadają za pobranie i wyświetlenie
            # listy archiwalnych wykresów z ćwiczeń wykonywanych przez pacjenta:
            file_list = drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format('1MH62rnEyI0vkZFo3Ii2oMGJ3UrJHbGRG')}).GetList()
            for file in file_list:
                if file['title']==plik:
                    file2 = drive.CreateFile({'id': file['id']})

                    dane=file2.GetContentString(file2).splitlines(True)
                    return dane

        def pobrano():
            global pobrane_wyniki
            pobrane_wyniki=pobranie_wykresów(wybrany_hist_wykres.get())

        # metoda zagnieżdzona w metodzie open_popup_wykr klasy Odbierz_wyniki
        # odpowiedzialna za pobranie danych i narysowanie wykresów pobranych z archiwum:
        def wykres(czas,wyniki,tryb):
            #linie 2890-2899 odpowiadają za obróbkę pobranych danych
            wyniki2=wyniki.strip("['']")
            wyniki3=wyniki2.replace("', '"," ")
            wyniki4=wyniki3.split(" ")
            wyn = list()

            for w in wyniki4:
                try:
                    wyn.append(float(w))
                except:
                    pass
            print(wyn)
            try:
                #stworzenie nowego wykresu:
                fig = Figure(figsize=(6,4))
                #skonfigurowanie osi czasu na wykresie:
                t=np.arange(0,float(czas),float(czas)/len(wyn))
                #linie 2908-2918 odpowiadają za wyrysowanie wykresu,
                # a także za ustawienie etykiet osi:
                ax = fig.add_subplot()
                ax.plot(t, wyn)
                ax.set_xlabel('czas [s]')
                if tryb in range(0, 5):
                    ax.set_ylabel('kąt ugięcia [°]')
                elif tryb == 5:
                    ax.set_ylabel('siła nacisku [g]')
                #linie 2916-2918 odpowiadają za umieszczenie wykresu w oknie z przeglądarką archiwum:
                canvas = FigureCanvasTkAgg(fig, master=top4)  # A tk.DrawingArea.
                canvas.draw()
                canvas.get_tk_widget().grid(column=1, columnspan=3, row=8, rowspan=3, padx=(280, 0), pady=5)
            except:
                #obsługa błędów:
                messagebox.showerror("","Brak danych, sprawdź połączenie z urządzeniem.")
                top4.destroy()



class Zarejestruj_Pacjenta(Frame,App):
    def __init__(self, aplikacja, kontener_stron):
        super().__init__(kontener_stron)

        self.configure(bg="#2d2e2e")
        napis_rejestracja = Label(self, text="REJESTRACJA PACJENTA W SYSTEMIE", width=33, font=("Arial", 15, 'bold'),
                                  fg="white",
                                  bg="#2d2e2e")
        napis_rejestracja.grid(column=1, row=2, padx=525, pady=(25, 0))

        napis_indeks_2 = Label(self, text="Nadaj indeks pacjentowi:", width=19, font=("Arial", 12), fg="white",
                               bg="#2d2e2e")
        napis_indeks_2.grid(column=1, row=3, padx=(0, 0), pady=(15, 0))

        okno_indeks_2 = Entry(self, width=12, font=('Arial', 12))
        okno_indeks_2.grid(row=4, column=1, columnspan=1, padx=(0, 0), pady=(10, 0))

        napis_login_haslo = Label(self, text="Poproś pacjenta o wybór loginu i hasła do aplikacji.", width=39,
                                  font=("Arial", 12), fg="white",
                                  bg="#2d2e2e")
        napis_login_haslo.grid(column=1, row=5, padx=(0, 0), pady=(15, 0))

        napis_nadaj_login = Label(self, text="Login:", width=10, font=("Arial", 12), fg="white",
                                  bg="#2d2e2e")
        napis_nadaj_login.grid(column=1, row=6, padx=(0, 0), pady=(15, 0))

        okno_nadaj_login = Entry(self, width=18, font=('Arial', 12))
        okno_nadaj_login.grid(row=7, column=1, columnspan=1, padx=(0, 0), pady=(10, 0))

        napis_nadaj_haslo = Label(self, text="Hasło:", width=10, font=("Arial", 12), fg="white",
                                  bg="#2d2e2e")
        napis_nadaj_haslo.grid(column=1, row=8, padx=(0, 0), pady=(15, 0))

        okno_nadaj_haslo = Entry(self, width=18, font=('Arial', 12), show="*")
        okno_nadaj_haslo.grid(row=9, column=1, columnspan=1, padx=(0, 0), pady=(10, 0))

        wartosc = IntVar(value=0)

        def pokaz_haslo():
            if (wartosc.get() == 1):
                okno_nadaj_haslo.config(show='')
            else:
                okno_nadaj_haslo.config(show='*')

        widok_hasla = Checkbutton(self, text='Pokaż hasło', variable=wartosc,
                                  onvalue=1, offvalue=0, command=pokaz_haslo, bg="#2d2e2e", fg="white",
                                  font=("Arial", 10), activebackground="#2d2e2e", activeforeground='white',
                                  selectcolor="#282828")
        widok_hasla.grid(row=9, column=1, padx=(300, 0), pady=(10, 0))

        przycisk_zaloz_konto = Button(self, text="Załóż konto", fg="white", bg="#01786F", width=10, height=1,
                                      font=('Arial', 12), activebackground="#319177", activeforeground="white",
                                      cursor="hand2",command=lambda : self.baza_rejestracja(str(okno_indeks_2.get()),str(okno_nadaj_login.get()),str(okno_nadaj_haslo.get())))
        przycisk_zaloz_konto.grid(row=10, column=1, columnspan=1, padx=(0, 0), pady=20)



        global otwarcie

        global zamkniecie

        global b2
        b2 = Button(self,
                    image=otwarcie,
                    command=lambda :self.lista_menu(aplikacja),
                    border=0,
                    bg='#2d2e2e',
                    cursor="hand2",
                    activebackground='#2d2e2e')
        b2.place(x=5, y=8)

    def lista_menu(self, aplikacja):
        # global f1

        f1 = Frame(self, width=250, height=700, bg='#01786F')
        f1.place(x=0, y=0)
        b2.place(x=5, y=8)

        def przycisk_menu(x, y, tekst, bcolor, fcolor, komenda):
            przycisk_m = Button(f1, text=tekst,
                                width=27,
                                height=2,
                                fg='white',
                                border=0,
                                bg=fcolor,
                                activeforeground='white',
                                activebackground=bcolor,
                                font=('Arial', 13),
                                cursor="hand2",
                                command=komenda)
            przycisk_m.place(x=x, y=y)

        przycisk_menu(0, 140, 'Wgraj filmy ', '#319177', '#01786F',
                      lambda: [f1.destroy(), aplikacja.show_frame(aplikacja.Wgraj_Filmy)])
        przycisk_menu(0, 240, 'Przypisz ćwiczenia', '#319177', '#01786F',
                      lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Przypisz_Ćwiczenia)])
        przycisk_menu(0, 340, 'Odbierz wyniki', '#319177', '#01786F',
                      lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Odbierz_Wyniki)])
        przycisk_menu(0, 440, 'Strona Główna', '#319177', '#01786F',
                      lambda: [f1.destroy(),aplikacja.show_frame(aplikacja.Zalogowano_Fizjo)])
        przycisk_menu(0, 540, 'Wyloguj', '#319177', '#01786F',
                      lambda: wyloguj())

        def zamknij():
            f1.destroy()
        def wyloguj():
            f1.destroy()
            pytanie = messagebox.askyesno('Wylogowywanie', 'Czy chcesz się wylogować?')
            if pytanie == True:
                messagebox.showinfo('Wylogowywanie', 'Pomyślnie wylogowano.')
                aplikacja.show_frame(aplikacja.Wybor_profilu)


        Button(f1,
               image=zamkniecie,
               border=0,
               command=zamknij,
               bg='#01786F',
               cursor="hand2",
               activebackground='#01786F').place(x=5, y=10)
    #metoda klasy Zarejestruj_Pacjenta odpowiedzialna
    # za wpisanie do bazy danych nowego pazcjenta podanymi przez fizjoterapeutę:
    def baza_rejestracja(self,indeks, login_pacjent, haslo_pacjent):
        indeks=indeks
        login = login_pacjent
        haslo=haslo_pacjent
        try:
            # wprowadzenie danych używanej bazy danych i otwarcie jej
            mysqldb4 = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="login")
            # sprawdzenie połączenia:
            print(mysqldb4.connection_id)
            # tworzenie zmiennej tymczasowej użwyanej do pobrania wyniku zapytania do bazy danych:
            mycursor4 = mysqldb4.cursor()
            # zapytania(kwerendy) sql wprowadzające dane do bazy:
            sql = "INSERT into logowanie (nr, login, haslo) VALUES (%s, %s, %s)"
            sql2 = "INSERT into pacjenci_dane (nr, login) VALUES (%s, %s)"
            # wartości wysyłane do bazy danych:
            val = (indeks, login,haslo)
            val2=(indeks,login)
            # wykonanie zapytania sql do bazy danych:
            mycursor4.execute(sql, val)
            mycursor4.execute(sql2, val2)
            try:
                # zatwierdzenie zmian dokonanych przez zapytanie SQL:
                mysqldb4.commit()
                messagebox.showinfo("","Pomyślnie zarejestrowano pacjenta")

            except:
                #obsługa błędów
                messagebox.showinfo("", "Niepowodzenie w rejestrowaniu pacjenta")

        except mysql.connector.Error:
            messagebox.showinfo("", "Błąd przy połączeniu")
        except:
            messagebox.showinfo("", "Błąd")
        else:
            # zamknięcie otwartej bazy danych:
            mysqldb4.close()

#linie odpowiadające za działanie programu w pętli
if __name__ == "__main__":
    program=App()
    program.mainloop()




