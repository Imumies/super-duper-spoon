import pygame
import sys
from pygame.locals import *


# alustaa pugamen
pygame.init()

koko = (400,600)  # eka on leveys ja toka korkeus
ruutu = pygame.display.set_mode(koko)

taustavari = (0, 255, 4)
pallovari = (255, 0, 0)
#käsittelee tapahtumia
def FARD():
    tapahtumat = pygame.event.get()
    for tapahtuma in tapahtumat:
        if tapahtuma.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


#piirtää
def MONKE():
    napit =  pygame.mouse.get_pressed()
    if napit[0]:
        ruutu.fill(taustavari)
    keskipiste = pygame.mouse.get_pos()
    koko2 = (15,10)
    pygame.draw.circle(ruutu, pallovari, keskipiste, 30)
    #pygame.draw.rect(ruutu, pallovari, keskipiste+koko2)

#pelin silmukka
while True:
    FARD()
    MONKE()
    pygame.display.flip()