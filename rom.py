from tile import Tile
from util import get_class
from mappers import *

class Rom:
    VERTICAL_MIRRORING= 0
    HORIZONTAL_MIRRORING= 1
    FOURSCREEN_MIRRORING= 2
    SINGLESCREEN_MIRRORING= 3
    SINGLESCREEN_MIRRORING2= 4
    SINGLESCREEN_MIRRORING3= 5
    SINGLESCREEN_MIRRORING4= 6
    CHRROM_MIRRORING= 7
    
    mapperName = ['Unknown Mapper']*255
    mapperName[ 0] = "NROM"
    mapperName[ 1] = "Nintendo MMC1"
    mapperName[ 2] = "UxROM"
    mapperName[ 3] = "CNROM"
    mapperName[ 4] = "Nintendo MMC3"
    mapperName[ 5] = "Nintendo MMC5"
    mapperName[ 6] = "FFE F4xxx"
    mapperName[ 7] = "AxROM"
    mapperName[ 8] = "FFE F3xxx"
    mapperName[ 9] = "Nintendo MMC2"
    mapperName[10] = "Nintendo MMC4"
    mapperName[11] = "Color Dreams"
    mapperName[12] = "FFE F6xxx"
    mapperName[13] = "CPROM"
    mapperName[15] = "iNES Mapper #015"
    mapperName[16] = "Bandai"
    mapperName[17] = "FFE F8xxx"
    mapperName[18] = "Jaleco SS8806"
    mapperName[19] = "Namcot 106"
    mapperName[20] = "(Hardware) Famicom Disk System"
    mapperName[21] = "Konami VRC4a, VRC4c"
    mapperName[22] = "Konami VRC2a"
    mapperName[23] = "Konami VRC2b, VRC4e, VRC4f"
    mapperName[24] = "Konami VRC6a"
    mapperName[25] = "Konami VRC4b, VRC4d"
    mapperName[26] = "Konami VRC6b"
    mapperName[32] = "Irem G-101"
    mapperName[33] = "Taito TC0190, TC0350"
    mapperName[34] = "BxROM, NINA-001"
    mapperName[41] = "Caltron 6-in-1"
    mapperName[46] = "Rumblestation 15-in-1"
    mapperName[47] = "Nintendo MMC3 Multicart (Super Spike V'Ball + Nintendo World Cup)"
    mapperName[48] = "iNES Mapper #048"
    mapperName[64] = "Tengen RAMBO-1"
    mapperName[65] = "Irem H-3001"
    mapperName[66] = "GxROM"
    mapperName[67] = "Sunsoft 3"
    mapperName[68] = "Sunsoft 4"
    mapperName[69] = "Sunsoft FME-7"
    mapperName[70] = "iNES Mapper #070"
    mapperName[71] = "Camerica"
    mapperName[72] = "iNES Mapper #072"
    mapperName[73] = "Konami VRC3"
    mapperName[75] = "Konami VRC1"
    mapperName[76] = "iNES Mapper #076 (Digital Devil Monogatari - Megami Tensei)"
    mapperName[77] = "iNES Mapper #077 (Napoleon Senki)"
    mapperName[78] = "Irem 74HC161/32"
    mapperName[79] = "American Game Cartridges"
    mapperName[80] = "iNES Mapper #080"
    mapperName[82] = "iNES Mapper #082"
    mapperName[85] = "Konami VRC7a, VRC7b"
    mapperName[86] = "iNES Mapper #086 (Moero!! Pro Yakyuu)"
    mapperName[87] = "iNES Mapper #087"
    mapperName[88] = "iNES Mapper #088"
    mapperName[89] = "iNES Mapper #087 (Mito Koumon)"
    mapperName[92] = "iNES Mapper #092"
    mapperName[93] = "iNES Mapper #093 (Fantasy Zone)"
    mapperName[94] = "iNES Mapper #094 (Senjou no Ookami)"
    mapperName[95] = "iNES Mapper #095 (Dragon Buster) [MMC3 Derived]"
    mapperName[96] = "(Hardware) Oeka Kids Tablet"
    mapperName[97] = "iNES Mapper #097 (Kaiketsu Yanchamaru)"
    mapperName[105] = "NES-EVENT [MMC1 Derived]"
    mapperName[113] = "iNES Mapper #113"
    mapperName[115] = "iNES Mapper #115 (Yuu Yuu Hakusho Final) [MMC3 Derived]"
    mapperName[118] = "iNES Mapper #118 [MMC3 Derived]"
    mapperName[119] = "TQROM"
    mapperName[140] = "iNES Mapper #140 (Bio Senshi Dan)"
    mapperName[152] = "iNES Mapper #152"
    mapperName[154] = "iNES Mapper #152 (Devil Man)"
    mapperName[159] = "Bandai (Alternate of #016)"
    mapperName[180] = "(Hardware) Crazy Climber Controller"
    mapperName[182] = "iNES Mapper #182"
    mapperName[184] = "iNES Mapper #184"
    mapperName[185] = "iNES Mapper #185"
    mapperName[207] = "iNES Mapper #185 (Fudou Myouou Den)"
    mapperName[228] = "Active Enterprises"
    mapperName[232] = "Camerica (Quattro series)"
    
    bMapperSupported = [False]*255
    bMapperSupported[ 0] = True # No Mapper
    bMapperSupported[ 1] = True # MMC1
    bMapperSupported[ 2] = True # UNROM
    bMapperSupported[ 3] = True # CNROM
    bMapperSupported[ 4] = True # MMC3
    bMapperSupported[ 7] = True # AOROM
    bMapperSupported[ 9] = True # MMC2
    bMapperSupported[10] = True # MMC4
    bMapperSupported[11] = True # ColorDreams
    bMapperSupported[15] = True
    bMapperSupported[18] = True
    bMapperSupported[21] = True
    bMapperSupported[22] = True
    bMapperSupported[23] = True
    bMapperSupported[32] = True
    bMapperSupported[33] = True
    bMapperSupported[34] = True # BxROM
    bMapperSupported[48] = True
    bMapperSupported[64] = True
    bMapperSupported[66] = True # GNROM
    bMapperSupported[68] = True # SunSoft4 chip
    bMapperSupported[71] = True # Camerica
    bMapperSupported[72] = True
    bMapperSupported[75] = True
    bMapperSupported[78] = True
    bMapperSupported[79] = True
    bMapperSupported[87] = True
    bMapperSupported[94] = True
    bMapperSupported[105] = True
    bMapperSupported[140] = True
    bMapperSupported[182] = True
    bMapperSupported[232] = True # Camerica /Quattro


    def __init__(self, nes):
        self.nes = nes
        
        self.header = None
        self.romData = None
        self.rom = None
        self.vrom = None
        self.saveRam = None
        self.vromTile = None
        
        self.romCount = 0
        self.vromCount = 0
        self.mirroring = False
        self.batteryRam = False
        self.trainer = False
        self.fourScreen = False
        self.mapperType = 0
        self.crc32 = 0
        self.valid = False
        self.fileName = ""
        

    def load(self, fileName):
        self.fileName = fileName
        fh = open(fileName, 'rb')
        self.romData = bytearray(fh.read())
        fh.close()
        
        if not self.romData[:4] == 'NES\x1a':
            self.valid = False
            return
        
        # Reading header
        self.header = self.romData[:16]
        self.romCount = self.header[4]
        self.vromCount = self.header[5] * 2
        self.mirroring = True if ((self.header[6]&1) != 0) else False
        self.batteryRam = not ((self.header[6]&2) == 0)
        self.trainer = not ((self.header[6]&4) == 0)
        self.fourScreen = not ((self.header[6]&8) == 0)
        self.mapperType = (self.header[6] >> 4) | (self.header[7] & 0XF0);
        
        if self.batteryRam:
            pass #TODO: loading battery ram
        
        foundError = False
        # 8~15 bytes must be 0's
        for i in range(8, 16):
            if not self.header[i] == 0:
                foundError = True
                break
        
        if foundError:
            # Ignore byte 7
            self.mapperType &= 0xF
        
        # self.rom[romCount][16384]
        self.rom = [[0] * 16384 for i in range(self.romCount)]
        # self.vrom[vromCount][4096]
        self.vrom = [[0] * 4096 for i in range(self.vromCount)]
        # self.vromTile[vromCount][256]
        self.vromTile = [[0] * 256 for i in range(self.vromCount)]
        
        # Loading PRG-ROM banks
        offset = 16
        for i in range(self.romCount):
            for j in range(16384):
                if offset + j >= len(self.romData):
                    break
                self.rom[i][j] = self.romData[offset + j]
            offset += 16384
        
        # Loading CHR-ROM banks
        for i in range(self.vromCount):
            for j in range(4096):
                if offset + j >= len(self.romData):
                    break
                self.vrom[i][j] = self.romData[offset + j]
            offset += 4096
            
        # Creating vrom tiles
        for i in range(self.vromCount):
            for j in range(256):
                self.vromTile[i][j] = Tile()
                
        tileIndex = 0
        leftOver = 0
        for v in range(self.vromCount):
            for i in range(4096):
                tileIndex = i >> 4
                leftOver = i % 16
                if leftOver < 8:
                    self.vromTile[v][tileIndex].setScanline(
                        leftOver,
                        self.vrom[v][i],
                        self.vrom[v][i+8]
                    )
                else:
                    self.vromTile[v][tileIndex].setScanline(
                        leftOver-8,
                        self.vrom[v][i-8],
                        self.vrom[v][i]
                    )
        
        self.valid = True
    
    def getMirroringType(self):
        if self.fourScreen:
            return self.FOURSCREEN_MIRRORING
        if not self.mirroring:
            return self.HORIZONTAL_MIRRORING
        return self.VERTICAL_MIRRORING
    
    def getMapperName(self):
        if len(self.mapperName) > self.mapperType >= 0:
            return self.mapperName[self.mapperType]
        return "Unknown Mapper, {0}".format(self.mapperType)
    
    def mapperSupported(self):
        if len(self.bMapperSupported) > self.mapperType >= 0:
            return self.bMapperSupported[self.mapperType]
        return False
    
    def createMapper(self):
        if self.mapperSupported():
            mapper_class_name = 'mappers.Mapper{0}'.format(self.mapperType)
            MapperClass = get_class(mapper_class_name)
            if MapperClass:
                mc = MapperClass(self.nes)
                return mc
            else:
                print "Mapper class {0} not found.".format(mapper_class_name)
                return None
        else:
            return None
        
    