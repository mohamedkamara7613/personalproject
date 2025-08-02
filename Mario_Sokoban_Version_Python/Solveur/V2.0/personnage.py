# coding:utf-8
"""
    starting at Wen 27 Aug 2021
    Par Mohamed Kamara
--------------------- Mario Sokoban v2.0 --------------------------
-------------- main.py


    Rôle du fichier : gere les actions pouvant etre faite sur les personnages
"""
from data import *

import pygame
import sys
import time


def choisir_personnage(window_surface):
    pygame.init()
    joueur = {"HAUT": 0, "BAS": 0, "GAUCHE": 0, "DROITE": 0}
    joueur_selectionne = ""
    joueur_choisi = False
    police = pygame.font.Font("doc/police.ttf", 30)

    # Loading picture
    mario_menu = pygame.image.load("doc/src_img/personnage/mario/menu_mario.png")
    ndeya_menu = pygame.image.load("doc/src_img/personnage/ndeya/menu_ndeya.png")
    shadow_menu = pygame.image.load("doc/src_img/personnage/shadow/menu_shadow.png")
    tail_menu = pygame.image.load("doc/src_img/personnage/tail/menu_tail.png")
    sonic_menu = pygame.image.load("doc/src_img/personnage/sonic/menu_sonic.png")

    # Main loop
    launched = True
    while launched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP1:
                    joueur_selectionne = "MARIO"
                    joueur_choisi = True
                    joueur["HAUT"] = pygame.image.load("doc/src_img/personnage/mario/mario_haut.gif")
                    joueur["BAS"] = pygame.image.load("doc/src_img/personnage/mario/mario_bas.gif")
                    joueur["GAUCHE"] = pygame.image.load("doc/src_img/personnage/mario/mario_gauche.gif")
                    joueur["DROITE"] = pygame.image.load("doc/src_img/personnage/mario/mario_droite.gif")
                    launched = False

                elif event.key == pygame.K_KP2:
                    joueur_selectionne = "NDEYA"
                    joueur_choisi = True
                    joueur["HAUT"] = pygame.image.load("doc/src_img/personnage/ndeya/ndeya.png")
                    joueur["BAS"] = pygame.image.load("doc/src_img/personnage/ndeya/ndeya.png")
                    joueur["GAUCHE"] = pygame.image.load("doc/src_img/personnage/ndeya/ndeya.png")
                    joueur["DROITE"] = pygame.image.load("doc/src_img/personnage/ndeya/ndeya.png")
                    launched = False

                elif event.key == pygame.K_KP3:
                    joueur_selectionne = "SHADOW"
                    joueur_choisi = True
                    joueur["HAUT"] = pygame.image.load("doc/src_img/personnage/shadow/shadow_haut.png")
                    joueur["BAS"] = pygame.image.load("doc/src_img/personnage/shadow/shadow_bas.png")
                    joueur["GAUCHE"] = pygame.image.load("doc/src_img/personnage/shadow/shadow_gauche.png")
                    joueur["DROITE"] = pygame.image.load("doc/src_img/personnage/shadow/shadow_droite.png")
                    launched = False

                elif event.key == pygame.K_KP4:
                    joueur_selectionne = "TAIL"
                    joueur_choisi = True
                    joueur["HAUT"] = pygame.image.load("doc/src_img/personnage/tail/tail_haut.png")
                    joueur["BAS"] = pygame.image.load("doc/src_img/personnage/tail/tail_bas.png")
                    joueur["GAUCHE"] = pygame.image.load("doc/src_img/personnage/tail/tail_gauche.png")
                    joueur["DROITE"] = pygame.image.load("doc/src_img/personnage/tail/tail_droite.png")
                    launched = False

                elif event.key == pygame.K_KP5:
                    joueur_selectionne = "SONIC"
                    joueur_choisi = True
                    joueur["HAUT"] = pygame.image.load("doc/src_img/personnage/sonic/sonic_haut.png")
                    joueur["BAS"] = pygame.image.load("doc/src_img/personnage/sonic/sonic_bas.png")
                    joueur["GAUCHE"] = pygame.image.load("doc/src_img/personnage/sonic/sonic_gauche.png")
                    joueur["DROITE"] = pygame.image.load("doc/src_img/personnage/sonic/sonic_droite.png")
                    launched = False

        if joueur_choisi:
            # Afficher en text le joueur choisi
            print(joueur_selectionne)
            window_surface.fill(font)
            text = police.render("Vous avez choisi : {} ".format(joueur_selectionne), True, (255, 255, 255))
            position = [(window_width / 2) - (text.get_width() / 2), (window_height / 2) - (text.get_height() / 2)]
            window_surface.blit(text, position)
            position = [position[0] + text.get_width() + 10, position[1]]
            window_surface.blit(joueur["BAS"], position)

            pygame.display.flip()
            time.sleep(2)

        # Effacement de l'ecran
        window_surface.fill(font)
        position = [(window_width / 2) - (mario_menu.get_width() / 2),
                    mario_menu.get_height() + 200]
        window_surface.blit(mario_menu, position)

        position = [(window_width / 2) - (mario_menu.get_width() / 2),
                    position[1] + mario_menu.get_height() + 20]
        window_surface.blit(ndeya_menu, position)

        position = [(window_width / 2) - (mario_menu.get_width() / 2),
                    position[1] + ndeya_menu.get_height() + 20]
        window_surface.blit(shadow_menu, position)

        position = [(window_width / 2) - (mario_menu.get_width() / 2),
                    position[1] + shadow_menu.get_height() + 20]
        window_surface.blit(tail_menu, position)

        position = [(window_width / 2) - (mario_menu.get_width() / 2),
                    position[1] + tail_menu.get_height() + 20]
        window_surface.blit(sonic_menu, position)

        pygame.display.flip()
    return joueur
