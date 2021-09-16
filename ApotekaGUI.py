from tkinter import *
from PIL import ImageTk, Image
from tkinter.ttk import Combobox
from tkinter import messagebox
# from datetime import datetime
# import uuid
from Apoteka import *


class GlavniProzor(Tk):

    def recept_prozor(self):
        recept = ReceptProzor(self, self.__podaci)
        self.wait_window(recept)
        if recept.otkazano:
            return

    def lek_prozor(self):
        lek = LekProzor(self, self.__podaci)
        self.wait_window(lek)
        if lek.otkazano:
            return

    def lekar_prozor(self):
        lekar = LekarProzor(self, self.__podaci)
        self.wait_window(lekar)
        if lekar.otkazano:
            return

    def pacijent_prozor(self):
        prozor = PacijentProzor(self, self.__podaci)
        self.wait_window(prozor)
        if prozor.otkazano:
            return

    def izlaz(self):
        odgovor = messagebox.askokcancel("Pharmacy", "Da li ste sigurni da želite da napustite aplikaciju?", icon="warning")
        if odgovor:
            self.destroy()

    def __init__(self, podaci):
        super().__init__()
        self.__podaci = podaci
        self.frame = Frame()
        self.frame.grid(row=0, column=0, columnspan=4)
        self.frame.configure(bg="#ffffff")
        self.frame.canvas = Canvas(height=530, width=915).grid(row=0, column=1, columnspan=4, rowspan=25)
        image1 = Image.open("apoteka1.jpg")
        self.frame.backgroundimage = ImageTk.PhotoImage(image1)
        self.frame.backgroundlabel = Label(image=self.frame.backgroundimage).place(relheight=1, relwidth=1)

        bkg = "#05dff7"
        bkg3 = "#0cc918"
        bkg2 = "#858585"

        self.button1 = Button(text="Pacijenti", font=("Comic Sans MS", 25, "bold"), padx=40, pady=20, bg=bkg, fg="#ffffff", activebackground=bkg, activeforeground=bkg2, relief=GROOVE, command=self.pacijent_prozor).grid(row=1, column=0)
        self.button2 = Button(text="Lekari", font=("Comic Sans MS", 25, "bold"), padx=60, pady=20, bg=bkg3, fg="#ffffff", activebackground=bkg3, activeforeground=bkg2, relief=GROOVE, command=self.lekar_prozor).grid(row=2, column=0)
        self.button3 = Button(text="Lekovi", font=("Comic Sans MS", 25, "bold"), padx=60, pady=20, bg=bkg, fg="#ffffff", activebackground=bkg, activeforeground=bkg2, relief=GROOVE, command=self.lek_prozor).grid(row=3, column=0)
        self.button4 = Button(text="Recepti", font=("Comic Sans MS", 25, "bold"), padx=50, pady=20, bg=bkg3, fg="#ffffff", activebackground=bkg3, activeforeground=bkg2, relief=GROOVE, command=self.recept_prozor).grid(row=4, column=0)
        self.button4 = Button(text="Izlaz", font=("Comic Sans MS", 15, "bold"), padx=30, pady=10, bg=bkg2, fg="#ffffff", activebackground=bkg2, activeforeground="#ffffff", relief=GROOVE, command=self.izlaz).grid(row=3, column=4)
        meni = Menu(self)
        self.config(menu=meni)

        izlaz_meni = Menu(meni)
        navigacija_meni = Menu(meni)
        meni.add_cascade(label="Navigacija", menu=navigacija_meni)
        navigacija_meni.add_command(label="Pacijenti", command=self.pacijent_prozor)
        navigacija_meni.add_command(label="Lekari", command=self.lekar_prozor)
        navigacija_meni.add_command(label="Recepti", command=self.recept_prozor)
        navigacija_meni.add_command(label="Lek", command=self.lek_prozor)
        meni.add_cascade(label="Izlaz", menu=izlaz_meni)
        izlaz_meni.add_command(label="Izlaz", command=self.izlaz)
        self.protocol("WM_DELETE_WINDOW", self.izlaz)
        self.title("PHARMACY")

        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)


class PacijentProzor(Toplevel):

    def prikazi(self):
        index = self.__pacijent_listbox.curselection()[0]
        pacijent = self.__podaci.pacijent[index]
        for recept in self.__podaci.recept:
            if pacijent == recept.pacijent:
                messagebox.showinfo("Recept", recept)
            else:
                messagebox.showinfo("Recept", "Nema recepta")

    def izmeni(self):
        index = self.__pacijent_listbox.curselection()[0]
        pacijenti = self.pretraga()
        pacijent = pacijenti[index]
        izmena = IzmeniPacijenta(self, self.__podaci, pacijent)
        self.wait_window(izmena)
        if izmena.otkazano:
            return

        self.__pacijent_listbox.delete(index)  # trenutni
        self.__pacijent_listbox.insert(index, pacijent.ime + " " + pacijent.prezime)
        self.__pacijent_listbox.select_set(index)
        self.selekcija()
        self.__pretraga_text.delete("1.0", "end")

    def obrisi(self):

        if messagebox.askquestion("Upozorenje", "Da li ste sigurni da zelite da obrisete pacijenta?", icon="warning") == "no":
            return
        index = self.__pacijent_listbox.curselection()[0]

        pacijenti = self.pretraga()
        pacijent = pacijenti[index]

        self.__pacijent_listbox.select_set(index)
        self.__podaci.obrisi_pacijenta(pacijent)

        self.config(cursor="wait")
        self.update()
        self.__podaci.sacuvaj_se()
        self.config(cursor="")

        self.__pacijent_listbox.delete(index)
        self.__pacijent_listbox.select_set(index)

        self.selekcija()

    def dodaj(self):
        dodaj = DodajPacijent(self, self.__podaci)
        self.wait_window(dodaj)
        if dodaj.otkazano:
            return

        self.__pretraga_text.delete("1.0", "end")
        pacijent = self.__podaci.pacijent[-1]  # poslednji sa liste
        self.__pacijent_listbox.selection_clear(0, END)
        self.__pacijent_listbox.insert(END, pacijent.ime + " " + pacijent.prezime)
        self.__pacijent_listbox.select_set(END)
        self.selekcija()

    def popuni_listbox(self, pacijenti):
        self.__pacijent_listbox.delete(0, END)
        for pacijenti in pacijenti:
            self.__pacijent_listbox.insert(END, pacijenti.ime + " " + pacijenti.prezime)

    def pretraga(self, event=None):
        self.ocisti_labele()
        self.__izmeni_button["state"] = DISABLED
        self.__brisi_button["state"] = DISABLED
        self.__recept_button["state"] = DISABLED
        pretraga = self.__pretraga_text.get("1.0", 'end-1c')
        if pretraga == "":
            pacijenti = self.__podaci.pacijent
        else:
            pacijenti = []
            for pacijent in self.__podaci.pacijent:
                if pretraga.upper() in pacijent.ime.upper() or pretraga.upper() in pacijent.prezime.upper():
                    pacijenti.append(pacijent)

        self.popuni_listbox(pacijenti)
        return pacijenti

    def ocisti_labele(self):
        self.__JMBG_labela["text"] = ""
        self.__ime_labela["text"] = ""
        self.__prezime_labela["text"] = ""
        self.__datum_labela["text"] = ""
        self.__LBO_labela["text"] = ""

    def popuni_labele(self, pacijent):

        self.__JMBG_labela["text"] = pacijent.JMBG
        self.__ime_labela["text"] = pacijent.ime
        self.__prezime_labela["text"] = pacijent.prezime
        self.__datum_labela["text"] = pacijent.datum_rodjenja
        self.__LBO_labela["text"] = pacijent.LBO

    def selekcija(self, event=None):

        if not self.__pacijent_listbox.curselection():
            self.ocisti_labele()
            self.__izmeni_button["state"] = DISABLED
            self.__brisi_button["state"] = DISABLED
            self.__recept_button["state"] = DISABLED
            return

        indeks = self.__pacijent_listbox.curselection()[0]
        pacijenti = self.pretraga()
        pacijent = pacijenti[indeks]
        self.__pacijent_listbox.select_set(indeks)
        self.popuni_labele(pacijent)
        self.__izmeni_button["state"] = NORMAL
        self.__brisi_button["state"] = NORMAL
        self.__recept_button["state"] = NORMAL

    def izlaz(self):
        odgovor = messagebox.askokcancel("Pacijenti", "Da li ste sigurni da želite da napustite aplikaciju?", icon="warning")
        if odgovor:
            self.destroy()

    @property
    def otkazano(self):
        return self.__otkazano

    @property
    def podaci(self):
        return self.__podaci

    @property
    def pretraga_text(self):
        return self.__pretraga_text

    @pretraga_text.setter
    def pretraga_text(self, pre):
        self.__pretraga_text = pre

    def __init__(self, master, podaci):
        super().__init__(master)
        self.__otkazano = True
        self.__podaci = podaci

        self.__pacijent_listbox = Listbox(self, activestyle="none", bg="#efefef")
        self.__pacijent_listbox.pack(side=LEFT, fill=BOTH, expand=1)
        self.__pacijent_listbox.bind("<<ListboxSelect>>", self.selekcija)

        pretraga_frame = Frame(self, borderwidth=2, relief="ridge", bg="#A9CFA5")
        pretraga_frame.pack(side=LEFT, fill=BOTH, expand=1)

        self.__pretraga_text = Text(pretraga_frame, height=1, width=50)

        Label(pretraga_frame, text="Pretraga:", font=("Comic Sans MS", 12),  fg="#FFFFFF", bg="#A9CFA5").grid(row=0, sticky=W)
        self.__pretraga_text.grid(row=0, column=1, sticky=E)

        self.__pretraga_text.bind("<KeyRelease>", self.pretraga)

        pacijent_frame = Frame(self, borderwidth=2, relief="ridge", padx=30, pady=30, bg="#A9CFA5")
        pacijent_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        self.__JMBG_labela = Label(pacijent_frame)
        self.__ime_labela = Label(pacijent_frame)
        self.__prezime_labela = Label(pacijent_frame)
        self.__datum_labela = Label(pacijent_frame)
        self.__LBO_labela = Label(pacijent_frame)

        red = 0
        Label(pacijent_frame, text="JMBG:", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(pacijent_frame, text="ime:", font=("Century Gothic", 11, "bold"), bg="#A9CFA5", fg="#EFEFEF").grid(row=red, sticky=E)
        red = red + 1
        Label(pacijent_frame, text="prezime:", font=("Century Gothic", 11, "bold"), bg="#A9CFA5", fg="#EFEFEF").grid(row=red, sticky=E)
        red = red + 1
        Label(pacijent_frame, text="datum rodjenja:", font=("Century Gothic", 11, "bold"), bg="#A9CFA5", fg="#EFEFEF").grid(row=red, sticky=E)
        red = red + 1
        Label(pacijent_frame, text="LBO:", font=("Century Gothic", 11, "bold"), bg="#A9CFA5", fg="#EFEFEF").grid(row=red, sticky=E)

        red = 0
        kolona = 1
        self.__JMBG_labela.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__ime_labela.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__prezime_labela.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__datum_labela.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__LBO_labela.grid(row=red, column=kolona, sticky=W)

        self.__dodaj_button = Button(pretraga_frame, text="Dodaj pacijenta", font=("Century Gothic", 11, "bold"), width=15, height=2, command=self.dodaj)
        self.__izmeni_button = Button(pretraga_frame, text="Izmeni pacijenta", font=("Century Gothic", 11, "bold"), width=15, height=2, state=DISABLED, command=self.izmeni)
        self.__brisi_button = Button(pretraga_frame, text="Obrisi pacijenta", font=("Century Gothic", 11, "bold"), width=15, height=2, state=DISABLED, command=self.obrisi)
        self.__recept_button = Button(pretraga_frame, text="Prikazi recept", font=("Century Gothic", 11, "bold"), width=15, height=2, state=DISABLED, command=self.prikazi)

        red = 1
        kolona = 0
        self.__dodaj_button.grid(row=red, column=kolona)
        kolona = kolona + 1
        self.__izmeni_button.grid(row=red, column=kolona)
        kolona = kolona + 1
        self.__brisi_button.grid(row=red, column=kolona)
        kolona = kolona + 1
        self.__recept_button.grid(row=red, column=kolona)

        self.popuni_listbox(self.__podaci.pacijent)
        self.protocol("WM_DELETE_WINDOW", self.izlaz)
        self.title("Pacijenti")
        self.iconbitmap("logo.ico")
        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self.transient(master)


class DodajIzmeniPacijent(Toplevel):

    def jmbg_validacija(self):
        jmbg = self.__JMBG.get()
        if len(jmbg) != 13:
            messagebox.showerror("Greška!", "JMBG mora sadržati 13 karaktera!")
            return None
        else:
            for pacijent in self.__podaci.pacijent:
                if pacijent.JMBG == jmbg:
                    messagebox.showerror("Greška!", "Ovaj JMBG već postoji!")
                    return None
        return jmbg

    def ime_validacija(self):
        ime = self.__ime.get()
        if len(ime) < 2:
            messagebox.showerror("Greška!", "Ime mora sadržati bar dva karaktera!")
            return None
        return ime

    def prezime_validacija(self):
        prezime = self.__prezime.get()
        if len(prezime) < 2:
            messagebox.showerror("Greška!", "Prezime mora sadržati bar dva karaktera!")
            return None
        return prezime

    def lbo_validacija(self):
        lbo = self.__LBO.get()
        if len(lbo) != 11:
            messagebox.showerror("Greška!", "LBO mora sadržati 11 karaktera!")
            return None
        for pacijent in self.__podaci.pacijent:
            if pacijent.LBO == lbo:
                messagebox.showerror("Greška!", "Ovaj LBO već postoji!")
                return None
        return lbo

    def datum_validacija(self):
        datum = self.__datum_rodjenja.get()
        try:
            dt_str = datetime.strptime(datum, '%d.%m.%Y.')
        except ValueError:
            messagebox.showerror("Greška!", "Datum mora biti oblika dd.mm.yyyy.!")
            return False
        return datum

    @property
    def otkazano(self):
        return self.__otkazano

    @property
    def podaci(self):
        return self.__podaci

    @property
    def JMBG(self):
        return self.__JMBG

    @property
    def ime(self):
        return self.__ime

    @property
    def prezime(self):
        return self.__prezime

    @property
    def datum_rodjenja(self):
        return self.__datum_rodjenja

    @property
    def LBO(self):
        return self.__LBO

    @property
    def JMBG_entry(self):
        return self.__JMBG_entry

    @property
    def LBO_entry(self):
        return self.__LBO_entry

    @property
    def ok_button(self):
        return self.__ok_button

    def izlaz(self):
        odgovor = messagebox.askokcancel("Izlaz", "Da li ste sigurni da želite da napustite aplikaciju? :(", icon="warning")
        if odgovor:
            self.destroy()

    def ok(self):
        odgovor = messagebox.askokcancel("Potvrda", "Da li ste sigurni?", icon="warning")
        if odgovor:
            self.config(cursor="wait")
            self.update()
            self.podaci.sacuvaj_se()
            self.config(cursor="")

            self.__otkazano = False
            self.destroy()

    def __init__(self, master, podaci):
        super().__init__(master)
        self.__otkazano = True
        self.__podaci = podaci
        self.__JMBG = StringVar(master)
        self.__ime = StringVar(master)
        self.__prezime = StringVar(master)
        self.__datum_rodjenja = StringVar(master)
        self.__LBO = StringVar(master)

        pacijent_frame = Frame(self, padx=10, pady=10, bg="#A9CFA5")
        pacijent_frame.pack(expand=1)

        self.__JMBG_entry = Entry(pacijent_frame, width=30, textvariable=self.__JMBG)
        self.__ime_entry = Entry(pacijent_frame, width=30, textvariable=self.__ime)
        self.__prezime_entry = Entry(pacijent_frame, width=30, textvariable=self.__prezime)
        self.__datum_entry = Entry(pacijent_frame, width=30, textvariable=self.__datum_rodjenja)
        self.__LBO_entry = Entry(pacijent_frame, width=30, textvariable=self.__LBO)

        self.__ok_button = Button(pacijent_frame, font=("Century Gothic", 11, "bold"), width=10, command=self.ok)
        self.__izlaz = Button(pacijent_frame, text="Izlaz", font=("Century Gothic", 11, "bold"), width=10, command=self.izlaz)

        red = 0
        Label(pacijent_frame, text="JMBG: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(pacijent_frame, text="Ime: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(pacijent_frame, text="Prezime: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(pacijent_frame, text="Datum rođenja: ",  font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(pacijent_frame, text="LBO: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)

        red = 0
        kolona = 1
        self.__JMBG_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__ime_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__prezime_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__datum_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__LBO_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__ok_button.grid(row=red, column=0, sticky=E)
        self.__izlaz.grid(row=red, column=1, sticky=W)

        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)

        self.focus_force()
        self.grab_set()
        self.transient(master)


class DodajPacijent(DodajIzmeniPacijent):

    def izlaz(self):
        odgovor = messagebox.askokcancel("Dodaj pacijenta", "Da li ste sigurni da želite da napustite aplikaciju? :(", icon="warning")
        if odgovor:
            self.destroy()

    def ok(self):
        jmbg = self.jmbg_validacija()
        if not jmbg:
            return
        ime = self.ime_validacija()
        if not ime:
            return
        prezime = self.prezime_validacija()
        if not prezime:
            return
        lbo = self.lbo_validacija()
        if not lbo:
            return
        datum = self.datum_validacija()
        if not datum:
            return

        pacijent = Pacijent(jmbg, ime, prezime, datum, lbo)
        self.podaci.dodaj_pacijenta(pacijent)
        super().ok()

    def __init__(self, master, podaci):
        super().__init__(master, podaci)
        self.ok_button["text"] = "Dodaj"
        self.iconbitmap("logo.ico")
        self.title("Dodavanje pacijent")


class IzmeniPacijenta(DodajIzmeniPacijent):

    def izlaz(self):
        odgovor = messagebox.askokcancel("Izmeni pacijenta", "Da li ste sigurni da želite da napustite aplikaciju? :(", icon="warning")
        if odgovor:
            self.destroy()

    def ok(self):
        ime = self.ime_validacija()
        if not ime:
            return
        prezime = self.prezime_validacija()
        if not prezime:
            return
        datum = self.datum_validacija()
        if not datum:
            return

        self.__pacijent.ime = ime
        self.__pacijent.prezime = prezime
        self.__pacijent.datum_rodjenja = datum
        super().ok()

    def __init__(self, master, podaci, pacijent):
        super().__init__(master, podaci)

        self.__pacijent = pacijent

        self.JMBG.set(self.__pacijent.JMBG)
        self.LBO.set(self.__pacijent.LBO)
        self.ime.set(self.__pacijent.ime)
        self.prezime.set(self.__pacijent.prezime)
        self.datum_rodjenja.set(self.__pacijent.datum_rodjenja)

        self.JMBG_entry["state"] = DISABLED
        self.LBO_entry["state"] = DISABLED

        self.ok_button["text"] = "Izmeni"
        self.iconbitmap("logo.ico")
        self.title("Izmena pacijenta")


class LekarProzor(Toplevel):

    def prikazi(self):
        index = self.__lekar_listbox.curselection()[0]
        lekar = self.__podaci.lekar[index]
        ima_recept = False

        for recept in self.__podaci.recept:
            if lekar == recept.lekar:
                messagebox.showinfo("Recept", recept)
                ima_recept = True

        if ima_recept == False:
            messagebox.showinfo("Recept", "Nema recepta")

    def izmeni(self):
        index = self.__lekar_listbox.curselection()[0]
        lekari = self.pretraga()
        lekar = lekari[index]

        izmena = IzmeniLekara(self, self.__podaci, lekar)
        self.wait_window(izmena)
        if izmena.otkazano:
            return

        self.__lekar_listbox.delete(index)  # trenutni
        self.__lekar_listbox.insert(index, lekar.ime + " " + lekar.prezime)
        self.__lekar_listbox.select_set(index)
        self.selekcija()

    def obrisi(self):
        if messagebox.askquestion("Upozorenje!", "Da li ste sigurni da želite da obrišete lekara?", icon="warning") == "no":
            return
        index = self.__lekar_listbox.curselection()[0]
        lekari = self.pretraga()
        lekar = lekari[index]

        self.__lekar_listbox.select_set(index)
        self.__podaci.obrisi_lekara(lekar)

        self.config(cursor="wait")
        self.update()
        self.__podaci.sacuvaj_se()
        self.config(cursor="")

        self.__lekar_listbox.delete(index)
        self.__lekar_listbox.select_set(index)
        self.selekcija()

    def dodaj(self):
        dodaj = DodajLekara(self, self.__podaci)
        self.wait_window(dodaj)
        if dodaj.otkazano:
            return

        self.__pretraga_text.delete("1.0", "end")
        lekar = self.__podaci.lekar[-1]  # poslednji sa liste
        self.__lekar_listbox.selection_clear(0, END)
        self.__lekar_listbox.insert(END, lekar.ime + " " + lekar.prezime)
        self.__lekar_listbox.select_set(END)
        self.selekcija()

    def popuni_listbox(self, lekar):
        self.__lekar_listbox.delete(0, END)
        for lekari in lekar:
            self.__lekar_listbox.insert(END, lekari.ime + " " + lekari.prezime)

    def pretraga(self, event=None):
        self.ocisti_labele()
        self.__izmeni_button["state"] = DISABLED
        self.__brisi_button["state"] = DISABLED
        self.__recept_button["state"] = DISABLED
        pretraga = self.__pretraga_text.get("1.0", 'end-1c')

        if pretraga == "":
            lekari = self.__podaci.lekar
        else:
            lekari = []
            for lekar in self.__podaci.lekar:
                if pretraga.upper() in lekar.ime.upper() or pretraga.upper() in lekar.prezime.upper():
                    lekari.append(lekar)
        self.popuni_listbox(lekari)
        return lekari

    def ocisti_labele(self):
        self.__JMBG_labela["text"] = ""
        self.__ime_labela["text"] = ""
        self.__prezime_labela["text"] = ""
        self.__datum_labela["text"] = ""
        self.__specijalizacija_labela["text"] = ""

    def popuni_labele(self, lekar):
        self.__JMBG_labela["text"] = lekar.JMBG
        self.__ime_labela["text"] = lekar.ime
        self.__prezime_labela["text"] = lekar.prezime
        self.__datum_labela["text"] = lekar.datum_rodjenja
        self.__specijalizacija_labela["text"] = lekar.specijalizacija

    def selekcija(self, event=None):
        if not self.__lekar_listbox.curselection():
            self.ocisti_labele()
            self.__izmeni_button["state"] = DISABLED
            self.__brisi_button["state"] = DISABLED
            self.__recept_button["state"] = DISABLED
            return
        indeks = self.__lekar_listbox.curselection()[0]
        lekari = self.pretraga()
        lekar = lekari[indeks]
        self.__lekar_listbox.select_set(indeks)
        self.popuni_labele(lekar)
        self.__izmeni_button["state"] = NORMAL
        self.__brisi_button["state"] = NORMAL
        self.__recept_button["state"] = NORMAL

    def izlaz(self):
        odgovor = messagebox.askokcancel("Lekari", "Da li ste sigurni da želite da napustite aplikaciju? :(", icon="warning")
        if odgovor:
            self.destroy()

    @property
    def otkazano(self):
        return self.__otkazano

    @property
    def podaci(self):
        return self.__podaci

    @property
    def pretraga_text(self):
        return self.__pretraga_text

    @pretraga_text.setter
    def pretraga_text(self, pre):
        self.__pretraga_text = pre

    def __init__(self, master, podaci):
        super().__init__(master)
        self.__otkazano = True
        self.__podaci = podaci

        self.__lekar_listbox = Listbox(self, activestyle="none", bg="#efefef")
        self.__lekar_listbox.pack(side=LEFT, fill=BOTH, expand=1)
        self.__lekar_listbox.bind("<<ListboxSelect>>", self.selekcija)

        pretraga_frame = Frame(self, borderwidth=4, relief="ridge", bg="#A9CFA5")
        pretraga_frame.pack(side=LEFT, fill=BOTH, expand=1)

        self.__pretraga_text = Text(pretraga_frame, height=1, width=50)
        Label(pretraga_frame, text="Pretraga: ", font=("Comic Sans MS", 12),  fg="#FFFFFF", bg="#A9CFA5").grid(row=0, sticky=W)
        self.__pretraga_text.grid(row=0, column=1, sticky=E)
        self.__pretraga_text.bind("<KeyRelease>", self.pretraga)

        lekar_frame = Frame(self, borderwidth=2, relief="ridge", padx=30, pady=30, bg="#A9CFA5")
        lekar_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        self.__JMBG_labela = Label(lekar_frame)
        self.__ime_labela = Label(lekar_frame)
        self.__prezime_labela = Label(lekar_frame)
        self.__datum_labela = Label(lekar_frame)
        self.__specijalizacija_labela = Label(lekar_frame)

        red = 0
        Label(lekar_frame, text="JMBG: ", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(lekar_frame, text="Ime: ", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(lekar_frame, text="Prezime: ", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(lekar_frame, text="Datum rođenja: ", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(lekar_frame, text="Specijalizacija: ", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)

        red = 0
        kolona = 1
        self.__JMBG_labela.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__ime_labela.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__prezime_labela.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__datum_labela.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__specijalizacija_labela.grid(row=red, column=kolona, sticky=W)

        self.__dodaj_button = Button(pretraga_frame, text="Dodaj lekara", font=("Century Gothic", 11, "bold"), width=15, height=2, command=self.dodaj)
        self.__izmeni_button = Button(pretraga_frame, text="Izmeni lekara", font=("Century Gothic", 11, "bold"), width=15, height=2, state=DISABLED, command=self.izmeni)
        self.__brisi_button = Button(pretraga_frame, text="Obriši lekara", font=("Century Gothic", 11, "bold"), width=15, height=2, state=DISABLED, command=self.obrisi)
        self.__recept_button = Button(pretraga_frame, text="Prikaži recept", font=("Century Gothic", 11, "bold"), width=15, height=2, state=DISABLED, command=self.prikazi)

        red = 1
        kolona = 0
        self.__dodaj_button.grid(row=red, column=kolona)
        kolona = kolona + 1
        self.__izmeni_button.grid(row=red, column=kolona)
        kolona = kolona + 1
        self.__brisi_button.grid(row=red, column=kolona)
        kolona = kolona + 1
        self.__recept_button.grid(row=red, column=kolona)

        self.popuni_listbox(self.__podaci.lekar)
        self.protocol("WM_DELETE_WINDOW", self.izlaz)
        self.title("Lekari")
        self.iconbitmap("logo.ico")
        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self.transient(master)


class DodajIzmeniLekar(Toplevel):

    def jmbg_validacija(self):
        jmbg = self.__JMBG.get()
        if len(jmbg) != 13:
            messagebox.showerror("Greška", "JMBG mora sadržati 13 karaktera!")
            return None
        else:
            for pacijent in self.__podaci.pacijent:
                if pacijent.JMBG == jmbg:
                    messagebox.showerror("Greška!", "Ovaj JMBG već postoji!")
                    return None

        return jmbg

    def ime_validacija(self):
        ime = self.__ime.get()
        if len(ime) < 2:
            messagebox.showerror("Greška!", "Ime mora sadržati bar dva karaktera!")
            return None
        return ime

    def prezime_validacija(self):
        prezime = self.__prezime.get()
        if len(prezime) < 2:
            messagebox.showerror("Greška!", "Prezime mora sadržati bar dva karaktera!")
            return None
        return prezime

    def specijalizacija_validacija(self):
        specijalizacija = self.__specijalizacija.get()
        if len(specijalizacija) < 2:
            messagebox.showerror("Greška!", "Specijalizacija mora sadržati bar dva karaktera!")
            return None
        return specijalizacija

    def datum_validacija(self):
        datum = self.__datum_rodjenja.get()
        try:
            dt_str = datetime.strptime(datum, '%d.%m.%Y.')
        except ValueError:
            messagebox.showerror("Greška!", "Datum mora biti oblika dd.mm.yyyy.!")
            return False
        return datum

    @property
    def otkazano(self):
        return self.__otkazano

    @property
    def podaci(self):
        return self.__podaci

    @property
    def JMBG(self):
        return self.__JMBG

    @property
    def ime(self):
        return self.__ime

    @property
    def prezime(self):
        return self.__prezime

    @property
    def datum_rodjenja(self):
        return self.__datum_rodjenja

    @property
    def specijalizacija(self):
        return self.__specijalizacija

    @property
    def JMBG_entry(self):
        return self.__JMBG_entry

    @property
    def ok_button(self):
        return self.__ok_button

    def izlaz(self):
        odgovor = messagebox.askokcancel("Izlaz", "Da li ste sigurni da želite da napustite aplikaciju? :(", icon="warning")
        if odgovor:
            self.destroy()

    def ok(self):
        odgovor = messagebox.askokcancel("Potvrda", "Da li ste sigurni?", icon="warning")
        if odgovor:
            self.config(cursor="wait")
            self.update()
            self.podaci.sacuvaj_se()
            self.config(cursor="")

            self.__otkazano = False
            self.destroy()

    def __init__(self, master, podaci):
        super().__init__(master)
        self.__otkazano = True
        self.__podaci = podaci

        self.__JMBG = StringVar(master)
        self.__ime = StringVar(master)
        self.__prezime = StringVar(master)
        self.__datum_rodjenja = StringVar(master)
        self.__specijalizacija = StringVar(master)

        lekar_frame = Frame(self, padx=10, pady=10, bg="#A9CFA5")
        lekar_frame.pack(expand=1)

        self.__JMBG_entry = Entry(lekar_frame, width=30, textvariable=self.__JMBG)
        self.__ime_entry = Entry(lekar_frame, width=30, textvariable=self.__ime)
        self.__prezime_entry = Entry(lekar_frame, width=30, textvariable=self.__prezime)
        self.__datum_entry = Entry(lekar_frame, width=30, textvariable=self.__datum_rodjenja)
        self.__specijalizacija_entry = Entry(lekar_frame, width=30, textvariable=self.__specijalizacija)

        self.__ok_button = Button(lekar_frame, font=("Century Gothic", 11, "bold"), width=10, command=self.ok)
        self.__izlaz = Button(lekar_frame, text="Izlaz", font=("Century Gothic", 11, "bold"), width=10, command=self.izlaz)

        red = 0
        Label(lekar_frame, text="JMBG: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(lekar_frame, text="Ime: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(lekar_frame, text="Prezime: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(lekar_frame, text="Datum rođenja: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(lekar_frame, text="Specijalizacija: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)

        red = 0
        kolona = 1
        self.__JMBG_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__ime_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__prezime_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__datum_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__specijalizacija_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__ok_button.grid(row=red, column=0, sticky=E)
        self.__izlaz.grid(row=red, column=1, sticky=W)

        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self.focus_force()
        self.grab_set()
        self.transient(master)


class DodajLekara(DodajIzmeniLekar):

    def izlaz(self):
        odgovor = messagebox.askokcancel("Dodaj lekara", "Da li ste sigurni da želite da napustite aplikaciju? :(", icon="warning")
        if odgovor:
            self.destroy()

    def ok(self):
        jmbg = self.jmbg_validacija()
        if not jmbg:
            return
        ime = self.ime_validacija()
        if not ime:
            return
        prezime = self.prezime_validacija()
        if not prezime:
            return
        specijalizacija = self.specijalizacija_validacija()
        if not specijalizacija:
            return
        datum = self.datum_validacija()
        if not datum:
            return

        #KREIRANJE
        lekar = Lekar(jmbg, ime, prezime, datum, specijalizacija)
        self.podaci.dodaj_lekara(lekar)
        super().ok()

    def __init__(self, master, podaci):
        super().__init__(master, podaci)
        self.ok_button["text"] = "Dodaj"
        self.iconbitmap("logo.ico")
        self.title("Dodavanje lekara")


class IzmeniLekara(DodajIzmeniLekar):

    def izlaz(self):
        odgovor = messagebox.askokcancel("Izmeni lekara", "Da li ste sigurni da želite da napustite aplikaciju? :(", icon="warning")
        if odgovor:
            self.destroy()

    def ok(self):
        ime = self.ime_validacija()
        if not ime:
            return
        prezime = self.prezime_validacija()
        if not prezime:
            return
        datum = self.datum_validacija()
        if not datum:
            return
        specijalizacija = self.specijalizacija_validacija()
        if not specijalizacija:
            return

        self.__lekar.ime = ime
        self.__lekar.prezime = prezime
        self.__lekar.datum_rodjenja = datum
        self.__lekar.specijalizacija = specijalizacija
        super().ok()

    def __init__(self, master, podaci, lekar):
        super().__init__(master, podaci)
        self.__lekar = lekar

        self.JMBG.set(self.__lekar.JMBG)
        self.specijalizacija.set(self.__lekar.specijalizacija)
        self.ime.set(self.__lekar.ime)
        self.prezime.set(self.__lekar.prezime)
        self.datum_rodjenja.set(self.__lekar.datum_rodjenja)

        self.JMBG_entry["state"] = DISABLED

        self.ok_button["text"] = "Izmeni"
        self.iconbitmap("logo.ico")
        self.title("Izmena lekara")


class LekProzor(Toplevel):

    def izmeni(self):
        index = self.__lek_listbox.curselection()[0]
        leko = self.pretraga()
        lek = leko[index]

        izmena = IzmeniLek(self, self.__podaci, lek)
        self.wait_window(izmena)
        if izmena.otkazano:
            return

        self.__lek_listbox.delete(index)  # trenutni
        self.__lek_listbox.insert(index, lek.naziv)
        self.__lek_listbox.select_set(index)
        self.selekcija()

    def obrisi(self):
        if messagebox.askquestion("Upozorenje!", "Da li ste sigurni da želite da obrišete lek?", icon="warning") == "no":
            return
        index = self.__lek_listbox.curselection()[0]

        leka = self.pretraga()
        lek = leka[index]

        self.__lek_listbox.select_set(index)
        self.__podaci.obrisi_lek(lek)

        self.config(cursor="wait")
        self.update()
        self.__podaci.sacuvaj_se()
        self.config(cursor="")

        self.__lek_listbox.delete(index)
        self.__lek_listbox.select_set(index)
        self.selekcija()

    def dodaj(self):
        dodaj = DodajLek(self, self.__podaci)
        self.wait_window(dodaj)
        if dodaj.otkazano:
            return

        self.__pretraga_text.delete("1.0", "end")
        lek = self.__podaci.lek[-1]  # poslednji sa liste
        self.__lek_listbox.selection_clear(0, END)
        self.__lek_listbox.insert(END, lek.naziv)
        self.__lek_listbox.select_set(END)
        self.selekcija()

    def popuni_listbox(self, lek):
        self.__lek_listbox.delete(0, END)
        for lek in lek:
            self.__lek_listbox.insert(END, lek.naziv)

    def pretraga(self, event=None):
        self.ocisti_labele()
        self.__izmeni_button["state"] = DISABLED
        self.__brisi_button["state"] = DISABLED

        pretraga = self.__pretraga_text.get("1.0", 'end-1c')
        if pretraga == "":
            leki = self.__podaci.lek
        else:
            leki = []
            for lek in self.__podaci.lek:
                if pretraga.upper() in lek.naziv.upper():
                    leki.append(lek)
        self.popuni_listbox(leki)

        return leki

    def ocisti_labele(self):
        self.__JKL_labela["text"] = ""
        self.__naziv_labela["text"] = ""
        self.__proizvodjac_labela["text"] = ""
        self.__tip_labela["text"] = ""

    def popuni_labele(self, lek):
        self.__JKL_labela["text"] = lek.JKL
        self.__naziv_labela["text"] = lek.naziv
        self.__proizvodjac_labela["text"] = lek.proizvodjac
        self.__tip_labela["text"] = lek.tip

    def selekcija(self, event=None):
        if not self.__lek_listbox.curselection():
            self.ocisti_labele()
            self.__izmeni_button["state"] = DISABLED
            self.__brisi_button["state"] = DISABLED
            return

        indeks = self.__lek_listbox.curselection()[0]
        lekovi = self.pretraga()
        lek = lekovi[indeks]
        self.__lek_listbox.select_set(indeks)
        self.popuni_labele(lek)
        self.__izmeni_button["state"] = NORMAL
        self.__brisi_button["state"] = NORMAL

    def izlaz(self):
        odgovor = messagebox.askokcancel("Lek", "Da li ste sigurni da želite da napustite aplikaciju? :(", icon="warning")
        if odgovor:
            self.destroy()

    @property
    def otkazano(self):
        return self.__otkazano

    @property
    def podaci(self):
        return self.__podaci

    @property
    def pretraga_text(self):
        return self.__pretraga_text

    @pretraga_text.setter
    def pretraga_text(self, pre):
        self.__pretraga_text = pre

    def __init__(self, master, podaci):
        super().__init__(master)
        self.__otkazano = True
        self.__podaci = podaci

        self.__lek_listbox = Listbox(self, activestyle="none", bg="#efefef")
        self.__lek_listbox.pack(side=LEFT, fill=BOTH, expand=1)
        self.__lek_listbox.bind("<<ListboxSelect>>", self.selekcija)

        pretraga_frame = Frame(self, borderwidth=2, relief="ridge", bg="#A9CFA5")
        pretraga_frame.pack(side=LEFT, fill=BOTH, expand=1)
        self.__pretraga_text = Text(pretraga_frame, height=1, width=50)
        Label(pretraga_frame, text="Pretraga: ", font=("Comic Sans MS", 12),  fg="#FFFFFF", bg="#A9CFA5").grid(row=0, sticky=W)
        self.__pretraga_text.grid(row=0, column=1, sticky=E)
        self.__pretraga_text.bind("<KeyRelease>", self.pretraga)

        lek_frame = Frame(self, borderwidth=2, relief="ridge", padx=30, pady=30, bg="#A9CFA5")
        lek_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        self.__JKL_labela = Label(lek_frame)
        self.__naziv_labela = Label(lek_frame)
        self.__proizvodjac_labela = Label(lek_frame)
        self.__tip_labela = Label(lek_frame)

        red = 0
        Label(lek_frame, text="JKL: ", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(lek_frame, text="Naziv leka: ", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(lek_frame, text="Naziv proizvođaca leka: ", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(lek_frame, text="Tip leka: ", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)

        red = 0
        kolona = 1
        self.__JKL_labela.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__naziv_labela.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__proizvodjac_labela.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__tip_labela.grid(row=red, column=kolona, sticky=W)

        self.__dodaj_button = Button(pretraga_frame, text="Dodaj lek", font=("Century Gothic", 11, "bold"), width=15, height=2, command=self.dodaj)
        self.__izmeni_button = Button(pretraga_frame, text="Izmeni lek", font=("Century Gothic", 11, "bold"), width=15, height=2, state=DISABLED, command=self.izmeni)
        self.__brisi_button = Button(pretraga_frame, text="Obriši lek", font=("Century Gothic", 11, "bold"), width=15, height=2, state=DISABLED, command=self.obrisi)

        red = 1
        kolona = 0
        self.__dodaj_button.grid(row=red, column=kolona)
        kolona = kolona + 1
        self.__izmeni_button.grid(row=red, column=kolona)
        kolona = kolona + 1
        self.__brisi_button.grid(row=red, column=kolona)

        self.popuni_listbox(self.__podaci.lek)
        self.protocol("WM_DELETE_WINDOW", self.izlaz)
        self.title("Lek")
        self.iconbitmap("logo.ico")
        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self.transient(master)


class DodajIzmeniLek(Toplevel):

    def jkl_validacija(self):
        jkl = self.__JKL.get()
        if len(jkl) != 7:
            messagebox.showerror("Greška!", "Jedinstvena klasifikacija leka (JKL) mora sadržati 7 karaktera!")
            return None
        else:
            for lek in self.__podaci.lek:
                if jkl == lek.JKL:
                    messagebox.showerror("Greška!", "Ova JKL već postoji!")
                    return None
        return jkl

    def naziv_validacija(self):
        naziv = self.__naziv.get()
        if len(naziv) < 2:
            messagebox.showerror("Greška!", "Naziv mora sadržati bar dva karaktera!")

            return None
        return naziv

    def proizvodjac_validacija(self):
        proizvodjac = self.__prozivodjac.get()
        if len(proizvodjac) < 2:
            messagebox.showerror("Greška!", "Proizvođac mora sadržati bar dva karaktera!")

            return None
        return proizvodjac

    def tip_validacija(self):
        tip = self.__tip.get()
        if len(tip) < 2:
            messagebox.showerror("Greška!", "Tip leka mora sadržati bar dva karaktera!")

            return None
        return tip

    @property
    def otkazano(self):
        return self.__otkazano

    @property
    def podaci(self):
        return self.__podaci

    @property
    def JKL(self):
        return self.__JKL

    @property
    def naziv(self):
        return self.__naziv

    @property
    def proizvodjac(self):
        return self.__prozivodjac

    @property
    def tip(self):
        return self.__tip

    @property
    def JKL_entry(self):
        return self.__JKL_entry

    @property
    def ok_button(self):
        return self.__ok_button

    def izlaz(self):
        odgovor = messagebox.askokcancel("Izlaz", "Da li ste sigurni da želite da napustite aplikaciju? :(", icon="warning")
        if odgovor:
            self.destroy()

    def ok(self):
        odgovor = messagebox.askokcancel("Potvrda", "Da li ste sigurni?", icon="warning")
        if odgovor:
            self.config(cursor="wait")
            self.update()
            self.podaci.sacuvaj_se()
            self.config(cursor="")

            self.__otkazano = False
            self.destroy()

    def __init__(self, master, podaci):
        super().__init__(master)
        self.__otkazano = True
        self.__podaci = podaci

        self.__JKL = StringVar(master)
        self.__naziv = StringVar(master)
        self.__prozivodjac = StringVar(master)
        self.__tip = StringVar(master)

        lek_frame = Frame(self, padx=10, pady=10, bg="#A9CFA5")
        lek_frame.pack(expand=1)

        self.__JKL_entry = Entry(lek_frame, width=30, textvariable=self.__JKL)
        self.__naziv_entry = Entry(lek_frame, width=30, textvariable=self.__naziv)
        self.__proizvodjac_entry = Entry(lek_frame, width=30, textvariable=self.__prozivodjac)
        self.__tip_entry = Entry(lek_frame, width=30, textvariable=self.__tip)

        self.__ok_button = Button(lek_frame, font=("Century Gothic", 11, "bold"), width=10, command=self.ok)
        self.__izlaz = Button(lek_frame, text="Izlaz", font=("Century Gothic", 11, "bold"), width=10, command=self.izlaz)

        red = 0
        Label(lek_frame, text="JKL: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(lek_frame, text="Naziv: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(lek_frame, text="Naziv proizvođača leka: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(lek_frame, text="Tip leka: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)

        red = 0
        kolona = 1
        self.__JKL_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__naziv_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__proizvodjac_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__tip_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__ok_button.grid(row=red, column=0, sticky=E)
        self.__izlaz.grid(row=red, column=1, sticky=W)

        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self.focus_force()
        self.grab_set()
        self.transient(master)


class DodajLek(DodajIzmeniLek):

    def izlaz(self):
        odgovor = messagebox.askokcancel("Dodaj lek", "Da li ste sigurni da želite da napustite aplikaciju? :(", icon="warning")
        if odgovor:
            self.destroy()

    def ok(self):
        jkl = self.jkl_validacija()
        if not jkl:
            return
        naziv = self.naziv_validacija()
        if not naziv:
            return
        proizvodjac = self.proizvodjac_validacija()
        if not proizvodjac:
            return
        tip = self.tip_validacija()
        if not tip:
            return

        lek = Lek(jkl, naziv, proizvodjac, tip)
        self.podaci.dodaj_lek(lek)
        super().ok()

    def __init__(self, master, podaci):
        super().__init__(master, podaci)
        self.ok_button["text"] = "Dodaj"
        self.iconbitmap("logo.ico")
        self.title("Dodavanje leka")


class IzmeniLek(DodajIzmeniLek):

    def izlaz(self):
        odgovor = messagebox.askokcancel("Izmeni lek", "Da li ste sigurni da želite da napustite aplikaciju? :(", icon="warning")
        if odgovor:
            self.destroy()

    def ok(self):
        naziv = self.naziv_validacija()
        if not naziv:
            return
        proizvodjac = self.proizvodjac_validacija()
        if not proizvodjac:
            return
        tip = self.tip_validacija()
        if not tip:
            return

        self.__lek.naziv = naziv
        self.__lek.proizvodjac = proizvodjac
        self.__lek.tip = tip
        super().ok()

    def __init__(self, master, podaci, lek):
        super().__init__(master, podaci)

        self.__lek = lek
        self.JKL.set(self.__lek.JKL)
        self.naziv.set(self.__lek.naziv)
        self.proizvodjac.set(self.__lek.proizvodjac)
        self.tip.set(self.__lek.tip)
        self.JKL_entry["state"] = DISABLED

        self.ok_button["text"] = "Izmeni"
        self.iconbitmap("logo.ico")
        self.title("Izmena lek")


class ReceptProzor(Toplevel):

    @property
    def otkazano(self):
        return self.__otkazano

    @property
    def podaci(self):
        return self.__podaci

    @property
    def pacijent_comobox(self):
        return self.__pacijent_comobox

    def dodaj(self):
        index = self.__pacijent_comobox.current()
        pa = self.__podaci.pacijent[index]
        dodaj = DodajRecept(self, self.__podaci, pa)
        self.wait_window(dodaj)
        if dodaj.otkazano:
            return

        recept = self.__podaci.recept[-1]  # poslednji sa liste
        self.__recept_listbox.insert(END, recept.izvestaj)
        self.__recept_listbox.select_set(END)
        self.selekcija()

    def obrisi(self):

        if messagebox.askquestion("Upozorenje!", "Da li ste sigurni da želite da obrišete recept?", icon="warning") == "no":
            return
        index = self.__recept_listbox.curselection()[0]
        self.__podaci.obrisi_recept(index)

        self.config(cursor="wait")
        self.update()
        self.__podaci.sacuvaj_se()
        self.config(cursor="")

        self.__recept_listbox.delete(index)
        self.__recept_listbox.select_set(index)
        self.selekcija()

    def izmeni(self):
        index = self.__recept_listbox.curselection()[0]
        recept = self.__podaci.recept[index]
        izmena = IzmeniRecept(self, self.__podaci, recept)
        self.wait_window(izmena)
        if izmena.otkazano:
            return

        self.__recept_listbox.delete(index)  # trenutni
        self.__recept_listbox.insert(index, recept.izvestaj)
        self.__recept_listbox.select_set(index)
        self.selekcija()

    def izlaz(self):
        odgovor = messagebox.askokcancel("Recept", "Da li ste sigurni da želite da napustite aplikaciju? :(", icon="warning")
        if odgovor:
            self.destroy()

    def trenutni(self, event=None):

        index = self.__pacijent_comobox.current()
        if index < 0:
            self.__dodaj_button["state"] = DISABLED
        else:
            self.__dodaj_button["state"] = NORMAL
            pa = self.__podaci.pacijent[index]
            print(pa)
            self.popuni_listbox(pa)

    def popuni_listbox(self, pa):
        recepti = self.__podaci.recept
        self.__recept_listbox.delete(0, END)
        self.__recept_listbox.selection_clear(0, END)
        for recept in recepti:
            if recept.pacijent == pa:
                print(recept)
                self.__recept_listbox.insert(END, recept.izvestaj)
            else:
                self.__recept_listbox.insert(END, "")

    def ocisti_labele(self):
        self.__imeprezime_label["text"] = ""
        self.__lek_label["text"] = ""
        self.__lekar_label["text"] = ""
        self.__datum_label["text"] = ""
        self.__kolicina_label["text"] = ""
        self.__izvestaj_label["text"] = ""

    def popuni_labele(self, recept):
        self.__imeprezime_label["text"] = recept.pacijent.ime
        self.__lek_label["text"] = recept.lek.naziv
        self.__lekar_label["text"] = recept.lekar.ime
        self.__datum_label["text"] = recept.datum_i_vreme.strftime("%d.%m.%Y. %H:%M:%S")
        self.__kolicina_label["text"] = recept.kolicina
        self.__izvestaj_label["text"] = recept.izvestaj

    def selekcija(self, event=None):
        if not self.__recept_listbox.curselection():
            self.ocisti_labele()
            self.__izmeni_button["state"] = DISABLED
            self.__brisi_button["state"] = DISABLED
            return
        indeks = self.__recept_listbox.curselection()[0]
        recept = self.__podaci.recept[indeks]
        self.__recept_listbox.select_set(indeks)
        self.__izmeni_button["state"] = NORMAL
        self.__brisi_button["state"] = NORMAL
        self.popuni_labele(recept)

    def __init__(self, master, podaci):
        super().__init__(master)
        self.__podaci = podaci
        self.__otkazano = True

        pacijent_frame = Frame(self,  borderwidth=4, relief="ridge", bg="#A9CFA5")
        pacijent_frame.pack(side=TOP, fill=BOTH, expand=1)

        self.__recept_listbox = Listbox(self, activestyle="none", bg="#efefef")
        self.__recept_listbox.pack(side=LEFT, fill=BOTH, expand=1)
        self.__recept_listbox.bind("<<ListboxSelect>>", self.selekcija)

        recept_frame = Frame(self,  borderwidth=2, relief="ridge", bg="#A9CFA5")
        recept_frame.pack(side=RIGHT, fill=BOTH, expand=1)

# COMBOX

        pacijenti = []
        for pacijent in self.__podaci.pacijent:
            pacijenti.append(pacijent.ime + " " + pacijent.prezime)

        self.__pacijent_comobox = Combobox(pacijent_frame,  state="readonly", values=pacijenti)

        if len(pacijenti) > 0:
            self.__pacijent_comobox.current(0)

        self.__pacijent_comobox.grid(row=0, column=0)
        self.__pacijent_comobox.bind("<<ComboboxSelected>>", self.trenutni)
# LABELI
        self.__imeprezime_label = Label(recept_frame)
        self.__lek_label = Label(recept_frame)
        self.__lekar_label = Label(recept_frame)
        self.__datum_label = Label(recept_frame)
        self.__kolicina_label = Label(recept_frame)
        self.__izvestaj_label = Label(recept_frame)

        red = 0
        Label(recept_frame, text="Ime: ", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(recept_frame, text="Lek: ", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(recept_frame, text="Lekar: ", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(recept_frame, text="Datum: ", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(recept_frame, text="Količina: ", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(recept_frame, text="Izveštaj: ", font=("Century Gothic", 11, "bold"), fg="#EFEFEF", bg="#A9CFA5").grid(row=red, sticky=E)

        red = 0
        kolona = 1
        self.__imeprezime_label.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__lek_label.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__lekar_label.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__datum_label.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__kolicina_label.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__izvestaj_label.grid(row=red, column=kolona, sticky=W)

        self.__dodaj_button = Button(pacijent_frame, text="Dodaj recept", font=("Century Gothic", 8, "bold"), width=12, state=DISABLED, command=self.dodaj)
        self.__izmeni_button = Button(pacijent_frame, text="Izmeni recept", font=("Century Gothic", 8, "bold"), width=12, state=DISABLED, command=self.izmeni)
        self.__brisi_button = Button(pacijent_frame, text="Obriši recept", font=("Century Gothic", 8, "bold"), width=12, state=DISABLED, command=self.obrisi)

        red = 0
        kolona = 1
        self.__dodaj_button.grid(row=red, column=kolona)
        kolona = kolona + 1
        self.__izmeni_button.grid(row=red, column=kolona)
        kolona = kolona + 1
        self.__brisi_button.grid(row=red, column=kolona)

        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)

        self.protocol("WM_DELETE_WINDOW", self.izlaz)
        self.title("Recept")
        self.iconbitmap("logo.ico")
        self.focus_force()
        self.grab_set()
        self.transient(master)


class DodajIzmeniRecept(Toplevel):

    def lekar_validacija(self):
        indeks = self.__lekar_combobox.current()
        if indeks < 0:
            messagebox.showerror("Greška!", "Lekar nije odabran!")
            return None
        indeks = self.__lekar_combobox.current()
        lekar = self.podaci.lekar[indeks]
        return lekar

    def lek_validacija(self):
        indeks = self.__lek_combobox.current()
        if indeks < 0:
            messagebox.showerror("Greška!", "Lek nije odabran!")
            return None

        indeks = self.__lek_combobox.current()
        lek = self.podaci.lek[indeks]
        return lek

    @property
    def otkazano(self):
        return self.__otkazano

    @property
    def podaci(self):
        return self.__podaci

    @property
    def datum(self):
        return self.__datum

    @property
    def izvestaj(self):
        return self.__izvestaj

    @property
    def kolicina(self):
        return self.__kolicina

    @property
    def lekar_combobox(self):
        return self.__lekar_combobox

    @property
    def lek_combobox(self):
        return self.__lek_combobox

    @property
    def datum_entry(self):
        return self.__datum_entry

    @property
    def izvestaj_entry(self):
        return self.__izvestaj_entry

    @property
    def kolicina_entry(self):
        return self.__kolicina_entry

    @property
    def ok_button(self):
        return self.__ok_button

    def izlaz(self):
        odgovor = messagebox.askokcancel("Izlaz", "Da li ste sigurni da želite da napustite aplikaciju? :(", icon="warning")
        if odgovor:
            self.destroy()

    def ok(self):
        odgovor = messagebox.askokcancel("Potvrda", "Da li ste sigurni?", icon="warning")
        if odgovor:
            self.config(cursor="wait")
            self.update()
            self.podaci.sacuvaj_se()
            self.config(cursor="")
            self.__otkazano = False
            self.destroy()

    def __init__(self, master, podaci):
        super().__init__(master)
        self.__otkazano = True
        self.__podaci = podaci

        lekar = []
        for lekari in self.__podaci.lekar:
            lekar.append(lekari.ime)

        lek = []
        for leko in self.__podaci.lek:
            lek.append(leko.naziv)

        recept_frame = Frame(self, padx=10, pady=10, bg="#A9CFA5")
        recept_frame.pack(expand=1)

        self.__datum = StringVar(master)
        self.__izvestaj = StringVar(master)
        self.__kolicina = DoubleVar(master)

        self.__datum_entry = Entry(recept_frame, width=30, textvariable=self.__datum)
        self.__kolicina_entry = Entry(recept_frame, width=30, textvariable=self.__kolicina)
        self.__izvestaj_entry = Entry(recept_frame, width=30, textvariable=self.__izvestaj)

        self.__ok_button = Button(recept_frame, font=("Century Gothic", 11, "bold"), width=10, command=self.ok)
        self.__izlaz = Button(recept_frame, text="Izlaz", font=("Century Gothic", 11, "bold"), width=10, command=self.izlaz)

        self.__lekar_combobox = Combobox(recept_frame, state="readonly", values=lekar)
        self.__lek_combobox = Combobox(recept_frame, state="readonly", values=lek)

        if len(lek) > 0:
            self.__lek_combobox.current(0)
        if len(lekar) > 0:
            self.__lekar_combobox.current(0)
        red = 0
        Label(recept_frame, text="Datum i vreme: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(recept_frame, text="Izveštaj: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(recept_frame, text="Količina: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(recept_frame, text="Lekar: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)
        red = red + 1
        Label(recept_frame, text="Lek: ", font=("Century Gothic", 11, "bold"), bg="#A9CFA5").grid(row=red, sticky=E)

        red = 0
        kolona = 1
        self.__datum_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__izvestaj_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__kolicina_entry.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__lekar_combobox.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__lek_combobox.grid(row=red, column=kolona, sticky=W)
        red = red + 1
        self.__ok_button.grid(row=red, column=0, sticky=E)
        self.__izlaz.grid(row=red, column=1, sticky=W)

        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)

        self.focus_force()
        self.grab_set()
        self.transient(master)


class DodajRecept(DodajIzmeniRecept):

    def izlaz(self):
        odgovor = messagebox.askokcancel("Izmeni recept", "Da li ste sigurni da želite da napustite aplikaciju? :(", icon="warning")
        if odgovor:
            self.destroy()

    def ok(self):
        lek = self.lek_validacija()
        if not lek:
            return
        lekar = self.lekar_validacija()
        if not lekar:
            return

        recept = Recept(self.__pacijent, lekar, lek)
        self.podaci.dodaj_recept(recept)
        super().ok()

    def __init__(self, master, podaci, pa):
        super().__init__(master, podaci)
        self.__pacijent = pa

        self.datum.set(datetime.now())
        self.izvestaj.set(uuid.uuid4())
        self.kolicina.set("4")

        self.datum_entry["state"] = DISABLED
        self.izvestaj_entry["state"] = DISABLED
        self.kolicina_entry["state"] = DISABLED

        self.ok_button["text"] = "Dodaj"
        self.iconbitmap("logo.ico")
        self.title("Dodavanje recepta")


class IzmeniRecept(DodajIzmeniRecept):

    def izlaz(self):
        odgovor = messagebox.askokcancel("Izmeni recept", "Da li ste sigurni da želite da napustite aplikaciju? :(", icon="warning")
        if odgovor:
            self.destroy()

    def ok(self):
        lek = self.lek_validacija()
        if not lek:
            return

        lekar = self.lekar_validacija()
        if not lekar:
            return
        self.__recept.lekar = lekar
        self.__recept.lek = lek
        self.__recept.datum = datetime.now()
        super().ok()

    def __init__(self, master, podaci, recept):
        super().__init__(master, podaci)
        self.__recept = recept
        self.datum.set(self.__recept.datum_i_vreme)
        self.izvestaj.set(self.__recept.izvestaj)
        self.kolicina.set(self.__recept.kolicina)

        lekari = self.podaci.lekar

        for indeks in range(len(lekari)):
            lekar = lekari[indeks]
            if lekar == recept.lekar:
                self.lekar_combobox.current(indeks)
                break

        leko = self.podaci.lek
        for ind in range(len(leko)):
            lek = leko[ind]
            if lek == recept.lek:
                self.lek_combobox.current(ind)
                break

        self.datum_entry["state"] = DISABLED
        self.izvestaj_entry["state"] = DISABLED
        self.kolicina_entry["state"] = DISABLED

        self.ok_button["text"] = "Izmeni"
        self.iconbitmap("logo.ico")
        self.title("Izmena recepta")


def main():
    podaci = Podaci.ucitaj()
    prozor = GlavniProzor(podaci)
    prozor.iconbitmap("logo.ico")
    prozor.title("Pharmacy")
    prozor.mainloop()


main()
