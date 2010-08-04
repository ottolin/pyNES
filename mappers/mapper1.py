from base import MapperBase

class Mapper1(MapperBase):
    def __init__(self, nes):
        MapperBase.__init__(self, nes)
    
    def reset(self):
        MapperBase.reset(self)
        
        # 5 bit buffer
        self.regBuffer = 0
        self.regBufferCounter = 0
        
        # Register 0:
        self.mirroring = 0
        self.oneScreenMirroring = 0
        self.prgSwitchingArea = 1
        self.prgSwitchingSize = 1
        self.vromSwitchingSize = 0
    
        # Register 1:
        self.romSelectionReg0 = 0
    
        # Register 2:
        self.romSelectionReg1 = 0
    
        # Register 3:
        self.romBankSelect = 0

    def write(self, address, value):
        if address < 0x8000:
            MapperBase.write(self, address, value)
            return
        
        if not ((value&128) == 0):
            # reset buffer
            self.regBufferCounter = 0
            self.regBuffer = 0
            # reset register
            if self.getRegNumber(address) == 0:
                self.prgSwitchingArea = 1
                self.prgSwitchingSize = 1
        else:
            # Continue buffering:
            self.regBuffer = (self.regBuffer & (0xFF-(1<<self.regBufferCounter))) | ((value&1)<<self.regBufferCounter)
            self.regBufferCounter += 1
            if self.regBufferCounter == 5:
                self.setReg(self.getRegNumber(address), self.regBuffer)
                #reset buffer
                self.regBufferCounter = 0
                self.regBuffer = 0
    
    def setReg(self, reg, value):
        runDefault = False
        if reg == 0:
            # Mirroring
            tmp = value&3
            if not tmp == self.mirroring:
                self.mirroring = tmp
                if self.mirroring&2 == 0:
                    # SingleScreen mirroring overrides the other setting
                    self.nes.ppu.setMirroring(self.nes.rom.SINGLESCREEN_MIRRORING)
                else:
                    # Not overridden by SingleScreen mirroring
                    self.nes.ppu.setMirroring(
                        self.nes.rom.HORIZONTAL_MIRRORING if not self.mirroring&1 == 0 else self.nes.rom.VERTICAL_MIRRORING
                    )
            # PRG Switching Area
            self.prgSwitchingArea = (value>>2)&1
        
            # PRG Switching Size:
            self.prgSwitchingSize = (value>>3)&1
    
            # VROM Switching Size:
            self.vromSwitchingSize = (value>>4)&1
        
        elif reg == 1:
            # ROM Selection
            self.romSelectionReg0 = (value>>4)&1
            
            if self.nes.rom.vromCount > 0:
                # Select VROM bank at 0x0000
                if self.vromSwitchingSize == 0:
                    # Swap 8kB VROM
                    if self.romSelectionReg0 == 0:
                        self.load8kVromBank((value&0xF), 0x0000)
                    else:
                        self.load8kVromBank(
                            self.nes.rom.vromCount/2 + value&0xF,
                            0x0000
                        )
                else:
                    # Swap 4kB VROM
                    if self.romSelectionReg0 == 0:
                        self.loadVromBank((value&0xF), 0x0000)
                    else:
                        self.loadVromBank(
                            self.nes.rom.vromCount/2 + value&0xF,
                            0x0000
                        )
        elif reg == 2:
            # ROM Selection
            self.romSelectionReg1 = (value>>4)&1
            
            if self.nes.rom.vromCount > 0:
                # Select VROM bank at 0x1000
                if self.vromSwitchingSize == 1:
                    # Swap 4kB VROM
                    if self.romSelectionReg1 == 0:
                        self.loadVromBank((value&0xF), 0x1000)
                    else:
                        self.loadVromBank(
                            self.nes.rom.vromCount/2 + value&0xF,
                            0x1000
                        )
            runDefault = True
        else:
            runDefault = True
            
        if runDefault:
            tmp = value & 0xF
            bank, baseBank = 0, 0
            
            if self.nes.rom.romCount >= 32:
                # 1024kB cart
                if self.vromSwitchingSize == 0:
                    if self.romSelectionoReg0 == 1:
                        baseBank = 16
                else:
                    baseBank = (self.romSelectionReg0 | (self.romSelectionReg1<<1)) << 3
            elif self.nes.rom.romCount >= 16:
                # 512kB cart
                if self.romSelectionReg0 == 1:
                    baseBank = 8
            
            if self.prgSwitchingSize == 0:
                # 32kB
                bank = baseBank + (value&0xF)
                self.load32kRomBank(bank, 0x8000)
            else:
                # 16kB
                bank = baseBank*2 + (value&0xF)
                if self.prgSwitchingArea == 0:
                    self.loadRomBank(bank, 0xC000)
                else:
                    self.loadRomBank(bank, 0x8000)
    
    def getRegNumber(self, address):
        if 0x9FFF >= address >= 0x8000:
            return 0
        elif 0xBFFF >= address >= 0xA000:
            return 1
        elif 0xDFFF >= address >= 0xC000:
            return 2
        else:
            return 3
        
    def loadROM(self):
        if not self.nes.rom.valid:
            print "MMC1: Invalid ROM! Unable to load."
            return
        
        #loading PRG-ROM
        self.loadRomBank(0, 0x8000)
        self.loadRomBank(self.nes.rom.romCount-1, 0xC000)
        
        #loading CHR-ROM
        self.loadCHRROM()
        
        #loading battery RAM
        self.loadBatteryRam()
        
        #resetting irq
        self.nes.cpu.requestIrq(self.nes.cpu.IRQ_RESET)
    
    def switchLowHighPrgRom(self, oldSetting):
        pass #TODO
    
    def switch16to32(self):
        pass #TODO
    
    def switch32to16(self):
        pass #TODO
