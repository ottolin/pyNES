class MapperBase:
    def __init__(self, nes):
        self.nes = nes
        self.reset()

    def reset(self):
        self.joy1StrobeState = 0
        self.joy2StrobeState = 0
        self.joypadLastWrite = 0
        
        self.mousePressed = False
        self.mouseX = 0
        self.mouseY = 0
        
        self.gameGenieActive = False
        #TODO crc?
        
    def write(self, address, value):
        if address < 0x2000:
            # Mirroring of RAM
            self.nes.cpu.mem[address&0x7FF] = value
        elif address > 0x4017:
            self.nes.cpu.mem[address] = value
            #if 0x8000 > address >= 0x6000:
                # Write to SaveRAM. Store in file
                # TODO:
                #if not self.nes.rom == None:
                #    self.nes.rom.writeBatteryRam(address, value)
        elif 0x4000 > address > 0x2007:
            self._regWrite(0x2000+(address&0x7),value)
        else:
            self._regWrite(address,value)
    
    def load(self, address):
        # Wrap around
        address &= 0xFFFF
        
        if address > 0x4017:
            # ROM
            return self.nes.cpu.mem[address]
        elif address >= 0x2000:
            # I/O Ports
            return self._regLoad(address)
        else:
            # RAM (mirrored)
            return self.nes.cpu.mem[address&0x7FF]
    
    def _regLoad(self, address):
        flag = address >> 12 # use fourth nibble 0xF000
        
        if flag in (0, 1):
            return 0
        elif flag in (2, 3):
            # PPU Registers
            flag2 = address & 0x7

            if flag2 in (0x0, 0x1):
                # Value is stored in both main memory and PPU as flags, not in the real NES
                return self.nes.cpu.mem[0x2000 + flag2]
            elif flag2 == 0x2:
                # PPU Status Register, value is stored in main memory in addition to as flags in PPU, not in the real NES
                return self.nes.ppu.readStatusRegister()
            elif flag2 == 0x4:
                # Sprite memory read
                return self.nes.ppu.sramLoad()
        elif flag == 4:
            flag3 = address-0x4015
            
            if flag3 == 0:
                # 0x4015, Sound channel enabled, DMC Status
                return self.nes.papu.readReg(address)
            elif flag3 == 1:
                # 0x4016, Joy 1 + Strobe
                return self.joy1Read()
            elif flag3 == 2:
                if not self.mousePressed:
                    return self.joy2Read()
                else:
                    sx = max(0, self.mouseX -4)
                    ex = min(256, self.mouseX +4)
                    sy = max(0, self.mouseY -4)
                    ey = min(256, self.mouseY +4)
                    w = 0
                    
                    for y in (sy, ey):
                        for x in (sx, ex):
                            if self.nes.ppu.buffer[(y<<8)+x] == 0xFFFFFF:
                                w |= 0x1<<3
                                break
                    
                    w |= 0x1<<4
        
        return 0
    
    def _regWrite(self, address, value):
        if address == 0x2000:
            # PPU Control register 1
            self.nes.cpu.mem[address] = value
            self.nes.ppu.updateControlReg1(value)
        elif address == 0x2001:
            # PPU Control register 2
            self.nes.cpu.mem[address] = value
            self.nes.ppu.updateControlReg2(value)
        elif address == 0x2003:
            # Set Sprite RAM Address
            self.nes.ppu.writeSRAMAddress(value)
        elif address == 0x2004:
            # Write to sprite RAM
            self.nes.ppu.sramWrite(value)
        elif address == 0x2005:
            # Screen scroll offsets
            self.nes.ppu.scrollWrite(value)
        elif address == 0x2006:
            # Set VRAM address
            self.nes.ppu.writeVRAMAddress(value)
        elif address == 0x2007:
            # Write to VRAM
            self.nes.ppu.vramWrite(value)
        elif address == 0x4014:
            # Sprite Memory DMA
            self.nes.ppu.sramDMA(value)
        elif address == 0x4015:
            # Sound channel switch, DMC status
            self.nes.papu.writeReg(address, value)
        elif address == 0x4016:
            # Joy 1 + Strobe
            if value == 0 and self.joypadLastWrite == 1:
                self.joy1StrobeState, self.joy2StrobeState = 0, 0
            
            self.joypadLastWrite = value
        elif address == 0x4017:
            # Sound channel frame sequencer
            self.nes.papu.writeReg(address, value)
        else:
            # Sound registers
            if 0x4017 > address >= 0x4000:
                self.nes.papu.writeReg(address, value)
    
    def joy1Read(self):
        rv = 0
        if self.joy1StrobeState in range(0, 8):
            rv = self.nes.keyboard.state1[self.joy1StrobeState]
        elif self.joy1StrobeState == 19:
            rv = 1
            
        self.joy1StrobeState += 1
        if self.joy1StrobeState >= 24:
            self.joy1StrobeState = 0
        return rv
    
    def joy2Read(self):
        rv = 0

        self.joy2StrobeState += 1
        if self.joy2StrobeState >= 24:
            self.joy2StrobeState = 0

        if self.joy2StrobeState in range(0, 8):
            rv = self.nes.keyboard.state2[self.joy2StrobeState]
        elif self.joy2StrobeState == 18:
            rv = 1
        return rv
    
    def loadROM(self):
        if (not self.nes.rom.valid) or self.nes.rom.romCount < 1:
            print "Invalid ROM. Mapper will not be loaded"
            return
        
        # Load ROM into memory
        self.loadPRGROM()
        # Load CHR ROM
        self.loadCHRROM()
        # Load Battery RAM
        self.loadBatteryRam()
        # Reset IRQ
        self.nes.cpu.requestIrq(self.nes.cpu.IRQ_RESET)
    
    def loadPRGROM(self):
        if self.nes.rom.romCount > 1:
            self.loadRomBank(0, 0x8000)
            self.loadRomBank(1, 0xC000)
        else:
            self.loadRomBank(0, 0x8000)
            self.loadRomBank(0, 0xC000)
    
    def loadCHRROM(self):
        if self.nes.rom.vromCount > 0:
            if self.nes.rom.vromCount == 1:
                self.loadVromBank(0, 0x0000)
                self.loadVromBank(0, 0x1000)
            else:
                self.loadVromBank(0, 0x0000)
                self.loadVromBank(1, 0x1000)
        else:
            print "No CHR-ROM banks"
    
    def loadBatteryRam(self):
        if self.nes.rom.batteryRam:
            ram = self.nes.rom.batteryRam
            if ram and len(ram) == 0x2000:
                # need a deep copy or not...?
                # just do a slice copy
                self.nes.cpu.mem[0x6000: 0x8000] = ram[:0x2000]
    
    def loadRomBank(self, bank, address):
        # Load a ROM bank into specific address
        bank %= self.nes.rom.romCount
        self.nes.cpu.mem[address: address + 0x4000] = self.nes.rom.rom[bank][:0x4000]

    def loadVromBank(self, bank, address):
        if self.nes.rom.vromCount == 0:
            return
        
        bank %= self.nes.rom.vromCount
        self.nes.ppu.triggerRendering()
        self.nes.ppu.vramMem[address: address + 0x1000] = self.nes.rom.vrom[bank][:0x1000]
        self.nes.ppu.ptTile[address>>4:(address>>4)+0x100] = self.nes.rom.vromTile[bank][:0x100]
    
    def load32kRomBank(self, bank, address):
        self.loadRomBank( (bank*2)%self.nes.rom.romCount, address)
        self.loadRomBank( (bank*2+1)%self.nes.rom.romCount, address+0x4000)
    
    def load8kVromBank(self, bank4kStart, address):
        if self.nes.rom.vromCount == 0:
            return
        
        self.nes.ppu.triggerRendering()
        self.loadVromBank((bank4kStart)%self.nes.rom.vromCount, address)
        self.loadVromBank((bank4kStart+1)%self.nes.rom.vromCount, address+0x1000)
        
    def load1kVromBank(self, bank1k, address):
        if self.nes.rom.vromCount == 0:
            return
        
        self.nes.ppu.triggerRendering()
        bank4k = (bank1k/4) % self.nes.rom.vromCount
        bankoffset = (bank1k%4) * 1024
        self.nes.ppu.vramMem[bankoffset: bankoffset + 1024] = self.nes.rom.vrom[bank4k][:1024]
        
        # Update Tiles
        vromTile = self.nes.rom.vromTile[bank4k]
        baseIndex = address >> 4
        for i in range(64):
            self.nes.ppu.ptTile[baseIndex+i] = vromTile[((bank1k%4)<<6)+i]
        
    def load2kVromBank(self, bank2k, address):
        if self.nes.rom.vromCount == 0:
            return
        
        self.nes.ppu.triggerRendering()
        bank4k = (bank2k/2) % self.nes.rom.vromCount
        bankoffset = (bank2k%2) * 2048
        self.nes.ppu.vramMem[bankoffset: bankoffset + 2048] = self.nes.rom.vrom[bank4k][:2048]
        
        # Update Tiles
        vromTile = self.nes.rom.vromTile[bank4k]
        baseIndex = address >> 4
        for i in range(128):
            self.nes.ppu.ptTile[baseIndex+i] = vromTile[((bank2k%2)<<7)+i]
    
    def load8kRomBank(self, bank8k, address):
        bank16k = (bank8k/2) % self.nes.rom.romCount
        offset = (bank8k%2)*0x2000
        self.nes.cpu.mem[address: address+ 0x2000] = self.nes.rom.rom[bank16k][offset: offset + 0x2000]
    
    def clockIrqCounter(self):
        pass # Does nothing, used by MMC3 mapper
    
    def latchAccess(self, address):
        pass # Does nothing, used by MMC2 mapper
    
    