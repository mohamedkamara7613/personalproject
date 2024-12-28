#coding:utf-8
import pygame
import sys
FPS = 30
pygame.init()
screen = pygame.display.set_mode((480, 500))
rectScreen = screen.get_rect()
chat = pygame.image.load("mario.gif").convert()
rectChat = chat.get_rect()
vChat = int(round(150/FPS))
clock = pygame.time.Clock()

#BOUCLE DE JEU
while True:
    time = clock.tick(FPS)
    # GESTION DES EVENEMENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(25)

    #TOUCHES APPUYEES
    keys = pygame.key.get_pressed()

    #... A COMPLETER AVEC LE CODE DE VOTRE JEU ...
    vxchat = 0
    vychat = 0

    if keys[pygame.K_RIGHT]:
        vxchat = vChat

    if keys[pygame.K_LEFT]:
        vxchat = -vChat
    if keys[pygame.K_DOWN]:
        vychat = vChat
    if keys[pygame.K_UP]:
        vychat = -vChat

    rectChat = rectChat.move(vxchat, vychat).clamp(rectScreen)
    screen.fill(0x90EE90)
    screen.blit(chat, rectChat)
    # MAJ DE L'AFFICHAGE
    pygame.display.update()