#!/usr/bin/env python

import pygame

pygame.init()

screenWidth = 500
screenHeight = 500

win = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("ConnectFour")

run = True
while(run):
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()