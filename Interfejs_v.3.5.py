# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 20:38:53 2021

@author: Jarek, Patrycja
"""

import wx
import wx.grid
import os
from itertools import product
from random import sample
import numpy as np
from PIL import Image,ImageDraw
import pyautogui
import PIL
import random 
import time
import multiprocessing  as mp
from wx.adv import Animation, AnimationCtrl
import imageio

Parametry={
    "samotnosc" : 1, 
    "scisk" : 4, 
    'nadzieja': 3, 
    "ile_generacji" : 10 
    }

Konfiguracja={
    "klucz_zabezpieczający_slownik":"$*&*&*@002!",
    "klucz_zabezpieczający_zestaw":"6273##$2nnd!",
    "Klucz zabezpieczający_scenariusz":"**823$%@@7&*&*!",
    "Klucz zabezpieczający_symulacje":"SyMuLaCjA112!",
    "szer_kom":6
    }

Widzety_1920={
    "Start_pos":(200,815),
    "Start_size": (150,60),
    "Animancja_pos":(540,815),
    "Animancja_size":(150,60),
    "Obraz_pos":(40,10),
    "Okno_size":(900,950),
    
    "Lewo_pos":(50,760),
    "Lewo_size": (150,60),
    "Prawo_pos":(390,760),
    "Prawo_size":(150,60),
    "Okno_pomoc_size":(700,730),
    }

Widzety_1400={
    "Start_pos":(100,610),
    "Start_size": (100,30),
    "Animancja_pos":(440,610),
    "Animancja_size":(100,30),
    "Obraz_pos":(40,5),
    "Okno_size":(700,700),
    
    "Lewo_pos":(50,760),
    "Lewo_size": (150,60),
    "Prawo_pos":(390,760),
    "Prawo_size":(150,60),
    "Okno_pomoc_size":(700,730),
    }

Slownik_opisów={
    0: """
        Witaj użytkowniku, przed Tobą zapewne otworzyła się już nasza gra – Gra w życie.
        Czym jest w ogóle Gra w życie? Jest to automat komórkowy opracowany przez
        brytyjskiego matematyka Johna Conwaya w 1970 roku.
        Brzmi dosyć skomplikowanie? Nie martw się, zaraz wszystko Ci wytłumaczymy.
        
        Gra ta toczy się na skończonej planszy, podzielonej na kwadratowe komórki, 
        100 na 100 wiec jest ich aż 10 000. Aktualnie widzisz przed sobą pustą planszę 
        i kafelki z różnymi opcjami do wyboru.
        Każda komórka na naszej planszy ma 8 sąsiadów, przylegają do niej bokami i rogami.
        A każda taka komórka może znajdować się w jednym z dwóch stanów:
        może być „żywa” lub „martwa”. Stany komórek zmieniają się w pewnych jednostkach czasu,
        który następnie jest używany do obliczenia stanu wszystkich komórek w następnej jednostce.
        Po obliczeniu wszystkie komórki zmieniają swój stan dokładnie w tym samym momencie.
        
        Kiedy wiadomo, że komórka jest w stanie „życia”?
        W naszej wersji jest wtedy pokolorowana na czarno a jej dokładny stan
        zależy tylko i wyłącznie od liczby jej żywych sąsiadów. 
        
        Co ciekawe…w grze w życie nie ma graczy w dosłownym tego słowa znaczeniu,
        Twój udział sprowadza się jedynie do ustalenia stanu początkowego komórek. 
        
        Stan początkowy komórek opiera się na wzorcach, a dokładniej
        na regułach wymyślonych przez Conwaya, gdzie:
            
        • Martwa komórka, która ma dokładnie 3 żywych sąsiadów,
        staje się żywa w następnej jednostce czas
        • Żywa komórka z 2 albo 3 żywymi sąsiadami pozostaje nadal żywa; 
        przy innej liczbie sąsiadów umiera
        
        Pewnie się zastanawiasz, co dalej, jak masz zacząć?
        Specjalnie dla Ciebie stworzyliśmy instrukcję,
        więc usiądź wygodnie i baw się dobrze!""",
        
    1: """Zestawy:
        - Stwórz manualnie: Możliwość stworzenia własnego zestawu początkowego.
        1)	Otwarcie nowego okna „Rysowanie_zestawu”
        2)	Poruszanie po planszy: Z pomocą lewego przycisku myszki klikasz/przeciągasz
        myszkę na dowolną komórkę i z kombinacja przycisków shift + z tworzysz żywa komórkę,
        kombinacja shift + x możesz ją anulować/skasować. 
        3)	Zapisanie zestawu: Jeżeli chcesz zapisać zestaw,
        klikasz w „Zestawy” i zapisujesz, zapisa
        4)	Po zapisaniu, możesz spokojnie zamknąć okno i wrócić na interfejs główny.
        5)	Wczytanie: Jeżeli chcesz wczytać swój zapisany zestaw,
        na interfejsie głównym klikasz w „Zestawy”, następnie „Wczytaj”,
        wybierasz zestaw i gotowe.
        
        Zestaw komórek pojawia Ci się na planszy początkowej.
        
        - Wylosuj: Pojawia się losowy gotowy zestaw.
        
        1)	Możliwość zmiany wylosowanego zestawu po ponownym kliknięciu „Wylosuj”.
        2)	Zapisanie zestawu: Jeżeli chcesz zapisać zestaw, klikasz w „Zestawy” 
        i zapisujesz, zapisany zestaw ląduje w folderze w którym znajduję się zainstalowana gra. 
        
        - Stwórz ze zdjęcia: Wybranie gotowego zestawu zapisanego w formacie graficznym.

        1)	Przykładowe zestawy znajdują się w folderze gdzie została zainstalowana gra
        =
        Parametry:
            
        1)	Gra w życie posiada reguły, reguły te zostały zapisane
        pod nazwą parametry, ustalone przez autorów gry, ale…możesz je zmienić.
        2)	W Parametrach, kliknij zamień, pojawia się okienko w którym możesz 
        zmienić parametr dla „Samotność”, „Ścisk”, „Nadzieja”, „Ile generacji”
        3)	„Samotność” i „Ścisk”  – przy jakiej liczbie sąsiadów komórka umrze,
        ustalona przez autorów wynosi 1 i 4
        4)	„Nadzieja” -  przy jakiej ilości sąsiadów komórka ożyje przy następnej
        jednostce czasu, ustalona przez autorów wynosi 3
        5)	‘Ile generacji” – ile razy komórki żywe zmienią swój stan w jednostkach
        czasu, ustalona przez autorów wynosi 100, zalecane jest trzymanie ilości
        nie większej niż 100 i nie mniej niż 1
        """,
    2: """
        2. Symulacja i animacja.
    
        Mając stworzony manualnie, wylosowany lub stworzony ze zdjęcia zestaw,
        który wczytany został jako planszą początkowa możesz kliknąć przycisk „Symulacja”
        który odpowiada za pobranie pozycji komórek żywych i
        zapisanie ich w takiej formie aby mogła zostać stworzona Animacja.
        
        Po kliknięciu „Symulacja” musisz się uzbroić w cierpliwość i
        poczekać kilka sekund, po zakończeniu symulacji
        zostanie pokazany odpowiedni komunikat.
        
        Następnie klikasz „Animacja” powinien otworzyć się folder,
        w którym została zapisana symulacja pod nazwą „Symulacja.txt”
        po wybraniu pliku animacja zaczyna zostają pracę, 
        pod odczekaniu kolejnych kilku sekund na nowym oknie
        pojawia się animacja aktualnego zestawu. 
        
        Fajne prawda? A teraz kombinuj i baw się dobrze.
        """
    }

aktualny_widzet={}
aktualny_zestaw=[]

class Okno_interfejsu_glownego(wx.Frame):
    """
    Klasa głównego okna,stanowiąca trzon interfejsu programu.
    """
    def __init__(self,parent=None):
        """
        Konstruktor klasy Okno_interfejsu_glownego.
        """
        super(Okno_interfejsu_glownego,self).__init__(parent)
        self.intiUI()
        
    def intiUI(self):
        """
        Metoda odpowiadająca za formę i rozmieszczenie widżetow okna.
        """
        menubar=wx.MenuBar()
        self.SetMenuBar(menubar)
        panel=wx.Panel(self,wx.ID_ANY)
        k_zestawy=wx.Menu()
        
        zestawy_1=k_zestawy.Append(wx.ID_ANY,"Wczytaj")
        zestawy_2=k_zestawy.Append(wx.ID_ANY,"Zapisz")
        zestawy_3=k_zestawy.Append(wx.ID_ANY,"Stwórz manualnie") 
        zestawy_4=k_zestawy.Append(wx.ID_ANY,"Wylosuj") 
        zestawy_5=k_zestawy.Append(wx.ID_ANY,"Printuj")
        zestawy_6=k_zestawy.Append(wx.ID_ANY,"Stwórz ze zdjęcia")
        zestawy_7=k_zestawy.Append(wx.ID_ANY,"Zapisz podgląd")
        
        self.Bind(wx.EVT_MENU,self.wx_wczytaj_zestaw, zestawy_1)
        self.Bind(wx.EVT_MENU,self.wx_zapisz_zestaw, zestawy_2)
        self.Bind(wx.EVT_MENU,self.wx_zestaw_rysuj, zestawy_3)
        self.Bind(wx.EVT_MENU,self.wx_wylosuj_zestaw, zestawy_4)
        self.Bind(wx.EVT_MENU,self.wx_test_p_zestaw, zestawy_5)
        self.Bind(wx.EVT_MENU,self.wx_zestaw_ze_zdj ,zestawy_6)
        self.Bind(wx.EVT_MENU,self.wx_zapisz_podglad_zestawy,zestawy_7)
        menubar.Append(k_zestawy,"Zestawy")
        
        k_parametry=wx.Menu()
        parametry_1=k_parametry.Append(wx.ID_ANY, "Wczytaj")
        parametry_2=k_parametry.Append(wx.ID_ANY, "Zapisz")
        parametry_3=k_parametry.Append(wx.ID_ANY, "Zmień")
        parametry_4=k_parametry.Append(wx.ID_ANY,"Printuj")
        self.Bind(wx.EVT_MENU, self.wx_wczytaj_parametry, parametry_1)
        self.Bind(wx.EVT_MENU, self.wx_zapisz_parametry, parametry_2)
        self.Bind(wx.EVT_MENU, self.wx_zmień_parametry, parametry_3)
        self.Bind(wx.EVT_MENU, self.wx_test_p_parametry, parametry_4)
        menubar.Append(k_parametry,"Parametry")
        
        k_scenariusze=wx.Menu()
        scenariusze_1=k_scenariusze.Append(wx.ID_ANY, "Wczytaj")
        scenariusze_2=k_scenariusze.Append(wx.ID_ANY, "Zapisz")
        self.Bind(wx.EVT_MENU, self.wx_wczytaj_scenariusz, scenariusze_1)
        self.Bind(wx.EVT_MENU, self.wx_zapisz_scenariusz, scenariusze_2)
        menubar.Append(k_scenariusze,"Scenariusze")

        k_autorzy=wx.Menu()
        autorzy_0=k_autorzy.Append(wx.ID_ANY,"Autorzy")
        self.Bind(wx.EVT_MENU,self.wx_wyswietl_autorow,autorzy_0)      
        menubar.Append(k_autorzy,"Autorzy")
        
        k_zamknij=wx.Menu()
        zamknij_0=k_zamknij.Append(wx.ID_ANY,"Zakończ")
        self.Bind(wx.EVT_MENU,self.wx_zamknij, zamknij_0) 
        menubar.Append(k_zamknij,"Zamknij")
        
        k_pomoc=wx.Menu()
        pomoc_0=k_pomoc.Append(wx.ID_ANY,"Pomoc")
        self.Bind(wx.EVT_MENU,self.wx_help, pomoc_0) 
        menubar.Append(k_pomoc,"Instrukcja")
        
        self.Przycisk_symulacja=wx.Button(panel, -1, "Symulacja",
                                      pos=(aktualny_widzet["Start_pos"][0],
                                           aktualny_widzet["Start_pos"][1]),
                                      size=(aktualny_widzet["Start_size"][0],
                                            aktualny_widzet["Start_size"][1]))
        self.Przycisk_symulacja.Bind(wx.EVT_BUTTON,self.wx_test_do_symulacji)
        
        self.Przycisk_animacja=wx.Button(panel, -1, "Animacja",                                      
                                         pos=(aktualny_widzet["Animancja_pos"][0],
                                           aktualny_widzet["Animancja_pos"][1]),
                                      size=(aktualny_widzet["Animancja_size"][0],
                                            aktualny_widzet["Animancja_size"][1]))
        self.Przycisk_animacja.Bind(wx.EVT_BUTTON, self.wx_test_do_animacji) 
        
        if os.path.exists("Generacja_0.bmp")==True:
            os.remove("Generacja_0.bmp")
        stw_planszę_początkową()
        zdj=wx.Bitmap("Generacja_0.bmp", wx.BITMAP_TYPE_ANY)
        self.obraz = wx.StaticBitmap(panel, wx.ID_ANY, zdj,
                                     pos=(aktualny_widzet["Obraz_pos"][0],
                                          aktualny_widzet["Obraz_pos"][1]))
        self.SetSize((aktualny_widzet["Okno_size"][0],
                      aktualny_widzet["Okno_size"][1]))
        self.Centre()
        self.SetTitle("Program automatów komórkowych")
    def wx_help(self,evt):
        ok4=Okno_pomocy()
        ok4.Show()
        
    def wx_test_do_symulacji(self,evt):
        if len(aktualny_zestaw)!=0:
            self.wx_symulacja()
            self.wx_wyświetl_wiadomość(("Ukończono symulcje"),"info")
        else:
            self.wx_wyświetl_wiadomość(("Nie wybrano \ stworzone zestawu"),"error")
                         
    def wx_test_do_animacji(self,evt):
        dialog=wx.FileDialog(self,message='Wybierz plik z zapisem symulacji',defaultFile='',wildcard='*.TXT',style=wx.FD_OPEN, pos=(10,10))
        if dialog.ShowModal() == wx.ID_OK:
            sciezka = dialog.GetPaths()[0]
            dialog.Destroy()
            self.wx_animacja(sciezka)
            ok3=Okno_animacji()
            ok3.Show()
       
    def wx_animacja(self,nazwa_pliku):
        """
        Za pomocą głównej pętli sterującej każda linia z wczytanego pliku,
        ze znakowym zapisaem stanu jednostki czasu danej symulacji, 
        jest rozdzielana za pomocą multiprocesingu na są procesy potomne w 
        postaci argumentu dla funkcji koloruj mapę. Każdy proces potomny 
        skutkuje wyprodukowaniem 1 mapy, która ilustruje zadany moment 
        symulacji. Mapy te są zostająpo zwórceniu ze wspomnianej funckji
        odrazu wstawiane w odpowiednie miejsce wcześniej spreparowanej lsity
        "wyniki", poprzez zamianę pustego elementu o indeksie odpowiadającym 
        numerowi stworzonemu procesu.
        
        Wynik
        -------
        Tworzy plik nazwie "movie_CA.gif".
        """
        self.progres_bar = wx.ProgressDialog(title="Pasek postępu", message="Postęp animacji: {} / {}. Proszę czekać".format(0,1), maximum=1, parent=self)
        
        wyniki=[]
        lista=[]
        with open(nazwa_pliku) as f: # jest tylko 1  otawrcie pliku zmiast każdrazowego przy wywołaniu funkcji
            f.readline() #zbiera klucz zabezpieczajcy
            for x in range(0,Parametry["ile_generacji"]):
                line = f.readline().replace('\n', '')
                lista.append(line) #zrzuca plik do listy
        argumenty = tuple([("Generacja_0.bmp",lista[x],str(x),Konfiguracja["szer_kom"],100) for x in range(0,len(lista))]) #list comprehension zbierajacy wszystkie potrzebne argumenty wykonan funkcji koloruj
        with mp.Pool() as kolejka: #wpisanie liczby w nawias ustawia ilosc uzywanych wątków, domyslnie Pool() wybiera maksymalna ilosc wątkow ie. procesor 4c8t uruchomi 8 procesow 
            proc_result = kolejka.starmap(koloruj_mapę,argumenty) #starmap wywolujacy wszystkie wykonania przy uzyciu process poola
        wyniki = [x[0] for x in proc_result] #list comprehension robiacy podmianke na pierwszy elem z bitmapą, jak wczesniej
        tekst="Postęp animacji: {} / {}. Proszę czekać".format(1, 1)
        self.wx_test_uaktualnij_pasek(1, tekst)
        self.wx_wyświetl_wiadomość("Ukończono animację", "info")
        z_gifa(wyniki)    
        
    def wx_symulacja(self):
        """
        Funkcja pelniaca role symulacji
    
        Parameters
        ----------
        tupele: list
            pary liczb w tuplu w liscie, koordynaty punktów
        ile_gen: int
            ilosc generacji symulacji
        parametry: slownik
            ustalone ilosci sasiadow do przezycia, wskrzeszenia lub smierci
    
        Wynik
        -------
        Lista wszystkich generacji, w postaci zywych punktow na planszy (koordynaty punktów)
    
        """
        tupele=plansza_na_tuple(aktualny_zestaw)
        ile_gen=Parametry['ile_generacji']
        parametry=Parametry
        
        licznik = 0
        max_zakres=ile_gen
        tekst="Postęp symulacji: {} / {}. Proszę czekać".format(licznik, ile_gen)
        self.progres_bar = wx.ProgressDialog(title="Pasek postępu", message=tekst, maximum=max_zakres, parent=self)

        sasiedzi = [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]
        wszystkie_gen = [tupele] 
        wszystkie_koordynaty = [] 
        for x in range(100):
                for y in range(100):
                        wszystkie_koordynaty.append((x,y))
        while licznik < ile_gen:
            wynikowa = []
            for komorka in wszystkie_koordynaty:
                sasiedzi_koor = [tuple(map(sum,zip(x,komorka))) for x in sasiedzi]
                ilosc_sasiadow = len(set(wszystkie_gen[licznik]) & set(sasiedzi_koor))
                if komorka in wszystkie_gen[licznik]:
                    if parametry["samotnosc"] < ilosc_sasiadow < parametry["scisk"]:
                        wynikowa.append(komorka)
                elif ilosc_sasiadow == parametry["nadzieja"]:
                        wynikowa.append(komorka)
            wszystkie_gen.append(wynikowa)
            licznik += 1
            tekst="Postęp symulacji: {} / {}. Proszę czekać".format(licznik, ile_gen)
            self.wx_test_uaktualnij_pasek(licznik, tekst)
        tekst="Postęp symulacji: {} / {}. Proszę czekać".format(licznik, ile_gen)
        self.wx_test_uaktualnij_pasek(ile_gen, tekst)
        zapisz_generacje(wszystkie_gen, "Symulacja.txt")
        print("Symulacja skończona")

    def wx_aktualizuj_podglad_zestawu(self):
        koloruj_mapę_tylko_początkową(aktualny_zestaw)
        zdj=wx.Bitmap("Plansza_początkowa.bmp", wx.BITMAP_TYPE_ANY)
        Okno_interfejsu_glownego.obraz = wx.StaticBitmap(self, bitmap=zdj,pos=(aktualny_widzet["Obraz_pos"][0],
                                          aktualny_widzet["Obraz_pos"][1]))
        Okno_interfejsu_glownego.Refresh(self)
        Okno_interfejsu_glownego.Update(self)
        
    def wx_zapisz_podglad_zestawy(self,evt):
        
        pop=wx.TextEntryDialog(self,"Podaj nazwę dla zdjęcia z podglądem zestawu.")
        pop.ShowModal()
        nazwa=pop.GetValue() 
        if "podgląd" not in nazwa or "Podgląd" not in nazwa:
            nazwa="Podgląd_"+nazwa
        if os.path.exists(nazwa):
            nazwa2=nazwa.split(".")
            nazwa=nazwa2[0]+"_nowa_nazwa.txt"
            self.wx_wyświetl_wiadomość(("Podana nazwa jest już zajęta.\n Podgląd zestawu zostanie zapisany jako "+nazwa),"warning")
        
        podst=Image.open("Plansza_początkowa.bmp")
        podst.save(nazwa+".bmp")
        print("zapisano",)
        
    def wx_zamknij(self,evt):
        """
        Metoda zamykająca Obiekt Okno_interfejsu_glownego i tym samym wszystkie instancje
        obiektów potomnych.

        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Zamyka program.
        """
        dialog = wx.MessageDialog(self,"Czy na pewno?","Kończymy pracę", style = wx.OK|wx.CANCEL)
        x = dialog.ShowModal()
        if x == wx.ID_OK:
            self.Close()
            
    def wx_test_paska(self,evt):
        """
        Funckja do debugu paska postepu.

        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Wywołanie funckji wx_test_uaktualnij_pasek i stowrzenie atrybutu
        progres_bar

        """
        max_zakres=10
        self.progres_bar = wx.ProgressDialog("Postęp symulacji", "prosze czekać", maximum=max_zakres, parent=self)
        for x in range(1,max_zakres):
            time.sleep(0.1)
            self.wx_test_uaktualnij_pasek(x)
        self.wx_test_uaktualnij_pasek(max_zakres)
            
    def wx_test_uaktualnij_pasek(self,wartosc,wiadomosc):
        """
        Funckja pozwalajaca na zaktualizawanie paska postępu do podanej 
        w argumencie wartosci

        Parameters
        ----------
        wartosc : (int) - cyfra okreslajaca procentowy postep prac
        
        Wynik
        -------
        None.

        """
        self.progres_bar.Update(wartosc,newmsg=wiadomosc)
        
    def test(self,evt):
        """
        Funckja do podpięć kafelek i przycisków.
        Docelowo zostanie usunięta po ukończeniu prac nad funkcjami.

        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Nic.

        """
        pass
    
    def wx_wyswietl_autorow(self,evt):
        """
        Wyswietla okno dialogowe z informacja o autorach.

        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Wywołanie funkcji wx_wyświetl_wiadomość

        """
        wiadomosc=" Program autorstwa:\n Patrycji Chmielowskiej oraz Jarosława Wełeszczuk, \n studentów Uniwersytetu Przyrodniczego we Wrocławiu."
        self.wx_wyświetl_wiadomość(wiadomosc,"info")
    
    def wx_test_p_zestaw(self,evt):
        """
        Funkcja debugująca dla zestawów.
    
        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Wyswietlenie tekstu w konsoli
        """
        print(aktualny_zestaw)
        
    def wx_test_p_parametry(self,evt):
        """
        Funkcja debugująca dla parametrów.
        
        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Wyswietlenie tekstu w konsoli
        """
        print(Parametry)
    
    def wx_zapisz_zestaw(self,evt):
        """
        Zapisuje ciąg tulp reprezentujących osobniki ze zmiennej
        aktualny zestaw. W przypadku istnienia już takiego pliku modyfikuje
        jego nazwe i wyświetla o tym komuniakt.

        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika
        
        Wynik
        -------
        Zapisuje plik z tulpową reprezentacją żywych komórek.
        """
        if type(aktualny_zestaw) != list:
            pop=wx.TextEntryDialog(self,"Podaj nazwę dla pliku ze zestawem : ")
            pop.ShowModal()
            nazwa=pop.GetValue() 
            
            if "Zestaw" not in nazwa:
                nazwa="Zestaw_"+nazwa
            if ".txt" not in nazwa:
                nazwa=nazwa+".txt"
            if os.path.exists(nazwa):
                nazwa2=nazwa.split(".")
                nazwa=nazwa2[0]+"_nowa_nazwa.txt"
                self.wx_wyświetl_wiadomość(("Podana nazwa jest już zajęta.\n Zestaw został zapisany jako "+nazwa),"warning")
    
            pary_tupli= plansza_na_tuple(aktualny_zestaw)
            zapisz_zestaw(pary_tupli,nazwa)
        else:
            self.wx_wyświetl_wiadomość(("Brak zestawu"),"error")
        
    def wx_wczytaj_zestaw(self,evt):
        """
        Wyświetla okno wyboru pliku. 
        
        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Zmienia zmienną aktualny_zestaw.
        """
        dialog=wx.FileDialog(self,message='Wybierz plik zestawu',defaultFile='',wildcard='*.TXT',style=wx.FD_OPEN, pos=(10,10))
        if dialog.ShowModal() == wx.ID_OK:
            sciezka = dialog.GetPaths()[0]
            sciezka=sciezka.split("\\")
            global aktualny_zestaw
            aktualny_zestaw=wczytaj_zestaw(sciezka[-1])
            self.wx_aktualizuj_podglad_zestawu()
            dialog.Destroy()
            
    def wx_wylosuj_zestaw(self,evt):
        """
        Funkcja tworzy zestaw, z iloscią komórek z zakresu 10-100

        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Zmiana globalnej zmiennej aktualny zestaw

        """
        ilosc=random.randrange(500,1500) #przy tym symulacja trwa prawie 2min (na moim laptopie - P), 
        #im rzadsze pole tym krócej, ale za to mniej efektywniejsza będzie animacja
        plansza=(wylosuj_zestaw(ilosc))[0]
        global aktualny_zestaw
        aktualny_zestaw = plansza
        self.wx_aktualizuj_podglad_zestawu()
        
    def wx_zestaw_rysuj(self,evt):
        """
        Tworzy instancje klasy Okno_rysowania_zestawu.
        
        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Wywołanie nowego okno

        """
        okno_potomne_2=Okno_rysowania_zestawu()
        okno_potomne_2.Show()
        
    def wx_zestaw_ze_zdj(self,evt): 
        """
        Funckja służąca do okreslenia przez uzytkownika, jakie zdjecie
        chce przetworzyć.

        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Wywołanie funckji wx_skanuj_zdjecie

        """
        dialog=wx.FileDialog(self,message='Wybierz zdjecie planszy do przetworzenia',defaultFile='',wildcard='*.PNG',style=wx.FD_OPEN, pos=(10,10))
        if dialog.ShowModal() == wx.ID_OK:
            sciezka = dialog.GetPaths()[0]
            sciezka=sciezka.split("\\")
            dialog.Destroy()
        self.wx_skanuj_zdjecie(sciezka[-1])

        
    def wx_skanuj_zdjecie(self,plik):  
        """
        Funckja wywołuje szereg innnych funkcji, mających na celu
        ustalenie pozycji żywych kom komórek na zdjęciu.

        Parameters
        ----------
        plik : (jpg) - plik, który posłuży dalej za argument

        Wynik
        -------
        Zmiana globalnej zmiennej aktualny zestaw

        """
        image = PIL.Image.open(plik)
        wartosci=zbadaj_zdj(image)
        if wartosci =="Nope":
            self.wx_wyświetl_wiadomość("Zdjecie zawiera wiecej niz 3 kolory. Nie mozna go przetworzyc","error")
        else:
            szer_lini = wartosci[0]
            szer_kom = wartosci[1]
            l_z_k=zywe_kom_ze_zdj(image,szer_lini,szer_kom)
            global aktualny_zestaw
            plansza= tupla_na_plansze(l_z_k)
            aktualny_zestaw = plansza
            self.wx_aktualizuj_podglad_zestawu()
            
    def wx_zapisz_scenariusz(self,evt):
        pop=wx.TextEntryDialog(self,"Podaj nazwę dla parametrów : ")
        pop.ShowModal()
        nazwa=pop.GetValue() # GetValue do okienek
        if "Scenariusz" not in nazwa:
            nazwa="Scenariusz_"+nazwa
        if ".txt" not in nazwa:
            nazwa=nazwa+".txt"
        if os.path.exists(nazwa):
            nazwa2=nazwa.split(".")
            nazwa=nazwa2[0]+"_nowa_nazwa.txt"
            self.wx_wyświetl_wiadomość(("Podana nazwa jest już zajęta.\n Parametry zostały zapisany jako "+nazwa),"warning")
        zapisz_scenariusz(nazwa)
        """
        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Zapisanie scenariusza z pliku .txt

        """
        pass

    def wx_wczytaj_scenariusz(self,evt):
        dialog=wx.FileDialog(self,"Wybierz plik scenariusza",defaultFile='',wildcard='*.TXT',style=wx.FD_OPEN, pos=(10,10))
        if dialog.ShowModal() == wx.ID_OK:
            sciezka = dialog.GetPaths()
            global Parametry
            global aktualny_zestaw
            Parametry,aktualny_zestaw=wczytaj_scenariusz(sciezka[0]) 
            dialog.Destroy()
        """
        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        WWczytanie scenariusza z pliku .txt

        """
        pass
       
    def wx_zapisz_parametry(self,evt):
        """
        Zapisuje wszystkie wartości z aktualnie używanego słownika "Parametry"
        pod  wskazaną przez użytkownika nazwą. W przypadku istnienia
        już takiego pliku modyfikuje jego nazwe i wyświetla o tym komuniakt.

        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Zapisuje parametry słownika w pliku ".txt".
        """
        pop=wx.TextEntryDialog(self,"Podaj nazwę dla parametrów : ")
        pop.ShowModal()
        nazwa=pop.GetValue() # GetValue do okienek
        if "Parametry" not in nazwa:
            nazwa="Parametry_"+nazwa
        if ".txt" not in nazwa:
            nazwa=nazwa+".txt"
        if os.path.exists(nazwa):
            nazwa2=nazwa.split(".")
            nazwa=nazwa2[0]+"_nowa_nazwa.txt"
            self.wx_wyświetl_wiadomość(("Podana nazwa jest już zajęta.\n Parametry zostały zapisany jako "+nazwa),"warning")
        zapisz_parametry(nazwa)

    def wx_wczytaj_parametry(self,evt):
        """
        Zmienia aktualnie użytkowany słownik "Parametry" poprzez podmienienie
        go na nowego, wskazanego przez użytkownika w oknie wyboru pliku.

        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Zmiana wartosći slownila parametry, na te ze wskazanego z pliku.
        """
        dialog=wx.FileDialog(self,"Wybierz plik parametrów",defaultFile='',wildcard='*.TXT',style=wx.FD_OPEN, pos=(10,10))
        if dialog.ShowModal() == wx.ID_OK:
            sciezka = dialog.GetPaths()
            global Parametry
            Parametry=wczytaj_parametry(sciezka[0]) 
            dialog.Destroy()
            
    def wx_zmień_parametry(self, evt):
        """
        Tworzy okno, na którym użytkownik może skonfigorować parametry.

        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Utworzenie instancji klasy Okno_zmiany_parametrów

        """
        okno_potomne=Okno_zmiany_parametrów()
        okno_potomne.Show() 
        
    def wx_wyświetl_wiadomość(self,wiadomość,tryb):
        """
        Wyświetla okno dialogowe z wartościami argumentów.

        Parameters
        ----------
        wiadomość (str): komunikat do przekazania użytkownikowi
        tryb (str) : odpowiada stylowu okna. 
            Tryby:
                1) error
                2) warning
                3) info
        Wynik
        -------
        Okno z komunikatem.
        """
        if tryb=="error":
            styl= wx.ICON_ERROR
        elif tryb=="warning":
            styl= wx.ICON_WARNING
        elif tryb=="info":
            styl= wx.ICON_INFORMATION
        else:
            styl= wx.ICON_NONE        
        powiadomienie1=wx.MessageDialog(None,message=wiadomość,style = wx.OK | styl )
        powiadomienie1.ShowModal()

class Okno_zmiany_parametrów(wx.Frame):
    def __init__(self,parent = None):
        """
        Konstruktor klasy Okno_interfejsu_glownego.
        """
        super(Okno_zmiany_parametrów,self).__init__(parent)
        self.intiUI()
    
    def intiUI(self):
        """
        Metoda odpowiadająca za formę i widżety okna.
        """
        self.SetTitle("Zmiana parametrów")
        self.Centre(wx.BOTH)
        self.SetSize(290,180)
        panel_p=wx.Panel(self,wx.ID_ANY)
        
        lbl_1 = wx.StaticText(panel_p, -1, label="Samotnosc:",pos = (10,10))
        self.t_samotnosc = wx.TextCtrl(panel_p, pos=(90,10),size=(50,20), value="0") 
        
        lbl_2 = wx.StaticText(panel_p, -1, label="Scisk",pos = (30,40))
        self.t_scisk = wx.TextCtrl(panel_p, pos=(90,40),size=(50,20), value="0") 
        
        lbl_3 = wx.StaticText(panel_p, -1, label="Nadzieja:",pos = (25,70))
        self.t_nadzieja = wx.TextCtrl(panel_p, pos=(90,70),size=(50,20), value="0") 
        
        lbl_4 = wx.StaticText(panel_p, -1, label="Ile generacji:",pos = (10,100))
        self.t_generacje = wx.TextCtrl(panel_p, pos=(90,100),size=(50,20), value="0") 
        
        self.Przycisk_zmień=wx.Button(panel_p, -1, label="Zmień",pos=(160,5),
                                      size=(100,55))
        self.Przycisk_zmień.Bind(wx.EVT_BUTTON,self.wx_2_uakutalnij_parametry) 
    
        self.Przycisk_wyczysc=wx.Button(panel_p, -1, label="Wyczysc",pos=(160,75),
                                      size=(100,55))
        self.Przycisk_wyczysc.Bind(wx.EVT_BUTTON,self.wx_2_wyczysc)
        
    def wx_2_uakutalnij_parametry(self,evt):
        """
        Zmienia wartosci słownika "Parametry" poprzez pzczytanie wartosci
        wpisanych przez użytkownika w oknie zmiany parametrów.
        
        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Zastapienie wartosci ze slownika 
        """
        scisk=int(self.t_scisk.GetValue())
        samotnosc=int(self.t_samotnosc.GetValue())
        nadzieja=int(self.t_nadzieja.GetValue())
        generacje=int(self.t_generacje.GetValue())
        
        if samotnosc >=0 and scisk >0 and generacje >0 and nadzieja >0:
            if samotnosc <=8 and scisk <=8 and nadzieja<=8:
                Parametry["samotnosc"] = samotnosc
                Parametry["scisk"] = scisk
                Parametry["ile_generacji"] = generacje
                Parametry["nadzieja"] = nadzieja
            else:
                Okno_interfejsu_glownego.wx_wyświetl_wiadomość(self,"Maksymalne sąsiedztwo to 8","error")
        else:
            Okno_interfejsu_glownego.wx_wyświetl_wiadomość(self,"Parametry nie mogą być ujemne","error")
        
    def wx_2_wyczysc(self,evt):
        """
        Usuwa wartosci wpisane przez uzytkownika.
        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Zastapienie wartosci pól na 0.

        """
        self.t_scisk.SetValue("0")
        self.t_samotnosc.SetValue("0")
        self.t_generacje.SetValue("0")
    
class Okno_rysowania_zestawu(wx.Frame):
    def __init__(self, parent=None):
        super(Okno_rysowania_zestawu,self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        """
        Metoda odpowiadająca za formę i widżety okna.
        """
        self.SetTitle("Rysowanie_zestawu")
        self.Centre(wx.BOTH)
        self.SetSize(700,700)
        menubar=wx.MenuBar()
        self.SetMenuBar(menubar)
        self.Centre()
        self.grid = wx.grid.Grid(self, -1)
        self.grid.SetDefaultRowSize(1)
        self.grid.SetDefaultColSize(1)
        self.grid.CreateGrid(100, 100)
        self.grid.DisableDragGridSize()
        self.grid.EnableEditing(False)
        for x in range(0,100):    
            self.grid.SetRowLabelValue(x, str(x+1))
            self.grid.SetColLabelValue(x, str(x+1))
            
        self.aktualnie_zaznaczone_kom = (0, 0) 
        self.grid.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.wx_3_pojedyncze_klikniecie)
        self.grid.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.wx_3_przeciaganie_zaznaczenia)
        
        k_wyczysc=wx.Menu()
        wyczysc_1=k_wyczysc.Append(wx.ID_ANY,"Wyczysc") 
        self.Bind(wx.EVT_MENU, self.wx_3_wyczysc_siatke, wyczysc_1)
        menubar.Append(k_wyczysc,"Wyczysc")
        
        k_zestawy=wx.Menu()
        zestawy_1=k_zestawy.Append(wx.ID_ANY, "Zapisz")
        self.Bind(wx.EVT_MENU,self.wx_3_zapisz_siatke, zestawy_1)
        
        zestawy_2=k_zestawy.Append(wx.ID_ANY,"Wczytaj") 
        self.Bind(wx.EVT_MENU,self.wx_3_wczytaj_na_siatke, zestawy_2)
 
        menubar.Append(k_zestawy,"Zestawy")
        
        k_pomoc = wx.Menu()
        pomoc_0 = k_pomoc.Append(wx.ID_ANY,"Pomoc")
        self.Bind(wx.EVT_MENU, self.wx_3_pomoc, pomoc_0)
        menubar.Append(k_pomoc, "Pomoc")
        
        shift_z_id=wx.NewIdRef(count=1)
        self.Bind(wx.EVT_MENU,self.wx_3_komorki_na_czarno,id=shift_z_id)
        
        shift_x_id=wx.NewIdRef(count=1)
        self.Bind(wx.EVT_MENU,self.wx_3_komorki_na_bialo,id=shift_x_id)
        
        self.accel_tbl=wx.AcceleratorTable([
            (wx.ACCEL_SHIFT,ord('Z'),shift_z_id), #na czarno
            (wx.ACCEL_SHIFT,ord('X'),shift_x_id), #na bialo
            ])
        self.SetAcceleratorTable(self.accel_tbl)
        
    def wx_3_przeciaganie_zaznaczenia(self, evt):
        """
        Pobiera komorki, które są aktualnie zaznaczona poprzez przytrzymanie
        lewego przycisku myszy i przeciągnięcie kursora.
        
        Parameters
        ----------
        evt : Wywołanie przez okresloną akcja użytkownika
  
        Wynik
        -------
        Wyowałnie funkcji
        """
        if self.grid.GetSelectionBlockTopLeft():
            top_left = self.grid.GetSelectionBlockTopLeft()[0]
            bottom_right = self.grid.GetSelectionBlockBottomRight()[0]
            self.wx_3_wylicz_kom_zaznaczone_przeciagnieciem(top_left, bottom_right)  

    def wx_3_klikniecie_w_poj_kom(self, evt):# wykrywa ze kliknalem jedno
        """
        Funkcja sprawdzajaca, czy klikniecie trafilo w siatke, czy w linie.
        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika
  
        Wynik
        -------
        Wyowałnie funkcji
        """
        cells = self.grid.GetSelectedCells()
        if not cells:
            if self.grid.GetSelectionBlockTopLeft():
                top_left = self.grid.GetSelectionBlockTopLeft()[0]
                bottom_right = self.grid.GetSelectionBlockBottomRight()[0]
                self.wx_3_wylicz_kom_zaznaczone_przeciagnieciem(top_left, bottom_right)
                
    def wx_3_pojedyncze_klikniecie(self, evt): 

        """ 
        Pobiera aktualnie zaznaczona pojedyncza komorke, poprzez klikniecie
        kursorem, lub przejscie za pomoca strzałek.
        
        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika
  
        Wynik
        -------
        Nadpisanie atrybutu aktualnie_zaznaczone_kom klasy Okno_rysowania_zestawu
        """                                      
        lista_kom=[]
        z=(evt.GetRow(),evt.GetCol())
        lista_kom.append(z)
        self.aktualnie_zaznaczone_kom = (lista_kom)
        evt.Skip()

    def wx_3_wylicz_kom_zaznaczone_przeciagnieciem(self, top_left, bottom_right): 
        """
        Funkcja z podanych argumentow, wylicza wspolrzedne aktualnie
        zaznaczonych komorek.
        
        Parameters
        ----------
        top_left (int): zakres zaznaczenia
        bottom_right (int): zakres zaznaczenia
  
        Wynik
        -------
        Nadpisanie atrybutu aktualnie_zaznaczone_kom klasy Okno_rysowania_zestawu
        """
        cells = []
        rows_start = top_left[0]
        rows_end = bottom_right[0]
        cols_start = top_left[1]
        cols_end = bottom_right[1]
        rows = range(rows_start, rows_end+1)
        cols = range(cols_start, cols_end+1)
        cells.extend([(row, col)
            for row in rows
            for col in cols])
        self.aktualnie_zaznaczone_kom = cells
    
    def wx_3_test(self,evt):
        """
        Funckja do testowania.
          
        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika
          
        Wynik
        -------
        Nic.
          
        """
        pass 
  
    def wx_3_wyczysc_siatke(self, evt):
        """
        Zmienia kolor wszystkich komorek na siatce na biały.
          
        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika
          
        Wynik
        -------
        Nic.
          
        """
        for x in range(0,100):
            for y in range(0,100):
                self.grid.SetCellBackgroundColour(x,y, wx.WHITE)
        self.grid.ForceRefresh()
        
    def wx_3_zapisz_siatke(self,evt):
        """
        
        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Utworzenie pliku .txt

        """
        lista_pozycja_zyw=[]
        for x in range(0,100):
            for y in range(0,100):
                kolor=self.grid.GetCellBackgroundColour(x,y)
                if kolor == wx.BLACK:
                    z=(x,y)
                    lista_pozycja_zyw.append(z)
        plansza = tupla_na_plansze(lista_pozycja_zyw)
        global aktualny_zestaw
        kopia=aktualny_zestaw
        aktualny_zestaw  = plansza
        self.wx_3_zapisz_zestaw(evt)
        aktualny_zestaw = kopia
        
    def wx_3_znajdz_zyjace_komorki_na_siatce(self):
        """
        Przeszukuje kazda ze wspolrzednych i na podstawie jej koloru
        stwierdza czy jest zywa. Jesli tak, to dodaje ja listy        
        
        Wynik
        -------
        lista z koordyatami w postaci tulp
        """
        lista_pozycja_zyw=[]
        for x in range(0,100):
            for y in range(0,100):
                kolor=self.grid.GetCellBackgroundColour(x,y)
                if kolor == wx.BLACK:
                    z=(x,y)
                    lista_pozycja_zyw.append(z)
        return lista_pozycja_zyw    
    
    def wx_3_wczytaj_na_siatke(self,evt):
        """
        Wczytuje wskazany plik txt i tworzy jego wizualizacje

        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Zmiana koloru komorek siatki.

        """
        dialog=wx.FileDialog(self,message='Wybierz plik zestawu',defaultFile='',wildcard='*.TXT',style=wx.FD_OPEN, pos=(10,10))
        if dialog.ShowModal() == wx.ID_OK:
            self.wx_3_wyczysc_siatke(evt)
            sciezka = dialog.GetPaths()[0]
            sciezka=sciezka.split("\\")
            zestaw=wczytaj_zestaw(sciezka[-1])
            dialog.Destroy()
            for x in range(0,100):
                for y in range(0,100):
                    if zestaw[x][y]==1.0:
                        self.grid.SetCellBackgroundColour(x, y, wx.BLACK)
            self.grid.ForceRefresh()
        

    def wx_3_pomoc(self, evt):
        """
        Uzywajac funkcji z klasy Okno_interfejsu_glownego,
        wyswietla uzytkownikowi instrukcje do rysownaia.

        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika

        Wynik
        -------
        Wywołanie okna dialogowego

        """
        tresc_wiadomosci = "Aby umiescic na planszy zywa komorke,\n nalezy kliknac \ przeciagnac myszkee \n i uzyc kombinacji shift+z. \n Analogicznie dla komorki martwej shif+x"
        Okno_interfejsu_glownego.wx_wyświetl_wiadomość(self,tresc_wiadomosci, "info")
    
    def wx_3_komorki_na_czarno(self,evt):
        """
        Wywoluje funckje koloruj z argumentem koloru: czarny  
        
        Parameters
        ----------
        evt :Wywołanie przez okreloną akcja użytkownika
          
        Wynik
        -------
        Wywołanie funckji
        """
        self.wx_3_koloruj(wx.BLACK,self.aktualnie_zaznaczone_kom)
            
    
    def wx_3_komorki_na_bialo(self,evt):
        """
        Wywoluje funckje koloruj z argumentem koloru: biały 
          
        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika
          
        Wynik
        -------
        Wywołanie funckji
        """
        self.wx_3_koloruj(wx.WHITE,self.aktualnie_zaznaczone_kom)
    
    def wx_3_koloruj(self,kolor,lista):
        """
        Zmieia kolor aktualnie podanego jako argument
        zestawu komorek na odpowiedni koloer. 
          
        Parameters
        ----------
        kolor : atrybut wx.python
        
        lista: lista ze wspolrzednym w postaci tulp
          
        Wynik
        -------
        Zmiana koloru siatki.
        """
        #koloru nie dzialaja. Wszystko na czerowono jest 
        if type(lista)==list:
            if len(lista) !=0:
                for x in lista:
                    self.grid.SetCellBackgroundColour(x[0], x[1], kolor)
                self.grid.ForceRefresh()
        
    def wx_3_zapisz_zestaw(self,evt):
        """
        Zapisuje ciąg tulp reprezentujących osobniki ze zmiennej
        aktualny zestaw. W przypadku istnienia już takiego pliku modyfikuje
        jego nazwe i wyświetla o tym komuniakt.

        Parameters
        ----------
        evt : Wywołanie przez okreloną akcja użytkownika
        
        Wynik
        -------
        Zapisuje plik z tulpową reprezentacją żywych komórek.
        """
        pop=wx.TextEntryDialog(self,"Podaj nazwę dla pliku ze zestawem : ")
        pop.ShowModal()
        nazwa=pop.GetValue() 
        
        if "Zestaw" not in nazwa:
            nazwa="Zestaw_"+nazwa
        if ".txt" not in nazwa:
            nazwa=nazwa+".txt"
        if os.path.exists(nazwa):
            nazwa2=nazwa.split(".")
            nazwa=nazwa2[0]+"_nowa_nazwa.txt"
            Okno_interfejsu_glownego.wx_wyświetl_wiadomość(("Podana nazwa jest już zajęta.\n Zestaw został zapisany jako "+nazwa),"warning")
        pary_tupli= plansza_na_tuple(aktualny_zestaw)
        zapisz_zestaw(pary_tupli,nazwa)
        
class Okno_animacji(wx.Frame):
   """
   Klasa której jedynym celem jesy utworzenie nowego okna i ustawienie 
   animacji jako tło.
   """
   def __init__(self, parent=None):
       """
       Konstruktor klasy Okno_animacji.
       """
       super(Okno_animacji, self).__init__(parent)
       self.InitUI()

   def InitUI(self):   
       """
       Metoda odpowiadająca za formę i widżety okna.
       """
       sizer = wx.BoxSizer(wx.VERTICAL)
       anim = Animation('movie_CA.gif')
       ctrl = AnimationCtrl(self, -1, anim)
       ctrl.Play()
       sizer.Add(ctrl)
       self.SetSizerAndFit(sizer)
       self.Centre()    
       self.SetTitle('Podgląd animacji')
       self.Show() 
   


class Okno_pomocy(wx.Frame):
   """
   Klasa której jedynym celem jest utworzenie nowego okna i wyswietlenie 
   instrukcji obslugi programu dla uztkownika.
   """
   def __init__(self, parent=None):
       """
       Konstruktor klasy Okno_animacji.
       """
       super(Okno_pomocy, self).__init__(parent)
       self.InitUI()

   def InitUI(self):   
       """
       Metoda odpowiadająca za formę i widżety okna.
       """
       self.panel=wx.Panel(self,wx.ID_ANY)
       k_zestawy=wx.Menu()
       self.numer=0
       
       self.napis = wx.StaticText(self.panel, -1, label=Slownik_opisów[self.numer],pos = (0,0))
       
       self.Przycisk_cofnij=wx.Button(self.panel, -1, "<==",
                                      pos=(aktualny_widzet["Lewo_pos"][0],
                                           aktualny_widzet["Lewo_pos"][1]),
                                      size=(aktualny_widzet["Lewo_size"][0],
                                            aktualny_widzet["Lewo_size"][1]))
       self.Przycisk_cofnij.Bind(wx.EVT_BUTTON,self.wx_4_p_cofnij)
        
       self.Przycisk_dalej=wx.Button(self.panel, -1, "==>",                                      
                                         pos=(aktualny_widzet["Prawo_pos"][0],
                                           aktualny_widzet["Prawo_pos"][1]),
                                      size=(aktualny_widzet["Prawo_size"][0],
                                            aktualny_widzet["Prawo_size"][1]))
       self.Przycisk_dalej.Bind(wx.EVT_BUTTON, self.wx_4_p_dalej) 
        
       self.SetSize((aktualny_widzet["Okno_pomoc_size"][0],
                      aktualny_widzet["Okno_pomoc_size"][1]))
       self.Centre()    
       self.SetTitle('Manual')
       self.Show()      
       
   def wx_4_test(self,evt):
       pass
   
   def wx_4_p_dalej(self,evt):
       if self.numer <2:
          self.numer+=1
          self.napis.Destroy() 
          self.napis = wx.StaticText(self.panel, -1, label=Slownik_opisów[self.numer],pos = (0,0))
          self.Refresh()
          self.Update()
       
   def wx_4_p_cofnij(self,evt):
       if self.numer >0:
          self.numer-=1
          self.napis.Destroy()
          self.napis = wx.StaticText(self.panel, -1, label=Slownik_opisów[self.numer],pos = (0,0))
          self.Refresh()
          self.Update()
           
       
       
def wylosuj_zestaw(ilosc):
    """
    Generuje/Losuje zestaw losowych par liczb tak zwanych "tuple" i zapisuje
    je jako zmienna o nazwie "plansza", która przechowuje już ustawione losowo
    na planszy pozycje żywych komórek.
    W fragemencie "return: plansza,tupele" instrukcja return,zwraca wywołane 
    pary tupli, w postaci numerów odpowiadających danej pozycji komórki żywej na 
    naszej planszy oraz jako pary liczb czyli wygenerowane nasze losowo tuple.
    Jeżeli nasz stworzony i wskazany plik nie posiada zabezpieczenia w 
    formie ciągu znaków, lub nie istnieje w folderze z aplikacją, zostanie 
    wyswietlony stosowny komnunikat.
    
    Parametry
    ----------
    ilosc : int
        ilosc wystąpienia naszych par liczb (tupli), które zapisywane są aktualnie 
        na planszy (macierzy) w zmiennej o nazwie "plansza"
        
    Wynik
    -------
    Generuje okreloną ilosc tupli z przedziału od 0 do 100, zwraca wynik do zmiennej
    "plansza" i a przechowuje je już w pamięci komputera pod nazwą "komorki_zywe" 
    """
    plansza = np.zeros((100,100))
    tupele = sample(tuple(product(range(0,100), repeat=2)),ilosc)
    for tupel in tupele:
        plansza[int(tupel[0])][int(tupel[1])] = 1
    return plansza, tupele

#komorki_zywe, pary_tupli = wylosuj_zestaw(1000)

def tupla_na_plansze(tupla):
    """
    Zamienia pary tupli, czyli nasze wylosowane pary liczb stanowiące położenie 
    komórki, na planszę, czyli na plik programu z informacjami, w której kolumnie i 
    rzędzie będzie znajdować się nasza żywa komórka (żywa komórka oznaczona jako 1).
    
    Parametry
    ----------
    tupla : int
        zestaw losowych par liczb tak zwanych "tuple" zapisanych w postaci 
        listy
        
    Wynik
    -------
    Generuje plik programu z informacjami, w której kolumnie i rzędzie będzie 
    znajdować się nasza żywa komórka (żywa komórka oznaczona jako 1).
    """
    plansza = np.zeros((100,100))
    for tupel in tupla:
        plansza[int(tupel[1])][int(tupel[0])] = 1 ##ZMIANA## tupel[1] miejscem z tupel[0]
    return plansza

def plansza_na_tuple(plansza):
    """
    Zamienia plansze z już nałożonymi parametrami żywej komórki, spowrotem 
    na pary tupli zapisane w zmiennej.
    
    Parametry
    ----------
    plansza: int
        plik programu z informacjami, w której kolumnie i rzędzie będzie 
        znajdować się nasza żywa komórka.
        
    Wynik
    -------
    Generuje uporzadkowaną listę tupli, powstałą z odczytanych parametrów
    znajdujących się w pliku programu "plansza"/"komorki_zywe", a dokładniej z
    odczytania numeru wiersza i kolumny w miejscu gdzie występuje żywa komórka, 
    następnie zapisuje je w postaci par liczb.
    """
    tupla = []
    for x in range(100):
        for y in range(100):
            if plansza[x][y] != 0:
                tupla.append((y, x)) ##ZMIANA## y miejscem na x
    return tupla


def zapisz_zestaw(pary_tupli,nazwa_pliku):
    """
    Zapisuje wygenerowany/wylosowaney wczesniej zestaw losowych par liczb i 
    zapisuje je jako plik programu z informacjami, w której kolumnie i rzędzie
    będzie znajdować się nasza żywa komórka.
    Jeżeli nasz stworzony i wskazany plik nie posiada zabezpieczenia w 
    formie ciągu znaków, lub nie istnieje w folderze z aplikacją, zostanie 
    wyswietlony stosowny komnunikat.
    
    Parametry
    ----------
    pary_tupli : int
        zestaw losowych par liczb tak zwanych "tuple" zapisanych w postaci 
        listy
    nazwa_pliku : str
        nazwa pliku o rozszerzeniu .txt
        
    Wynik
    -------
    Zapisuje wygenerowany wczeniej zestaw par tupli do pliku z rozszerzeniem txt.
     
    """
    with open(nazwa_pliku, 'w') as f:
        f.write(Konfiguracja["klucz_zabezpieczający_zestaw"] + '\n')
        for item in pary_tupli:
            f.write("%s\n" % ','.join(map(str,item)))
        f.close()

         
def wczytaj_zestaw(nazwa_pliku):
    """
    Otwiera wczesniej wygenerowany plik .txt 
    Jeżeli istnieje już plik o wksazanej nazwie, lub nie posiada 
    ustalonego zabezpieczenia, zostanie wyswietlony stosowny komnunikat.
    Tworzy planszę gry o ustalonej wczesniej wielkosci, nastepnie pobiera
    z pliku wczesniej wygenerowanego pary liczb (tuple) i w miejsce 
    odpowiedniej kolumny i wiersza podstawia "1"
    Parametry
    ----------
    nazwa_pliku : str
        nazwa pliku, w którym zostaly zapisane wczesniej wygenerowane pary 
        liczb (tuple)
    Wynik
    -------
    Wygenerowanie planszy gry (macierzy) z zaznaczonymi na niej żywymi 
    komorkami - zywe oznaczone jako 1

    """
    with open(nazwa_pliku,"r") as plik:
        a=plik.readline()
        plik.close()
        if a != Konfiguracja["klucz_zabezpieczający_zestaw"]+"\n":
            print("Wybrany plik nie jest plikiem programu")
            return
    plansza = np.zeros((100,100))
    tupele = np.genfromtxt(nazwa_pliku, delimiter=',', skip_header=1)
    for tupel in tupele:
        plansza[int(tupel[0])][int(tupel[1])] = 1
    return plansza


def stw_planszę_początkową(): 
    """
    Tworzy oryginalną, niepokolorowaną mapę bitmapową. Ogólny szkic kratownicy,
    która potem będzie kolorowana przez inne procesy. Wszelki wartości potrzebne
    do jej stworzenia pobierane są z aktualnie załadowanego słownika Konfiguracja.

    Wynik
    -------
    Bitmapa "Generacja_0".

    """
    szerokość =100
    wysokość =100
    step=Konfiguracja["szer_kom"]
    height=wysokość*step # prosta matematyka
    width=szerokość*step
    obraz=Image.new(mode="RGB",size=(width,height),color=(255,255,255)) #mode=F bo dziele niżej
    draw=ImageDraw.Draw(obraz) # nasze tło                          szerokość x wysokość
    x=0
    y_start=0
    y_end=obraz.height
    for x in range(0,width,step): # wszystkie pionowe
        line=((x,y_start),(x,y_end))
        draw.line(line,fill=20)
    line=((width-1,0),(width-1,height))
    draw.line(line,fill=20)
    y=0
    x_start=0
    x_end=obraz.width
    for y in range(0,height,step): # wszystkie poziome lewo-prawo
        line=((x_start,y),(x_end,y))
        draw.line(line,fill=20)
    line=((0,height-1),(width,height-1))
    draw.line(line,fill=20)
    obraz.save("Generacja_0.bmp")
    
def koloruj_mapę_tylko_początkową(macierz): # z macierzy pobiera rzędy i szereg
    """
    Funkcja kolorująca tylko 1 generację z podstawki krawtownicy, stworzonej
    w funckji "stw_planszę_początkową" o nazwie "Generacja_0.bmp"
    Potrzebne parametry są pobierane z aktualnego słownika.

    Parameters
    ----------
    macierz (list) : lista obiektów,

    Wynik
    -------
    Plik "Plansza_początkowa.bmp"
    """
    krok = Konfiguracja["szer_kom"]
    #sekcja wczytywania danych opisujących arkusz
    podst=Image.open("Generacja_0.bmp") # zmienna jako oryginal
    im2=podst.copy() # w tym  miejscu robimy kopię oryginału i na nim praucjemy
    n2=0 # licznik szeregów - szerokość
    s_odl=krok
    x0=1
    x1=s_odl
    y0=1
    y1=s_odl
    litera=0
    
    for a_1 in range(100): # rzad
        for b_2 in range(100): # kolumna
            kom=macierz[a_1,b_2]
            if kom == 1.0:
                for y in range(y0,y1):
                    for x in range(x0,x1):
                        im2.putpixel((x,y),(0,0,0))# ten fragment zamalowuje 1 komórkę
            x0=x0+s_odl
            x1=x1+s_odl
            n2+=1 #szerokość
            litera=litera+1 # ktory element ze str
        n2=0
        x0=1
        x1=s_odl
        y0=y0+s_odl
        y1=y1+s_odl
    im2.save("Plansza_początkowa.bmp")
    
    
def wczytaj_parametry(nazwa_pliku):
    """
    Wczytuje plik programu z informacjami o ustawieniach gry.
    Jeżeli wskazany plik nie posiada zabezpieczenia w formie ciągu znaków,
    lub nie istnieje w folderze z aplikacją, zostanie wyswietlony
    stosowny komnunikat.
    
    Parametry
    ----------
    nazwa_pliku : str
        nazwa pliku z o rozszerzeniu .txt
    
    Wynik
    -------
    Zwraca słownik o kluczach i wartosciach ze wsakzanego pliku.
    """
    wczytany_slownik={}
    if os.path.isfile(nazwa_pliku) :
        with open(nazwa_pliku,"r") as plik:
            a=plik.readline()
            a=a.replace('\n', '')
            if a ==Konfiguracja["klucz_zabezpieczający_slownik"]:
                while True:
                    a=plik.readline()
                    if not a:
                        break
                    a=a.replace('\n', '')
                    a=a.split(":")
                    wczytany_slownik[a[0]]=int(a[1])
            else:
                print("Wybrany plik nie jest plikiem programu")               
    else:
        print("Nie ma takiego pliku")
    return(wczytany_slownik)

def zapisz_parametry(nazwa_pliku):
    """
    Zapisuje aktualny słownik do pliku.txt
    Jeżeli istnieje już plik o wksazanej nazwie, lub nie posiada 
    ustalonego zabezpieczenia, zostanie wyswietlony stosowny komnunikat.
    
    Parametry
    ----------
    nazwa_pliku : str
        nazwa pliku, do ktorego zostana zapisane parametry gry.

    Wynik
    -------
    Utworzenie pliku .txt o wskazanej nazwie.

    """
    if os.path.isfile(nazwa_pliku) :
        Okno_interfejsu_glownego.wx_wyświetl_wiadomość("Istnieje już taki plik","warning")
    else:
        with open(nazwa_pliku,"w") as f:
            f.write(Konfiguracja["klucz_zabezpieczający_slownik"]+"\n")
            for k,v in Parametry.items():
                linia=k+":"+str(v)+"\n"
                f.write(linia)
                

def wczytaj_scenariusz(nazwa_pliku):
    """
    Wczytuje plik programu z informacjami o parametrach gry i aktualnym zestawie,
    którym może być: losowa generacja, wczytanie z obrazka, rysowanie.
    Jeżeli wskazany plik nie posiada zabezpieczenia w formie ciągu znaków,
    lub nie istnieje w folderze z aplikacją, zostanie wyswietlony
    stosowny komnunikat.
    
    Parametry
    ----------
    nazwa_pliku : str
        nazwa pliku z o rozszerzeniu .txt
    
    Wynik
    -------
    Zwraca słownik o kluczach i wartosciach ze wsakzanego pliku.
    """
    
    wczytany_slownik={}
    if os.path.isfile(nazwa_pliku) :
        
        with open(nazwa_pliku,"r") as plik:
            a=plik.readline()
            licz = 0
            a=a.replace('\n', '')
            if a == Konfiguracja["Klucz zabezpieczający_scenariusz"]:
                while True:
                    licz += 1
                    a=plik.readline()
                    if not a or a == "__PARAMETRY_KONIEC__\n":
                        break
                    a=a.replace('\n', '')
                    a=a.split(":")
                    wczytany_slownik[a[0]]=int(a[1])
                plansza = np.zeros((100,100))
                tupele = np.genfromtxt(nazwa_pliku, delimiter=',', skip_header=licz+1)
                for tupel in tupele:
                    plansza[int(tupel[0])][int(tupel[1])] = 1     
            else:
                print("Wybrany plik nie jest plikiem programu")
                return
    else:
        print("Nie ma takiego pliku")
    return(wczytany_slownik, plansza)

def zapisz_scenariusz(nazwa_pliku):
    """
    Funkcja zapisuje aktualny słownik i parametry do pliku.txt o wskazanej 
    nazwie.
    Jeżeli istnieje już plik o wksazanej nazwie, lub nie posiada 
    ustalonego zabezpieczenia, zostanie wyswietlony stosowny komnunikat.
    
    Parametry
    ----------
    nazwa_pliku : str
        nazwa pliku, do ktorego zostana zapisane parametry gry i aktualny zestaw.
    parametry: int
        ustalone i niezmienne zasady gru związane z samotnoscia, sciskiem,
        nadzieja i iloscia generacji.
    aktualny_zestaw: int
        plik programu z informacjami o umiejscowieniu żywych komórek.

    Wynik
    -------
    Utworzenie pliku.txt o wskazanej nazwie.

    """
    global aktualny_zestaw
    if len(aktualny_zestaw) == 0:
        print("Nie można zapisać scenariusza, brak zestawu.")
        return
    if os.path.isfile(nazwa_pliku) :
        print("Wybrany plik juz istnieje")
    else:
        with open(nazwa_pliku,"w") as f:
            f.write(Konfiguracja["Klucz zabezpieczający_scenariusz"]+"\n")
            for k,v in Parametry.items():
                linia=k+":"+str(v)+"\n"
                f.write(linia)
            f.write("__PARAMETRY_KONIEC__\n")
            if type(aktualny_zestaw) is not list:
                aktualny_zestaw = plansza_na_tuple(aktualny_zestaw)
            for item in aktualny_zestaw:
                f.write("%s\n" % ','.join(map(str,item)))
            f.close()
    
def wykryj_rozdzielczosc():
    """
    Tworzy zrzut ekranu i pobiera jego własciwosci.
    
    Wynik
    -------
    Tulpa z 2 warosciami int

    """
    Screenshot = pyautogui.screenshot()
    wysokosc=Screenshot.height
    szerokosc=Screenshot.width
    ustaw_rozdzielczonsc((szerokosc,wysokosc))

def ustaw_rozdzielczonsc(rozdzielczosc):
    """
    Instrukcja warunkowa, przyporządkowująca do uzywanego przez program 
    slownika, spisu pozycji dla widzetow w zaleznosci od wykrytej 
    rozdzielczosci.

    Parameters
    ----------
    rozdzielczosc : tulpa z 2 wartosciami int

    Wynik
    -------
    Ustawienie wartosci słownika aktualny_widzet
    """
    global aktualny_widzet
    if  rozdzielczosc[0] >1400:
        aktualny_widzet=Widzety_1920
        Konfiguracja["szer_kom"]=8
    else:
        aktualny_widzet=Widzety_1400
        Konfiguracja["szer_kom"]=6
        
        
def zbadaj_zdj(image):
    """
    Okresla jakie wielkosci (w pixelach) ma szerokosc lini pomiedzy komórkami
    na zdjęciu, oraz komórki

    Parameters
    ----------
    image : jpg plik do przebadania

    Wynik
    -------
    Tulpa,  z 2 wartosciami

    """
    width, height = image.size
    kolor_lini=image.getpixel((0,0))
    w_1=False
    szer_lini=0
    szer_kom=0
    lista_kolorów=[]
    for y in range(height):
        for x in range(width):        
            pixel=image.getpixel((x,y))
            if pixel not in lista_kolorów:
                lista_kolorów.append(pixel)
                if len(lista_kolorów)>3:
                    return "Nope"
            if pixel != kolor_lini:
                if w_1 == False:
                    szer_lini = y
                    w_1=True
                for x_2 in range(x,width):
                    pixel=image.getpixel((x_2,y))
                    if pixel == kolor_lini:
                        szer_kom= x_2-szer_lini
                        paczka=(szer_lini,szer_kom)
                        return paczka
            
def zywe_kom_ze_zdj(image,szer_lini,szer_kom):
    """
    Funkcja pobiera wartosci RGB na zdjęciu  w odpowiednich miejscach.
    Jeżeli wartoć odpowada kolorowi czarnemu, to dodaje do listy
    odpowiadajace tej komorce wspolrzedne.

    Parameters
    ----------
    image : jpg - obraz zestawu
    szer_lini : int - szerokosc lini pomiedzy komórkami w pixelach
    szer_kom : int - szerokosc komórki w pixelach

    Wynik
    -------
    Lista

    """
    lista_wsp_zywych_kom=[]
    width, height = image.size
    kolor_kom=(0, 0, 0, 255)
    skok=szer_lini+szer_kom
    pocz=int((szer_lini+szer_kom)/2)
    ile_kom_y=int((height-skok)/skok)+1
    ile_kom_x=int((width-skok)/skok)+1
    for y in range(0,ile_kom_y):
        for x in range(0,ile_kom_x):
            punkt=(pocz+(x*skok),pocz+(y*skok))
            pixel=image.getpixel(punkt)
            if pixel == kolor_kom:
                cos=(x,y)
                lista_wsp_zywych_kom.append(cos)
    return lista_wsp_zywych_kom

def symulacja(tupele, ile_gen, parametry):
    """
    Funkcja pelniaca role symulacji

    Parameters
    ----------
    tupele: list
        pary liczb w tuplu w liscie, koordynaty punktów
    ile_gen: int
        ilosc generacji symulacji
    parametry: slownik
        ustalone ilosci sasiadow do przezycia, wskrzeszenia lub smierci

    Wynik
    -------
    Lista wszystkich generacji, w postaci zywych punktow na planszy (koordynaty punktów)

    """
    pierwotne_tulpe=tupele
    licznik = 0


    sasiedzi = [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]
    wszystkie_gen = [tupele] 
    wszystkie_koordynaty = [] 
    for x in range(100):
            for y in range(100):
                    wszystkie_koordynaty.append((x,y))
    while licznik < ile_gen:
        wynikowa = []
        for komorka in wszystkie_koordynaty:
            sasiedzi_koor = [tuple(map(sum,zip(x,komorka))) for x in sasiedzi]
            ilosc_sasiadow = len(set(wszystkie_gen[licznik]) & set(sasiedzi_koor))
            if komorka in wszystkie_gen[licznik]:
                if parametry["samotnosc"] < ilosc_sasiadow < parametry["scisk"]:
                    wynikowa.append(komorka)
            elif ilosc_sasiadow == parametry["nadzieja"]:
                    wynikowa.append(komorka)
        wszystkie_gen.append(wynikowa)
        licznik += 1
        if wynikowa==tupele:
            print("Wykryto cyklicznosć")
            return wszystkie_gen
    return wszystkie_gen

def zapisz_generacje(symulacja, nazwa_pliku):
    i = 0
    f= open(nazwa_pliku,"w")
    f.write(Konfiguracja["Klucz zabezpieczający_symulacje"]+"\n")
    while i < len(symulacja):
        line = list("0"*10000+"\n")
        for koor in symulacja[i]:
            line[koor[1]*100+koor[0]] = "1"
        f.write(''.join(line))
        i+=1
    f.close()
    return
    
def koloruj_mapę(ścieżka,macierz,nazwa,krok,szerokość): # z macierzy pobiera rzędy i szereg
    """
    Funckja używana w celu stworzenia i umieszczenia w pamięci podrecznej 
    zbioru bitmap, które docelowo zostaną później przeakazane funkcji "z_gifa"
    w celu wizualizacji przebiegu symulacji.
    
    Parameters
    ----------
    ścieżka (str) : nazwa pliku "*.bmp", który jest szkicem, białą planszą z 
    zaznaczoną kratownicą,
    
    macierz (list) : Lista list z obiektami,
    
    nazwa (str) : nazwa pliku "*.txt", w któym znajdue się zapis Środowiska,
    
    krok (int) : odległość pomiędzy liniami kratownicy,
    
    szerokość (int) : ilość obiektów  w lini poziomej,
    
    kolejka (queue) : instancja klasy queue,

    Wynik
    -------
    Dodajanie elementów do zadeklarowanego obiektu "kolejka".
    """
    #sekcja wczytywania danych opisujących arkusz
    podst=Image.open(ścieżka) # zmienna jako oryginal
    im2=podst.copy() # w tym  miejscu robimy kopię oryginału i na nim praucjemy
    n2=0 # licznik szeregów - szerokość
    s_odl=krok
    x0=1
    x1=s_odl
    y0=1
    y1=s_odl
    litera=0
    while litera<len(macierz):# rzędy  | góra -> dół
        n2=0
        while n2<szerokość:# szeregi | lewo-> prawo
            komórka_w=macierz[litera] # ustala który znak
            kolor=słownik_kolorów(komórka_w)  # zwraca odpowiedni mu kolor
            for y in range(y0,y1):
                for x in range(x0,x1):
                    im2.putpixel((x,y),kolor)# ten fragment zamalowuje 1 komórkę
            x0=x0+s_odl
            x1=x1+s_odl
            n2+=1 #szerokość
            litera=litera+1 # ktory element ze str
        n2=0
        x0=1
        x1=s_odl
        y0=y0+s_odl
        y1=y1+s_odl
    tulpa=(im2,nazwa)
    return tulpa ##ZMIANA## zwykly return z funkcji zamiast put do kolejki  
    
def słownik_kolorów(znak):
    """
    Zwraca odpowiedni dla symbolu danej klasy kolor RGB.
    Używana przy kolorowaniu_map.
    
    Parameters
    ----------
    znak (str) : symbol klasy,

    Wyniki
    -------
    kolor (list) - wartości RGB.

    """
    kom=znak
    kolor=0
    if kom =="0":   # Cell 
        kolor=(255,255,255) #= biały 
    elif kom=="1":   # Cell_Dead 
        kolor=(0,0,0) # = czarny
    return kolor

def z_gifa(zbiór_bitmap):
    """
    Tworzy plik "*.gif", z podanego w argumentach zbioru uszeregowanych 
    chronologicznie bitmap w celu animacji przebiegu symulacji.

    Parameters
    ----------
    zbiór_bitmap (list) : lista bitmap

    Wynik
    -------
    Plik "movie_ASF.gif".

    """
    imageio.mimsave(os.getcwd()+'\\movie_CA.gif', zbiór_bitmap, duration=0.4)
    
if __name__=='__main__':    
    wykryj_rozdzielczosc()
    app=wx.App()
    okno=Okno_interfejsu_glownego()
    okno.Show()
    app.MainLoop()
