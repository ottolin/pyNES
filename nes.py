from cpu import CPU
from rom import Rom
from ppu import PPU
from papu import PAPU
from input import Keyboard
from threading import Thread

class Nes:
    #class ExecutionThread(Thread):
    #    def __init__(self, nes):
    #        self.nes = nes
    #        Thread.__init__(self)
    #    
    #    def run(self):
    #        print "Execution thread started."
    #        while self.nes.isRunning:
    #            self.nes.cpu.emulate()

    class Options:
        CPU_FREQ_NTSC= 1789772.5 #1789772.72727272d
        CPU_FREQ_PAL= 1773447.4
        def __init__(self):
            self.preferredFrameRate= 60,
            self.fpsInterval= 500 # Time between updating FPS in ms
            self.showDisplay= True
    
            self.emulateSound= False
            self.sampleRate= 44100 # Sound sample rate in hz
    
    def __init__(self):
        self.cpu = CPU(self)
        self.ppu = PPU(self)
        self.papu = PAPU(self)
        self.keyboard = Keyboard(self)
        self.rom = None
        self.romFile = None
        self.mmap = None

        self.isRunning = False
        self.limitFrames = True
        self.fpsFrameCount = 0
        
        self.opts = Nes.Options()
        self.frameTime = self.opts.preferredFrameRate

        #self.executionThread = Nes.ExecutionThread(self)
        
    def reset(self):
        if self.mmap:
            self.mmap.reset()
        self.cpu.reset()
        self.ppu.reset()
        self.papu.reset()

    def start(self):
        if (self.rom and self.rom.valid):
            if (not self.isRunning):
                self.isRunning = True;
                self.ppu.startFrame()
                #self.executionThread.start()
        else:
            print "There is no ROM loaded, or it is invalid."
    
    def printFps(self):
        pass
    
    def stop(self):
        self.isRunning = False
    
    def reloadRom(self):
        if self.romFile:
            self.loadRom(self.romFile)
    
    def loadRom(self, file):
        if self.isRunning:
            self.stop()
        
        print "Loading rom {0}...".format(file)
        
        # Load ROM file
        self.rom = Rom(self)
        self.rom.load(file)
        if self.rom.valid:
            print "Rom loaded."
            self.reset()
            print "Creating rom mapper..."
            self.mmap = self.rom.createMapper()
            if not self.mmap:
                return
            self.mmap.loadROM()
            # TODO:
            self.ppu.setMirroring(self.rom.getMirroringType())
            self.romFile = file
            
            print "Initialized NES, ready to start."
        else:
            print "Invalid ROM: {0}".format(file)
        
        return self.rom.valid