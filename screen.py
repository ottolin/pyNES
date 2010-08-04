import pygame
class Screen:
    def __init__(self, nes):
        self.nes = nes
        self.screen = pygame.display.set_mode((256,240), pygame.HWSURFACE)
        self.surf = pygame.PixelArray(self.screen)
        #self.fps = 0
    
    def putImageData(self, imageData, x, y):
        #print self.fps
        #self.fps += 1
        
        for sy in range(240):
            for sx in range(256):
                self.surf[sx][sy] = imageData[sy*256+sx]
        pygame.display.update()

    def reset(self):
        pass