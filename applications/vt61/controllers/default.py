# -*- coding: utf-8 -*-


# -------------------------------------------------------------------------
# Viikkotehtävä 6, videovuokraamon käyttöliittymän kontrolleri
# date: 9.11.2016
# authot: Toni Pikkarainen
# -------------------------------------------------------------------------

@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Hello World")
    #return dict(message=T('Welcome to web2py!'))
    redirect(URL('vuokraukset'))

# Lisää uuden vuokrauksen    
@auth.requires_login() 
def uusivuokraus():
    response.title = "Lisää uusi vuokraus"
    if request.get_vars['id'] != None:
        vuokraus = db.vuokraus( request.get_vars['id'] )
        form = SQLFORM(db.vuokraus, vuokraus, showid=False)
        form.add_button('Delete', URL('poistavuokraus',vars=dict(id=request.get_vars['id'])))
    else:
        form = SQLFORM(db.vuokraus)
    if form.process().accepted:
        response.flash = 'Vuokraus on lisätty/muokattu'
    elif form.errors:
        response.flash = 'Lomakkeen tiedoissa on virheitä'
    else:
        response.flash = 'Täytä lomake lisätäksesi uuden vuokrauksen(/muokataksesi vuokrausta)'
    return dict(lomake=form)

# Lisää uuden elokuvan    
@auth.requires_login()  
def uusielokuva():
    response.title = "Lisää uusi elokuva"
    elokuvat = db().select(db.elokuva.ALL)
    
    if request.get_vars['id'] != None:
        elokuva = db.elokuva( request.get_vars['id'] )
        form = SQLFORM(db.elokuva, elokuva, showid=False)
        form.add_button('Delete', URL('poistaelokuva',vars=dict(id=request.get_vars['id'])))
    else:
        form = SQLFORM(db.elokuva)

    if form.process().accepted:
        response.flash = 'Elokuva on lisätty/muokattu'
    elif form.errors:
        response.flash = 'Lomakkeen tiedoissa on virheitä'
    else:
        response.flash = 'Täytä lomake lisätäksesi uuden elokuvan (/muokataksesi elokuvaa)'
    return dict(lomake=form,elokuvat=elokuvat)

# Lisää uuden jäsenen
@auth.requires_login()  
def uusijasen():

    response.title = "Lisää uusi jäsen"

    if request.get_vars['id'] != None:
        jasen = db.jasen( request.get_vars['id'] )
        form = SQLFORM(db.jasen, jasen, showid=False)
        form.add_button('Delete', URL('poistajasen',vars=dict(id=request.get_vars['id'])))
    else:
        form = SQLFORM(db.jasen)
 
    if form.process().accepted:
        response.flash = 'Jäsen on lisätty/muokattu'
    elif form.errors:
        response.flash = 'Lomakkeen tiedoissa on virheitä'
    else:
        response.flash = 'Täytä lomake lisätäksesi uuden jäsenen (/muokataksesi jäsentä)'
    return dict(lomake=form)
 
# Poistaa elokuvan, jos voi. 
@auth.requires_login()   
def poistaelokuva():
    eid = request.get_vars['id']
    
    if not db(db.vuokraus.elokuvaid == eid).select(db.vuokraus):
        db(db.elokuva.id == eid).delete()
        response.flash = 'Elokuva on poistettu'
        redirect(URL('uusielokuva'))
    response.flash = 'Poisto ei onnistunut'    
    redirect(URL('uusielokuva'))
    
# Poistaa vuokrauksen, jos voi.    
@auth.requires_login()
def poistavuokraus():
    vid = request.get_vars['id']
    db(db.vuokraus.id == vid).delete()
   
    redirect(URL('uusivuokraus'))
    
# Poistaa jäsenen, jos voi.    
@auth.requires_login()  
def poistajasen():
    jid = request.get_vars['id']
    
    if not db(db.vuokraus.jasenid == jid).select(db.vuokraus):
        db(db.jasen.id == jid).delete()
        redirect(URL('vuokraukset'))
        
    redirect(URL('vuokraukset'))

# Listaa elokuvat ja niiden vuokraukset
# lajiteltuna niiden vuokrausmäärän mukaan
@auth.requires_login()   
def elokuvat():
    response.title = "Elokuvat"
 
    elokuvat=[]
    kaikki_el = db().select(db.elokuva.ALL)

    for e in kaikki_el:
        lkm=db(db.vuokraus.elokuvaid == e.id).count()
        elokuvat.append(dict(nimi=e.nimi, lkm=lkm,id=e.id))
    # Lajittelu tehty pythonilla, koska en osannut kiertää
    # tämän non-relational -db:n rajoitteita liittyen
    # Taulu linkittämiseen keskenään.
    elokuvat.sort(key=lambda x: x['lkm'], reverse=True) 

    return dict(elokuvat=elokuvat)
    
# Jäsenet-sivu. Ei vielä kovin hyvä kokonaisuus.
@auth.requires_login() 
def jasenet():
   
    response.title = "Jäsenet"
    jasenet=db().select(db.jasen.ALL)
 
    return dict(jasenet=jasenet)
 
 
# Käytetään jäsenet-sivulla, tämä kokonaisuus ei vielä ole kovin hyvä.
@auth.requires_login() 
def naytavuokraukset():
    if request.get_vars['id'] != None:
        jasenid=request.get_vars['id']
        jasen=db.jasen(jasenid)
        vuokraukset=[]
        vuokraukset_jasen = db(db.vuokraus.jasenid == jasenid).select(db.vuokraus, orderby=db.vuokraus.vuokrauspvm)
        # tiettyyn vuokraukseen liittyvä elokuva
        for v in vuokraukset_jasen:
            elokuva = db(db.elokuva.id == v.elokuvaid).select(db.elokuva.ALL).first()
            
            #vuokraukset.append(dict(jasen=j, elokuva=elokuva, vuokraus=v))
            vuokraukset.append(dict(elokuva=elokuva, vuokraus=v))
        return dict(vuokraukset=vuokraukset, jasen=jasen)
    else:
        redirect(URL('jasenet'))
    
# Ei oikein hyvä, mutta tällä hetkellä mennään tällä 
@auth.requires_login() 
def vuokrauslomake():
  
    if request.get_vars['id'] != None:
        vuokraus = db.vuokraus( request.get_vars['id'] )
        form = SQLFORM(db.vuokraus, vuokraus, showid=False,buttons=[INPUT(_type='submit'),INPUT(_type='hidden', _name="_formname", _value="test")]) 
  
    else:
        form = SQLFORM(db.vuokraus)
    
    if not request.post_vars:
        response.flash = 'Muokkaa vuokrausta'
        return dict(form=form)
    
      
    if form.process(session=None, formname="test").accepted:
        response.flash = 'Vuokrausta on muokattu, klikkaa nimeä niin näet muutokset'
        form = SQLFORM(db.vuokraus,buttons=[])
    elif form.errors:
        response.flash = 'Lomakkeen tiedoissa on virheitä, klikkaa elokuvaa uudelleen'
        form = SQLFORM(db.vuokraus,buttons=[])
    else:
        response.flash = 'Täytä lomake lisätäksesi uuden vuokrauksen(/muokataksesi vuokrausta)'
    
    return dict(form=form)
  

# Listaa kaikki jäsenet ja niihin liittyvät vuokraukset.
@auth.requires_login()
def vuokraukset():
    response.title = "Kaikki vuokraukset"

    jasenet_lista=[]

    #liitos pitää tehdä ohjelmallisesti
    jasenet = db().select(db.jasen.ALL,orderby=db.jasen.nimi)
    # jäseneen liittyvät vuokraukset
    for j in jasenet:
        vuokraukset=[]
        vuokraukset_jasen = db(db.vuokraus.jasenid == j.id).select(db.vuokraus, orderby=db.vuokraus.vuokrauspvm)
        # tiettyyn vuokraukseen liittyvä elokuva
        for v in vuokraukset_jasen:
            elokuva = db(db.elokuva.id == v.elokuvaid).select(db.elokuva.ALL).first()
            
            #vuokraukset.append(dict(jasen=j, elokuva=elokuva, vuokraus=v))
            vuokraukset.append(dict(elokuva=elokuva, vuokraus=v))
        jasenet_lista.append(dict(jasen=j,vuokraukset=vuokraukset))

    return dict(jasenet=jasenet_lista)

    
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
 



