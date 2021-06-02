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
from wx.adv import Animation, AnimationCtrl
import imageio
import wx.lib.scrolledpanel
from datetime import datetime

Parametry={
    "samotnosc" : 1, 
    "scisk" : 4, 
    'nadzieja': 3, 
    "ile_generacji" : 100
    }

Konfiguracja={
    "klucz_zabezpieczajacy_slownik":"$*&*&*@002!",
    "klucz_zabezpieczajacy_zestaw":"6273##$2nnd!",
    "Klucz_zabezpieczajacy_scenariusz":"**823$%@@7&*&*!",
    "Klucz_zabezpieczajacy_symulacje":"SyMuLaCjA112!",
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
    "Okno_pomoc_size":(650,830),
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

Slownik_opisow={
    0: """
        Witaj uzytkowniku, przed Toba zapewne otworzyla sie juz nasza gra – Gra w zycie.
        Czym jest w ogole Gra w zycie? Jest to automat komorkowy opracowany przez
        brytyjskiego matematyka Johna Conwaya w 1970 roku.
        Brzmi dosyc skomplikowanie? Nie martw sie, zaraz wszystko Ci wytlumaczymy.
        
        Gra ta toczy sie na skończonej planszy, podzielonej na kwadratowe komorki, 
        100 na 100 wiec jest ich az 10 000. Aktualnie widzisz przed soba pusta plansze 
        i kafelki z roznymi opcjami do wyboru.
        Kazda komorka na naszej planszy ma 8 sasiadow, przylegaja do niej bokami i rogami.
        
        A kazda taka komorka moze znajdowac sie w jednym z dwoch stanow:
        moze byc „zywa” lub „martwa”. Stany komorek zmieniaja sie w pewnych jednostkach czasu,
        ktory nastepnie jest uzywany do obliczenia stanu wszystkich komorek w nastepnej jednostce.
        Po obliczeniu wszystkie komorki zmieniaja swoj stan dokladnie w tym samym momencie.
        
        Kiedy wiadomo, ze komorka jest w stanie „zycia”?
        W naszej wersji jest wtedy pokolorowana na czarno a jej dokladny stan
        zalezy tylko i wylacznie od liczby jej zywych sasiadow. A gdy „zywa” komorka dojdzie do 
        krawedzi planszy, umiera.
        
        Co ciekawe…w grze w zycie nie ma graczy w doslownym tego slowa znaczeniu,
        Twoj udzial sprowadza sie jedynie do ustalenia stanu poczatkowego komorek. 
        
        Stan poczatkowy komorek opiera sie na wzorcach, a dokladniej
        na regulach wymyslonych przez Conwaya, gdzie: 
        • Martwa komorka, ktora ma dokladnie 3 zywych sasiadow,
        staje sie zywa w nastepnej jednostce czas
        • zywa komorka z 2 albo 3 zywymi sasiadami pozostaje nadal zywa; 
        przy innej liczbie sasiadow umiera
        
        
        Pewnie sie zastanawiasz, co dalej, jak masz zaczac?
        Specjalnie dla Ciebie stworzylismy instrukcje,
        wiec usiadz wygodnie i baw sie dobrze!
        
        Zestawy:
            
        - Stworz manualnie: Mozliwosc stworzenia wlasnego zestawu poczatkowego.
        1)	Otwarcie nowego okna „Rysowanie_zestawu”.
        2)	Poruszanie po planszy: Z pomoca lewego przycisku myszy klikasz/przeciagasz
        myszke na dowolna komorke i z kombinacja przyciskow shift + z tworzysz zywa komorke,
        kombinacja shift + x mozesz ja anulowac/skasowac.
        3)	Zapisanie zestawu: Jezeli chcesz zapisac zestaw,
        klikasz w „Zestawy” i zapisujesz.
        4)	Po zapisaniu, mozesz spokojnie zamknac okno i wrocic na interfejs glowny.
        5)	Wczytanie: Jezeli chcesz wczytac swoj zapisany zestaw,
        na interfejsie glownym klikasz w „Zestawy”, nastepnie „Wczytaj”,
        wybierasz zestaw i gotowe.
        
        Zestaw komorek pojawia Ci sie na planszy poczatkowej.
        
        - Wylosuj: Pojawia sie losowy gotowy zestaw.
        
        1)	Mozliwosc zmiany wylosowanego zestawu po ponownym kliknieciu „Wylosuj”.
        2)	Zapisanie zestawu: Jezeli chcesz zapisac zestaw, klikasz w „Zestawy” 
        i zapisujesz, zapisany zestaw laduje w folderze w ktorym znajduje sie zainstalowana gra. 
        
        - Stworz ze zdjecia: Wybranie gotowego zestawu zapisanego w formacie graficznym.
    
        1)	Przykladowe zestawy znajduja sie w folderze gdzie zostala zainstalowana gra
        - komorki z niektorych zestawow moga szybko umrzec, badz formowac sie w te same pozycje w 
        nieskończonosc 
        - dane zestawy posiadaja swoje wlasne nazwy, pochodzace z specjalnej biblioteki, dostepnej w 
        internecie, na przyklad na stronie https://conwaylife.appspot.com/library
        
        ******************************************************************************************************
        Zestawy zapisuja sie w formacie txt, plik z zestawem posiada kod zabezpieczajacy oraz
        aktualne pozycje zywych komorek zapisanych w formie pary liczb, odpowiadajacych numerze
        kolumny i wiersza danej zywej komorki.
        
        W przypadku zestawow "stworz ze zdjecia", sa to pliki graficzne, zapisane w formacie png.
        
        ******************************************************************************************************        

        Parametry:
            
        1)	Gra w zycie posiada reguly, reguly te zostaly zapisane
        pod nazwa parametry, ustalone przez autorow gry, ale…mozesz je zmienic.
        2)	W Parametrach, kliknij zamień, pojawia sie okienko w ktorym mozesz 
        zmienic parametr dla „Samotnosc”, „scisk”, „Nadzieja”, „Ile generacji”
        3)	„Samotnosc” i „scisk”  – przy jakiej liczbie sasiadow komorka umrze,
        ustalona przez autorow wynosi 1 i 4
        4)	„Nadzieja” -  przy jakiej ilosci sasiadow komorka ozyje przy nastepnej
        jednostce czasu, ustalona przez autorow wynosi 3
        5)	„Ile generacji” – ile razy komorki zywe zmienia swoj stan w jednostkach
        czasu, ustalona przez autorow wynosi 100, zalecane jest trzymanie ilosci
        nie wiekszej niz 100 i nie mniej niz 1
        
        ******************************************************************************************************
        Parametry zapisuja sie w formacie txt, plik sklada sie z 5 linijek:
        - klucz zabezpieczajacy
        - wartosc aktualna: samotnosc
        - wartosc aktualna: scisk
        - wartosc aktualna: nadzieja
        - wartosc aktualna: ile_generacji
        
        ******************************************************************************************************

        ******************************************************************************************************
        Scenariusze zapisuja sie w formacie txt, plik sklada sie z kilkunastu linijek:
        - klucz zabezpieczajacy
        - wartosc aktualna: samotnosc
        - wartosc aktualna: scisk
        - wartosc aktualna: nadzieja
        - wartosc aktualna: ile_generacji
        - informacja o zakończeniu parametrow: __PARAMETRY_KONIEC__
        - aktualne pozycje zywych komorek zapisanych w formie pary liczb, odpowiadajacych numerze
        kolumny i wiersza danej zywej komorki
        
        ******************************************************************************************************
        
        2. Symulacja i animacja.
    
        Majac stworzony manualnie, wylosowany lub stworzony ze zdjecia zestaw,
        ktory wczytany zostal jako plansza poczatkowa mozesz kliknac przycisk „Symulacja”
        ktory odpowiada za pobranie pozycji komorek zywych i zapisanie ich w takiej formie 
        aby mogla zostac stworzona Animacja.
        
        Po kliknieciu „Symulacja” musisz sie uzbroic w cierpliwosc i poczekac kilka sekund, 
        po zakończeniu symulacji zostanie pokazany odpowiedni komunikat.
        
        Nastepnie klikasz „Animacja” plik z aktualna symulacja zapisze sie w folderze o nazwie
        "Folder_na_symulacje", folder ten znajduje sie w miejscu zainstalowanej gry. Aktualna symulacja 
        zapisana jest pod nazwa "Symulacja" z data i godzina jej stworzenia, po wybraniu pliku
        animacja zaczyna swoja prace, pod odczekaniu kolejnych kilku sekund na nowym oknie pojawia
        sie animacja aktualnego zestawu. 
        
        Fajne prawda? A teraz kombinuj i baw sie dobrze.
        
        """
    }

aktualny_widzet={}
aktualny_zestaw=[]

class Okno_interfejsu_glownego(wx.Frame):
    """
    Klasa glownego okna,stanowiaca trzon interfejsu programu.
    """
    def __init__(self,parent=None):
        """
        Konstruktor klasy Okno_interfejsu_glownego.
        """
        super(Okno_interfejsu_glownego,self).__init__(parent)
        self.intiUI()
        
    def intiUI(self):
        """
        Metoda odpowiadajaca za forme i rozmieszczenie widzetow okna.
        """
        menubar=wx.MenuBar()
        self.SetMenuBar(menubar)
        self.panel=wx.Panel(self,wx.ID_ANY)
        k_zestawy=wx.Menu()
        
        zestawy_1=k_zestawy.Append(wx.ID_ANY,"Wczytaj")
        zestawy_2=k_zestawy.Append(wx.ID_ANY,"Zapisz")
        zestawy_3=k_zestawy.Append(wx.ID_ANY,"Stworz manualnie") 
        zestawy_4=k_zestawy.Append(wx.ID_ANY,"Wylosuj") 
        zestawy_6=k_zestawy.Append(wx.ID_ANY,"Stworz ze zdjecia")
        zestawy_7=k_zestawy.Append(wx.ID_ANY,"Zapisz podglad")
        zestawy_8=k_zestawy.Append(wx.ID_ANY,"Wyczysc plansze")
        
        self.Bind(wx.EVT_MENU,self.wx_wczytaj_zestaw, zestawy_1)
        self.Bind(wx.EVT_MENU,self.wx_zapisz_zestaw, zestawy_2)
        self.Bind(wx.EVT_MENU,self.wx_zestaw_rysuj, zestawy_3)
        self.Bind(wx.EVT_MENU,self.wx_wylosuj_zestaw, zestawy_4)
        self.Bind(wx.EVT_MENU,self.wx_zestaw_ze_zdj ,zestawy_6)
        self.Bind(wx.EVT_MENU,self.wx_zapisz_podglad_zestawy,zestawy_7)
        self.Bind(wx.EVT_MENU,self.wx_wyczysc_plansze_poczatkowa,zestawy_8)
        
        menubar.Append(k_zestawy,"Zestawy")
        
        k_parametry=wx.Menu()
        parametry_1=k_parametry.Append(wx.ID_ANY, "Wczytaj")
        parametry_2=k_parametry.Append(wx.ID_ANY, "Zapisz")
        parametry_3=k_parametry.Append(wx.ID_ANY, "Zmień")
        self.Bind(wx.EVT_MENU, self.wx_wczytaj_parametry, parametry_1)
        self.Bind(wx.EVT_MENU, self.wx_zapisz_parametry, parametry_2)
        self.Bind(wx.EVT_MENU, self.wx_zmien_parametry, parametry_3)
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
        
        self.Przycisk_symulacja=wx.Button(self.panel, -1, "Symulacja",
                                      pos=(aktualny_widzet["Start_pos"][0],
                                           aktualny_widzet["Start_pos"][1]),
                                      size=(aktualny_widzet["Start_size"][0],
                                            aktualny_widzet["Start_size"][1]))
        self.Przycisk_symulacja.Bind(wx.EVT_BUTTON,self.wx_test_do_symulacji)
        
        self.Przycisk_animacja=wx.Button(self.panel, -1, "Animacja",                                      
                                         pos=(aktualny_widzet["Animancja_pos"][0],
                                           aktualny_widzet["Animancja_pos"][1]),
                                      size=(aktualny_widzet["Animancja_size"][0],
                                            aktualny_widzet["Animancja_size"][1]))
        self.Przycisk_animacja.Bind(wx.EVT_BUTTON, self.wx_test_do_animacji) 
        
        if os.path.exists("Generacja_0.bmp")==True:
            os.remove("Generacja_0.bmp")
        if os.path.isdir('./Folder_na_symulacje')==False:
            os.mkdir('./Folder_na_symulacje')
        stw_plansze_poczatkowa()
        zdj=wx.Bitmap("Generacja_0.bmp", wx.BITMAP_TYPE_ANY)
        self.obraz = wx.StaticBitmap(self.panel, wx.ID_ANY, zdj,
                                     pos=(aktualny_widzet["Obraz_pos"][0],
                                          aktualny_widzet["Obraz_pos"][1]))
        self.SetSize((aktualny_widzet["Okno_size"][0],
                      aktualny_widzet["Okno_size"][1]))
        self.Centre()
        self.SetTitle("Program automatow komorkowych")
        
    def wx_wyczysc_plansze_poczatkowa(self,evt):
        zdj=wx.Bitmap("Generacja_0.bmp", wx.BITMAP_TYPE_ANY)
        Okno_interfejsu_glownego.obraz = wx.StaticBitmap(self, bitmap=zdj,pos=(aktualny_widzet["Obraz_pos"][0],
                                          aktualny_widzet["Obraz_pos"][1]))
        Okno_interfejsu_glownego.Refresh(self)
        Okno_interfejsu_glownego.Update(self)
        
    def wx_help(self,evt):
        ok4=Okno_pomocy()
        ok4.Show()
        
    def wx_test_do_symulacji(self,evt):
        if len(aktualny_zestaw)!=0:
            self.wx_symulacja()
            self.wx_wyswietl_wiadomosc(("Ukończono symulacje"),"info")
        else:
            self.wx_wyswietl_wiadomosc(("Nie wybrano \ stworzone zestawu"),"error")
                         
    def wx_test_do_animacji(self,evt):
        dialog=wx.FileDialog(self,message='Wybierz plik z zapisem symulacji',defaultFile='',wildcard='*.TXT',style=wx.FD_OPEN, pos=(10,10))
        if dialog.ShowModal() == wx.ID_OK:
            sciezka = dialog.GetPaths()[0]
            dialog.Destroy()
            self.wx_animacja(sciezka)
                 
    def wx_animacja(self,nazwa_pliku):
        """
        Za pomoca glownej petli sterujacej kazda linia z wczytanego pliku,
        ze znakowym zapisaem stanu jednostki czasu danej symulacji, 
        jest rozdzielana za pomoca multiprocesingu na sa procesy potomne w 
        postaci argumentu dla funkcji koloruj mape. Kazdy proces potomny 
        skutkuje wyprodukowaniem 1 mapy, ktora ilustruje zadany moment 
        symulacji. Mapy te sa zostajapo zworceniu ze wspomnianej funckji
        odrazu wstawiane w odpowiednie miejsce wczesniej spreparowanej lsity
        "wyniki", poprzez zamiane pustego elementu o indeksie odpowiadajacym 
        numerowi stworzonemu procesu.
        
        Wynik
        -------
        Tworzy plik nazwie "movie_CA.gif".
        """
        
        
        wyniki=[]
        lista=[]
        with open(nazwa_pliku) as f: # jest tylko 1  otawrcie pliku zmiast kazdrazowego przy wywolaniu funkcji
            klucz_zab=f.readline() #zbiera klucz zabezpieczajcy
            klucz_zab=klucz_zab.replace('\n', '')
            if klucz_zab!=Konfiguracja['Klucz_zabezpieczajacy_symulacje']:
                self.wx_wyswietl_wiadomosc(("Wybrany plik nie jest plikiem symulacji"),"error")
                return 
            while True:
                line = f.readline().replace('\n', '')
                if not line:
                    break
                lista.append(line) #zrzuca plik do listy
        self.progres_bar = wx.ProgressDialog(title="Pasek postepu", message="Postep animacji: {} / {}. Prosze czekac".format(0,len(lista)-1), maximum=len(lista)-1, parent=self)
        for x in range(0,len(lista)):
            wyniki.append(koloruj_mape("Generacja_0.bmp",lista[x],str(x),Konfiguracja["szer_kom"],100)[0])
            tekst="Postep animacji: {} / {}. Prosze czekac".format(x, len(lista)-1)
            self.wx_test_uaktualnij_pasek(x, tekst)
        self.progres_bar.Destroy()
        self.wx_wyswietl_wiadomosc("Ukończono animacje", "info")
        z_gifa(wyniki)    
        ok3=Okno_animacji()
        ok3.Show()
        
    def wx_symulacja(self):
        """
        Funkcja pelniaca role symulacji
    
        Parameters
        ----------
        tupele: list
            pary liczb w tuplu w liscie, koordynaty punktow
        ile_gen: int
            ilosc generacji symulacji
        parametry: slownik
            ustalone ilosci sasiadow do przezycia, wskrzeszenia lub smierci
    
        Wynik
        -------
        Lista wszystkich generacji, w postaci zywych punktow na planszy (koordynaty punktow)
    
        """
        tupele=plansza_na_tuple(aktualny_zestaw)
        ile_gen=Parametry['ile_generacji']
        parametry=Parametry
        licznik = 0
        max_zakres=ile_gen
        tekst="Postep symulacji: {} / {}. Prosze czekac".format(licznik, ile_gen)
        self.progres_bar = wx.ProgressDialog(title="Pasek postepu", message=tekst, maximum=max_zakres, parent=self)

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
            
            
            if wynikowa in wszystkie_gen:
                tekst="Postep symulacji: {} / {}. Prosze czekac".format(licznik, ile_gen)
                self.wx_test_uaktualnij_pasek(ile_gen, tekst)
                zapisz_generacje(wszystkie_gen, "Symulacja.txt")
                return
            wszystkie_gen.append(wynikowa)
            licznik += 1
            tekst="Postep symulacji: {} / {}. Prosze czekac".format(licznik, ile_gen)
            self.wx_test_uaktualnij_pasek(licznik, tekst)
                
        tekst="Postep symulacji: {} / {}. Prosze czekac".format(licznik, ile_gen)
        self.wx_test_uaktualnij_pasek(ile_gen, tekst)
        self.progres_bar.Destroy()
        zapisz_generacje(wszystkie_gen, "Symulacja.txt")

    def wx_aktualizuj_podglad_zestawu(self):
        koloruj_mape_tylko_poczatkowa(aktualny_zestaw)
        zdj=wx.Bitmap("Plansza_poczatkowa.bmp", wx.BITMAP_TYPE_ANY)
        Okno_interfejsu_glownego.obraz = wx.StaticBitmap(self, bitmap=zdj,pos=(aktualny_widzet["Obraz_pos"][0],
                                          aktualny_widzet["Obraz_pos"][1]))
        Okno_interfejsu_glownego.Refresh(self)
        Okno_interfejsu_glownego.Update(self)
        
    def wx_zapisz_podglad_zestawy(self,evt):
        
        pop=wx.TextEntryDialog(self,"Podaj nazwe dla zdjecia z podgladem zestawu.")
        pop.ShowModal()
        nazwa=pop.GetValue() 
        if "podglad" not in nazwa or "Podglad" not in nazwa:
            nazwa="Podglad_"+nazwa
        if os.path.exists(nazwa):
            nazwa2=nazwa.split(".")
            nazwa=nazwa2[0]+"_nowa_nazwa.txt"
            self.wx_wyswietl_wiadomosc(("Podana nazwa jest juz zajeta.\n Podglad zestawu zostanie zapisany jako "+nazwa),"warning")
        
        podst=Image.open("Plansza_poczatkowa.bmp")
        podst.save(nazwa+".bmp")

        
    def wx_zamknij(self,evt):
        """
        Metoda zamykajaca Obiekt Okno_interfejsu_glownego i tym samym wszystkie instancje
        obiektow potomnych.

        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        Zamyka program.
        """
        dialog = wx.MessageDialog(self,"Czy na pewno?","Kończymy prace", style = wx.OK|wx.CANCEL)
        x = dialog.ShowModal()
        if x == wx.ID_OK:
            self.Close()
            
    def wx_test_paska(self,evt):
        """
        Funckja do debugu paska postepu.

        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        Wywolanie funckji wx_test_uaktualnij_pasek i stowrzenie atrybutu
        progres_bar

        """
        max_zakres=10
        self.progres_bar = wx.ProgressDialog("Postep symulacji", "prosze czekac", maximum=max_zakres, parent=self)
        for x in range(1,max_zakres):
            time.sleep(0.1)
            self.wx_test_uaktualnij_pasek(x)
        self.wx_test_uaktualnij_pasek(max_zakres)
            
    def wx_test_uaktualnij_pasek(self,wartosc,wiadomosc):
        """
        Funckja pozwalajaca na zaktualizawanie paska postepu do podanej 
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
        Funckja do podpiec kafelek i przyciskow.
        Docelowo zostanie usunieta po ukończeniu prac nad funkcjami.

        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika

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
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        Wywolanie funkcji wx_wyswietl_wiadomosc

        """
        wiadomosc=" Program autorstwa:\n Patrycji Chmielowskiej oraz Jaroslawa Weleszczuk, \n studentow Uniwersytetu Przyrodniczego we Wroclawiu."
        self.wx_wyswietl_wiadomosc(wiadomosc,"info")
    

    def wx_zapisz_zestaw(self,evt):
        """
        Zapisuje ciag tulp reprezentujacych osobniki ze zmiennej
        aktualny zestaw. W przypadku istnienia juz takiego pliku modyfikuje
        jego nazwe i wyswietla o tym komuniakt.

        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika
        
        Wynik
        -------
        Zapisuje plik z tulpowa reprezentacja zywych komorek.
        """
        if type(aktualny_zestaw) != list:
            pop=wx.TextEntryDialog(self,"Podaj nazwe dla pliku ze zestawem : ")
            pop.ShowModal()
            nazwa=pop.GetValue() 
            
            if "Zestaw" not in nazwa:
                nazwa="Zestaw_"+nazwa
            if ".txt" not in nazwa:
                nazwa=nazwa+".txt"
            if os.path.exists(nazwa):
                nazwa2=nazwa.split(".")
                nazwa=nazwa2[0]+"_nowa_nazwa.txt"
                self.wx_wyswietl_wiadomosc(("Podana nazwa jest juz zajeta.\n Zestaw zostal zapisany jako "+nazwa),"warning")
    
            pary_tupli= plansza_na_tuple(aktualny_zestaw)
            zapisz_zestaw(pary_tupli,nazwa)
        else:
            self.wx_wyswietl_wiadomosc(("Brak zestawu"),"error")
        
    def wx_wczytaj_zestaw(self,evt):
        """
        Wyswietla okno wyboru pliku. 
        
        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        Zmienia zmienna aktualny_zestaw.
        """
        dialog=wx.FileDialog(self,message='Wybierz plik zestawu',defaultFile='',wildcard='*.TXT',style=wx.FD_OPEN, pos=(10,10))
        if dialog.ShowModal() == wx.ID_OK:
            sciezka = dialog.GetPaths()[0]
            global aktualny_zestaw
            aktualny_zestaw=wczytaj_zestaw(sciezka)
            self.wx_aktualizuj_podglad_zestawu()
            dialog.Destroy()
            
    def wx_wylosuj_zestaw(self,evt):
        """
        Funkcja tworzy zestaw, z iloscia komorek z zakresu 10-100

        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        Zmiana globalnej zmiennej aktualny zestaw

        """
        ilosc=random.randrange(500,1500)
        plansza=(wylosuj_zestaw(ilosc))[0]
        global aktualny_zestaw
        aktualny_zestaw = plansza
        self.wx_aktualizuj_podglad_zestawu()
        
    def wx_zestaw_rysuj(self,evt):
        """
        Tworzy instancje klasy Okno_rysowania_zestawu.
        
        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        Wywolanie nowego okno

        """
        okno_potomne_2=Okno_rysowania_zestawu()
        okno_potomne_2.Show()
        
    def wx_zestaw_ze_zdj(self,evt): 
        """
        Funckja sluzaca do okreslenia przez uzytkownika, jakie zdjecie
        chce przetworzyc.

        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        Wywolanie funckji wx_skanuj_zdjecie

        """
        dialog=wx.FileDialog(self,message='Wybierz zdjecie planszy do przetworzenia',defaultFile='',wildcard='*.PNG',style=wx.FD_OPEN, pos=(10,10))
        if dialog.ShowModal() == wx.ID_OK:
            sciezka = dialog.GetPaths()[0]
            dialog.Destroy()
        self.wx_skanuj_zdjecie(sciezka)

        
    def wx_skanuj_zdjecie(self,plik):  
        """
        Funckja wywoluje szereg innnych funkcji, majacych na celu
        ustalenie pozycji zywych kom komorek na zdjeciu.

        Parameters
        ----------
        plik : (jpg) - plik, ktory posluzy dalej za argument

        Wynik
        -------
        Zmiana globalnej zmiennej aktualny zestaw

        """
        image = PIL.Image.open(plik)
        wartosci=zbadaj_zdj(image)
        if wartosci =="Nope":
            self.wx_wyswietl_wiadomosc("Zdjecie zawiera wiecej niz 3 kolory. Nie mozna go przetworzyc","error")
        else:
            szer_lini = wartosci[0]
            szer_kom = wartosci[1]
            l_z_k=zywe_kom_ze_zdj(image,szer_lini,szer_kom)
            global aktualny_zestaw
            plansza= tupla_na_plansze(l_z_k)
            aktualny_zestaw = plansza
            self.wx_aktualizuj_podglad_zestawu()
            
    def wx_zapisz_scenariusz(self,evt):
        """
        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        Zapisanie scenariusza z pliku .txt

        """
        pop=wx.TextEntryDialog(self,"Podaj nazwe dla parametrow : ")
        pop.ShowModal()
        nazwa=pop.GetValue() # GetValue do okienek
        if "Scenariusz" not in nazwa:
            nazwa="Scenariusz_"+nazwa
        if ".txt" not in nazwa:
            nazwa=nazwa+".txt"
        if os.path.exists(nazwa):
            nazwa2=nazwa.split(".")
            nazwa=nazwa2[0]+"_nowa_nazwa.txt"
            self.wx_wyswietl_wiadomosc(("Podana nazwa jest juz zajeta.\n Parametry zostaly zapisany jako "+nazwa),"warning")
        zapisz_scenariusz(nazwa)
        pass

    def wx_wczytaj_scenariusz(self,evt):
        """
        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        WWczytanie scenariusza z pliku .txt

        """
        dialog=wx.FileDialog(self,"Wybierz plik scenariusza",defaultFile='',wildcard='*.TXT',style=wx.FD_OPEN, pos=(10,10))
        if dialog.ShowModal() == wx.ID_OK:
            sciezka = dialog.GetPaths()
            global Parametry
            global aktualny_zestaw
            Parametry,aktualny_zestaw=wczytaj_scenariusz(sciezka[0]) 
            dialog.Destroy()
        pass
       
    def wx_zapisz_parametry(self,evt):
        """
        Zapisuje wszystkie wartosci z aktualnie uzywanego slownika "Parametry"
        pod  wskazana przez uzytkownika nazwa. W przypadku istnienia
        juz takiego pliku modyfikuje jego nazwe i wyswietla o tym komuniakt.

        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        Zapisuje parametry slownika w pliku ".txt".
        """
        pop=wx.TextEntryDialog(self,"Podaj nazwe dla parametrow : ")
        pop.ShowModal()
        nazwa=pop.GetValue() # GetValue do okienek
           
        if "Parametry" not in nazwa:
            nazwa="Parametry_"+nazwa
        if ".txt" not in nazwa:
            nazwa=nazwa+".txt"
        if os.path.exists(nazwa):
            nazwa2=nazwa.split(".")
            nazwa=nazwa2[0]+"_nowa_nazwa.txt"
            self.wx_wyswietl_wiadomosc(("Podana nazwa jest juz zajeta.\n Parametry zostaly zapisany jako "+nazwa),"warning")
        zapisz_parametry(nazwa)

    def wx_wczytaj_parametry(self,evt):
        """
        Zmienia aktualnie uzytkowany slownik "Parametry" poprzez podmienienie
        go na nowego, wskazanego przez uzytkownika w oknie wyboru pliku.

        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        Zmiana wartosci slownila parametry, na te ze wskazanego z pliku.
        """
        dialog=wx.FileDialog(self,"Wybierz plik parametrow",defaultFile='',wildcard='*.TXT',style=wx.FD_OPEN, pos=(10,10))
        if dialog.ShowModal() == wx.ID_OK:
            sciezka = dialog.GetPaths()
            global Parametry
            Parametry=wczytaj_parametry(sciezka[0]) 
            dialog.Destroy()
            
    def wx_zmien_parametry(self, evt):
        """
        Tworzy okno, na ktorym uzytkownik moze skonfigorowac parametry.

        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        Utworzenie instancji klasy Okno_zmiany_parametrow

        """
        okno_potomne=Okno_zmiany_parametrow()
        okno_potomne.Show() 
        
    def wx_wyswietl_wiadomosc(self,wiadomosc,tryb):
        """
        Wyswietla okno dialogowe z wartosciami argumentow.

        Parameters
        ----------
        wiadomosc (str): komunikat do przekazania uzytkownikowi
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
        powiadomienie1=wx.MessageDialog(None,message=wiadomosc,style = wx.OK | styl )
        powiadomienie1.ShowModal()

class Okno_zmiany_parametrow(wx.Frame):
    def __init__(self,parent = None):
        """
        Konstruktor klasy Okno_interfejsu_glownego.
        """
        super(Okno_zmiany_parametrow,self).__init__(parent)
        self.intiUI()
    
    def intiUI(self):
        """
        Metoda odpowiadajaca za forme i widzety okna.
        """
        self.SetTitle("Zmiana parametrow")
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
        Zmienia wartosci slownika "Parametry" poprzez pzczytanie wartosci
        wpisanych przez uzytkownika w oknie zmiany parametrow.
        
        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        Zastapienie wartosci ze slownika 
        """
        scisk=self.t_scisk.GetValue()
        samotnosc=self.t_samotnosc.GetValue()
        nadzieja=self.t_nadzieja.GetValue()
        generacje=self.t_generacje.GetValue()
        
        if scisk.isnumeric() and samotnosc.isnumeric() and nadzieja.isnumeric()  and generacje.isnumeric():
            scisk=int(scisk)
            samotnosc=int(samotnosc)
            nadzieja=int(nadzieja)
            generacje=int(generacje)
            if samotnosc >=0 and scisk >0 and generacje >0 and nadzieja >0:
                if samotnosc <=8 and scisk <=8 and nadzieja<=8:
                    Parametry["samotnosc"] = samotnosc
                    Parametry["scisk"] = scisk
                    Parametry["ile_generacji"] = generacje
                    Parametry["nadzieja"] = nadzieja
                    Okno_interfejsu_glownego.wx_wyswietl_wiadomosc(self, "Zmieniono parametry", "info")
                else:
                    Okno_interfejsu_glownego.wx_wyswietl_wiadomosc(self,"Maksymalne sasiedztwo to 8","error")
            else:
                Okno_interfejsu_glownego.wx_wyswietl_wiadomosc(self,"Parametry nie moga byc ujemne","error")
        else:
            Okno_interfejsu_glownego.wx_wyswietl_wiadomosc(self,"Wprowadzone wartosci nie sa liczbami","error")
        
        
    def wx_2_wyczysc(self,evt):
        """
        Usuwa wartosci wpisane przez uzytkownika.
        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        Zastapienie wartosci pol na 0.

        """
        self.t_scisk.SetValue("0")
        self.t_samotnosc.SetValue("0")
        self.t_nadzieja.SetValue("0")
        self.t_generacje.SetValue("0")
    
class Okno_rysowania_zestawu(wx.Frame):
    def __init__(self, parent=None):
        super(Okno_rysowania_zestawu,self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        """
        Metoda odpowiadajaca za forme i widzety okna.
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
        Pobiera komorki, ktore sa aktualnie zaznaczona poprzez przytrzymanie
        lewego przycisku myszy i przeciagniecie kursora.
        
        Parameters
        ----------
        evt : Wywolanie przez okreslona akcja uzytkownika
  
        Wynik
        -------
        Wyowalnie funkcji
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
        evt : Wywolanie przez okrelona akcja uzytkownika
  
        Wynik
        -------
        Wyowalnie funkcji
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
        kursorem, lub przejscie za pomoca strzalek.
        
        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika
  
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
        evt : Wywolanie przez okrelona akcja uzytkownika
          
        Wynik
        -------
        Nic.
          
        """
        pass 
  
    def wx_3_wyczysc_siatke(self, evt):
        """
        Zmienia kolor wszystkich komorek na siatce na bialy.
          
        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika
          
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
        evt : Wywolanie przez okrelona akcja uzytkownika

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
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        Zmiana koloru komorek siatki.

        """
        dialog=wx.FileDialog(self,message='Wybierz plik zestawu',defaultFile='',wildcard='*.TXT',style=wx.FD_OPEN, pos=(10,10))
        if dialog.ShowModal() == wx.ID_OK:
            self.wx_3_wyczysc_siatke(evt)
            sciezka = dialog.GetPaths()[0]
            zestaw=wczytaj_zestaw(sciezka)
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
        evt : Wywolanie przez okrelona akcja uzytkownika

        Wynik
        -------
        Wywolanie okna dialogowego

        """
        tresc_wiadomosci = "Aby umiescic na planszy zywa komorke,\n nalezy kliknac \ przeciagnac myszkez \n i uzyc kombinacji shift+z. \n Analogicznie dla komorki martwej shif+x"
        Okno_interfejsu_glownego.wx_wyswietl_wiadomosc(self,tresc_wiadomosci, "info")
    
    def wx_3_komorki_na_czarno(self,evt):
        """
        Wywoluje funckje koloruj z argumentem koloru: czarny  
        
        Parameters
        ----------
        evt :Wywolanie przez okrelona akcja uzytkownika
          
        Wynik
        -------
        Wywolanie funckji
        """
        self.wx_3_koloruj(wx.BLACK,self.aktualnie_zaznaczone_kom)
            
    
    def wx_3_komorki_na_bialo(self,evt):
        """
        Wywoluje funckje koloruj z argumentem koloru: bialy 
          
        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika
          
        Wynik
        -------
        Wywolanie funckji
        """
        self.wx_3_koloruj(wx.WHITE,self.aktualnie_zaznaczone_kom)
    
    def wx_3_koloruj(self,kolor,lista):
        """
        Zmieia kolor aktualnie podanego jako argument
        zestawu komorek na odpowiedni kolor. 
          
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
        Zapisuje ciag tulp reprezentujacych osobniki ze zmiennej
        aktualny zestaw. W przypadku istnienia juz takiego pliku modyfikuje
        jego nazwe i wyswietla o tym komuniakt.

        Parameters
        ----------
        evt : Wywolanie przez okrelona akcja uzytkownika
        
        Wynik
        -------
        Zapisuje plik z tulpowa reprezentacja zywych komorek.
        """
        pop=wx.TextEntryDialog(self,"Podaj nazwe dla pliku ze zestawem : ")
        pop.ShowModal()
        nazwa=pop.GetValue() 
        
        if "Zestaw" not in nazwa:
            nazwa="Zestaw_"+nazwa
        if ".txt" not in nazwa:
            nazwa=nazwa+".txt"
        if os.path.exists(nazwa):
            nazwa2=nazwa.split(".")
            nazwa=nazwa2[0]+"_nowa_nazwa.txt"
            Okno_interfejsu_glownego.wx_wyswietl_wiadomosc(("Podana nazwa jest juz zajeta.\n Zestaw zostal zapisany jako "+nazwa),"warning")
        pary_tupli= plansza_na_tuple(aktualny_zestaw)
        zapisz_zestaw(pary_tupli,nazwa)
        
class Okno_animacji(wx.Frame):
   """
   Klasa ktorej jedynym celem jesy utworzenie nowego okna i ustawienie 
   animacji jako tlo.
   """
   def __init__(self, parent=None):
       """
       Konstruktor klasy Okno_animacji.
       """
       super(Okno_animacji, self).__init__(parent)
       self.InitUI()

   def InitUI(self):   
       """
       Metoda odpowiadajaca za forme i widzety okna.
       """
       sizer = wx.BoxSizer(wx.VERTICAL)
       anim = Animation('movie_CA.gif')
       ctrl = AnimationCtrl(self, -1, anim)
       ctrl.Play()
       sizer.Add(ctrl)
       self.SetSizerAndFit(sizer)  
       self.SetTitle('Podglad animacji')
       self.Show() 
   

class Okno_pomocy(wx.Frame):
   """
   Klasa ktorej jedynym celem jest utworzenie nowego okna i wyswietlenie 
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
       Metoda odpowiadajaca za forme i widzety okna.
       """
       self.Center()
       self.SetSize(700,700)
       self.CreateStatusBar()
       mainSizer = wx.BoxSizer(wx.VERTICAL)

       self.scroll = wx.ScrolledWindow(self, -1)
       self.scroll.SetScrollbars(1, 1, 700, 400)
       panelA = wx.lib.scrolledpanel.ScrolledPanel(self.scroll, -1, style=wx.SIMPLE_BORDER, size=(800,1985)) # to 2 sluzy do regulacji
       #jak daleko w dol mozesz zeskrolowac
       panelA.SetupScrolling()
       static_text=wx.StaticText(panelA, -1, Slownik_opisow[0])
       
       mainSizer.Add(panelA, 1, wx.ALL|wx.EXPAND|wx.ALIGN_LEFT, 5)
       self.scroll.SetSizer(mainSizer)
       self.Centre()

       
def wylosuj_zestaw(ilosc):
    """
    Generuje/Losuje zestaw losowych par liczb tak zwanych "tuple" i zapisuje
    je jako zmienna o nazwie "plansza", ktora przechowuje juz ustawione losowo
    na planszy pozycje zywych komorek.
    W fragemencie "return: plansza,tupele" instrukcja return,zwraca wywolane 
    pary tupli, w postaci numerow odpowiadajacych danej pozycji komorki zywej na 
    naszej planszy oraz jako pary liczb czyli wygenerowane nasze losowo tuple.
    Jezeli nasz stworzony i wskazany plik nie posiada zabezpieczenia w 
    formie ciagu znakow, lub nie istnieje w folderze z aplikacja, zostanie 
    wyswietlony stosowny komnunikat.
    
    Parametry
    ----------
    ilosc : int
        ilosc wystapienia naszych par liczb (tupli), ktore zapisywane sa aktualnie 
        na planszy (macierzy) w zmiennej o nazwie "plansza"
        
    Wynik
    -------
    Generuje okrelona ilosc tupli z przedzialu od 0 do 100, zwraca wynik do zmiennej
    "plansza" i a przechowuje je juz w pamieci komputera pod nazwa "komorki_zywe" 
    """
    plansza = np.zeros((100,100))
    tupele = sample(tuple(product(range(0,100), repeat=2)),ilosc)
    for tupel in tupele:
        plansza[int(tupel[0])][int(tupel[1])] = 1
    return plansza, tupele

def tupla_na_plansze(tupla):
    """
    Zamienia pary tupli, czyli nasze wylosowane pary liczb stanowiace polozenie 
    komorki, na plansze, czyli na plik programu z informacjami, w ktorej kolumnie i 
    rzedzie bedzie znajdowac sie nasza zywa komorka (zywa komorka oznaczona jako 1).
    
    Parametry
    ----------
    tupla : int
        zestaw losowych par liczb tak zwanych "tuple" zapisanych w postaci 
        listy
        
    Wynik
    -------
    Generuje plik programu z informacjami, w ktorej kolumnie i rzedzie bedzie 
    znajdowac sie nasza zywa komorka (zywa komorka oznaczona jako 1).
    """
    plansza = np.zeros((100,100))
    for tupel in tupla:
        plansza[int(tupel[1])][int(tupel[0])] = 1 
    return plansza

def plansza_na_tuple(plansza):
    """
    Zamienia plansze z juz nalozonymi parametrami zywej komorki, spowrotem 
    na pary tupli zapisane w zmiennej.
    
    Parametry
    ----------
    plansza: int
        plik programu z informacjami, w ktorej kolumnie i rzedzie bedzie 
        znajdowac sie nasza zywa komorka.
        
    Wynik
    -------
    Generuje uporzadkowana liste tupli, powstala z odczytanych parametrow
    znajdujacych sie w pliku programu "plansza"/"komorki_zywe", a dokladniej z
    odczytania numeru wiersza i kolumny w miejscu gdzie wystepuje zywa komorka, 
    nastepnie zapisuje je w postaci par liczb.
    """
    tupla = []
    for x in range(100):
        for y in range(100):
            if plansza[x][y] != 0:
                tupla.append((y, x))
    return tupla


def zapisz_zestaw(pary_tupli,nazwa_pliku):
    """
    Zapisuje wygenerowany/wylosowaney wczesniej zestaw losowych par liczb i 
    zapisuje je jako plik programu z informacjami, w ktorej kolumnie i rzedzie
    bedzie znajdowac sie nasza zywa komorka.
    Jezeli nasz stworzony i wskazany plik nie posiada zabezpieczenia w 
    formie ciagu znakow, lub nie istnieje w folderze z aplikacja, zostanie 
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
        f.write(Konfiguracja["klucz_zabezpieczajacy_zestaw"] + '\n')
        for item in pary_tupli:
            f.write("%s\n" % ','.join(map(str,item)))
        f.close()

         
def wczytaj_zestaw(nazwa_pliku):
    """
    Otwiera wczesniej wygenerowany plik .txt 
    Jezeli istnieje juz plik o wksazanej nazwie, lub nie posiada 
    ustalonego zabezpieczenia, zostanie wyswietlony stosowny komnunikat.
    Tworzy plansze gry o ustalonej wczesniej wielkosci, nastepnie pobiera
    z pliku wczesniej wygenerowanego pary liczb (tuple) i w miejsce 
    odpowiedniej kolumny i wiersza podstawia "1"
    Parametry
    ----------
    nazwa_pliku : str
        nazwa pliku, w ktorym zostaly zapisane wczesniej wygenerowane pary 
        liczb (tuple)
    Wynik
    -------
    Wygenerowanie planszy gry (macierzy) z zaznaczonymi na niej zywymi 
    komorkami - zywe oznaczone jako 1

    """
    with open(nazwa_pliku,"r") as plik:
        a=plik.readline()
        plik.close()
        if a != Konfiguracja["klucz_zabezpieczajacy_zestaw"]+"\n":
            print("Wybrany plik nie jest plikiem programu")
            return
    plansza = np.zeros((100,100))
    tupele = np.genfromtxt(nazwa_pliku, delimiter=',', skip_header=1)
    for tupel in tupele:
        plansza[int(tupel[0])][int(tupel[1])] = 1
    return plansza


def stw_plansze_poczatkowa(): 
    """
    Tworzy oryginalna, niepokolorowana mape bitmapowa. Ogolny szkic kratownicy,
    ktora potem bedzie kolorowana przez inne procesy. Wszelki wartosci potrzebne
    do jej stworzenia pobierane sa z aktualnie zaladowanego slownika Konfiguracja.

    Wynik
    -------
    Bitmapa "Generacja_0".

    """
    szerokosc =100
    wysokosc =100
    step=Konfiguracja["szer_kom"]
    height=wysokosc*step # prosta matematyka
    width=szerokosc*step
    obraz=Image.new(mode="RGB",size=(width,height),color=(255,255,255)) #mode=F bo dziele nizej
    draw=ImageDraw.Draw(obraz) # nasze tlo                          szerokosc x wysokosc
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
    
def koloruj_mape_tylko_poczatkowa(macierz): # z macierzy pobiera rzedy i szereg
    """
    Funkcja kolorujaca tylko 1 generacje z podstawki krawtownicy, stworzonej
    w funckji "stw_plansze_poczatkowa" o nazwie "Generacja_0.bmp"
    Potrzebne parametry sa pobierane z aktualnego slownika.

    Parameters
    ----------
    macierz (list) : lista obiektow,

    Wynik
    -------
    Plik "Plansza_poczatkowa.bmp"
    """
    krok = Konfiguracja["szer_kom"]
    #sekcja wczytywania danych opisujacych arkusz
    podst=Image.open("Generacja_0.bmp") # zmienna jako oryginal
    im2=podst.copy() # w tym  miejscu robimy kopie oryginalu i na nim praucjemy
    n2=0 # licznik szeregow - szerokosc
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
                        im2.putpixel((x,y),(0,0,0))# ten fragment zamalowuje 1 komorke
            x0=x0+s_odl
            x1=x1+s_odl
            n2+=1 #szerokosc
            litera=litera+1 # ktory element ze str
        n2=0
        x0=1
        x1=s_odl
        y0=y0+s_odl
        y1=y1+s_odl
    im2.save("Plansza_poczatkowa.bmp")
      
def wczytaj_parametry(nazwa_pliku):
    """
    Wczytuje plik programu z informacjami o ustawieniach gry.
    Jezeli wskazany plik nie posiada zabezpieczenia w formie ciagu znakow,
    lub nie istnieje w folderze z aplikacja, zostanie wyswietlony
    stosowny komnunikat.
    
    Parametry
    ----------
    nazwa_pliku : str
        nazwa pliku z o rozszerzeniu .txt
    
    Wynik
    -------
    Zwraca slownik o kluczach i wartosciach ze wsakzanego pliku.
    """
    wczytany_slownik={}
    if os.path.isfile(nazwa_pliku) :
        with open(nazwa_pliku,"r") as plik:
            a=plik.readline()
            a=a.replace('\n', '')
            if a ==Konfiguracja["klucz_zabezpieczajacy_slownik"]:
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
    Zapisuje aktualny slownik do pliku.txt
    Jezeli istnieje juz plik o wksazanej nazwie, lub nie posiada 
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
        Okno_interfejsu_glownego.wx_wyswietl_wiadomosc("Istnieje juz taki plik","warning")
    else:
        with open(nazwa_pliku,"w") as f:
            f.write(Konfiguracja["klucz_zabezpieczajacy_slownik"]+"\n")
            for k,v in Parametry.items():
                linia=k+":"+str(v)+"\n"
                f.write(linia)
                

def wczytaj_scenariusz(nazwa_pliku):
    """
    Wczytuje plik programu z informacjami o parametrach gry i aktualnym zestawie,
    ktorym moze byc: losowa generacja, wczytanie z obrazka, rysowanie.
    Jezeli wskazany plik nie posiada zabezpieczenia w formie ciagu znakow,
    lub nie istnieje w folderze z aplikacja, zostanie wyswietlony
    stosowny komnunikat.
    
    Parametry
    ----------
    nazwa_pliku : str
        nazwa pliku z o rozszerzeniu .txt
    
    Wynik
    -------
    Zwraca slownik o kluczach i wartosciach ze wsakzanego pliku.
    """
    
    wczytany_slownik={}
    if os.path.isfile(nazwa_pliku) :
        
        with open(nazwa_pliku,"r") as plik:
            a=plik.readline()
            licz = 0
            a=a.replace('\n', '')
            if a == Konfiguracja["Klucz_zabezpieczajacy_scenariusz"]:
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
    Funkcja zapisuje aktualny slownik i parametry do pliku.txt o wskazanej 
    nazwie.
    Jezeli istnieje juz plik o wksazanej nazwie, lub nie posiada 
    ustalonego zabezpieczenia, zostanie wyswietlony stosowny komnunikat.
    
    Parametry
    ----------
    nazwa_pliku : str
        nazwa pliku, do ktorego zostana zapisane parametry gry i aktualny zestaw.
    parametry: int
        ustalone i niezmienne zasady gru zwiazane z samotnoscia, sciskiem,
        nadzieja i iloscia generacji.
    aktualny_zestaw: int
        plik programu z informacjami o umiejscowieniu zywych komorek.

    Wynik
    -------
    Utworzenie pliku.txt o wskazanej nazwie.

    """
    global aktualny_zestaw
    if len(aktualny_zestaw) == 0:
        print("Nie mozna zapisac scenariusza, brak zestawu.")
        return
    if os.path.isfile(nazwa_pliku) :
        print("Wybrany plik juz istnieje")
    else:
        with open(nazwa_pliku,"w") as f:
            f.write(Konfiguracja["Klucz_zabezpieczajacy_scenariusz"]+"\n")
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
    Tworzy zrzut ekranu i pobiera jego wlasciwosci.
    
    Wynik
    -------
    Tulpa z 2 warosciami int

    """
    Screenshot = pyautogui.screenshot()
    wysokosc=Screenshot.height
    szerokosc=Screenshot.width
    ustaw_rozdzielczosc((szerokosc,wysokosc))

def ustaw_rozdzielczosc(rozdzielczosc):
    """
    Instrukcja warunkowa, przyporzadkowujaca do uzywanego przez program 
    slownika, spisu pozycji dla widzetow w zaleznosci od wykrytej 
    rozdzielczosci.

    Parameters
    ----------
    rozdzielczosc : tulpa z 2 wartosciami int

    Wynik
    -------
    Ustawienie wartosci slownika aktualny_widzet
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
    Okresla jakie wielkosci (w pixelach) ma szerokosc lini pomiedzy komorkami
    na zdjeciu, oraz komorki

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
    lista_kolorow=[]
    for y in range(height):
        for x in range(width):        
            pixel=image.getpixel((x,y))
            if pixel not in lista_kolorow:
                lista_kolorow.append(pixel)
                if len(lista_kolorow)>3:
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
    Funkcja pobiera wartosci RGB na zdjeciu  w odpowiednich miejscach.
    Jezeli wartoc odpowada kolorowi czarnemu, to dodaje do listy
    odpowiadajace tej komorce wspolrzedne.

    Parameters
    ----------
    image : jpg - obraz zestawu
    szer_lini : int - szerokosc lini pomiedzy komorkami w pixelach
    szer_kom : int - szerokosc komorki w pixelach

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
        pary liczb w tuplu w liscie, koordynaty punktow
    ile_gen: int
        ilosc generacji symulacji
    parametry: slownik
        ustalone ilosci sasiadow do przezycia, wskrzeszenia lub smierci

    Wynik
    -------
    Lista wszystkich generacji, w postaci zywych punktow na planszy (koordynaty punktow)

    """
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
            print("Wykryto cyklicznosc")
            return wszystkie_gen
    return wszystkie_gen

def zapisz_generacje(symulacja, nazwa_pliku):
    i = 0
    a=datetime.now()
    
    nazwa_pliku='Symulacja_'+a.strftime("%D_%H/%M")+'.txt'
    nazwa_pliku=nazwa_pliku.replace("/", "_")
    nazwa_pliku='./Folder_na_symulacje/'+nazwa_pliku
    f= open(nazwa_pliku,"w")
    f.write(Konfiguracja["Klucz_zabezpieczajacy_symulacje"]+"\n")
    while i < len(symulacja):
        line = list("0"*10000+"\n")
        for koor in symulacja[i]:
            line[koor[1]*100+koor[0]] = "1"
        f.write(''.join(line))
        i+=1
    f.close()
    return
    
def koloruj_mape(sciezka,macierz,nazwa,krok,szerokosc): # z macierzy pobiera rzedy i szereg
    """
    Funckja uzywana w celu stworzenia i umieszczenia w pamieci podrecznej 
    zbioru bitmap, ktore docelowo zostana pozniej przeakazane funkcji "z_gifa"
    w celu wizualizacji przebiegu symulacji.
    
    Parameters
    ----------
    sciezka (str) : nazwa pliku "*.bmp", ktory jest szkicem, biala plansza z 
    zaznaczona kratownica,
    
    macierz (list) : Lista list z obiektami,
    
    nazwa (str) : nazwa pliku "*.txt", w ktoym znajdue sie zapis srodowiska,
    
    krok (int) : odleglosc pomiedzy liniami kratownicy,
    
    szerokosc (int) : ilosc obiektow  w lini poziomej,
    
    kolejka (queue) : instancja klasy queue,

    Wynik
    -------
    Dodajanie elementow do zadeklarowanego obiektu "kolejka".
    """
    #sekcja wczytywania danych opisujacych arkusz
    podst=Image.open(sciezka) # zmienna jako oryginal
    im2=podst.copy() # w tym  miejscu robimy kopie oryginalu i na nim praucjemy
    n2=0 # licznik szeregow - szerokosc
    s_odl=krok
    x0=1
    x1=s_odl
    y0=1
    y1=s_odl
    litera=0
    while litera<len(macierz):# rzedy  | gora -> dol
        n2=0
        while n2<szerokosc:# szeregi | lewo-> prawo
            komorka_w=macierz[litera] # ustala ktory znak
            kolor=slownik_kolorow(komorka_w)  # zwraca odpowiedni mu kolor
            for y in range(y0,y1):
                for x in range(x0,x1):
                    im2.putpixel((x,y),kolor)# ten fragment zamalowuje 1 komorke
            x0=x0+s_odl
            x1=x1+s_odl
            n2+=1 #szerokosc
            litera=litera+1 # ktory element ze str
        n2=0
        x0=1
        x1=s_odl
        y0=y0+s_odl
        y1=y1+s_odl
    tulpa=(im2,nazwa)
    return tulpa  
    
def slownik_kolorow(znak):
    """
    Zwraca odpowiedni dla symbolu danej klasy kolor RGB.
    Uzywana przy kolorowaniu_map.
    
    Parameters
    ----------
    znak (str) : symbol klasy,

    Wyniki
    -------
    kolor (list) - wartosci RGB.

    """
    kom=znak
    kolor=0
    if kom =="0":   # Cell 
        kolor=(255,255,255) #= bialy 
    elif kom=="1":   # Cell_Dead 
        kolor=(0,0,0) # = czarny
    return kolor

def z_gifa(zbior_bitmap):
    """
    Tworzy plik "*.gif", z podanego w argumentach zbioru uszeregowanych 
    chronologicznie bitmap w celu animacji przebiegu symulacji.

    Parameters
    ----------
    zbior_bitmap (list) : lista bitmap

    Wynik
    -------
    Plik "movie_ASF.gif".

    """
    imageio.mimsave(os.getcwd()+'\\movie_CA.gif', zbior_bitmap)
    
if __name__=='__main__':    
    wykryj_rozdzielczosc()
    app=wx.App()
    okno=Okno_interfejsu_glownego()
    okno.Show()
    app.MainLoop()
