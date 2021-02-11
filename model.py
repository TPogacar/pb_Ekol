from baza import *
import sqlite3
from geslo import sifriraj_geslo, preveri_geslo
import time

conn = sqlite3.connect('Ekol.sqlite')
ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

uporabnik, podjetja, vrsta_odpadka, skladisce, odpadek, opomba = pripravi_tabele(conn)


class LoginError(Exception):
    """
    Napaka ob napačnem uporabniškem imenu ali geslu.
    """
    pass


# ----------------------------------------------------------------------------------------------------
class Uporabnik(Ekol):
    """
    Razred za uporabnika.
    """

    def __init__(self, ime, *, id=None):
        """
        Konstruktor uporabnika.
        """
        self.id = id
        self.ime = ime


    def __str__(self):
        """
        Znakovna predstavitev uporabnika.
        Vrne uporabniško ime.
        """
        return self.ime


    @staticmethod
    def prijava(ime, geslo):
        """
        Preveri, ali sta uporabniško ime geslo pravilna.
        """
        sql = """
            SELECT id, zgostitev, sol FROM uporabnik
            WHERE ime = ?
        """
        try:
            id, zgostitev, sol = conn.execute(sql, [ime]).fetchone()
            if preveri_geslo(geslo, zgostitev, sol):
                return Uporabnik(ime, id=id)
        except TypeError:
            pass
        raise LoginError(ime)


    def dodaj_v_bazo(self, geslo):
        """
        V bazo doda uporabnika s podanim geslom.
        """
        assert self.id is None
        zgostitev, sol = sifriraj_geslo(geslo)
        with conn:
            self.id = Uporabnik.dodaj_vrstico(ime=self.ime, zgostitev=zgostitev, sol=sol)


# ----------------------------------------------------------------------------------------------------
class Podjetja(Ekol):
    def __init__(self, ime, id = None):
        self.id = id
        self.ime = ime
   
   
    def __str__(self):
        return self.ime
   
   
    def dodaj_v_bazo(self):
        assert self.id is None
        with conn:
            id = Podjetja.dodaj_vrstico(ime=self.ime)
            self.id = id


    @staticmethod
    def ime_podjetja(index):
        '''
            vrne ime podjetja, ki mu pripada dani index
        '''
        return conn.execute(''' SELECT ime FROM podjetje
                            WEHERE id = ?;''', (index)).fetchone()


# ----------------------------------------------------------------------------------------------------
class Opomba(Ekol):
    def __init__(self, ime, id = None):
        self.id = id
        self.ime = ime
   
   
    def __str__(self):
        return self.ime
   
   
    def dodaj_v_bazo(self):
        assert self.id is None
        with conn:
            id = Opomba.dodaj_vrstico(ime=self.ime)
            self.id = id

    
    @staticmethod
    def opomba():
        '''
            vrne tabelo vseh parov opomb (id, ime)
        '''
        return [(id, ime) for id, ime in conn.execute('''
                SELECT *
                FROM opomba
            ;''')]

        
# ----------------------------------------------------------------------------------------------------
class VrstaOdpadka(Ekol):
    def __init__(self, klasifikacijska_stevilka, naziv):
        self.klasifikacijska_stevilka = klasifikacijska_stevilka
        self.naziv = naziv
    
    
    def __str__(self):
        return self.naziv
    
    
    def dodaj_v_bazo(self):
        with conn:
            VrstaOdpadka.dodaj_vrstico(klasifikacijska_stevilka=self.klasifikacijska_stevilka, naziv=self.naziv)


    @staticmethod
    def vrsta_odpadka():
        '''
            vrne tabelo vseh parov vrst odpadkov (klas_st, naziv)
        '''
        return [(klas_st, naziv) for klas_st, naziv in conn.execute('''
                SELECT *
                FROM vrsta_odpadka
            ;''')]


# ----------------------------------------------------------------------------------------------------
class Skladisce(Ekol):
    def __init__(self, id, ime=None, odp=None, st=None, kl=None, t=None):
        self.id = id
        self.ime = ime

    
    def __str__(self):
        return self.ime
    
    
    def dodaj_v_bazo(self):
        with conn:
            Skladisce.dodaj_vrstico(ime=self.ime, id=self.id)


    @staticmethod
    def skladisce():
        '''
            vrne tabelo vseh parov skladišč (id, ime)
        '''
        return [(id, ime) for id, ime in conn.execute('''
                SELECT *
                FROM skladisce
            ;''')]


    @staticmethod
    def skladisce_id():
        '''
            vrne tabelo vseh id skladišč (nizi)
        '''
        return [str(id) for (id,) in conn.execute('''
                SELECT id
                FROM skladisce
            ;''')]


    @staticmethod
    def kolicina(skladisce=None):
        '''
            vrne tabelo z elementi oblike (klas_st, naziv, teza, stevilo),
            kjer je teža skupna teža vseh odpadkov neke klas_st,
            število pa število kosov odpadkov z določeno klas_št
        '''
        sql = '''SELECT odpadek.klasifikacijska_stevilka,
                    vrsta_odpadka.naziv,
                    SUM(odpadek.teza),
                    COUNT(odpadek.klasifikacijska_stevilka) 
                FROM odpadek
                    JOIN
                    vrsta_odpadka ON odpadek.klasifikacijska_stevilka = vrsta_odpadka.klasifikacijska_stevilka
                WHERE datum_izvoza IS NULL
            '''
        
        if skladisce in Skladisce.skladisce_id():
            sql += f''' AND odpadek.skladisce = {skladisce} '''

        sql += ''' GROUP BY odpadek.klasifikacijska_stevilka;'''

        return [(klas_st, naziv, teza, stevilo) for klas_st, naziv, teza, stevilo in conn.execute(sql)]


# ----------------------------------------------------------------------------------------------------
class Odpadek(Ekol):
    def __init__(self, teza=None, klasifikacijska_stevilka=None, skladisce=None,
     datum_uvoza=None, povzrocitelj=None, opomba_uvoz=None, datum_izvoza=None, opomba_izvoza=None, prejemnik=None,
     naziv=None, id=None):
        self.teza = teza
        if povzrocitelj:
            self.povzrocitelj = povzrocitelj.upper()
        else:
            self.povzrocitelj = None
        self.klasifikacijska_stevilka = klasifikacijska_stevilka
        self.skladisce = skladisce
        self.datum_uvoza = datum_uvoza
        self.opomba_uvoz = opomba_uvoz
        
        # za izpis pri funkciji od do   
        self.datum_izvoza = datum_izvoza
        self.opomba_izvoza = opomba_izvoza
        self.prejemnik = prejemnik
        self.id = id
        self.naziv = naziv
    

    def dodaj_v_bazo(self):
        sl = dict()
        sl['klasifikacijska_stevilka'] = self.klasifikacijska_stevilka
        sl['teza'] = self.teza 
        sl['datum_uvoza'] = self.datum_uvoza
        sl['opomba_uvoz'] = self.opomba_uvoz       
        # skladišče je vnešeno kot št. {3, 7}
        sl['skladisce'] = self.skladisce

        # potrebujemo index
        if self.povzrocitelj:
            try:
                # povzročitelj je že v tabeli podjetij
                sl['povzrocitelj'] = conn.execute("""
                        SELECT id FROM podjetje
                        WHERE ime = ?;
                    """, [self.povzrocitelj]).fetchone()[0]
            except:
                # imamo novo podjetje
                cur = conn.execute("INSERT INTO podjetje (ime) VALUES (?);", [self.povzrocitelj])
                print(cur.lastrowid)               
                sl['povzrocitelj'] = cur.lastrowid

        else:
            sl['povzrocitelj'] = None
        with conn:
            print(self)
            print(sl)
            return odpadek.dodaj_vrstico(**sl)  # id


    @staticmethod
    def izvozi(id, datum_izvoza, opomba_izvoz=None, prejemnik=None):
        id = id
        datum_izvoza = datum_izvoza
        opomba_izvoz = opomba_izvoz
        prejemnik = prejemnik
        sl = dict()
        if prejemnik:
            prejemnik = prejemnik.upper()
            try:
                sl['prejemnik'] = conn.execute("""
                        SELECT id FROM podjetje
                        WHERE ime = ?;
                    """, [prejemnik]).fetchone()[0]
            except:
                with conn:
                    sl['prejemnik'] = Podjetja.dodaj_vrstico(ime=prejemnik)
        else:
            sl['prejemnik'] = None
        sl['datum_izvoza'] = datum_izvoza
        sl['opomba_izvoz'] = opomba_izvoz
        sl['id'] = id
        
        with conn:
            Odpadek.za_izvoz(sl)


    @staticmethod
    def za_izvoz(sl):
        conn.execute('''
            UPDATE odpadek
                SET prejemnik = ?,
                    datum_izvoza = ?,
                    opomba_izvoz = ?
                WHERE id = ?;''',
            [
            sl['prejemnik'],
            sl['datum_izvoza'],
            sl['opomba_izvoz'],
            sl['id'],
            ])

        
    @staticmethod
    def zadnji():
        '''
            vrne tabelo trojic (klas_št, datum_uvoz, datum_izvoz) -
            za vse različne klas. št. skladiščenih odpadkov datum
            zadnjega izvoza, za tiste odpadke, ki pa so še skladiščeni,
            izpiše tudi datum prvega uvoza
        '''
        # ni več skladiščen
        izvoz = {klas_st: datum_izvoz for klas_st, datum_izvoz in conn.execute(
            '''SELECT klasifikacijska_stevilka,
                MAX(datum_izvoza) 
            FROM odpadek
            WHERE datum_izvoza is not Null
            GROUP BY klasifikacijska_stevilka;''')}
        
        # še vedno v skladišču
        uvoz = {klas_st: datum_uvoz for klas_st, datum_uvoz in conn.execute(
            '''SELECT klasifikacijska_stevilka,
                MIN(datum_uvoza)
            FROM odpadek
            WHERE datum_izvoza is Null
            GROUP BY klasifikacijska_stevilka;''')}
        
        # združimo
        tab = []
        for klas in izvoz:
            if klas in uvoz:
                tab.append((klas, uvoz[klas], izvoz[klas]))
            else:
                tab.append((klas, '', izvoz[klas]))
        for klas in uvoz:
            if klas not in izvoz:
                tab.append((klas, uvoz[klas], ''))
        
        return tab


    @staticmethod
    def vsi_id():
        '''
            vrne vse ID odpadkov, ki so v skladišču
        '''
        return [id for id in conn.execute('''
                SELECT id
                FROM odpadek
                WHERE datum_izvoza is Null
            ;''')]


    @staticmethod
    def cas(id=False, klas_st= False, naziv=False, skladisce=False, teza=False, opomba_uvoz=False, opomba_izvoz=False, 
                povzrocitelj=False, prejemnik=False, dat_uvoza=False, dat_izvoza=False, od=None, do=None):
        '''
            Vrne tabelo vseh skladiščenih odpadkov v nekem časovnem obdobju. Po želji lahko izpišemo tudi samo ozbrane stolpce.
            Če ne podamo mej za časovno obdobje, izpiše vse odpadke.

            Torej imamo lahko v izhodni tabeli zgolj nekatere izmed:
                * id,
                * klas_st,
                * naziv,
                * skladisce,
                * teza,
                * opomba_uvoz,
                * opomba_izvoz,
                * povzrocitelj,
                * prejemnik,
                * datum_uvoza,
                * datum_izvoza,
                * od,
                * do
        '''
        stolpci = []
        if id:
            stolpci.append("ifnull(odpadek.id, '')")
        if klas_st:
            stolpci.append("ifnull(odpadek.klasifikacijska_stevilka, '')")
        if naziv:
            stolpci.append("ifnull(vrsta_odpadka.naziv, '')")
        if skladisce:
            stolpci.append("ifnull(skladisce.ime, '')")
        if teza:
            stolpci.append("ifnull(odpadek.teza, '')")
        if opomba_uvoz:
            stolpci.append("ifnull(opomba.ime, '')")
        if opomba_izvoz:
            stolpci.append("ifnull(opomba_izvoza.ime, '')")
        if povzrocitelj:
            stolpci.append("ifnull(podjetje.ime, '')")
        if prejemnik:
            stolpci.append("ifnull(prejemnik.ime, '')")
        if dat_uvoza:
            stolpci.append("ifnull(odpadek.datum_uvoza, '')")
        if dat_izvoza:
            stolpci.append("ifnull(odpadek.datum_izvoza, '')")
        
        if stolpci == []: 
            # brez izbranih parametrov => potrebujemo vse podatke o odpadku
            poizvedba = '''SELECT odpadek.id,
                odpadek.klasifikacijska_stevilka,
                ifnull(vrsta_odpadka.naziv, ''),
                skladisce.ime,
                ifnull(odpadek.teza, ''),
                ifnull(opomba.ime, ''),
                ifnull(opomba_izvoza.ime, ''),
                ifnull(podjetje.ime, ''),
                ifnull(prejemnik.ime, ''),
                ifnull(odpadek.datum_uvoza, ''),
                ifnull(odpadek.datum_izvoza, '')
                '''
        else:
            # izberemo le žejene podatke o odpadku
            poizvedba = '''SELECT {} ''' .format(", ".join(stolpci))
        
        # poizvedbi dodamo tabelo
        poizvedba += '''FROM odpadek
                LEFT JOIN
                vrsta_odpadka ON odpadek.klasifikacijska_stevilka = vrsta_odpadka.klasifikacijska_stevilka
                LEFT JOIN
                opomba ON odpadek.opomba_uvoz = opomba.id
                LEFT JOIN
                opomba AS opomba_izvoza ON odpadek.opomba_izvoz = opomba_izvoza.id
                LEFT JOIN
                skladisce ON odpadek.skladisce = skladisce.id
                LEFT JOIN
                podjetje ON odpadek.povzrocitelj = podjetje.id
                LEFT JOIN
                podjetje AS prejemnik ON odpadek.prejemnik = prejemnik.id
            '''
        slo = dict() 
        if od is not None or do is not None:
            # filtriramo glede na časovno obdobje
            poizvedba += ' WHERE '
            
            if od is None:
                # zagotovo ni bilo nobenega odpadka pred 1. 1. 2000
                od = '2000-01-01'
            if do is None:
                # zanima nas največ do današnjega dne
                do = time.strftime('%Y-%m-%d', time.localtime())

            poizvedba += "(date(odpadek.datum_uvoza) BETWEEN date(:od) AND date(:do)) OR \
                (date(odpadek.datum_izvoza) BETWEEN date(:od) AND date(:do)) OR \
                ((date(:od) >= date(odpadek.datum_uvoza)) AND \
                    ((date(odpadek.datum_izvoza) >= date(:od)) OR (date(odpadek.datum_izvoza) IS NULL)))"
        
            slo['od'] = od
            slo['do'] = do
        poizvedba += ';'

        return [podatek for podatek in conn.execute(poizvedba, slo)]
        

    @staticmethod
    def nekateri(id=False, klas_st=False, naziv=False, skladisce=None, teza=False, opomba_uvoz=False, opomba_izvoz=False, 
                povzrocitelj=False, prejemnik=False, dat_uvoza=False, dat_izvoza=False):
        '''
            Vrne tabelo vseh skladiščenih odpadkov v nekem skladišču. Po želji lahko izpišemo tudi samo ozbrane stolpce.
            Če ne podamo skladišča, izpiše vse odpadke.

            Torej imamo lahko v izhodni tabeli zgolj nekatere izmed:
                * id,
                * klas_st,
                * naziv,
                * skladisce,
                * teza,
                * opomba_uvoz,
                * opomba_izvoz,
                * povzrocitelj,
                * prejemnik,
                * datum_uvoza,
                * datum_izvoza,
                * od,
                * do
        '''
        stolpci = []
        if id:
            stolpci.append("ifnull(odpadek.id, '')")
        if klas_st:
            stolpci.append("ifnull(odpadek.klasifikacijska_stevilka, '')")
        if naziv:
            stolpci.append("ifnull(vrsta_odpadka.naziv, '')")
        if skladisce is None:
            # izpis za vsa skladišča
            stolpci.append("skladisce.ime")
        if teza:
            stolpci.append("ifnull(odpadek.teza, '')")
        if opomba_uvoz:
            stolpci.append("ifnull(opomba.ime, '')")
        if opomba_izvoz:
            stolpci.append("ifnull(opomba_izvoza.ime, '')")
        if  povzrocitelj:
            stolpci.append("ifnull(podjetje.ime, '')")
        if prejemnik:
            stolpci.append("ifnull(prejemnik.ime, '')")
        if dat_uvoza:
            stolpci.append("ifnull(odpadek.datum_uvoza, '')")
        if dat_izvoza:
            stolpci.append("ifnull(odpadek.datum_izvoza, '')")
        
        if stolpci == []:
            # brez izbranih parametrov => potrebujemo vse podatke o odpadku
            # v vseh skladiščih
            poizvedba = '''SELECT odpadek.id,
                odpadek.klasifikacijska_stevilka,
                ifnull(vrsta_odpadka.naziv, ''),
                ifnull(odpadek.teza, ''),
                ifnull(opomba.ime, ''),
                ifnull(opomba_izvoza.ime, ''),
                ifnull(podjetje.ime, ''),
                ifnull(prejemnik.ime, ''),
                ifnull(odpadek.datum_uvoza, ''),
                ifnull(odpadek.datum_izvoza, '')
                '''
        elif stolpci == ["skladisce.ime"]:
            # zanimajo nas vsi podatki v nekem skladišču
            poizvedba = '''SELECT odpadek.id,
                odpadek.klasifikacijska_stevilka,
                ifnull(vrsta_odpadka.naziv, ''),
                skladisce.ime,
                ifnull(odpadek.teza, ''),
                ifnull(opomba.ime, ''),
                ifnull(opomba_izvoza.ime, ''),
                ifnull(podjetje.ime, ''),
                ifnull(prejemnik.ime, ''),
                ifnull(odpadek.datum_uvoza, ''),
                ifnull(odpadek.datum_izvoza, '')
                '''

        else:
            # izberemo le žejene podatke o odpadku
            poizvedba = '''SELECT {} '''.format(", ".join(stolpci))
        
        # poizvedbi dodamo tabelo
        poizvedba += '''FROM odpadek
                LEFT JOIN
                vrsta_odpadka ON odpadek.klasifikacijska_stevilka = vrsta_odpadka.klasifikacijska_stevilka
                LEFT JOIN
                opomba ON odpadek.opomba_uvoz = opomba.id
                LEFT JOIN
                opomba AS opomba_izvoza ON odpadek.opomba_izvoz = opomba_izvoza.id
                LEFT JOIN
                skladisce ON odpadek.skladisce = skladisce.id
                LEFT JOIN
                podjetje ON odpadek.povzrocitelj = podjetje.id
                LEFT JOIN
                podjetje AS prejemnik ON odpadek.prejemnik = prejemnik.id
            '''

        if skladisce in Skladisce.skladisce_id():
            # zanimajo nas odpadki samo v enem skladišču
            poizvedba += f''' WHERE odpadek.skladisce = {skladisce} '''

        poizvedba += ';'
        return [podatek for podatek in conn.execute(poizvedba)]