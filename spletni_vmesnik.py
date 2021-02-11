from model import *
import os
from bottle import *

app = default_app()


def template(predloga, /, opozorilo=None, **kwargs):
    '''
        Povožena funkcija za predloge s podajanjem spremenljivke opozorilo.
    '''
    from bottle import template
    return template(predloga, opozorilo=opozorilo, **kwargs)


# STATIC -----------------------------------------------------------------------------------------------
@get('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='static')


# -------------------------------------------------------------------------------------------------------
# SPLETNE STRANI ----------------------------------------------------------------------------------------

# ZAČETNA STRAN -----------------------------------------------------------------------------------------
@route('')
@route('/')
def zacetna_stran():
    return template('zacetna_stran.tpl')


@route('/izbira_dejavnosti', method='POST')
def izberi():
    pot = {'uvoz': '/uvoz_odpadka',
           'izvoz': '/izvoz_odpadka',
           'pregled': '/pregled'}.get(request.forms.get('dejavnost'), None)
    if pot is None:
        return template('zacetna_stran.tpl', opozorilo="Neveljavna izbira! Prosimo, poskusite ponovno.")
    redirect(pot)


# UVOZ ODPADKA ------------------------------------------------------------------------------------------
@get('/uvoz_odpadka')
def uvoz_odpadka():
    opomba = [(id, ime) for id, ime in Opomba.opomba()]
    return template('uvoz_odpadka.tpl')


@route('/podatki_o_odpadku', method='POST')
def dodaj_odpadek():
    teza = request.forms.get('teza')
    povzrocitelj = request.forms.get('povzrocitelj')
    datum_uvoza = request.forms.get('datum_uvoza')
    klasifikacijska_stevilka = request.forms.get('klasifikacijska_stevilka')
    skladisce = request.forms.get('skladisce')
    opomba_uvoza = request.forms.get('opomba_uvoza')   
    
    if opomba_uvoza == '':
        opomba_uvoza = None
    if povzrocitelj == '':
        povzrocitelj = None
    
    if teza == '' or datum_uvoza == '' or klasifikacijska_stevilka == '' or skladisce == '':
        return template('uvoz_odpadka.tpl', opozorilo="Neustrezni vnos! Prosimo, poskusite ponovno.")
    
    odpadek = Odpadek(teza, klasifikacijska_stevilka, skladisce,
     datum_uvoza, povzrocitelj, opomba_uvoza)
    
    odpadek.dodaj_v_bazo()
    
    return template('zacetna_stran.tpl', opozorilo="Odpadek je uvožen.")


# ODVOZ ODPADKA -----------------------------------------------------------------------------------------
@get('/izvoz_odpadka')
def izvoz_odpadka():
    return template('izvoz_odpadka.tpl')


@route('/podatki_o_odpadku_izvoz', method='POST')
def izvozi_odpadek():
    id = int(request.forms.get('id'))
    datum_izvoza = request.forms.get('datum_izvoza')
    prejemnik = request.forms.get('prejemnik')
    opomba_izvoza = request.forms.get('opomba_izvoza')
    
    if opomba_izvoza == '':
        opomba_izvoza = None
    if prejemnik == '':
        prejemnik = None
    
    if (id,) not in Odpadek.vsi_id():
        return template('izvoz_odpadka.tpl', opozorilo="Neustrezni vnos! Prosimo, poskusite ponovno.")
    
    try:
        Odpadek.izvozi(id, datum_izvoza, opomba_izvoza, prejemnik)
        return template('zacetna_stran.tpl', opozorilo="Odpadek je izvožen.")

    except:
        return template('izvoz_odpadka.tpl', opozorilo="Izbranega odpadka ni na skladišču. Poskusi znova!")


# PREGLED SKLADIŠČENIH ODPADKOV --------------------------------------------------------------------------
@get('/pregled')
def pregled():
    return template('pregled.tpl')


@route('/filtriraj', method='POST')
def filtriraj_odpadke():
    pot = {'kolicina': '/kolicina',
           'nekateri': '/nekateri',
           'cas': '/cas',
           'zadnji': '/zadnji'}.get(request.forms.get('pregled'), None)
    if pot is None:  # dejavnost == ''
        return template('pregled.tpl', opozorilo="Neveljavna izbira! Prosimo, poskusite ponovno.")
    redirect(pot)


# KOLIČINA POSAMEZNIH ODPADKOV (GLEDE NA KLAS. ŠT.) ------------------------------------------------------------------------------
@get('/kolicina')
def kolicina_odpadkov():
    return template('kolicina.tpl')


@route('/izpis_kolicina', method='POST')
def filtriraj_odpadke():
    skladisce = request.forms.get('skladisce')
        
    if skladisce == '':
        skladisce = None

    stolpci = ['Klasifikacijska številka',
                'Naziv',
                'Teža',
                'Število',
                ]

    return template('izpis.tpl', stolpci=stolpci, odpadki=Skladisce.kolicina(skladisce))


# SKUPNA TEŽA POSAMEZNIH ODPADKOV V NEKEM SKLADIŠČU -------------------------------------------------------------------------------
@get('/nekateri')
def skupna_teza_odpadkov():
    return template('nekateri.tpl')


@route('/izpis_nekateri', method='POST')
def filtriraj_odpadke():
    skladisce = request.forms.get('skladisce')
    
    id = request.forms.get('id') != None
    klas_st = request.forms.get('klas_st') != None
    naziv = request.forms.get('naziv') != None
    teza = request.forms.get('teza') != None
    opomba_uvoz = request.forms.get('opomba_uvoz') != None 
    opomba_izvoz = request.forms.get('opomba_izvoz') != None
    povzrocitelj = request.forms.get('povzrocitelj') != None
    prejemnik = request.forms.get('prejemnik') != None
    dat_uvoza = request.forms.get('dat_uvoza') != None
    dat_izvoza = request.forms.get('dat_izvoza') != None
   
    if skladisce == '':
        skladisce = None
    
    stolpci = []

    if id:
        stolpci.append('ID')
    if klas_st:
        stolpci.append('Klasifikacijska številka')
    if naziv:
        stolpci.append('Naziv')
    if skladisce is None:
        stolpci.append('Skladišče')
    if teza:
        stolpci.append('Teža')
    if opomba_uvoz:
        stolpci.append('Opomba uvoza')
    if opomba_izvoz:
        stolpci.append('Opomba izvoza')
    if povzrocitelj:
        stolpci.append('Povzročitelj')
    if prejemnik:
        stolpci.append('Prejemnik')
    if dat_uvoza:
        stolpci.append('Datum uvoza')
    if dat_izvoza:
        stolpci.append('Datum izvoza')

    if stolpci == ['Skladišče']:
        stolpci = ['ID', 'Klasifikacijska številka', 'Naziv', 'Skladišče', 'Teža', 'Opomba uvoza',
                'Opomba izvoza', 'Povzročitelj', 'Prejemnik', 'Datum uvoza', 'Datum izvoza']
    if stolpci == []:
        stolpci = ['ID', 'Klasifikacijska številka', 'Naziv', 'Teža', 'Opomba uvoza',
                'Opomba izvoza', 'Povzročitelj', 'Prejemnik', 'Datum uvoza', 'Datum izvoza']

    return template('izpis.tpl', stolpci=stolpci,
        odpadki=Odpadek.nekateri(id, klas_st, naziv, skladisce, teza, opomba_uvoz, 
            opomba_izvoz, povzrocitelj, prejemnik, dat_uvoza, dat_izvoza))


# VSI ODPADKI V SKLADIŠČU ---------------------------------------------------------------------------------------------------------
@get('/cas')
def vsi_odpadki():
    return template('cas.tpl')


@route('/izpis_cas', method='POST')
def filtriraj_odpadke():
    od = request.forms.get('od')
    do = request.forms.get('do')
    
    id = request.forms.get('id') != None
    klas_st = request.forms.get('klas_st') != None
    naziv = request.forms.get('naziv') != None
    skladisce = request.forms.get('skladisce') != None
    teza = request.forms.get('teza') != None
    opomba_uvoz = request.forms.get('opomba_uvoz') != None 
    opomba_izvoz = request.forms.get('opomba_izvoz') != None
    povzrocitelj = request.forms.get('povzrocitelj') != None
    prejemnik = request.forms.get('prejemnik') != None
    dat_uvoza = request.forms.get('dat_uvoza') != None
    dat_izvoza = request.forms.get('dat_izvoza') != None
   
    if od == '':
        od = None
    if do == '':
        do = None

    stolpci = []
    if id:
        stolpci.append('ID')
    if klas_st:
        stolpci.append('Klasifikacijska številka')
    if naziv:
        stolpci.append('Naziv')
    if skladisce:
        stolpci.append('Skladišče')
    if teza:
        stolpci.append('Teža')
    if opomba_uvoz:
        stolpci.append('Opomba uvoza')
    if opomba_izvoz:
        stolpci.append('Opomba izvoza')
    if povzrocitelj:
        stolpci.append('Povzročitelj')
    if prejemnik:
        stolpci.append('Prejemnik')
    if dat_uvoza:
        stolpci.append('Datum uvoza')
    if dat_izvoza:
        stolpci.append('Datum izvoza')

    if stolpci == []:
        stolpci = ['ID', 'Klasifikacijska številka', 'Naziv', 'Skladišče', 'Teža', 'Opomba uvoza',
                'Opomba izvoza', 'Povzročitelj', 'Prejemnik', 'Datum uvoza', 'Datum izvoza']

    return template('izpis.tpl', stolpci=stolpci,
        odpadki=Odpadek.cas(id, klas_st, naziv, skladisce, teza, opomba_uvoz, opomba_izvoz, 
                povzrocitelj, prejemnik, dat_uvoza, dat_izvoza, od, do))


# ZADNJI IZVOZ ZA POSAMEZNO KLAS. ŠT. ODPADKA -------------------------------------------------------------------------------------
@get('/zadnji')
def zadnji_odpadki():
    return template('zadnji.tpl')


@route('/zadnji')
def zadnji():   

    stolpci = ['Klasifikacijska številka',
                'Datum uvoza',
                'Datum izvoza',
                ]

    return template('izpis.tpl', stolpci=stolpci, odpadki=Odpadek.zadnji())


# ----------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    run(app, host='localhost', port=port, reloader=True, debug=True)