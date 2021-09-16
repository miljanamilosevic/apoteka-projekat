from datetime import datetime
import pickle
import uuid


class Korisnik:
    def __init__(self, JMBG, ime, prezime, datum_rodjenja):
        self.__JMBG = JMBG
        self.__ime = ime
        self.__prezime = prezime
        self.__datum_rodjenja = datum_rodjenja

    @property
    def JMBG(self):
        return self.__JMBG

    @JMBG.setter
    def JMBG(self, new_JMBG):
        self.__JMBG = new_JMBG

    @property
    def ime(self):
        return self.__ime

    @ime.setter
    def ime(self, new_ime):
        self.__ime = new_ime

    @property
    def prezime(self):
        return self.__prezime

    @prezime.setter
    def prezime(self, new_prezime):
        self.__prezime = new_prezime

    @property
    def datum_rodjenja(self):
        return self.__datum_rodjenja

    @datum_rodjenja.setter
    def datum_rodjenja(self, new_datum_rodjenja):
        self.__datum_rodjenja = new_datum_rodjenja

    __tekuca_godina = datetime.now().year

    def starost(self):
        # return self.__tekuca_godina - self.__datum_rodjenja
        return "17"

    def __str__(self):
        format_linije = "{:>20} {}"
        return "\n".join([
            "",
            format_linije.format("JMBG: ", self.__JMBG),
            format_linije.format("Ime: ", self.__ime),
            format_linije.format("Prezime: ", self.__prezime),
            format_linije.format("Datum rođenja: ", self.__datum_rodjenja),
            format_linije.format("Starost: ", self.starost())
        ])


class Pacijent(Korisnik):

    def __init__(self, JMBG, ime, prezime, datum_rodjenja, LBO):
        super().__init__(JMBG, ime, prezime, datum_rodjenja)
        self.__LBO = LBO
        #self.__recepti = recepti

    @property
    def LBO(self):
        return self.__LBO

    @LBO.setter
    def LBO(self, new_LBO):
        self.__LBO = new_LBO

    def __str__(self):
        format_linije = "{:>20} {}"
        return "\n".join([
            super().__str__(),
            format_linije.format("LBO: ", self.__LBO)])


class Lekar(Korisnik):

    def __init__(self, JMBG, ime, prezime, datum_rodjenja, specijalizacja):
        super().__init__(JMBG, ime, prezime, datum_rodjenja)
        self.__specijalizacija = specijalizacja

    @property
    def specijalizacija(self):
        return self.__specijalizacija

    @specijalizacija.setter
    def specijalizacija(self, new_specijalizacija):
        self.__specijalizacija = new_specijalizacija

    def __str__(self):
        format_linije = "{:>20} {}"
        return "\n".join([
            super().__str__(),
            format_linije.format("Specijalizacija: ", self.__specijalizacija)])


class Recept:

    def __init__(self, pacijent, lekar, lek):
        self.__izvestaj = uuid.uuid4()
        self.__kolicina = 1
        self.__datum_i_vreme = datetime.now()
        self.__pacijent = pacijent
        self.__lekar = lekar
        self.__lek = lek

    @property
    def izvestaj(self):
        return self.__izvestaj

    @izvestaj.setter
    def izvestaj(self, izvestaj):
        self.__izvestaj = izvestaj

    @property
    def kolicina(self):
        return self.__kolicina

    @kolicina.setter
    def kolicina(self, kolicina):
        self.__kolicina = kolicina

    @property
    def datum_i_vreme(self):
        return self.__datum_i_vreme

    @datum_i_vreme.setter
    def datum_i_vreme(self, datum):
        self.__datum_i_vreme = datum

    @property
    def pacijent(self):
        return self.__pacijent

    @property
    def lekar(self):
        return self.__lekar

    @lekar.setter
    def lekar(self, lekar):
        self.__lekar = lekar

    @property
    def lek(self):
        return self.__lek

    @lek.setter
    def lek(self, lek):
        self.__lek = lek

    def sadrzi(self, pacijent):
        print(self.__pacijent)
        return pacijent == self.__pacijent

    def sadrziLekar(self, lekar):
        return lekar == self.__lekar

    def sadrziLek(self, lek):
        return lek == self.__lek

    def __str__(self):
        format_linije = "{:>13}: {}"
        return "\n".join([
            "",
            format_linije.format("Izvestaj", self.__izvestaj),
            format_linije.format("Datum i vreme", self.__datum_i_vreme.strftime("%d.%m.%Y. %H:%M:%S")),
            format_linije.format("Pacijent", self.__pacijent.ime + " " + self.__pacijent.prezime),
            format_linije.format("Lekar", self.__lekar.ime + " " + self.__lekar.prezime),
            format_linije.format("Lek", self.__lek.naziv),
            format_linije.format("Kolicina", self.__kolicina)
        ])


class Lek:
    def __init__(self, JKL, naziv, proizvodjac, tip):
        self.__JKL = JKL
        self.__naziv = naziv
        self.__proizvodjac = proizvodjac
        self.__tip = tip

    @property
    def JKL(self):
        return self.__JKL

    @JKL.setter
    def JKL(self, new_JKL):
        self.__JKL = new_JKL

    @property
    def naziv(self):
        return self.__naziv

    @naziv.setter
    def naziv(self, new_naziv):
        self.__naziv = new_naziv

    @property
    def proizvodjac(self):
        return self.__proizvodjac

    @proizvodjac.setter
    def proizvodjac(self, new_proizvodjac):
        self.__proizvodjac = new_proizvodjac

    @property
    def tip(self):
        return self.__tip

    @tip.setter
    def tip(self, new_tip):
        self.__tip = new_tip

    def __str__(self):
        format_linije = "{:>17} {}"
        return "\n".join([
            "",
            format_linije.format("JKL: ", self.__JKL),
            format_linije.format("Naziv: ", self.__naziv),
            format_linije.format("Proizvodjac: ", self.__proizvodjac),
            format_linije.format("Tip leka: ", self.__tip)
        ])


class Podaci:

    def __init__(self):
        self.__pacijent = []
        self.__lekar = []
        self.__recept = []
        self.__lek = []

    @property
    def pacijent(self):
        return self.__pacijent

    @pacijent.setter
    def pacijent(self, pacijent):
        self.__pacijent = pacijent

    @property
    def lekar(self):
        return self.__lekar

    @property
    def recept(self):
        return self.__recept

    @property
    def lek(self):
        return self.__lek
# PACIJENT

    def dodaj_pacijenta(self, pacijent):
        self.__pacijent.append(pacijent)

    def obrisi_pacijenta(self, index):
        pacijent = self.__pacijent.remove(index)
        print(pacijent)
        brisanjeR = []
        for recept in self.__recept:
            print(recept)
            if recept.sadrzi(pacijent):
                print(recept)
                brisanjeR.append(recept)

        if len(brisanjeR) != 0:
            for recept in brisanjeR:
                self.__recept.remove(recept)
# LEKAR

    def dodaj_lekara(self, lekar):
        self.__lekar.append(lekar)

    def obrisi_lekara(self, index):
        lekar = self.__lekar.remove(index)
        brisanjeR = []
        for recept in self.__recept:
            if recept.sadrziL(lekar):
                brisanjeR.append(recept)
            else:
                brisanjeR = []
        if len(brisanjeR) != 0:
            for recept in brisanjeR:
                self.__recept.remove(recept)

# LEK

    def dodaj_lek(self, lek):
        self.__lek.append(lek)

    def obrisi_lek(self, index):
        lek = self.__lek.remove(index)
        brisanjeR = []
        for recept in self.__recept:
            if recept.sadrziLK(lek):
                brisanjeR.append(recept)
            else:
                brisanjeR = []
        if len(brisanjeR) != 0:
            for recept in brisanjeR:
                self.__recept.remove(recept)
# RECEPT

    def dodaj_recept(self, recept):
        self.__recept.append(recept)

    def obrisi_recept(self, index):
        recept = self.__recept.pop(index)

    @classmethod
    def napravi_pocetne(cls):
        podaci = Podaci()

        pacijent = podaci.pacijent
        pacijent.append(Pacijent("1112354789663", "Petar", "Miletić", "22.11.2005", "11123547896"))
        pacijent.append(Pacijent("1904016727816", "Srna", "Miletić", "19.04.2016.", "19040167278"))
        pacijent.append(Pacijent("2605001456827", "Lena", "Stanković", "26.05.2001.", "26050014568"))
        pacijent.append(Pacijent("1406001727212", "Milica", "Tomić", "14.06.2001.", "14060017272"))
        pacijent.append(Pacijent("1203001727123", "Mina", "Rajić", "12.03.2001.", "12030017271"))
        pacijent.append(Pacijent("2001005727153", "Ksenija", "Rašić", "20.01.2005.", "20010057271"))
        pacijent.append(Pacijent("1505000722217", "Nikola", "Rašić", "15.05.2000.", "22069997231"))
        pacijent.append(Pacijent("1010000730016", "Mladen", "Mladenović", "10.10.2000.", "12345698521"))
        pacijent.append(Pacijent("0405000735027", "Anđela", "Stanković", "04.05.2000.", "14785236521"))
        pacijent.append(Pacijent("2901002727816", "Miljana", "Milošević", "29.01.2002.", "20010148271"))
        pacijent.append(Pacijent("2712001727211", "Milica", "Aranđelović", "27.12.2001.", "52485236512"))
        pacijent.append(Pacijent("1708001727210", "Jelena", "Stanković", "17.08.2001.", "15236549852"))

        lek = podaci.lek
        lek.append(Lek("1135287", "DAYLETTE", "Gedeon Richter PLC", "Hormonska kontracepcija (Z30)"))
        lek.append(Lek("1071720", "BROMAZEPAM HF", "Hemofarm a.d", "-"))
        lek.append(Lek("0051845", "VITAMIN C", "Galenika a.d. Beograd", "-"))
        lek.append(Lek("0051351", "BEDOXIN", "Galenika a.d", "-"))
        lek.append(Lek("0140150", "OXYTOCIN SYNTHETIC", "Gedeon Richter PLC ", "-"))
        lek.append(Lek("1162442", "DIKLOFEN", "Galenika a.d.", "-"))
        lek.append(Lek("0086418", "ANALGIN", "Alkaloid a.d", "-"))
        lek.append(Lek("0086930", "PARACETAMOL", "PharmaSwiss d.o.o", "-"))
        lek.append(Lek("0071123", "BENSEDIN", "Galenika a.d", "-"))
        lek.append(Lek("0070138", "TREVICTA", "Janssen Pharmaceutica N.V.",
                       "Shizofrenija, shizotipski poremećaji i poremećaji sa sumanutošću (F20-F29)"))
        lek.append(Lek("2087506", "METADON", "Alkaloid a.d. ",
                       "Lečenje zavisnosti od opijata (F11). Suzbijanje snažnog bola(C00-C97"))
        lek.append(
            Lek("1124532", "ONDASAN", "Slaviamed d.o.o", "Za suzbijanje mučnine i povraćanja uz radio i hemioterapiju"))
        lek.append(Lek("N06AB06", "ZOLOFT", "Haupt Pharma Latina S.R.L.",
                       "Depresivni i anksiozni poremećaji,Agorafobija, OKP, PTSD"))
        lek.append(Lek("G03DC02", "PRIMOLUT", "Bayer Weimar GMBH&CO.KG",
                       "Disfunkcionalno krvarenje, amenoreja, PMS, odlaganje menstruacije, endometrioza."))
        lek.append(Lek("M01AE01", "BRUFEN", "Famar A.V.E. Anthoussa Plant", "Za uklanjanje blagih do umerenih bolova."))

        lekar = podaci.lekar
        lekar.append(Lekar("1703956727816", "Slavica", "Avramelović", "17.3.1976.", "Pedijatrija"))
        lekar.append(Lekar("0404979727112", "Gordana", "Vukašinović", "04.04.1979.", "Neurologija"))
        lekar.append(Lekar("0110966727145", "Verica", "Ivanovski", "01.10.1966.", "Ginekologija i akušerstvo"))
        lekar.append(Lekar("0101982727336", "Sofka", "Jeremić", "01.01.1982.", "Neuropsihijatrija"))
        lekar.append(Lekar("01121962727452", "Nevenka", "Jovičić", "01.12.1962.", "Fizikalna medicina i rehabilitacija"))
        lekar.append(Lekar("2107977722561", "Vuk", "Kadić", "21.07.1977.", "Radiologija"))
        lekar.append(Lekar("3001965722564", "Jovan", "Mladenović", "30.01.1965.", "Epidemiologija"))
        lekar.append(Lekar("2807972722456", "Vladimir", "Maričić", "25.07.1972.", "Otorinolaringologija"))
        lekar.append(Lekar("0504988727365", "Vesna", "Marjanović", "05.04.1988.", "Anesteziologija sa reanimatologijom"))
        lekar.append(Lekar("0209960727123", "Dragica", "Milovanović", "02.09.1960.", "Oftalmologija"))
        lekar.append(Lekar("2903975722756", "Zvonko", "Radosavljević", "29.03.1975.", "Opšta hirurgija"))
        lekar.append(Lekar("2506963727453", "Biljana", "Tomić", "25.06.1963.", "Urgentna medicina"))

        recept = podaci.recept
        recept.append(Recept(pacijent[4], lekar[2], lek[0]))
        recept.append(Recept(pacijent[1], lekar[0], lek[2]))
        return podaci

    __naziv_datoteke = "podaci.txt"

    @classmethod
    def sacuvaj(cls, podaci):
        datoteka = open(cls.__naziv_datoteke, "wb")
        pickle.dump(podaci, datoteka)
        datoteka.close()

    @classmethod
    def ucitaj(cls):
        try:
            datoteka = open(cls.__naziv_datoteke, "rb")
            podaci = pickle.load(datoteka)
            datoteka.close()
        except FileNotFoundError:
            return Podaci.napravi_pocetne()

        return podaci

    def sacuvaj_se(self):
        self.sacuvaj(self)


def test():
    podaci = Podaci.napravi_pocetne()
    print()
    print("Čuvanje...")
    Podaci.sacuvaj(podaci)
    print("Učitavanje...")
    podaci = Podaci.ucitaj()
    recept = podaci.recept

    for recept in recept:
        print(recept)


if __name__ == "__main__":
     test()