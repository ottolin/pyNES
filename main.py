#import pygame
#screen = pygame.display.set_mode((256,240), pygame.HWSURFACE)
#
#surf = pygame.PixelArray(screen)
#
#for i in range(100):
#    surf[i][10:51] = screen.map_rgb((0, 255, 0))
#    
#s = screen.map_rgb((0, 255, 0))
#pygame.display.update()

#while True:
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            break
#        
from nes import Nes
import pygame

nes = Nes()
nes.loadRom('test.nes')
nes.start()

eventCheckCount = 0
while nes.isRunning:
    eventCheckCount += 1
    if eventCheckCount >= 10000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                nes.stop()
                break
        
        eventCheckCount = 0

    nes.cpu.emulate()
