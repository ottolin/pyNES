class Tile:
    def __init__(self):
        self.pix = [0]*64
        self.fbIndex = 0
        self.tIndex = 0
        #self.x, self.y = 0, 0
        self.w, self.h = 0, 0
        self.incX, self.incY = 0, 0
        self.palIndex = 0
        self.tpri = 0
        self.c = 0
        self.initialized = False
        self.opaque = [False]*8
    
    def setBuffer(self, scanline):
        for y in range(8):
            # TODO: need to unpack scanline to byte?
            self.setScanline(y, scanline[y], scanline[y+8])
        
    def setScanline(self, sline, b1, b2):
        self.initialized = True
        self.tIndex = sline << 3
        for x in range(8):
            self.pix[self.tIndex+x] = ((b1 >> (7 - x)) & 1) + (((b2 >> (7 - x)) & 1) << 1)
            if self.pix[self.tIndex + x] == 0:
                self.opaque[sline] = False
                
    def render(self, buffer, srcx1, srcy1, srcx2, srcy2, dx, dy, palAdd, palette, flipHorizontal, flipVertical, pri, priTable):
        if dx<-7 or dx>=256 or dy<-7 or dy>=240:
            return
        
        self.w = srcx2-srcx1
        self.h = srcy2-srcy1
        
        if dx<0:
            srcx1 -= dx
        
        if dx + srcx2 >= 256:
            srcx2 = 256-dx
        
        if dy<0:
            srcy1 -= dy
            
        if dy + srcy2 >= 240:
            srcy2 = 240 -dy
        
        if not flipHorizontal and not flipVertical:
            self.fbIndex = (dy<<8)+dx
            self.tIndex = 0
            for self.y in range (8):
                for self.x in range (8):
                    if self.x>=srcx1 and self.x<srcx2 and self.y>=srcy1 and self.y<srcy2:
                        self.palIndex = self.pix[self.tIndex]
                        self.tpri = priTable[self.fbIndex]
                        if self.palIndex!=0 and pri<=(self.tpri&0xFF):
                            buffer[self.fbIndex] = palette[self.palIndex+palAdd]
                            self.tpri = (self.tpri&0xF00)|pri
                            priTable[self.fbIndex] =self.tpri
                    self.fbIndex += 1
                    self.tIndex += 1
                self.fbIndex -= 8
                self.fbIndex += 256
        elif flipHorizontal and not flipVertical:
            self.fbIndex = (dy<<8)+dx
            self.tIndex = 7
            for self.y in range (8):
                for self.x in range (8):
                    if self.x>=srcx1 and self.x<srcx2 and self.y>=srcy1 and self.y<srcy2:
                        self.palIndex = self.pix[self.tIndex]
                        self.tpri = priTable[self.fbIndex]
                        if self.palIndex!=0 and pri<=(self.tpri&0xFF):
                            buffer[self.fbIndex] = palette[self.palIndex+palAdd]
                            self.tpri = (self.tpri&0xF00)|pri
                            priTable[self.fbIndex] =self.tpri
                    self.fbIndex+=1
                    self.tIndex-=1
                self.fbIndex-=8
                self.fbIndex+=256
                self.tIndex+=16
        elif flipVertical and not flipHorizontal:
            self.fbIndex = (dy<<8)+dx
            self.tIndex = 56
            for self.y in range (8):
                for self.x in range (8):
                    if self.x>=srcx1 and self.x<srcx2 and self.y>=srcy1 and self.y<srcy2:
                        self.palIndex = self.pix[self.tIndex]
                        self.tpri = priTable[self.fbIndex]
                        if self.palIndex!=0 and pri<=(self.tpri&0xFF):
                            buffer[self.fbIndex] = palette[self.palIndex+palAdd]
                            self.tpri = (self.tpri&0xF00)|pri
                            priTable[self.fbIndex] =self.tpri
                    self.fbIndex+=1
                    self.tIndex+=1
                self.fbIndex-=8
                self.fbIndex+=256
                self.tIndex-=16
        else:
            self.fbIndex = (dy<<8)+dx
            self.tIndex = 63
            for self.y in range (8):
                for self.x in range (8):
                    if self.x>=srcx1 and self.x<srcx2 and self.y>=srcy1 and self.y<srcy2:
                        self.palIndex = self.pix[self.tIndex]
                        self.tpri = priTable[self.fbIndex]
                        if self.palIndex!=0 and pri<=(self.tpri&0xFF):
                            buffer[self.fbIndex] = palette[self.palIndex+palAdd]
                            self.tpri = (self.tpri&0xF00)|pri
                            priTable[self.fbIndex] =self.tpri
                    self.fbIndex+=1
                    self.tIndex-=1
                self.fbIndex-=8
                self.fbIndex+=256
        
        return buffer, priTable
    
    def isTransparent(self, x, y):
        return (self.pix[(y<<3)+x]==0)