import pygame
import sys
import random
from pygame.locals import *

# alustaa pygamen
pygame.init()
pygame.font.init()
pygame.mixer.init()

koko = (400,600)  # eka on leveys ja toka korkeus
ruutu = pygame.display.set_mode(koko)

# Lataus
tausta = pygame.image.load("saunan lattia.png")
pelaaja = pygame.image.load("kiuas.png")
vesi = pygame.image.load("löyly.png")

tausta = pygame.transform.scale(tausta, koko)
pelaaja = pygame.transform.scale(pelaaja, (64,64))
vesi = pygame.transform.scale(vesi, (32,32))

# Musa
pygame.mixer.music.load("putin wibe walk.mp3")
pygame.mixer.music.play(-1)

putti = pygame.mixer.Sound("puttis.mp3")
karlson = pygame.mixer.Sound("mosic.mp3")
cool = pygame.mixer.Sound("wow.mp3")

# tekstit
pelifontti = pygame.font.SysFont("Impact", 30)
loppufontti = pygame.font.SysFont("Tahoma", 60)
pelivari = (0, 255, 21)
loppuvari = (170, 0, 255)
voittovari = (255, 242, 0)
# muutujat
Pelax = 200-32
Pelay = 500
pelinopeus = 7
vihunopeus = 5
hp = 5
kakat = [[100,100],[200,200],[300,300]]
on_tehty = False
ennatys = 0.0

# Ennätyksen lukeminen
with open("ennatys","r") as tiedosto:
    luettu = tiedosto.read()
    ennatys = int(luettu)

# aika juuttuu
akastin = pygame.time.Clock()
FPS = 60
alkuaika = pygame.time.get_ticks()


def FARD():
    tapahtumat = pygame.event.get()
    for tapahtuma in tapahtumat:
        if tapahtuma.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    


# Ohjaa pelaajia, löylyä ja pisteitä
def OBAMIUM():
    global Pelax, Pelay, hp, ennatys, vihunopeus
    Aika = pygame.time.get_ticks()-alkuaika
    

    napit = pygame.key.get_pressed()
    if napit[pygame.K_d]:
        Pelax += pelinopeus
    if napit[pygame.K_a]:
        Pelax -= pelinopeus
    if napit[pygame.K_w]:
        Pelay-= pelinopeus
    if napit[pygame.K_s]:
        Pelay += pelinopeus
    
    # vihallisen kiihdytys
    if (Aika//1000) % 10 == 0: # onko jakojäännös nolla? tapahtuu joka 10 sekunttia
        vihunopeus += 0.01

    if Pelax < 0:
        Pelax = 0
    if Pelax > 400-64:
        Pelax = 400-64
    if Pelay < 0:
        Pelay = 0
    if Pelay > 600-64:
        Pelay = 600-64
    for jootti in kakat:
        jootti[1] += vihunopeus
        if jootti[1] > 600:
            jootti[1] = 5
            jootti[0] = random.randint(10, 400-32-10)


    for jootti in kakat:
        if jootti[1]+32 > Pelay and jootti[1] < Pelay+64:
            if jootti[0]+32 > Pelax and jootti[0] < Pelax+64:
                putti.play()
                hp -= 1
                jootti[1] = 5
                jootti[0] = random.randint(10, 400-32-10)



    Aika = pygame.time.get_ticks()-alkuaika
    if Aika > ennatys:
        ennatys = Aika

# piirtäjä
def MONKE():
    ruutu.blit(tausta, (0,0))
    ruutu.blit(pelaaja, (Pelax, Pelay))
    # vihollisen piirto
    for siainti in kakat:
        ruutu.blit(vesi, siainti)

        # textin piirto
    hpteksti = pelifontti.render("Elämät: "+str(hp), True, pelivari)
    ruutu.blit(hpteksti, (30,30))

    Aika = pygame.time.get_ticks()-alkuaika
    aikateksti = pelifontti.render("Aika: "+str(Aika/1000), True, pelivari)
    ruutu.blit(aikateksti, (30,70))

    ennatysteksti = pelifontti.render("Ennatys: "+str(ennatys/1000), True, pelivari)
    ruutu.blit(ennatysteksti, (30,120))



# häviö
def UDED():
    global on_tehty
    if not on_tehty:
        

        #Tämä lohko suoriutuu vain kerran pelin loputtua
        on_tehty = True
        pygame.mixer.music.stop()
        karlson.play()
        
        with open("ennatys","w") as tiedosto:
            tiedosto.write(str(ennatys))

    ruutu.fill(loppuvari)

    teksti = loppufontti.render("liikaa löylyä", True, pelivari)
    ruutu.blit(teksti, (30,245))
    teksti = loppufontti.render("haha u ded", True, pelivari)
    ruutu.blit(teksti, (30,300))

    ennatysteksti = pelifontti.render("Ennatys: "+str(ennatys/1000), True, pelivari)
    ruutu.blit(ennatysteksti, (125,120))


# voito
def UVON():
    global on_tehty
    if not on_tehty:

        on_tehty = True
        pygame.mixer.music.stop()
        cool.play()

    ruutu.fill(voittovari)

    teksti = loppufontti.render("What?", True, pelivari)
    ruutu.blit(teksti, (30,245))
    teksti = loppufontti.render("oh!", True, pelivari)
    ruutu.blit(teksti, (30,300))
    teksti = loppufontti.render("ur winner", True, pelivari)
    ruutu.blit(teksti, (30,355))
    teksti = loppufontti.render("pretty cool", True, pelivari)
    ruutu.blit(teksti, (30,410))
    teksti = loppufontti.render("secret ending", True, pelivari)
    ruutu.blit(teksti, (30,40))


#pelin silmukka
while True:
    FARD()
    Aika = pygame.time.get_ticks()-alkuaika
    if hp <= 0:
        UDED()
    elif Aika > 690000:
        UVON()


    else:
        MONKE()
        OBAMIUM()

    pygame.display.flip()
    akastin.tick(FPS)