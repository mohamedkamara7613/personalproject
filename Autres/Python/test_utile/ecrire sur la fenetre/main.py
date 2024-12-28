#coding:utf-8
import pygame
"""
Charger la police a partir d'un fichier
	pygame.font.Font("nom_police", taille)
	font.render('texte', forme_arrondi, couleur)
 """

white_color = (255, 255, 255)
texte = str()


pygame.init()

window_surface = pygame.display.set_mode((640,480))
pygame.display.set_caption("Afficher du texte avec pygame")

#Chargement de la police
arial_font = pygame.font.SysFont("arial", 20)



launched = True
while launched:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			launched = False
	
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				texte = texte + "a"
			

	#Rendu du texte
	texte_surface = arial_font.render(texte, True, white_color)

	window_surface.blit(texte_surface, [10,10])
	pygame.display.flip()