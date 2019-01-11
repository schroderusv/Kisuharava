import haravasto
import random
import time
import sys

#Tämän miinantallaajan on tehnyt Vappu Schroderus

### Pelin idea toimii seuraavanlaisesti: peli koostuu kahdesta 2-uloitteisesta listasta, kenttä ja näkymä, jossa näkymä on pelaajalle näkyvä peliruutu.
### Kenttään on määrätty miinat ja numerot.

tila = {
    "loppuaika": 0,
    "alkuaika": 0,
    "siirrot": 0,
    "tulos": None,
    "siirrot": 0,
    "leveys": 0,
    "miinamaara": 0,
    "korkeus": 0,
    "kentta": [], #Taustalla oleva 2-uloitteinen lista, josta luetaan piilotettuja ruutuja
    "nakyma": []  #Pelaajalle näkyvä ruutu
} #Pelin aikana sanakirjaan tallennetaan arvoja, joita voidaan käyttää funktioissa.

def paavalikko():
    """ Voidaan luoda uusi peli, tarkastella tuloksia tai lopettaa peli. """

    while True:
        print("Valitse seuraavista vaihtoehdoista:")
        print("1. Uusi peli \n2. Tarkastele tuloksia \n3. Lopeta peli? :C ")
        syote = input("Tee valintasi syöttämällä numero: ")
        if syote == "1":
            main()
        elif syote == "2":
            tarkastele_tuloksia()
        elif syote == "3":
            print()
            print("Nähdään taas <3")
            sys.exit()
        else:
            print()
            print("Toimintoa ei ole olemassa! Yritä uudelleen")
            print() 
            
def kysy_kentta():
    """ Kysytään kentän tiedot pelaajalta """    
    while True:
        try:
            leveys = int(input("Syötä kentän leveys kokonaislukuna: "))
            tila["leveys"] = leveys
            korkeus = int(input("Syötä kentän korkeus kokonaislukuna: "))
            tila["korkeus"] = korkeus
            miinamaara = int(input("Syötä halauamasi kisujen määrä: "))
            tila["miinamaara"] = miinamaara
            if leveys < 2 or korkeus < 2:
                print()
                print("Et voi pelata Kisuharavaa tällaisella kentällä! Yritä uudelleen.")
                print()
            elif miinamaara < 1:
                print()
                print("Ilman kisuja Kisuharava on vain harava...")
                print()
            elif miinamaara >= leveys * korkeus: #Vapaita ruutuja on oltava väh. 1
                print()
                print("Ei tehdä tästä pelistä mahdotonta...")
                print()
            else:
                break
        except ValueError:
            print()
            print("Vain kokonaislukuja senkin TYHÄM!")
            print()
    return leveys, korkeus, miinamaara                
def miinoita(miinakentta, jaljella, lkm):
    """
Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin.
    """
    tila["miinamaara"] = lkm
            
    for i in range(lkm):
        koordinaatit = random.choice(jaljella) #Valitaan vapaista koordinaateista satunnaisesti pareja
        y = koordinaatit[0]
        x = koordinaatit[1]
        miinakentta[x][y]="x" #Asetetaan miina koordinaattien osoittamaan paikkaan
        jaljella.remove(koordinaatit) #Poistetaan käytetyt koordinaatit listasta, ettei samoja ruutuja yritetä miinoittaa
    return miinakentta

        
def viereiset_ruudut(x, y, kentta):
    #Tarkistaa viereiset ruudut
    miina_lkm = 0
    alku_x = x-1
    loppu_x = x+1
    alku_y = y-1
    loppu_y = y+1
    

    for i in range(alku_y, loppu_y + 1): #Käydään toistorakenteilla läpi kaikki viereiset ja kulmattaiset ruudut
        for j in range(alku_x, loppu_x + 1):
            if 0 <= j < tila["leveys"] and 0 <= i < tila["korkeus"]: #Tarkistetaan että ruudut ovat kentän sisällä
                if kentta[i][j] == 'x': 
                    miina_lkm +=1
    return miina_lkm

def tulvataytto(kentta, x, y):

    if kentta[y][x] == " ":
        koordinaattilista=[(x, y)] #Aloituspiste
        while koordinaattilista: #Silmukka mahdollistaa ketjureaktion niin kauan että täytettävät alueet on täytetty
            x, y = koordinaattilista.pop() #Pop() poistaa ja palauttaa viimeisen arvon listasta
            kentta[y][x]=tila["kentta"][y][x]
            if kentta[y][x]=="0": #Ruudun ollessa 0 tarkistetaan viereiset ruudut, onko niissä nollia.
                
                for j in range(y-1, y + 2):
                    for i in range(x-1, x + 2):
                        if 0 <= i < tila["leveys"] and 0 <= j < tila["korkeus"]:
                            if kentta[j][i] == " ": #Jos viereinen ruutu on tuntematon, lisätään se koordinaattilistaan
                                koordinaattilista.append((i, j))
                            elif "x" in kentta[j][i]:
                                continue 
            
def luo_kentta():

    """ Luodaan juuri sellainen kenttä kun pelaaja haluaa """ 
    nakyma = []
    kentta = []
    
    leveys, korkeus, miinamaara = kysy_kentta()
    for rivi in range(korkeus): #Tällä muodostetaan näkymän alla oleva kenttä
        kentta.append([])
        for sarake in range(leveys):
            kentta[-1].append(" ") 
            
    jaljella = []
    for y in range(korkeus): #Miinoitetaan kenttä
        for x in range(leveys):
            jaljella.append((x, y))
    miinoita(kentta, jaljella, miinamaara) 
    
    for y_paikka, rivi in enumerate(kentta): 
        for x_paikka, ruutu in enumerate(rivi):
            if kentta[y_paikka][x_paikka] != "x":
                kentta[y_paikka][x_paikka] = str(viereiset_ruudut(x_paikka, y_paikka, kentta)) #Kenttään asetetaan miinoja vastaavat numeroruudut
                
    for rivi in range(korkeus): #Tällä muodostetaan kentän päällä oleva näkymä
        nakyma.append([])
        for sarake in range(leveys):
            nakyma[-1].append(" ") 
    
    tila["nakyma"] = nakyma
    tila["kentta"] = kentta
            
def kasittele_hiiri(x, y, nappula, muokkausnapit):
    #Funktio avaa näkymään kentän mukaisen ruudun. Jos käyttäjä osuu miinaan, peli loppuu. Ilmoitetaan myös voitto.
    #Asetetaan hiiren painikkeet
    pystyruutu = int(y/40)
    vaakaruutu = int(x/40)        
    try:
        if tila["nakyma"][pystyruutu][vaakaruutu]== " ":
            if nappula == int(haravasto.HIIRI_OIKEA): #asetetaan lippu
                tila["nakyma"][pystyruutu][vaakaruutu] = "f"
            elif nappula == int(haravasto.HIIRI_VASEN): #avataan ruutu
                tila["siirrot"] += 1
                if tila["kentta"][pystyruutu][vaakaruutu] == "x": #Painetaan miinaa
                    print()
                    print("VOI EI!! HERÄTIT KISUT!!!!\nHävisit pelin!\nSulje peliruutu jatkaaksesi")
                    print()
                    tila["loppuaika"] = time.time() #Pysäytetään kello
                    tila["tulos"] = "Häviö"
                    tila["nakyma"][:] = tila["kentta"][:] #Näytetään pelaajalle kenttä
                    
                elif 1 <= int(tila["kentta"][pystyruutu][vaakaruutu]) <= 8: #paljastetaan numeroruutu
                    tila["nakyma"][pystyruutu][vaakaruutu] = tila["kentta"][pystyruutu][vaakaruutu]
                    
                elif tila["kentta"][pystyruutu][vaakaruutu] == "0": #kun painetaan ruutua 0, tapahtuu tulvataytto
                    tulvataytto(tila["nakyma"], vaakaruutu, pystyruutu)
                    
        elif tila["nakyma"][pystyruutu][vaakaruutu]=="f": #Laitetaan lippu takaisin
            if nappula == int(haravasto.HIIRI_OIKEA):
                tila["nakyma"][pystyruutu][vaakaruutu]= " "
                
            else:
                pass 
        
        miinamaara = tila["miinamaara"]
        ruudut = 0
        for rivi in tila["nakyma"]:
            ruudut = ruudut + rivi.count("f") + rivi.count(" ") #Lasketaan yhteen avaamattomat ja liputetut ruudut
        if ruudut == miinamaara: 
            tila["nakyma"][:] = tila["kentta"][:]
            tila["tulos"] = "Voitto"
            tila["loppuaika"] = time.time()
            print()
            print("\nJIPIPIPIPIIII VOITIT PELIN!!\nSulje peliruutu jatkaaksesi")
            print()
    except IndexError: #Painetaan kentän ulkopuolelta
        print("Melkein painoit oikeaa kohtaa. Muttet aivan")    
def pelin_paatos():
    #Kun peli päättyy, tallennetaan tulokset listaan  
    minuutit, sekunnit = divmod(int(tila["loppuaika"]-tila["alkuaika"]), 60) #Jaetaan divmodilla minuutteihin ja sekunteihin
    while True:
        if minuutit < 0: #Jos suljet ruudun ennekuin pelin loppumisehto toteutuu, minuutit muuttuvat negatiivisiksi
            print()
            print("Keskeytynyttä peliä ei tallenneta >:C ") 
            print()
            break
        tallennus = input("Jos haluat että tulokset tallennetaan paina 1 ja jos et, paina 2: ")
        if tallennus == "1":
            while True:
                try:
                    nimimerkki= input("Anna nimimerkki tallennusta varten: ")
                except ValueError:
                    print("Anna vain nyt se nimimerkki")
                    print()
                    
                else:
                    with open("tiedosto.txt", "a") as tilasto: #Luodaan tiedosto, johon tallennetaan tiedot
                        tilasto.write("\nNimimerkki: {nimimerkki}\nTulos: {tulos}\nKesto: {minuutit} minuuttia {sekunnit} sekuntia\nSiirrot: {siirrot}\nKentän koko: {leveys} x {korkeus}\nKisujen määrä: {miinamaara}\n".format(
                                    siirrot = tila["siirrot"],
                                    nimimerkki = nimimerkki,
                                    leveys = tila["leveys"],
                                    korkeus = tila["korkeus"],
                                    miinamaara = tila["miinamaara"],
                                    alku = tila["alkuaika"],
                                    loppu = tila["loppuaika"], 
                                    tulos = tila["tulos"],
                                    minuutit = minuutit,
                                    sekunnit = sekunnit
                                    ))
                        print("Tulokset tallennettu")
                        print()
                    paavalikko()
                    break
        elif tallennus == "2":
            print("Tuloksia ei tallennettu")
            print()
            paavalikko()
            break
            
        else:
            print("Ei ole noin vaikeaa...")
                            
            
def piirra_kentta():

    """
Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
ruudun näkymän päivitystä.
    """    
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for i, rivi in enumerate(tila["nakyma"]):
        for j, sarake in enumerate(rivi):
            haravasto.lisaa_piirrettava_ruutu(sarake, j * 40, i * 40)
        
    haravasto.piirra_ruudut()    
    
def tarkastele_tuloksia():
    
    try:
        with open("tiedosto.txt") as tilasto:
            tiedostot = tilasto.read() #Luetaan tiedosto
    except FileNotFoundError:
        print("Ei aiempia tuloksia")
        
    else:
        print(tiedostot)

        
def main():
    """
    Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän.
    """
    
    luo_kentta()
    haravasto.lataa_kuvat("spritet")
    tila["alkuaika"] = time.time() #Asetetaan kello päälle
    haravasto.luo_ikkuna(tila["leveys"] * 40, tila["korkeus"] * 40)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aloita()
    pelin_paatos()

if __name__ == "__main__":
    print("Tässä pelissä on laatikoita, joita sinun täytyy avata!\nMutta varo! Osassa laatikossa nukkuu kissoja, etkä saa herättää niitä.")
    print("Voitat pelin, kun olet avannut kaikki kissattomat laatikot.\nHäviät jos herätät kisut.\nOnnea matkaan!")
    paavalikko()
    main()