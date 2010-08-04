from tile import Tile
from screen import Screen

class PPU:
    # private classes of PPU
    class NameTable:
        def __init__(self, width, height, name):
            self.width = width
            self.height = height
            self.name = name
            self.tile = [None]*(width*height)
            self.attrib = [None]*(width*height)
    
        def getTileIndex(self, x, y):
            return self.tile[y * self.width + x]
        
        def getAttrib(self, x, y):
            return self.attrib[y * self.width + x]
            
        def writeAttrib(self, index, value):
            basex = (index % 8) * 4
            basey = (index / 8) * 4
            
            for sqy in range (0, 2):
                for sqx in range (0, 2):
                    add = (value>>(2*(sqy*2+sqx)))&3
                    for y in range(0, 2):
                        for x in range(0, 2):
                            tx = basex + sqx*2 + x
                            ty = basey + sqy*2 + y
                            attindex = ty*self.width+tx
                            self.attrib[ty*self.width+tx] = (add<<2)&12
        
    class PaletteTable:
        def __init__(self):
            self.curTable = [None]*64
            self.emphTable = [[None]*64 for i in range(8)]
            self.currentEmph = -1
            
        def reset(self):
            self.setEmphasis(0)
        
        def loadNTSCPalette(self):
            self.curTable = [0x525252, 0xB40000, 0xA00000, 0xB1003D, 0x740069, 0x00005B, 0x00005F, 0x001840, 0x002F10, 0x084A08, 0x006700, 0x124200, 0x6D2800, 0x000000, 0x000000, 0x000000, 0xC4D5E7, 0xFF4000, 0xDC0E22, 0xFF476B, 0xD7009F, 0x680AD7, 0x0019BC, 0x0054B1, 0x006A5B, 0x008C03, 0x00AB00, 0x2C8800, 0xA47200, 0x000000, 0x000000, 0x000000, 0xF8F8F8, 0xFFAB3C, 0xFF7981, 0xFF5BC5, 0xFF48F2, 0xDF49FF, 0x476DFF, 0x00B4F7, 0x00E0FF, 0x00E375, 0x03F42B, 0x78B82E, 0xE5E218, 0x787878, 0x000000, 0x000000, 0xFFFFFF, 0xFFF2BE, 0xF8B8B8, 0xF8B8D8, 0xFFB6FF, 0xFFC3FF, 0xC7D1FF, 0x9ADAFF, 0x88EDF8, 0x83FFDD, 0xB8F8B8, 0xF5F8AC, 0xFFFFB0, 0xF8D8F8, 0x000000, 0x000000]
            self.makeTables()
            self.setEmphasis(0)
            
        def loadPALPalette(self):
            self.curTable = [0x525252, 0xB40000, 0xA00000, 0xB1003D, 0x740069, 0x00005B, 0x00005F, 0x001840, 0x002F10, 0x084A08, 0x006700, 0x124200, 0x6D2800, 0x000000, 0x000000, 0x000000, 0xC4D5E7, 0xFF4000, 0xDC0E22, 0xFF476B, 0xD7009F, 0x680AD7, 0x0019BC, 0x0054B1, 0x006A5B, 0x008C03, 0x00AB00, 0x2C8800, 0xA47200, 0x000000, 0x000000, 0x000000, 0xF8F8F8, 0xFFAB3C, 0xFF7981, 0xFF5BC5, 0xFF48F2, 0xDF49FF, 0x476DFF, 0x00B4F7, 0x00E0FF, 0x00E375, 0x03F42B, 0x78B82E, 0xE5E218, 0x787878, 0x000000, 0x000000, 0xFFFFFF, 0xFFF2BE, 0xF8B8B8, 0xF8B8D8, 0xFFB6FF, 0xFFC3FF, 0xC7D1FF, 0x9ADAFF, 0x88EDF8, 0x83FFDD, 0xB8F8B8, 0xF5F8AC, 0xFFFFB0, 0xF8D8F8, 0x000000, 0x000000]
            self.makeTables()
            self.setEmphasis(0)
            
        def makeTables(self):
            # Calculate a table for each possible emphasis setting
            for emph in range(0, 8):
                # Color component factors
                rFactor, gFactor, bFactor = 1.0, 1.0, 1.0
                if not emph&1 == 0:
                    rFactor, bFactor = 0.75, 0.75
                if not emph&2 == 0:
                    rFactor, gFactor = 0.75, 0.75
                if not emph&4 == 0:
                    gFactor, bFactor = 0.75, 0.75
                    
                self.emphTable[emph] = [None]*64
                
                for i in range(64):
                    col = self.curTable[i]
                    r = int(self.getRed(col) * rFactor)
                    g = int(self.getGreen(col) * gFactor)
                    b = int(self.getBlue(col) * bFactor)
                    self.emphTable[emph][i] = self.getRgb(r,g,b)
        
        def setEmphasis(self, emph):
            if not emph == self.currentEmph:
                self.currentEmph = emph
                self.curTable = self.emphTable[emph][:]
                
        def getEntry(self, yiq):
            return self.curTable[yiq]
        
        def getRed(self, rgb):
            return (rgb>>16)&0xFF
            
        def getGreen(self, rgb):
            return (rgb>>8)&0xFF
        
        def getBlue(self, rgb):
            return (rgb)&0xFF
        
        def getRgb(self, r, g, b):
            return ((r<<16)|(g<<8)|(b))
            
        def loadDefaultPalette(self):
            self.curTable[ 0] = self.getRgb(117,117,117)
            self.curTable[ 1] = self.getRgb( 39, 27,143)
            self.curTable[ 2] = self.getRgb(  0,  0,171)
            self.curTable[ 3] = self.getRgb( 71,  0,159)
            self.curTable[ 4] = self.getRgb(143,  0,119)
            self.curTable[ 5] = self.getRgb(171,  0, 19)
            self.curTable[ 6] = self.getRgb(167,  0,  0)
            self.curTable[ 7] = self.getRgb(127, 11,  0)
            self.curTable[ 8] = self.getRgb( 67, 47,  0)
            self.curTable[ 9] = self.getRgb(  0, 71,  0)
            self.curTable[10] = self.getRgb(  0, 81,  0)
            self.curTable[11] = self.getRgb(  0, 63, 23)
            self.curTable[12] = self.getRgb( 27, 63, 95)
            self.curTable[13] = self.getRgb(  0,  0,  0)
            self.curTable[14] = self.getRgb(  0,  0,  0)
            self.curTable[15] = self.getRgb(  0,  0,  0)
            self.curTable[16] = self.getRgb(188,188,188)
            self.curTable[17] = self.getRgb(  0,115,239)
            self.curTable[18] = self.getRgb( 35, 59,239)
            self.curTable[19] = self.getRgb(131,  0,243)
            self.curTable[20] = self.getRgb(191,  0,191)
            self.curTable[21] = self.getRgb(231,  0, 91)
            self.curTable[22] = self.getRgb(219, 43,  0)
            self.curTable[23] = self.getRgb(203, 79, 15)
            self.curTable[24] = self.getRgb(139,115,  0)
            self.curTable[25] = self.getRgb(  0,151,  0)
            self.curTable[26] = self.getRgb(  0,171,  0)
            self.curTable[27] = self.getRgb(  0,147, 59)
            self.curTable[28] = self.getRgb(  0,131,139)
            self.curTable[29] = self.getRgb(  0,  0,  0)
            self.curTable[30] = self.getRgb(  0,  0,  0)
            self.curTable[31] = self.getRgb(  0,  0,  0)
            self.curTable[32] = self.getRgb(255,255,255)
            self.curTable[33] = self.getRgb( 63,191,255)
            self.curTable[34] = self.getRgb( 95,151,255)
            self.curTable[35] = self.getRgb(167,139,253)
            self.curTable[36] = self.getRgb(247,123,255)
            self.curTable[37] = self.getRgb(255,119,183)
            self.curTable[38] = self.getRgb(255,119, 99)
            self.curTable[39] = self.getRgb(255,155, 59)
            self.curTable[40] = self.getRgb(243,191, 63)
            self.curTable[41] = self.getRgb(131,211, 19)
            self.curTable[42] = self.getRgb( 79,223, 75)
            self.curTable[43] = self.getRgb( 88,248,152)
            self.curTable[44] = self.getRgb(  0,235,219)
            self.curTable[45] = self.getRgb(  0,  0,  0)
            self.curTable[46] = self.getRgb(  0,  0,  0)
            self.curTable[47] = self.getRgb(  0,  0,  0)
            self.curTable[48] = self.getRgb(255,255,255)
            self.curTable[49] = self.getRgb(171,231,255)
            self.curTable[50] = self.getRgb(199,215,255)
            self.curTable[51] = self.getRgb(215,203,255)
            self.curTable[52] = self.getRgb(255,199,255)
            self.curTable[53] = self.getRgb(255,199,219)
            self.curTable[54] = self.getRgb(255,191,179)
            self.curTable[55] = self.getRgb(255,219,171)
            self.curTable[56] = self.getRgb(255,231,163)
            self.curTable[57] = self.getRgb(227,255,163)
            self.curTable[58] = self.getRgb(171,243,191)
            self.curTable[59] = self.getRgb(179,255,207)
            self.curTable[60] = self.getRgb(159,255,243)
            self.curTable[61] = self.getRgb(  0,  0,  0)
            self.curTable[62] = self.getRgb(  0,  0,  0)
            self.curTable[63] = self.getRgb(  0,  0,  0)
            
            self.makeTables()
            self.setEmphasis(0)
    
    # PPU class variables
    STATUS_VRAMWRITE= 4
    STATUS_SLSPRITECOUNT= 5
    STATUS_SPRITE0HIT= 6
    STATUS_VBLANK= 7
    
    def __init__(self, nes):
        self.nes = nes
        self.screen = Screen(nes)
    
    def reset(self):
        self.screen.reset()
        self.cycles = 0
        # memory
        self.vramMem = bytearray('\x00'*0x8000)
        self.spriteMem = bytearray('\x00'*0x100)
        
        # VRAM I/O
        self.vramAddress = 0
        self.vramTmpAddress = 0
        self.vramBufferedReadValue = 0
        self.firstWrite = True
        
        # SPR-RAM I/O
        self.sramAddress = 0 # 8-bit only
        
        self.mapperIrqCounter = 0
        self.currentMirroring = -1
        self.requestEndFrame = False
        self.nmiOk = False
        self.dummyCycleToggle = False
        self.validTileData = False
        self.nmiCounter = 0
        self.scanlineAlreadyRendered = False
        
        # Control Flags Register 1:
        self.f_nmiOnVblank = 0    # NMI on VBlank. 0=disable, 1=enable
        self.f_spriteSize = 0     # Sprite size. 0=8x8, 1=8x16
        self.f_bgPatternTable = 0 # Background Pattern Table address. 0=0x0000,1=0x1000
        self.f_spPatternTable = 0 # Sprite Pattern Table address. 0=0x0000,1=0x1000
        self.f_addrInc = 0        # PPU Address Increment. 0=1,1=32
        self.f_nTblAddress = 0    # Name Table Address. 0=0x2000,1=0x2400,2=0x2800,3=0x2C00
        
        # Control Flags Register 2:
        self.f_color = 0         # Background color. 0=black, 1=blue, 2=green, 4=red
        self.f_spVisibility = 0   # Sprite visibility. 0=not displayed,1=displayed
        self.f_bgVisibility = 0   # Background visibility. 0=Not Displayed,1=displayed
        self.f_spClipping = 0     # Sprite clipping. 0=Sprites invisible in left 8-pixel column,1=No clipping
        self.f_bgClipping = 0     # Background clipping. 0=BG invisible in left 8-pixel column, 1=No clipping
        self.f_dispType = 0       # Display type. 0=color, 1=monochrome
        
        # Counters:
        self.cntFV = 0
        self.cntV = 0
        self.cntH = 0
        self.cntVT = 0
        self.cntHT = 0
        
        # Registers:
        self.regFV = 0
        self.regV = 0
        self.regH = 0
        self.regVT = 0
        self.regHT = 0
        self.regFH = 0
        self.regS = 0
        
        self.scanlineChanged = [True]*240
        
        # These are temporary variables used in rendering and sound procedures.
        # Their states outside of those procedures can be ignored.
        # TODO: the use of self is a bit weird, investigate
        self.curNt = 0
        
        # Variables used when rendering:
        self.attrib = [None]*32;
        self.buffer = [None]*(256*240)
        self.prevBuffer = [None]*(256*240)
        self.bgbuffer = [None]*(256*240)
        self.pixrendered = [None]*(256*240)
        self.spr0dummybuffer = [None]*(256*240)
        self.dummyPixPriTable = [None]*(256*240)

        self.validTileData = False;
        self.scantile = [None]*32
        
        # Initialize misc vars:
        self.scanline = 0
        self.lastRenderedScanline = -1
        self.curX = 0
        
        # Sprite data:
        self.sprX = [0]*(64) # X coordinate
        self.sprY = [0]*(64) # Y coordinate
        self.sprTile = [0]*(64) # Tile Index (into pattern table)
        self.sprCol = [0]*(64) # Upper two bits of color
        self.vertFlip = [False]*(64) # Vertical Flip
        self.horiFlip = [False]*(64) # Horizontal Flip
        self.bgPriority = [False]*(64) # Background priority
        self.spr0HitX = 0 # Sprite #0 hit X coordinate
        self.spr0HitY = 0 # Sprite #0 hit Y coordinate
        self.hitSpr0 = False
        
        # Palette data:
        self.sprPalette = [0]*(16)
        self.imgPalette = [0]*(16)
        
        # Create pattern table tile buffers:
        self.ptTile = [Tile() for i in range(512)]
        
        # Create nametable buffers:
        # Name table data:
        self.ntable1 = [None]*(4)
        self.currentMirroring = -1
        self.nameTable = [PPU.NameTable(32,32, "Nt{0}".format(i)) for i in range(4)]
        
        # Initialize mirroring lookup table:
        self.vramMirrorTable = [i for i in range(0x8000)]

        self.showSpr0Hit = False
        self.clipToTvSize = True
        
        self.palTable = PPU.PaletteTable()
        self.palTable.loadNTSCPalette()
        self.palTable.loadDefaultPalette()
        
        self.updateControlReg1(0)
        self.updateControlReg2(0)
        
        self.oldFrame = [-1]*(256*240)
    
    def setMirroring(self, mirroring):
    
        if(mirroring == self.currentMirroring):
            return
        
        self.currentMirroring = mirroring
        self.triggerRendering()
    
        # Remove mirroring:
        if(not self.vramMirrorTable):
            self.vramMirrorTable = [i for i in range(0x8000)]

        # Palette mirroring:
        self.defineMirrorRegion(0x3f20,0x3f00,0x20)
        self.defineMirrorRegion(0x3f40,0x3f00,0x20)
        self.defineMirrorRegion(0x3f80,0x3f00,0x20)
        self.defineMirrorRegion(0x3fc0,0x3f00,0x20)
        
        # Additional mirroring:
        self.defineMirrorRegion(0x3000,0x2000,0xf00)
        self.defineMirrorRegion(0x4000,0x0000,0x4000)
    
        if(mirroring == self.nes.rom.HORIZONTAL_MIRRORING):
            # Horizontal mirroring.
            
            self.ntable1[0] = 0
            self.ntable1[1] = 0
            self.ntable1[2] = 1
            self.ntable1[3] = 1
            
            self.defineMirrorRegion(0x2400,0x2000,0x400)
            self.defineMirrorRegion(0x2c00,0x2800,0x400)
            
        elif(mirroring == self.nes.rom.VERTICAL_MIRRORING):
            # Vertical mirroring.
            
            self.ntable1[0] = 0
            self.ntable1[1] = 1
            self.ntable1[2] = 0
            self.ntable1[3] = 1
            
            self.defineMirrorRegion(0x2800,0x2000,0x400)
            self.defineMirrorRegion(0x2c00,0x2400,0x400)
            
        elif(mirroring == self.nes.rom.SINGLESCREEN_MIRRORING):
            
            # Single Screen mirroring
            
            self.ntable1[0] = 0
            self.ntable1[1] = 0
            self.ntable1[2] = 0
            self.ntable1[3] = 0
            
            self.defineMirrorRegion(0x2400,0x2000,0x400)
            self.defineMirrorRegion(0x2800,0x2000,0x400)
            self.defineMirrorRegion(0x2c00,0x2000,0x400)
            
        elif(mirroring == self.nes.rom.SINGLESCREEN_MIRRORING2):

            self.ntable1[0] = 1
            self.ntable1[1] = 1
            self.ntable1[2] = 1
            self.ntable1[3] = 1
            
            self.defineMirrorRegion(0x2400,0x2400,0x400)
            self.defineMirrorRegion(0x2800,0x2400,0x400)
            self.defineMirrorRegion(0x2c00,0x2400,0x400)
            
        else:
            
            # Assume Four-screen mirroring.
            
            self.ntable1[0] = 0
            self.ntable1[1] = 1
            self.ntable1[2] = 2
            self.ntable1[3] = 3
            
    
    def defineMirrorRegion(self, fromStart, toStart, size):
        """
        Define a mirrored area in the address lookup table.
        Assumes the regions don't overlap.
        The 'to' region is the region that is physically in memory.
        """
        for i in range(size):
            self.vramMirrorTable[fromStart+i] = toStart+i
    
    def startVBlank(self):
        # Do NMI:
        self.nes.cpu.requestIrq(self.nes.cpu.IRQ_NMI)
        
        # Make sure everything is rendered:
        if(self.lastRenderedScanline < 239):
            self.renderFramePartially(
                self.lastRenderedScanline+1,240-self.lastRenderedScanline
            )
        
        # End frame:
        self.endFrame()
        
        # Reset scanline counter:
        self.lastRenderedScanline = -1
        
        self.startFrame()
    
    def endScanline(self):
        
        if self.scanline == 19:
            # Dummy scanline.
            # May be variable length:
            if(self.dummyCycleToggle):

                # Remove dead cycle at end of scanline,
                # for next scanline:
                self.curX = 1
                self.dummyCycleToggle = not self.dummyCycleToggle
        elif self.scanline == 20:
            # Clear VBlank flag:
            self.setStatusFlag(self.STATUS_VBLANK,False)

            # Clear Sprite #0 hit flag:
            self.setStatusFlag(self.STATUS_SPRITE0HIT,False)
            self.hitSpr0 = False
            self.spr0HitX = -1
            self.spr0HitY = -1

            if(self.f_bgVisibility == 1 or self.f_spVisibility==1):

                # Update counters:
                self.cntFV = self.regFV
                self.cntV = self.regV
                self.cntH = self.regH
                self.cntVT = self.regVT
                self.cntHT = self.regHT

                if(self.f_bgVisibility==1):
                    # Render dummy scanline:
                    self.renderBgScanline(False,0)

            if(self.f_bgVisibility==1 and self.f_spVisibility==1):

                # Check sprite 0 hit for first scanline:
                self.checkSprite0(0)


            if(self.f_bgVisibility==1 or self.f_spVisibility==1):
                # Clock mapper IRQ Counter:
                self.nes.mmap.clockIrqCounter()
                
        elif self.scanline == 261:
            # Dead scanline, no rendering.
            # Set VINT:
            self.setStatusFlag(self.STATUS_VBLANK,True)
            self.requestEndFrame = True
            self.nmiCounter = 9
        
            # Wrap around:
            self.scanline = -1 # will be incremented to 0
            
        else:
            if(self.scanline>=21 and self.scanline<=260):

                # Render normally:
                if(self.f_bgVisibility == 1):

                    if(not self.scanlineAlreadyRendered):
                        # update scroll:
                        self.cntHT = self.regHT
                        self.cntH = self.regH
                        self.renderBgScanline(True,self.scanline+1-21)
                    
                    self.scanlineAlreadyRendered=False

                    # Check for sprite 0 (next scanline):
                    if((not self.hitSpr0) and self.f_spVisibility==1):
                        if(self.sprX[0]>=-7 and self.sprX[0]<256 and self.sprY[0]+1<=(self.scanline-20) and (self.sprY[0]+1+(8 if self.f_spriteSize==0 else 16))>=(self.scanline-20)):

                            if(self.checkSprite0(self.scanline-20)):
                                #console.log("found spr0. curscan="+self.scanline+" hitscan="+self.spr0HitY)
                                self.hitSpr0 = True

                if(self.f_bgVisibility==1 or self.f_spVisibility==1):
                    # Clock mapper IRQ Counter:
                    self.nes.mmap.clockIrqCounter()
        
        self.scanline+=1
        self.regsToAddress()
        self.cntsToAddress()
    
    def startFrame(self):
        # Set background color:
        bgColor=0
        
        if(self.f_dispType == 0):
            
            # Color display.
            # f_color determines color emphasis.
            # Use first entry of image palette as BG color.
            bgColor = self.imgPalette[0]
            
        else:
            
            # Monochrome display.
            # f_color determines the bg color.
            if self.f_color == 0:
                # Black
                bgColor = 0x000000
            elif self.f_color == 1:
                # Green
                bgColor = 0x00FF00
            elif self.f_color == 2:
                # Blue
                bgColor = 0xFF0000
            elif self.f_color == 3:
                # Invalid. Use black.
                bgColor = 0x000000
            elif self.f_color == 4:
                # Red
                bgColor = 0x0000FF
            else:
                # Invalid. Use black.
                bgColor = 0x000000
        
        buffer = self.buffer
        for i in range(256*240):
            buffer[i] = bgColor

        pixrendered = self.pixrendered
        for i in range(len(pixrendered)):
            pixrendered[i]=65
    
    def endFrame(self):

        buffer = self.buffer;
        
        # Draw spr#0 hit coordinates:
        if(self.showSpr0Hit):
            # Spr 0 position:
            if(self.sprX[0]>=0 and self.sprX[0]<256 and self.sprY[0]>=0 and self.sprY[0]<240):
                for i in range(256):
                    buffer[(self.sprY[0]<<8)+i] = 0xFF5555;
                for i in range(240):
                    buffer[(i<<8)+self.sprX[0]] = 0xFF5555;
            
            # Hit position:
            if(self.spr0HitX>=0 and self.spr0HitX<256 and self.spr0HitY>=0 and self.spr0HitY<240):
                for i in range(256):
                    buffer[(self.spr0HitY<<8)+i] = 0x55FF55;
                for i in range(240):
                    buffer[(i<<8)+self.spr0HitX] = 0x55FF55;
        
        # This is a bit lazy..
        # if either the sprites or the background should be clipped,
        # both are clipped after rendering is finished.
        if(self.clipToTvSize or self.f_bgClipping==0 or self.f_spClipping==0):
            # Clip left 8-pixels column:
            for y in range(240):
                for x in range(8):
                    buffer[(y<<8)+x] = 0;
        
        if(self.clipToTvSize):
            # Clip right 8-pixels column too:
            for y in range(240):
                for x in range(8):
                    buffer[(y<<8)+255-x] = 0;
        
        # Clip top and bottom 8 pixels:
        if(self.clipToTvSize):
            for y in range(8):
                for x in range(256):
                    buffer[(y<<8)+x] = 0;
                    buffer[((239-y)<<8)+x] = 0;
        
        # print buffer
        if (self.nes.opts.showDisplay):
            #imageData = self.canvasImageData.data;
            #prevBuffer = self.prevBuffer;
            #
            #for i in range(256*240):
            #    pixel = buffer[i];
            #    if (pixel != prevBuffer[i]) :
            #        j = i*4;
            #        imageData[j] = pixel&0xFF;
            #        imageData[j+1] = (pixel>>8)&0xFF;
            #        imageData[j+2] = (pixel>>16)&0xFF;
            #        prevBuffer[i] = pixel;
            
            self.screen.putImageData(buffer, 0, 0);
    
    def updatePalettes(self):
        """
        Reads data from $3f00 to $f20 
        into the two buffered palettes.
        """
        for i in range(16):
            if self.f_dispType == 0:
                self.imgPalette[i] = self.palTable.getEntry(
                    self.vramMem[0x3f00+i] & 63
                )
            else:
                self.imgPalette[i] = self.palTable.getEntry(
                    self.vramMem[0x3f00+i] & 32
                )
        
        for i in range(16):
            if self.f_dispType == 0:
                self.sprPalette[i] = self.palTable.getEntry(
                    self.vramMem[0x3f10+i] & 63
                )
            else:
                self.sprPalette[i] = self.palTable.getEntry(
                    self.vramMem[0x3f10+i] & 32
                )
    
    def updateControlReg1(self, value):
        self.triggerRendering()
        
        self.f_nmiOnVblank =    (value>>7)&1
        self.f_spriteSize =     (value>>5)&1
        self.f_bgPatternTable = (value>>4)&1
        self.f_spPatternTable = (value>>3)&1
        self.f_addrInc =        (value>>2)&1
        self.f_nTblAddress =     value&3
        
        self.regV = (value>>1)&1
        self.regH = value&1
        self.regS = (value>>4)&1
    
    def updateControlReg2(self, value):
        self.triggerRendering()
        
        self.f_color =       (value>>5)&7
        self.f_spVisibility = (value>>4)&1
        self.f_bgVisibility = (value>>3)&1
        self.f_spClipping =   (value>>2)&1
        self.f_bgClipping =   (value>>1)&1
        self.f_dispType =      value&1
        
        if self.f_dispType == 0:
            self.palTable.setEmphasis(self.f_color)
        self.updatePalettes()
    
    def setStatusFlag(self, flag, value):
        n = 1<<flag
        self.nes.cpu.mem[0x2002] = ((self.nes.cpu.mem[0x2002] & (255-n)) | (n if value else 0))
    
    def readStatusRegister(self):
        """
        CPU Register $2002:
        Read the Status Register.
        """
        
        rv = self.nes.cpu.mem[0x2002]
        
        # Reset scroll & VRAM Address toggle:
        self.firstWrite = True
        
        # Clear VBlank flag:
        self.setStatusFlag(self.STATUS_VBLANK,False)
        
        # Fetch status data:
        return rv
    
    def writeSRAMAddress(self, address):
        """
        CPU Register $2003:
        Write the SPR-RAM address that is used for sramWrite (Register 0x2004 in CPU memory map)
        """
        self.sramAddress = address
    
    def sramLoad(self):
        """
        CPU Register $2004 (R):
        Read from SPR-RAM (Sprite RAM).
        The address should be set first.
        """
        return self.spriteMem[self.sramAddress]
    
    def sramWrite(self, value):
        """
        CPU Register $2004 (W):
        Write to SPR-RAM (Sprite RAM).
        The address should be set first.
        """
        self.spriteMem[self.sramAddress] = value
        self.spriteRamWriteUpdate(self.sramAddress,value)
        self.sramAddress+=1
        self.sramAddress %= 0x100
    
    def scrollWrite(self, value):
        """
        CPU Register $2005:
        Write to scroll registers.
        The first write is the vertical offset, the second is the
        horizontal offset:
        """
        self.triggerRendering()
        
        if(self.firstWrite):
            # First write, horizontal scroll:
            self.regHT = (value>>3)&31
            self.regFH = value&7
        else:
            # Second write, vertical scroll:
            self.regFV = value&7
            self.regVT = (value>>3)&31
        
        self.firstWrite = not self.firstWrite
    
    def writeVRAMAddress(self, address):
        """
        CPU Register $2006:
        Sets the adress used when reading/writing from/to VRAM.
        The first write sets the high byte, the second the low byte.
        """
        
        if(self.firstWrite):
            self.regFV = (address>>4)&3
            self.regV = (address>>3)&1
            self.regH = (address>>2)&1
            self.regVT = (self.regVT&7) | ((address&3)<<3)
        else:
            self.triggerRendering()
            
            self.regVT = (self.regVT&24) | ((address>>5)&7)
            self.regHT = address&31
            
            self.cntFV = self.regFV
            self.cntV = self.regV
            self.cntH = self.regH
            self.cntVT = self.regVT
            self.cntHT = self.regHT
            
            self.checkSprite0(self.scanline-20)
        
        self.firstWrite = not self.firstWrite
        
        # Invoke mapper latch:
        self.cntsToAddress()
        if(self.vramAddress < 0x2000):
            self.nes.mmap.latchAccess(self.vramAddress)
    
    
    def vramLoad(self):
        """
        CPU Register $2007(R):
        Read from PPU memory. The address should be set first.
        """
        
        self.cntsToAddress()
        self.regsToAddress()
        
        # If address is in range 0x0000-0x3EFF, return buffered values:
        if(self.vramAddress <= 0x3EFF):
            tmp = self.vramBufferedReadValue
        
            # Update buffered value:
            if(self.vramAddress < 0x2000):
                self.vramBufferedReadValue = self.vramMem[self.vramAddress]
            else:
                self.vramBufferedReadValue = self.mirroredLoad(self.vramAddress)
            
            # Mapper latch access:
            if(self.vramAddress < 0x2000):
                self.nes.mmap.latchAccess(self.vramAddress)
            
            # Increment by either 1 or 32, depending on d2 of Control Register 1:
            self.vramAddress += (32 if self.f_addrInc==1 else 1)
            
            self.cntsFromAddress()
            self.regsFromAddress()
            return tmp # Return the previous buffered value.
            
        # No buffering in self mem range. Read normally.
        tmp = self.mirroredLoad(self.vramAddress)
        
        # Increment by either 1 or 32, depending on d2 of Control Register 1:
        self.vramAddress += (32 if self.f_addrInc==1 else 1) 
        
        self.cntsFromAddress()
        self.regsFromAddress()
        
        return tmp
    
    def vramWrite(self, value):
        """
        CPU Register $2007(W):
        Write to PPU memory. The address should be set first.
        """
        
        self.triggerRendering()
        self.cntsToAddress()
        self.regsToAddress()
        
        if(self.vramAddress >= 0x2000):
            # Mirroring is used.
            self.mirroredWrite(self.vramAddress,value)
        else:
            # Write normally.
            self.writeMem(self.vramAddress,value)
            
            # Invoke mapper latch:
            self.nes.mmap.latchAccess(self.vramAddress)
        
        # Increment by either 1 or 32, depending on d2 of Control Register 1:
        self.vramAddress += (32 if self.f_addrInc==1 else 1)
        self.regsFromAddress()
        self.cntsFromAddress()
    
    def sramDMA(self, value):
        """
        CPU Register $4014:
        Write 256 bytes of main memory
        into Sprite RAM.
        """
        baseAddress = value * 0x100
        
        for i in range(self.sramAddress, 256):
            data = self.nes.cpu.mem[baseAddress+i]
            self.spriteMem[i] = data
            self.spriteRamWriteUpdate(i, data)
        
        self.nes.cpu.haltCycles(513)
    
    
    def regsFromAddress(self):
        """
        Updates the scroll registers from a new VRAM address.
        """
        
        address = (self.vramTmpAddress>>8)&0xFF
        self.regFV = (address>>4)&7
        self.regV = (address>>3)&1
        self.regH = (address>>2)&1
        self.regVT = (self.regVT&7) | ((address&3)<<3)
        
        address = self.vramTmpAddress&0xFF
        self.regVT = (self.regVT&24) | ((address>>5)&7)
        self.regHT = address&31
    
    def cntsFromAddress(self):
        """
        Updates the scroll registers from a new VRAM address.
        """
        
        address = (self.vramAddress>>8)&0xFF
        self.cntFV = (address>>4)&3
        self.cntV = (address>>3)&1
        self.cntH = (address>>2)&1
        self.cntVT = (self.cntVT&7) | ((address&3)<<3)        
        
        address = self.vramAddress&0xFF
        self.cntVT = (self.cntVT&24) | ((address>>5)&7)
        self.cntHT = address&31
        
    def regsToAddress(self):
        b1  = (self.regFV&7)<<4
        b1 |= (self.regV&1)<<3
        b1 |= (self.regH&1)<<2
        b1 |= (self.regVT>>3)&3
        
        b2  = (self.regVT&7)<<5
        b2 |= self.regHT&31
        
        self.vramTmpAddress = ((b1<<8) | b2)&0x7FFF
    
    def cntsToAddress(self):
        b1  = (self.cntFV&7)<<4
        b1 |= (self.cntV&1)<<3
        b1 |= (self.cntH&1)<<2
        b1 |= (self.cntVT>>3)&3
        
        b2  = (self.cntVT&7)<<5
        b2 |= self.cntHT&31
        
        self.vramAddress = ((b1<<8) | b2)&0x7FFF
    
    def incTileCounter(self, count):
        for i in range(count, -1, -1):
            self.cntHT+=1
            if(self.cntHT==32):
                self.cntHT=0
                self.cntVT+=1
                if(self.cntVT>=30):
                    self.cntH+=1
                    if(self.cntH==2):
                        self.cntH=0
                        self.cntV+=1
                        if(self.cntV==2):
                            self.cntV=0
                            self.cntFV+=1
                            self.cntFV&=0x7
    
    def mirroredLoad(self, address):
        """
        Reads from memory, taking into account
        mirroring/mapping of address ranges.
        """
        return self.vramMem[self.vramMirrorTable[address]]
    
    def mirroredWrite(self, address, value):
        """
        Writes to memory, taking into account
        mirroring/mapping of address ranges.
        """
        
        if(address>=0x3f00 and address<0x3f20):
            # Palette write mirroring.
            if(address==0x3F00 or address==0x3F10):
                self.writeMem(0x3F00,value)
                self.writeMem(0x3F10,value)
            elif(address==0x3F04 or address==0x3F14):
                self.writeMem(0x3F04,value)
                self.writeMem(0x3F14,value)
            elif(address==0x3F08 or address==0x3F18):
                self.writeMem(0x3F08,value)
                self.writeMem(0x3F18,value)
            elif(address==0x3F0C or address==0x3F1C):
                self.writeMem(0x3F0C,value)
                self.writeMem(0x3F1C,value)
            else:
                self.writeMem(address,value)
        else:
            # Use lookup table for mirrored address:
            if(address<len(self.vramMirrorTable)):
                self.writeMem(self.vramMirrorTable[address],value)
            else:
                # FIXME
                print "Invalid VRAM address: {0}".format(address)
    
    def triggerRendering(self):
        if 260 >= self.scanline >= 21:
            # Render sprites, and combine
            self.renderFramePartially(
                self.lastRenderedScanline + 1,
                self.scanline - 21 - self.lastRenderedScanline
            )
            
            self.lastRenderedScanline = self.scanline - 21
    
    def renderFramePartially(self, startScan, scanCount):
        if self.f_spVisibility == 1:
            self.renderSpritesPartially(startScan,scanCount,True)
        
        if self.f_bgVisibility == 1:
            si = startScan << 8
            ei = (startScan + scanCount) << 8
            ei = 0xF000 if ei > 0xF000 else ei
            buffer = self.buffer
            bgbuffer = self.bgbuffer
            pixrendered = self.pixrendered
            for destIndex in range(si, ei):
                if pixrendered[destIndex] > 0xFF:
                    buffer[destIndex] = bgbuffer[destIndex]
            
        if self.f_spVisibility == 1:
            self.renderSpritesPartially(startScan, scanCount, False)
        
        self.validTileData = False
    
    def renderBgScanline(self, bgbuffer, scan):
        baseTile = 0 if (self.regS == 0) else 256
        destIndex = (scan <<8) - self.regFH
        
        self.curNt = self.ntable1[self.cntV+self.cntV+self.cntH]
        
        self.cntHT = self.regHT
        self.cntH = self.regH
        self.curNt = self.ntable1[self.cntV+self.cntV+self.cntH]
        
        if (scan<240 and (scan-self.cntFV)>=0):
            tscanoffset = self.cntFV<<3
            scantile = self.scantile
            attrib = self.attrib
            ptTile = self.ptTile
            nameTable = self.nameTable
            imgPalette = self.imgPalette
            pixrendered = self.pixrendered
            targetBuffer = self.bgbuffer if bgbuffer else self.buffer

            t, tpix, att, col = 0, 0, 0, 0
            for tile in range(32):
                if(scan>=0):
                    # Fetch tile & attrib data:
                    if(self.validTileData):
                        # Get data from array:
                        t = scantile[tile]
                        tpix = t.pix
                        att = attrib[tile]
                    else:
                        # Fetch data:
                        t = ptTile[baseTile+nameTable[self.curNt].getTileIndex(self.cntHT,self.cntVT)]
                        tpix = t.pix
                        att = nameTable[self.curNt].getAttrib(self.cntHT,self.cntVT)
                        scantile[tile] = t
                        attrib[tile] = att
                    
                    # Render tile scanline:
                    sx = 0
                    x = (tile<<3)-self.regFH

                    if(x>-8):
                        if(x<0):
                            destIndex-=x
                            sx = -x
                        
                        if(t.opaque[self.cntFV]):
                            while sx<8:
                                pix = imgPalette[tpix[tscanoffset+sx]+att]
                                targetBuffer[destIndex] = pix
                                pixrendered[destIndex] |= 256
                                destIndex+=1
                                sx+=1
                        else:
                            while sx<8:
                                col = tpix[tscanoffset+sx]
                                if(col != 0):
                                    pix = imgPalette[col+att]
                                    targetBuffer[destIndex] = pix
                                    pixrendered[destIndex] |= 256
                                destIndex+=1
                                sx+=1
                    
                # Increase Horizontal Tile Counter:
                self.cntHT += 1
                if(self.cntHT==32):
                    self.cntHT=0
                    self.cntH+=1
                    self.cntH%=2
                    self.curNt = self.ntable1[(self.cntV<<1)+self.cntH]
            
            # Tile data for one row should now have been fetched,
            # so the data in the array is valid.
            self.validTileData = True
        
        # update vertical scroll:
        self.cntFV+=1
        if(self.cntFV==8):
            self.cntFV = 0
            self.cntVT+=1
            if(self.cntVT==30):
                self.cntVT = 0
                self.cntV+=1
                self.cntV%=2
                self.curNt = self.ntable1[(self.cntV<<1)+self.cntH]
            elif(self.cntVT==32):
                self.cntVT = 0
            
            # Invalidate fetched data:
            self.validTileData = False
    
    def renderSpritesPartially(self, startscan, scancount, bgPri):
        if(self.f_spVisibility==1):
            for i in range(64):
                if(self.bgPriority[i]==bgPri and self.sprX[i]>=0 and self.sprX[i]<256 and self.sprY[i]+8>=startscan and self.sprY[i]<startscan+scancount):
                    # Show sprite.
                    if(self.f_spriteSize == 0):
                        # 8x8 sprites
                        
                        self.srcy1 = 0
                        self.srcy2 = 8
                        
                        if(self.sprY[i]<startscan):
                            self.srcy1 = startscan - self.sprY[i]-1
                        
                        if(self.sprY[i]+8 > startscan+scancount):
                            self.srcy2 = startscan+scancount-self.sprY[i]+1
                        
                        if(self.f_spPatternTable==0):
                            self.ptTile[self.sprTile[i]].render(self.buffer, 
                                0, self.srcy1, 8, self.srcy2, self.sprX[i], 
                                self.sprY[i]+1, self.sprCol[i], self.sprPalette, 
                                self.horiFlip[i], self.vertFlip[i], i, 
                                self.pixrendered
                            )
                        else:
                            self.ptTile[self.sprTile[i]+256].render(self.buffer, 0, self.srcy1, 8, self.srcy2, self.sprX[i], self.sprY[i]+1, self.sprCol[i], self.sprPalette, self.horiFlip[i], self.vertFlip[i], i, self.pixrendered)
                    else:
                        # 8x16 sprites
                        top = self.sprTile[i]
                        if((top&1)!=0):
                            top = self.sprTile[i]-1+256
                        
                        srcy1 = 0
                        srcy2 = 8
                        
                        if(self.sprY[i]<startscan):
                            srcy1 = startscan - self.sprY[i]-1
                        
                        if(self.sprY[i]+8 > startscan+scancount):
                            srcy2 = startscan+scancount-self.sprY[i]
                        
                        self.ptTile[top+(1 if self.vertFlip[i] else 0)].render(
                            self.buffer,
                            0,
                            srcy1,
                            8,
                            srcy2,
                            self.sprX[i],
                            self.sprY[i]+1,
                            self.sprCol[i],
                            self.sprPalette,
                            self.horiFlip[i],
                            self.vertFlip[i],
                            i,
                            self.pixrendered
                        )
                        
                        srcy1 = 0
                        srcy2 = 8
                        
                        if(self.sprY[i]+8<startscan):
                            srcy1 = startscan - (self.sprY[i]+8+1)
                        
                        if(self.sprY[i]+16 > startscan+scancount):
                            srcy2 = startscan+scancount-(self.sprY[i]+8)
                        
                        self.ptTile[top+(0 if self.vertFlip[i] else 1)].render(
                            self.buffer,
                            0,
                            srcy1,
                            8,
                            srcy2,
                            self.sprX[i],
                            self.sprY[i]+1+8,
                            self.sprCol[i],
                            self.sprPalette,
                            self.horiFlip[i],
                            self.vertFlip[i],
                            i,
                            self.pixrendered
                        )
                        
    def checkSprite0(self, scan):
        
        self.spr0HitX = -1
        self.spr0HitY = -1
        
        toffset = 0
        tIndexAdd = 0 if (self.f_spPatternTable==0) else 256
        bufferIndex = 0
        col = 0
        bgPri = 0
        t = 0
        
        x = self.sprX[0]
        y = self.sprY[0]+1
        
        if(self.f_spriteSize==0):
            # 8x8 sprites.

            # Check range:
            if(y<=scan and y+8>scan and x>=-7 and x<256):
                
                # Sprite is in range.
                # Draw scanline:
                t = self.ptTile[self.sprTile[0]+tIndexAdd]
                col = self.sprCol[0]
                bgPri = self.bgPriority[0]
                
                if(self.vertFlip[0]):
                    toffset = 7-(scan-y)
                else:
                    toffset = scan-y
                toffset*=8
                
                bufferIndex = scan*256+x
                if(self.horiFlip[0]):
                    for i in range(7, -1, -1):
                        if(x>=0 and x<256):
                            if(bufferIndex>=0 and bufferIndex<61440 and self.pixrendered[bufferIndex]!=0):
                                if(t.pix[toffset+i] != 0):
                                    self.spr0HitX = bufferIndex%256
                                    self.spr0HitY = scan
                                    return True
                        x+=1
                        bufferIndex+=1
                else:
                    for i in range(8):
                        if(x>=0 and x<256):
                            if(bufferIndex>=0 and bufferIndex<61440 and self.pixrendered[bufferIndex]!=0):
                                if(t.pix[toffset+i] != 0):
                                    self.spr0HitX = bufferIndex%256
                                    self.spr0HitY = scan
                                    return True
                        x+=1
                        bufferIndex+=1
        else:
            # 8x16 sprites:
        
            # Check range:
            if(y<=scan and y+16>scan and x>=-7 and x<256):
                
                # Sprite is in range.
                # Draw scanline:
                
                if(self.vertFlip[0]):
                    toffset = 15-(scan-y)
                else:
                    toffset = scan-y
                
                if(toffset<8):
                    # first half of sprite.
                    t = self.ptTile[self.sprTile[0]+(1 if self.vertFlip[0] else 0)+(255 if (self.sprTile[0]&1)!=0 else 0)]
                else:
                    # second half of sprite.
                    t = self.ptTile[self.sprTile[0]+(0 if self.vertFlip[0] else 1)+(255 if (self.sprTile[0]&1)!=0 else 0)]
                    if(self.vertFlip[0]):
                        toffset = 15-toffset
                    else:
                        toffset -= 8
                toffset*=8
                col = self.sprCol[0]
                bgPri = self.bgPriority[0]
                
                bufferIndex = scan*256+x
                if(self.horiFlip[0]):
                    for i in range(7, -1, -1):
                        if(x>=0 and x<256):
                            if(bufferIndex>=0 and bufferIndex<61440 and self.pixrendered[bufferIndex]!=0):
                                if(t.pix[toffset+i] != 0):
                                    self.spr0HitX = bufferIndex%256
                                    self.spr0HitY = scan
                                    return True
                        x+=1
                        bufferIndex+=1
                else:
                    for i in range(8):
                        if(x>=0 and x<256):
                            if(bufferIndex>=0 and bufferIndex<61440 and self.pixrendered[bufferIndex]!=0):
                                if(t.pix[toffset+i] != 0):
                                    self.spr0HitX = bufferIndex%256
                                    self.spr0HitY = scan
                                    return True
                        x+=1
                        bufferIndex+=1
        
        return False

    def writeMem(self, address, value):
        """
        This will write to PPU memory, and
        update internally buffered data
        appropriately.
        """
        self.vramMem[address] = value
        
        # Update internally buffered data:
        if(address < 0x2000):
            self.vramMem[address] = value
            self.patternWrite(address,value)
        elif(0x23c0 > address >=0x2000):
            self.nameTableWrite(self.ntable1[0],address-0x2000,value)
        elif(0x2400 > address >=0x23c0):
            self.attribTableWrite(self.ntable1[0],address-0x23c0,value)
        elif(0x27c0 > address >=0x2400):
            self.nameTableWrite(self.ntable1[1],address-0x2400,value)
        elif(0x2800 > address >=0x27c0):
            self.attribTableWrite(self.ntable1[1],address-0x27c0,value)
        elif(0x2bc0 > address >=0x2800):
            self.nameTableWrite(self.ntable1[2],address-0x2800,value)
        elif(0x2c00 > address >=0x2bc0):
            self.attribTableWrite(self.ntable1[2],address-0x2bc0,value)
        elif(0x2fc0 > address >=0x2c00):
            self.nameTableWrite(self.ntable1[3],address-0x2c00,value)
        elif(0x3000 > address >=0x2fc0):
            self.attribTableWrite(self.ntable1[3],address-0x2fc0,value)
        elif(0x3f20 > address >=0x3f00):
            self.updatePalettes()
    
    def patternWrite(self, address, value):
        """
        Updates the internal pattern
        table buffers with this new byte.
        In vNES, there is a version of this with 4 arguments which isn't used.
        """
        tileIndex = address/16
        leftOver = address%16;
        if (leftOver<8) :
            self.ptTile[tileIndex].setScanline(
                leftOver,
                value,
                self.vramMem[address+8]
            )
        else:
            self.ptTile[tileIndex].setScanline(
                leftOver-8,
                self.vramMem[address-8],
                value
            )

    
    def nameTableWrite(self, index, address, value):
        """
        Updates the internal name table buffers
        with this new byte.
        """
        self.nameTable[index].tile[address] = value
        
        # Update Sprite #0 hit:
        #updateSpr0Hit();
        self.checkSprite0(self.scanline-20)
    
    def attribTableWrite(self, index, address, value):
        """
        Updates the internal pattern
        table buffers with self new attribute
        table byte.
        """
    
        self.nameTable[index].writeAttrib(address,value)
    
    
    def spriteRamWriteUpdate(self, address, value):
        """
        Updates the internally buffered sprite
        data with this new byte of info.
        """
        tIndex = address/4
        
        if(tIndex == 0):
            #updateSpr0Hit()
            self.checkSprite0(self.scanline-20)
        
        if(address%4 == 0):
            # Y coordinate
            self.sprY[tIndex] = value
        elif(address%4 == 1):
            # Tile index
            self.sprTile[tIndex] = value
        elif(address%4 == 2):
            # Attributes
            self.vertFlip[tIndex] = ((value&0x80)!=0)
            self.horiFlip[tIndex] = ((value&0x40)!=0)
            self.bgPriority[tIndex] = ((value&0x20)!=0)
            self.sprCol[tIndex] = (value&3)<<2
        elif(address%4 == 3):
            # X coordinate
            self.sprX[tIndex] = value
    
    def doNMI(self):
        # Set VBlank flag
        self.setStatusFlag(self.STATUS_VBLANK,True)
        self.nes.cpu.requestIrq(self.nes.cpu.IRQ_NMI)
    
    def emulateCycles(self):
        while self.cycles > 0:
            
            if (self.scanline - 21 == self.spr0HitY
                and self.curX == self.spr0HitX
                and self.f_spVisibility == 1):
                # Set sprite 0 hit flag:
                self.setStatusFlag(PPU.STATUS_SPRITE0HIT, True)
            
            if (self.requestEndFrame):
                self.nmiCounter-=1
                if (self.nmiCounter == 0):
                    self.requestEndFrame = False
                    self.startVBlank()
                    #break
            
            self.curX+=1
            if (self.curX == 341):
                self.curX = 0
                self.endScanline()

            self.cycles -= 1
