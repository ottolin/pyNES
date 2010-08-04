class CPU:
    IRQ_NORMAL=0
    IRQ_NMI=1
    IRQ_RESET=2
    # CPU private classes
    class OpData:
        # Instructions =
        INS_ADC = 0
        INS_AND = 1
        INS_ASL = 2
        
        INS_BCC = 3
        INS_BCS = 4
        INS_BEQ = 5
        INS_BIT = 6
        INS_BMI = 7
        INS_BNE = 8
        INS_BPL = 9
        INS_BRK = 10
        INS_BVC = 11
        INS_BVS = 12
        
        INS_CLC = 13
        INS_CLD = 14
        INS_CLI = 15
        INS_CLV = 16
        INS_CMP = 17
        INS_CPX = 18
        INS_CPY = 19
        
        INS_DEC = 20
        INS_DEX = 21
        INS_DEY = 22
        
        INS_EOR = 23
        
        INS_INC = 24
        INS_INX = 25
        INS_INY = 26
        
        INS_JMP = 27
        INS_JSR = 28
        
        INS_LDA = 29
        INS_LDX = 30
        INS_LDY = 31
        INS_LSR = 32
        
        INS_NOP = 33
        
        INS_ORA = 34
        
        INS_PHA = 35
        INS_PHP = 36
        INS_PLA = 37
        INS_PLP = 38
        
        INS_ROL = 39
        INS_ROR = 40
        INS_RTI = 41
        INS_RTS = 42
        
        INS_SBC = 43
        INS_SEC = 44
        INS_SED = 45
        INS_SEI = 46
        INS_STA = 47
        INS_STX = 48
        INS_STY = 49
        
        INS_TAX = 50
        INS_TAY = 51
        INS_TSX = 52
        INS_TXA = 53
        INS_TXS = 54
        INS_TYA = 55
        
        INS_DUMMY = 56 # dummy instruction used for 'halting' the processor some cycles
        
        # -------------------------------- #
        
        # Addressing modes =
        ADDR_ZP         = 0
        ADDR_REL        = 1
        ADDR_IMP        = 2
        ADDR_ABS        = 3
        ADDR_ACC        = 4
        ADDR_IMM        = 5
        ADDR_ZPX        = 6
        ADDR_ZPY        = 7
        ADDR_ABSX       = 8
        ADDR_ABSY       = 9
        ADDR_PREIDXIND  = 10
        ADDR_POSTIDXIND = 11
        ADDR_INDABS     = 12
        
        cycTable = bytearray((
            7,6,2,8,3,3,5,5,3,2,2,2,4,4,6,6, #/*0x00*/ 
            2,5,2,8,4,4,6,6,2,4,2,7,4,4,7,7, #/*0x10*/ 
            6,6,2,8,3,3,5,5,4,2,2,2,4,4,6,6, #/*0x20*/ 
            2,5,2,8,4,4,6,6,2,4,2,7,4,4,7,7, #/*0x30*/ 
            6,6,2,8,3,3,5,5,3,2,2,2,3,4,6,6, #/*0x40*/ 
            2,5,2,8,4,4,6,6,2,4,2,7,4,4,7,7, #/*0x50*/ 
            6,6,2,8,3,3,5,5,4,2,2,2,5,4,6,6, #/*0x60*/ 
            2,5,2,8,4,4,6,6,2,4,2,7,4,4,7,7, #/*0x70*/ 
            2,6,2,6,3,3,3,3,2,2,2,2,4,4,4,4, #/*0x80*/ 
            2,6,2,6,4,4,4,4,2,5,2,5,5,5,5,5, #/*0x90*/ 
            2,6,2,6,3,3,3,3,2,2,2,2,4,4,4,4, #/*0xA0*/ 
            2,5,2,5,4,4,4,4,2,4,2,4,4,4,4,4, #/*0xB0*/ 
            2,6,2,8,3,3,5,5,2,2,2,2,4,4,6,6, #/*0xC0*/ 
            2,5,2,8,4,4,6,6,2,4,2,7,4,4,7,7, #/*0xD0*/ 
            2,6,3,8,3,3,5,5,2,2,2,2,4,4,6,6, #/*0xE0*/ 
            2,5,2,8,4,4,6,6,2,4,2,7,4,4,7,7  #/*0xF0*/ 
            ))
            
        instname = {}
        # Instruction Names:
        instname[ 0] = "ADC"
        instname[ 1] = "AND"
        instname[ 2] = "ASL"
        instname[ 3] = "BCC"
        instname[ 4] = "BCS"
        instname[ 5] = "BEQ"
        instname[ 6] = "BIT"
        instname[ 7] = "BMI"
        instname[ 8] = "BNE"
        instname[ 9] = "BPL"
        instname[10] = "BRK"
        instname[11] = "BVC"
        instname[12] = "BVS"
        instname[13] = "CLC"
        instname[14] = "CLD"
        instname[15] = "CLI"
        instname[16] = "CLV"
        instname[17] = "CMP"
        instname[18] = "CPX"
        instname[19] = "CPY"
        instname[20] = "DEC"
        instname[21] = "DEX"
        instname[22] = "DEY"
        instname[23] = "EOR"
        instname[24] = "INC"
        instname[25] = "INX"
        instname[26] = "INY"
        instname[27] = "JMP"
        instname[28] = "JSR"
        instname[29] = "LDA"
        instname[30] = "LDX"
        instname[31] = "LDY"
        instname[32] = "LSR"
        instname[33] = "NOP"
        instname[34] = "ORA"
        instname[35] = "PHA"
        instname[36] = "PHP"
        instname[37] = "PLA"
        instname[38] = "PLP"
        instname[39] = "ROL"
        instname[40] = "ROR"
        instname[41] = "RTI"
        instname[42] = "RTS"
        instname[43] = "SBC"
        instname[44] = "SEC"
        instname[45] = "SED"
        instname[46] = "SEI"
        instname[47] = "STA"
        instname[48] = "STX"
        instname[49] = "STY"
        instname[50] = "TAX"
        instname[51] = "TAY"
        instname[52] = "TSX"
        instname[53] = "TXA"
        instname[54] = "TXS"
        instname[55] = "TYA"
        
        addrDesc = (
            "Zero Page           ",
            "Relative            ",
            "Implied             ",
            "Absolute            ",
            "Accumulator         ",
            "Immediate           ",
            "Zero Page,X         ",
            "Zero Page,Y         ",
            "Absolute,X          ",
            "Absolute,Y          ",
            "Preindexed Indirect ",
            "Postindexed Indirect",
            "Indirect Absolute   "
        )
        
        def __init__(self):
            self.opdata = [0xFF] * 0x100
            
            # ADC:
            self._setOp(self.INS_ADC,0x69,self.ADDR_IMM,2,2)
            self._setOp(self.INS_ADC,0x65,self.ADDR_ZP,2,3)
            self._setOp(self.INS_ADC,0x75,self.ADDR_ZPX,2,4)
            self._setOp(self.INS_ADC,0x6D,self.ADDR_ABS,3,4)
            self._setOp(self.INS_ADC,0x7D,self.ADDR_ABSX,3,4)
            self._setOp(self.INS_ADC,0x79,self.ADDR_ABSY,3,4)
            self._setOp(self.INS_ADC,0x61,self.ADDR_PREIDXIND,2,6)
            self._setOp(self.INS_ADC,0x71,self.ADDR_POSTIDXIND,2,5)
            
            # AND:
            self._setOp(self.INS_AND,0x29,self.ADDR_IMM,2,2)
            self._setOp(self.INS_AND,0x25,self.ADDR_ZP,2,3)
            self._setOp(self.INS_AND,0x35,self.ADDR_ZPX,2,4)
            self._setOp(self.INS_AND,0x2D,self.ADDR_ABS,3,4)
            self._setOp(self.INS_AND,0x3D,self.ADDR_ABSX,3,4)
            self._setOp(self.INS_AND,0x39,self.ADDR_ABSY,3,4)
            self._setOp(self.INS_AND,0x21,self.ADDR_PREIDXIND,2,6)
            self._setOp(self.INS_AND,0x31,self.ADDR_POSTIDXIND,2,5)
            
            # ASL:
            self._setOp(self.INS_ASL,0x0A,self.ADDR_ACC,1,2)
            self._setOp(self.INS_ASL,0x06,self.ADDR_ZP,2,5)
            self._setOp(self.INS_ASL,0x16,self.ADDR_ZPX,2,6)
            self._setOp(self.INS_ASL,0x0E,self.ADDR_ABS,3,6)
            self._setOp(self.INS_ASL,0x1E,self.ADDR_ABSX,3,7)
            
            # BCC:
            self._setOp(self.INS_BCC,0x90,self.ADDR_REL,2,2)
            
            # BCS:
            self._setOp(self.INS_BCS,0xB0,self.ADDR_REL,2,2)
            
            # BEQ:
            self._setOp(self.INS_BEQ,0xF0,self.ADDR_REL,2,2)
            
            # BIT:
            self._setOp(self.INS_BIT,0x24,self.ADDR_ZP,2,3)
            self._setOp(self.INS_BIT,0x2C,self.ADDR_ABS,3,4)
            
            # BMI:
            self._setOp(self.INS_BMI,0x30,self.ADDR_REL,2,2)
            
            # BNE:
            self._setOp(self.INS_BNE,0xD0,self.ADDR_REL,2,2)
            
            # BPL:
            self._setOp(self.INS_BPL,0x10,self.ADDR_REL,2,2)
            
            # BRK:
            self._setOp(self.INS_BRK,0x00,self.ADDR_IMP,1,7)
            
            # BVC:
            self._setOp(self.INS_BVC,0x50,self.ADDR_REL,2,2)
            
            # BVS:
            self._setOp(self.INS_BVS,0x70,self.ADDR_REL,2,2)
            
            # CLC:
            self._setOp(self.INS_CLC,0x18,self.ADDR_IMP,1,2)
            
            # CLD:
            self._setOp(self.INS_CLD,0xD8,self.ADDR_IMP,1,2)
            
            # CLI:
            self._setOp(self.INS_CLI,0x58,self.ADDR_IMP,1,2)
            
            # CLV:
            self._setOp(self.INS_CLV,0xB8,self.ADDR_IMP,1,2)
            
            # CMP:
            self._setOp(self.INS_CMP,0xC9,self.ADDR_IMM,2,2)
            self._setOp(self.INS_CMP,0xC5,self.ADDR_ZP,2,3)
            self._setOp(self.INS_CMP,0xD5,self.ADDR_ZPX,2,4)
            self._setOp(self.INS_CMP,0xCD,self.ADDR_ABS,3,4)
            self._setOp(self.INS_CMP,0xDD,self.ADDR_ABSX,3,4)
            self._setOp(self.INS_CMP,0xD9,self.ADDR_ABSY,3,4)
            self._setOp(self.INS_CMP,0xC1,self.ADDR_PREIDXIND,2,6)
            self._setOp(self.INS_CMP,0xD1,self.ADDR_POSTIDXIND,2,5)
            
            # CPX:
            self._setOp(self.INS_CPX,0xE0,self.ADDR_IMM,2,2)
            self._setOp(self.INS_CPX,0xE4,self.ADDR_ZP,2,3)
            self._setOp(self.INS_CPX,0xEC,self.ADDR_ABS,3,4)
            
            # CPY:
            self._setOp(self.INS_CPY,0xC0,self.ADDR_IMM,2,2)
            self._setOp(self.INS_CPY,0xC4,self.ADDR_ZP,2,3)
            self._setOp(self.INS_CPY,0xCC,self.ADDR_ABS,3,4)
            
            # DEC:
            self._setOp(self.INS_DEC,0xC6,self.ADDR_ZP,2,5)
            self._setOp(self.INS_DEC,0xD6,self.ADDR_ZPX,2,6)
            self._setOp(self.INS_DEC,0xCE,self.ADDR_ABS,3,6)
            self._setOp(self.INS_DEC,0xDE,self.ADDR_ABSX,3,7)
            
            # DEX:
            self._setOp(self.INS_DEX,0xCA,self.ADDR_IMP,1,2)
            
            # DEY:
            self._setOp(self.INS_DEY,0x88,self.ADDR_IMP,1,2)
            
            # EOR:
            self._setOp(self.INS_EOR,0x49,self.ADDR_IMM,2,2)
            self._setOp(self.INS_EOR,0x45,self.ADDR_ZP,2,3)
            self._setOp(self.INS_EOR,0x55,self.ADDR_ZPX,2,4)
            self._setOp(self.INS_EOR,0x4D,self.ADDR_ABS,3,4)
            self._setOp(self.INS_EOR,0x5D,self.ADDR_ABSX,3,4)
            self._setOp(self.INS_EOR,0x59,self.ADDR_ABSY,3,4)
            self._setOp(self.INS_EOR,0x41,self.ADDR_PREIDXIND,2,6)
            self._setOp(self.INS_EOR,0x51,self.ADDR_POSTIDXIND,2,5)
            
            # INC:
            self._setOp(self.INS_INC,0xE6,self.ADDR_ZP,2,5)
            self._setOp(self.INS_INC,0xF6,self.ADDR_ZPX,2,6)
            self._setOp(self.INS_INC,0xEE,self.ADDR_ABS,3,6)
            self._setOp(self.INS_INC,0xFE,self.ADDR_ABSX,3,7)
            
            # INX:
            self._setOp(self.INS_INX,0xE8,self.ADDR_IMP,1,2)
            
            # INY:
            self._setOp(self.INS_INY,0xC8,self.ADDR_IMP,1,2)
            
            # JMP:
            self._setOp(self.INS_JMP,0x4C,self.ADDR_ABS,3,3)
            self._setOp(self.INS_JMP,0x6C,self.ADDR_INDABS,3,5)
            
            # JSR:
            self._setOp(self.INS_JSR,0x20,self.ADDR_ABS,3,6)
            
            # LDA:
            self._setOp(self.INS_LDA,0xA9,self.ADDR_IMM,2,2)
            self._setOp(self.INS_LDA,0xA5,self.ADDR_ZP,2,3)
            self._setOp(self.INS_LDA,0xB5,self.ADDR_ZPX,2,4)
            self._setOp(self.INS_LDA,0xAD,self.ADDR_ABS,3,4)
            self._setOp(self.INS_LDA,0xBD,self.ADDR_ABSX,3,4)
            self._setOp(self.INS_LDA,0xB9,self.ADDR_ABSY,3,4)
            self._setOp(self.INS_LDA,0xA1,self.ADDR_PREIDXIND,2,6)
            self._setOp(self.INS_LDA,0xB1,self.ADDR_POSTIDXIND,2,5)
            
            
            # LDX:
            self._setOp(self.INS_LDX,0xA2,self.ADDR_IMM,2,2)
            self._setOp(self.INS_LDX,0xA6,self.ADDR_ZP,2,3)
            self._setOp(self.INS_LDX,0xB6,self.ADDR_ZPY,2,4)
            self._setOp(self.INS_LDX,0xAE,self.ADDR_ABS,3,4)
            self._setOp(self.INS_LDX,0xBE,self.ADDR_ABSY,3,4)
            
            # LDY:
            self._setOp(self.INS_LDY,0xA0,self.ADDR_IMM,2,2)
            self._setOp(self.INS_LDY,0xA4,self.ADDR_ZP,2,3)
            self._setOp(self.INS_LDY,0xB4,self.ADDR_ZPX,2,4)
            self._setOp(self.INS_LDY,0xAC,self.ADDR_ABS,3,4)
            self._setOp(self.INS_LDY,0xBC,self.ADDR_ABSX,3,4)
            
            # LSR:
            self._setOp(self.INS_LSR,0x4A,self.ADDR_ACC,1,2)
            self._setOp(self.INS_LSR,0x46,self.ADDR_ZP,2,5)
            self._setOp(self.INS_LSR,0x56,self.ADDR_ZPX,2,6)
            self._setOp(self.INS_LSR,0x4E,self.ADDR_ABS,3,6)
            self._setOp(self.INS_LSR,0x5E,self.ADDR_ABSX,3,7)
            
            # NOP:
            self._setOp(self.INS_NOP,0xEA,self.ADDR_IMP,1,2)
            
            # ORA:
            self._setOp(self.INS_ORA,0x09,self.ADDR_IMM,2,2)
            self._setOp(self.INS_ORA,0x05,self.ADDR_ZP,2,3)
            self._setOp(self.INS_ORA,0x15,self.ADDR_ZPX,2,4)
            self._setOp(self.INS_ORA,0x0D,self.ADDR_ABS,3,4)
            self._setOp(self.INS_ORA,0x1D,self.ADDR_ABSX,3,4)
            self._setOp(self.INS_ORA,0x19,self.ADDR_ABSY,3,4)
            self._setOp(self.INS_ORA,0x01,self.ADDR_PREIDXIND,2,6)
            self._setOp(self.INS_ORA,0x11,self.ADDR_POSTIDXIND,2,5)
            
            # PHA:
            self._setOp(self.INS_PHA,0x48,self.ADDR_IMP,1,3)
            
            # PHP:
            self._setOp(self.INS_PHP,0x08,self.ADDR_IMP,1,3)
            
            # PLA:
            self._setOp(self.INS_PLA,0x68,self.ADDR_IMP,1,4)
            
            # PLP:
            self._setOp(self.INS_PLP,0x28,self.ADDR_IMP,1,4)
            
            # ROL:
            self._setOp(self.INS_ROL,0x2A,self.ADDR_ACC,1,2)
            self._setOp(self.INS_ROL,0x26,self.ADDR_ZP,2,5)
            self._setOp(self.INS_ROL,0x36,self.ADDR_ZPX,2,6)
            self._setOp(self.INS_ROL,0x2E,self.ADDR_ABS,3,6)
            self._setOp(self.INS_ROL,0x3E,self.ADDR_ABSX,3,7)
            
            # ROR:
            self._setOp(self.INS_ROR,0x6A,self.ADDR_ACC,1,2)
            self._setOp(self.INS_ROR,0x66,self.ADDR_ZP,2,5)
            self._setOp(self.INS_ROR,0x76,self.ADDR_ZPX,2,6)
            self._setOp(self.INS_ROR,0x6E,self.ADDR_ABS,3,6)
            self._setOp(self.INS_ROR,0x7E,self.ADDR_ABSX,3,7)
            
            # RTI:
            self._setOp(self.INS_RTI,0x40,self.ADDR_IMP,1,6)
            
            # RTS:
            self._setOp(self.INS_RTS,0x60,self.ADDR_IMP,1,6)
            
            # SBC:
            self._setOp(self.INS_SBC,0xE9,self.ADDR_IMM,2,2)
            self._setOp(self.INS_SBC,0xE5,self.ADDR_ZP,2,3)
            self._setOp(self.INS_SBC,0xF5,self.ADDR_ZPX,2,4)
            self._setOp(self.INS_SBC,0xED,self.ADDR_ABS,3,4)
            self._setOp(self.INS_SBC,0xFD,self.ADDR_ABSX,3,4)
            self._setOp(self.INS_SBC,0xF9,self.ADDR_ABSY,3,4)
            self._setOp(self.INS_SBC,0xE1,self.ADDR_PREIDXIND,2,6)
            self._setOp(self.INS_SBC,0xF1,self.ADDR_POSTIDXIND,2,5)
            
            # SEC:
            self._setOp(self.INS_SEC,0x38,self.ADDR_IMP,1,2)
            
            # SED:
            self._setOp(self.INS_SED,0xF8,self.ADDR_IMP,1,2)
            
            # SEI:
            self._setOp(self.INS_SEI,0x78,self.ADDR_IMP,1,2)
            
            # STA:
            self._setOp(self.INS_STA,0x85,self.ADDR_ZP,2,3)
            self._setOp(self.INS_STA,0x95,self.ADDR_ZPX,2,4)
            self._setOp(self.INS_STA,0x8D,self.ADDR_ABS,3,4)
            self._setOp(self.INS_STA,0x9D,self.ADDR_ABSX,3,5)
            self._setOp(self.INS_STA,0x99,self.ADDR_ABSY,3,5)
            self._setOp(self.INS_STA,0x81,self.ADDR_PREIDXIND,2,6)
            self._setOp(self.INS_STA,0x91,self.ADDR_POSTIDXIND,2,6)
            
            # STX:
            self._setOp(self.INS_STX,0x86,self.ADDR_ZP,2,3)
            self._setOp(self.INS_STX,0x96,self.ADDR_ZPY,2,4)
            self._setOp(self.INS_STX,0x8E,self.ADDR_ABS,3,4)
            
            # STY:
            self._setOp(self.INS_STY,0x84,self.ADDR_ZP,2,3)
            self._setOp(self.INS_STY,0x94,self.ADDR_ZPX,2,4)
            self._setOp(self.INS_STY,0x8C,self.ADDR_ABS,3,4)
            
            # TAX:
            self._setOp(self.INS_TAX,0xAA,self.ADDR_IMP,1,2)
            
            # TAY:
            self._setOp(self.INS_TAY,0xA8,self.ADDR_IMP,1,2)
            
            # TSX:
            self._setOp(self.INS_TSX,0xBA,self.ADDR_IMP,1,2)
            
            # TXA:
            self._setOp(self.INS_TXA,0x8A,self.ADDR_IMP,1,2)
            
            # TXS:
            self._setOp(self.INS_TXS,0x9A,self.ADDR_IMP,1,2)
            
            # TYA:
            self._setOp(self.INS_TYA,0x98,self.ADDR_IMP,1,2)
        
            
        def _setOp(self, inst, op, addr, size, cycles):
            self.opdata[op] = ((inst & 0xFF)) | ((addr & 0xFF)<<8) | ((size & 0xFF)<<16) | ((cycles & 0xFF)<<24)
    
    # CPU codes
    def __init__(self, nes):
        self.inst = {}
        for k, v in CPU.OpData.instname.items():
            self.inst[k] = getattr(self, 'do_' + v.upper())

        onAddrMode = {}
        onAddrMode[CPU.OpData.ADDR_ZP] = self.do_ADDR_ZP
        onAddrMode[CPU.OpData.ADDR_REL] = self.do_ADDR_REL
        onAddrMode[CPU.OpData.ADDR_IMP] = self.do_ADDR_IMP
        onAddrMode[CPU.OpData.ADDR_ABS] = self.do_ADDR_ABS
        onAddrMode[CPU.OpData.ADDR_ACC] = self.do_ADDR_ACC
        onAddrMode[CPU.OpData.ADDR_IMM] = self.do_ADDR_IMM
        onAddrMode[CPU.OpData.ADDR_ZPX] = self.do_ADDR_ZPX
        onAddrMode[CPU.OpData.ADDR_ZPY] = self.do_ADDR_ZPY
        onAddrMode[CPU.OpData.ADDR_ABSX] = self.do_ADDR_ABSX
        onAddrMode[CPU.OpData.ADDR_ABSY] = self.do_ADDR_ABSY
        onAddrMode[CPU.OpData.ADDR_PREIDXIND] = self.do_ADDR_PREIDXIND
        onAddrMode[CPU.OpData.ADDR_POSTIDXIND] = self.do_ADDR_POSTIDXIND
        onAddrMode[CPU.OpData.ADDR_INDABS] = self.do_ADDR_INDABS
        self.onAddrMode = onAddrMode

        self.nes = nes
        self.reset()
    
    def callOp(self, command):
        return getattr(self,  'do_' + command.upper(), None)

    def do_ADDR_ZP(self, opaddr):
        # 0. Zero Page mode. Use the address given after the opcode, 
        # but without high byte.
        return self._load(opaddr+2), 0
    
    def do_ADDR_REL(self, opaddr):
        # 1. Relative mode
        addr = self._load(opaddr+2)
        if addr<0x80:
            addr += self.REG_PC
        else:
            addr += self.REG_PC-256
        return addr, 0
    
    def do_ADDR_IMP(self, opaddr):
        return 0, 0
    
    def do_ADDR_ABS(self, opaddr):
        # 3. Absolute mode. Use the two bytes following the opcode as 
        # an address.
        return self._load16bit(opaddr+2), 0
    
    def do_ADDR_ACC(self, opaddr):
        # 4. Accumulator mode. The address is in the accumulator 
        # register.
        return self.REG_ACC, 0
    
    def do_ADDR_IMM(self, opaddr):
        # 5. Immediate mode. The value is given after the opcode.
        return self.REG_PC, 0
    
    def do_ADDR_ZPX(self, opaddr):
        # 6. Zero Page Indexed mode, X as index. Use the address given 
        # after the opcode, then add the
        # X register to it to get the final address.
        return (self._load(opaddr+2)+self.REG_X)&0xFF, 0
    
    def do_ADDR_ZPY(self, opaddr):
        # 7. Zero Page Indexed mode, Y as index. Use the address given 
        # after the opcode, then add the
        # Y register to it to get the final address.
        return (self._load(opaddr+2)+self.REG_Y)&0xFF, 0
    
    def do_ADDR_ABSX(self, opaddr):
        # 8. Absolute Indexed Mode, X as index. Same as zero page 
        # indexed, but with the high byte.
        cycleAdd = 0
        addr = self._load16bit(opaddr+2)
        if((addr&0xFF00)!=((addr+self.REG_X)&0xFF00)):
            cycleAdd = 1
        addr += self.REG_X
        return addr, cycleAdd
    
    def do_ADDR_ABSY(self, opaddr):
        # 9. Absolute Indexed Mode, Y as index. Same as zero page 
        # indexed, but with the high byte.
        cycleAdd = 0
        addr = self._load16bit(opaddr+2)
        if((addr&0xFF00)!=((addr+self.REG_Y)&0xFF00)):
            cycleAdd = 1
        addr += self.REG_Y
        return addr, cycleAdd
    
    def do_ADDR_PREIDXIND(self, opaddr):
        # 10. Pre-indexed Indirect mode. Find the 16-bit address 
        # starting at the given location plus
        # the current X register. The value is the contents of that 
        # address.
        cycleAdd = 0
        addr = self._load(opaddr+2)
        if((addr&0xFF00)!=((addr+self.REG_X)&0xFF00)):
            cycleAdd = 1
        addr += self.REG_X
        addr &= 0xFF
        addr = self._load16bit(addr)
        return addr, cycleAdd
    
    def do_ADDR_POSTIDXIND(self, opaddr):
        # 11. Post-indexed Indirect mode. Find the 16-bit address 
        # contained in the given location
        # (and the one following). Add to that address the contents 
        # of the Y register. Fetch the value
        # stored at that adress.
        cycleAdd = 0
        addr = self._load16bit(self._load(opaddr+2))
        if((addr&0xFF00)!=((addr+self.REG_Y)&0xFF00)):
            cycleAdd = 1
        addr += self.REG_Y
        return addr, cycleAdd
    
    def do_ADDR_INDABS(self, opaddr):
        # 12. Indirect Absolute mode. Find the 16-bit address contained 
        # at the given location.
        addr = self._load16bit(opaddr+2); # Find op
        if addr < 0x1FFF:
            addr = self.mem[addr] + (self.mem[(addr & 0xFF00) | (((addr & 0xFF) + 1) & 0xFF)] << 8) # Read from address given in op
        else:
            addr = self.nes.mmap._load(addr) + (self.nes.mmap._load((addr & 0xFF00) | (((addr & 0xFF) + 1) & 0xFF)) << 8)
        return addr, 0
    
    def do_ADC(self, **kwargs):
        """
        Add with carry
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        cycleAdd = kwargs['cycleAdd']
        
        temp = self.REG_ACC + self._load(addr) + self.F_CARRY
        self.F_OVERFLOW = 1 if (not (((self.REG_ACC ^ self._load(addr)) & 0x80)!=0) and (((self.REG_ACC ^ temp) & 0x80))!=0) else 0
        self.F_CARRY = 1 if (temp>255) else 0
        self.F_SIGN = (temp>>7)&1
        self.F_ZERO = temp&0xFF
        self.REG_ACC = (temp&255)
        return cycleAdd
    
    def do_AND(self, **kwargs):
        """
        AND memory with accumulator.
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        addrMode = kwargs['addrMode']
        cycleAdd = kwargs['cycleAdd']
        
        self.REG_ACC = self.REG_ACC & self._load(addr)
        self.F_SIGN = (self.REG_ACC>>7)&1
        self.F_ZERO = self.REG_ACC
        #self.REG_ACC = temp
        if not addrMode == CPU.OpData.ADDR_POSTIDXIND:
            return cycleAdd
        return 0
    
    def do_ASL(self, **kwargs):
        """
        Shift left one bit
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        addrMode = kwargs['addrMode']
        
        if addrMode == CPU.OpData.ADDR_ACC:
            self.F_CARRY = (self.REG_ACC>>7)&1
            self.REG_ACC = (self.REG_ACC<<1)&255
            self.F_SIGN = (self.REG_ACC>>7)&1
            self.F_ZERO = self.REG_ACC
        else:
            temp = self._load(addr)
            self.F_CARRY = (temp>>7)&1
            temp = (temp<<1)&255
            self.F_SIGN = (temp>>7)&1
            self.F_ZERO = temp
            self._write(addr, temp)
        return 0
    
    def do_BCC(self, **kwargs):
        """
        Branch on carry clear
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        opaddr = kwargs['opaddr']
        rv = 0
        if self.F_CARRY == 0:
            rv = 2 if ((opaddr&0xFF00)!=(addr&0xFF00)) else 1
            self.REG_PC = addr
        return rv
    
    def do_BCS(self, **kwargs):
        """
        Branch on carry set
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        opaddr = kwargs['opaddr']
        rv = 0
        if self.F_CARRY == 1:
            rv = 2 if ((opaddr&0xFF00)!=(addr&0xFF00)) else 1
            self.REG_PC = addr
        return rv
    
    def do_BEQ(self, **kwargs):
        """
        Branch on Zero
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        opaddr = kwargs['opaddr']
        rv = 0
        if self.F_ZERO == 0:
            rv = 2 if ((opaddr&0xFF00)!=(addr&0xFF00)) else 1
            self.REG_PC = addr
        return rv
            
    def do_BIT(self, **kwargs):
        """
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        temp = self._load(addr)
        self.F_SIGN = (temp>>7)&1
        self.F_OVERFLOW = (temp>>6)&1
        temp &= self.REG_ACC
        self.F_ZERO = temp
        return 0
    
    def do_BMI(self, **kwargs):
        """
        Branch on -ve result
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        rv = 0
        if self.F_SIGN == 1:
            rv = 1
            self.REG_PC = addr
        return rv
    
    def do_BNE(self, **kwargs):
        """
        Branch on not zero
        Return: cycles to be added after this operation
        """
        
        addr = kwargs['addr']
        opaddr = kwargs['opaddr']
        rv = 0
        if not self.F_ZERO == 0:
            rv = 2 if ((opaddr&0xFF00)!=(addr&0xFF00)) else 1
            self.REG_PC = addr
        return rv
        
    def do_BPL(self, **kwargs):
        """
        Branch on +ve result
        Return: cycles to be added after this operation
        """
        
        addr = kwargs['addr']
        opaddr = kwargs['opaddr']
        rv = 0
        if self.F_SIGN == 0:
            rv = 2 if ((opaddr&0xFF00)!=(addr&0xFF00)) else 1
            self.REG_PC = addr
        return rv
    
    def do_BRK(self, **kwargs):
        """
        Return: cycles to be added after this operation
        """
        
        self.REG_PC += 2
        self._push((self.REG_PC>>8)&255)
        self._push(self.REG_PC&255)
        self.F_BRK = 1

        self._push(
            (self.F_CARRY)| \
            ((1 if (self.F_ZERO==0) else 0)<<1)| \
            (self.F_INTERRUPT<<2)| \
            (self.F_DECIMAL<<3)| \
            (self.F_BRK<<4)| \
            (self.F_NOTUSED<<5)| \
            (self.F_OVERFLOW<<6)| \
            (self.F_SIGN<<7)
        )

        self.F_INTERRUPT = 1
        #self.REG_PC = self._load(0xFFFE) | (self._load(0xFFFF) << 8)
        self.REG_PC = self._load16bit(0xFFFE)
        self.REG_PC -= 1
        return 0
        
    def do_BVC(self, **kwargs):
        """
        Branch on overflow clear
        Return: cycles to be added after this operation
        """
        
        addr = kwargs['addr']
        opaddr = kwargs['opaddr']
        rv = 0
        if self.F_OVERFLOW == 0:
            rv = 2 if ((opaddr&0xFF00)!=(addr&0xFF00)) else 1
            self.REG_PC = addr
        return rv
    
    def do_BVS(self, **kwargs):
        """
        Branch on overflow set
        Return: cycles to be added after this operation
        """
        
        addr = kwargs['addr']
        opaddr = kwargs['opaddr']
        rv = 0
        if self.F_OVERFLOW == 1:
            rv = 2 if ((opaddr&0xFF00)!=(addr&0xFF00)) else 1
            self.REG_PC = addr
        return rv
    
    def do_CLC(self, **kwargs):
        """
        Clear carry flag
        Return: cycles to be added after this operation
        """
        self.F_CARRY = 0
        return 0
        
    def do_CLD(self, **kwargs):
        """
        Clear decimal flag
        Return: cycles to be added after this operation
        """
        self.F_DECIMAL = 0
        return 0
    
    
    def do_CLI(self, **kwargs):
        """
        Clear interrupt flag
        Return: cycles to be added after this operation
        """
        self.F_INTERRUPT = 0
        return 0
    
    def do_CLV(self, **kwargs):
        """
        Clear overflow flag
        Return: cycles to be added after this operation
        """
        self.F_OVERFLOW = 0
        return 0
    
    def do_CMP(self, **kwargs):
        """
        Compare memory and accumulator
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        cycleAdd = kwargs['cycleAdd']
        
        temp = self.REG_ACC - self._load(addr)
        self.F_CARRY = 1 if(temp>=0) else 0
        self.F_SIGN = (temp>>7)&1
        self.F_ZERO = temp&0xFF
        
        return cycleAdd
    
    def do_CPX(self, **kwargs):
        """
        Compare memory and index X
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        
        temp = self.REG_X - self._load(addr)
        self.F_CARRY = 1 if(temp>=0) else 0
        self.F_SIGN = (temp>>7)&1
        self.F_ZERO = temp&0xFF
        return 0
        
    def do_CPY(self, **kwargs):
        """
        Compare memory and index Y
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        
        temp = self.REG_Y - self._load(addr)
        self.F_CARRY = 1 if(temp>=0) else 0
        self.F_SIGN = (temp>>7)&1
        self.F_ZERO = temp&0xFF
        return 0
            
    def do_DEC(self, **kwargs):
        """
        Decrement memory by one
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        
        temp = (self._load(addr)-1)&0xFF
        self.F_SIGN = (temp>>7)&1
        self.F_ZERO = temp
        self._write(addr, temp)
        return 0
    
    def do_DEX(self, **kwargs):
        """
        Decrement index X by one:
        Return: cycles to be added after this operation
        """
        self.REG_X = (self.REG_X-1)&0xFF
        self.F_SIGN = (self.REG_X>>7)&1
        self.F_ZERO = self.REG_X
        return 0
    
    def do_DEY(self, **kwargs):
        """
        Decrement index Y by one:
        Return: cycles to be added after this operation
        """
        self.REG_Y = (self.REG_Y-1)&0xFF
        self.F_SIGN = (self.REG_Y>>7)&1
        self.F_ZERO = self.REG_Y
        return 0
            
    def do_EOR(self, **kwargs):
        """
        XOR Memory with accumulator, store in accumulator
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        cycleAdd = kwargs['cycleAdd']
        
        self.REG_ACC = (self._load(addr)^self.REG_ACC)&0xFF
        self.F_SIGN = (self.REG_ACC>>7)&1
        self.F_ZERO = self.REG_ACC
        return cycleAdd
            
    def do_INC(self, **kwargs):
        """
        Increment memory by one
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        
        temp = (self._load(addr)+1)&0xFF;
        self.F_SIGN = (temp>>7)&1;
        self.F_ZERO = temp;
        self._write(addr, temp&0xFF);
        return 0
        
    def do_INX(self, **kwargs):
        """
        Increment index X by one
        Return: cycles to be added after this operation
        """
        self.REG_X = (self.REG_X+1)&0xFF
        self.F_SIGN = (self.REG_X>>7)&1
        self.F_ZERO = self.REG_X
        return 0
    
    def do_INY(self, **kwargs):
        """
        Increment index Y by one
        Return: cycles to be added after this operation
        """
        self.REG_Y = (self.REG_Y+1)&0xFF
        self.F_SIGN = (self.REG_Y>>7)&1
        self.F_ZERO = self.REG_Y
        return 0
    
    def do_JMP(self, **kwargs):
        """
        Jump to new location
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        self.REG_PC = addr -1
        return 0
    
    def do_JSR(self, **kwargs):
        """
        Jump to new location, saving return address.
        Push return address on stack.
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        self._push((self.REG_PC>>8)&0xFF)
        self._push(self.REG_PC&0xFF)
        self.REG_PC = addr-1
        return 0
    
    def do_LDA(self, **kwargs):
        """
        Load accumulator with memory
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        cycleAdd = kwargs['cycleAdd']
        
        self.REG_ACC = self._load(addr)
        self.F_SIGN = (self.REG_ACC>>7)&1
        self.F_ZERO = self.REG_ACC
        return cycleAdd
    
    def do_LDX(self, **kwargs):
        """
        Load index X with memory
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        cycleAdd = kwargs['cycleAdd']
        
        self.REG_X = self._load(addr)
        self.F_SIGN = (self.REG_X>>7)&1
        self.F_ZERO = self.REG_X
        return cycleAdd
    
    def do_LDY(self, **kwargs):
        """
        Load index Y with memory
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        cycleAdd = kwargs['cycleAdd']
        
        self.REG_Y = self._load(addr)
        self.F_SIGN = (self.REG_Y>>7)&1
        self.F_ZERO = self.REG_Y
        return cycleAdd
    
    def do_LSR(self, **kwargs):
        """
        Shift right one bit
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        addrMode = kwargs['addrMode']
        
        if addrMode == CPU.OpData.ADDR_ACC:
            temp = (self.REG_ACC & 0xFF)
            self.F_CARRY = temp&1
            temp >>= 1
            self.REG_ACC = temp
        else:
            temp = self._load(addr) & 0xFF
            self.F_CARRY = temp&1
            temp >>= 1
            self._write(addr, temp)
        
        self.F_SIGN = 0
        self.F_ZERO = temp
        return 0
    
    def do_NOP(self, **kwargs):
        """
        Return: cycles to be added after this operation
        """
        return 0
    
    def do_ORA(self, **kwargs):
        """
        OR memory with accumulator, store in accumulator.
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        addrMode = kwargs['addrMode']
        cycleAdd = kwargs['cycleAdd']
        
        temp = (self._load(addr)|self.REG_ACC)&255
        self.F_SIGN = (temp>>7)&1
        self.F_ZERO = temp
        self.REG_ACC = temp
        if not addrMode == CPU.OpData.ADDR_POSTIDXIND:
            return cycleAdd
        return 0
    
    def do_PHA(self, **kwargs):
        """
        Push accumulator on stack
        Return: cycles to be added after this operation
        """
        self._push(self.REG_ACC)
        return 0
    
    def do_PHP(self, **kwargs):
        """
        Push processor status on stack
        Return: cycles to be added after this operation
        """
        self.F_BRK = 1
        self._push(
                    (self.F_CARRY)| \
                    (( 1 if (self.F_ZERO==0) else 0)<<1)| \
                    (self.F_INTERRUPT<<2)| \
                    (self.F_DECIMAL<<3)| \
                    (self.F_BRK<<4)| \
                    (self.F_NOTUSED<<5)| \
                    (self.F_OVERFLOW<<6)| \
                    (self.F_SIGN<<7)
                )
        return 0
    
    def do_PLA(self, **kwargs):
        """
        Pull accumulator from stack
        Return: cycles to be added after this operation
        """
        self.REG_ACC = self._pull()
        self.F_SIGN = (self.REG_ACC>>7)&1
        self.F_ZERO = self.REG_ACC
        return 0
    
    def do_PLP(self, **kwargs):
        """
        Pull processor status from stack
        Return: cycles to be added after this operation
        """
        temp = self._pull()
        self.F_CARRY     = (temp   )&1
        self.F_ZERO      = 0 if (((temp>>1)&1)==1) else 1
        self.F_INTERRUPT = (temp>>2)&1
        self.F_DECIMAL   = (temp>>3)&1
        self.F_BRK       = (temp>>4)&1
        self.F_NOTUSED   = (temp>>5)&1
        self.F_OVERFLOW  = (temp>>6)&1
        self.F_SIGN      = (temp>>7)&1

        self.F_NOTUSED = 1
        return 0
    
    def do_ROL(self, **kwargs):
        """
        Rotate one bit left
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        addrMode = kwargs['addrMode']
        
        if addrMode == CPU.OpData.ADDR_ACC:
            temp = self.REG_ACC
            add = self.F_CARRY
            self.F_CARRY = (temp>>7)&1
            temp = ((temp<<1)&0xFF)+add
            self.REG_ACC = temp
        else:
            temp = self._load(addr)
            add = self.F_CARRY
            self.F_CARRY = (temp>>7)&1
            temp = ((temp<<1)&0xFF)+add    
            self._write(addr, temp)

        self.F_SIGN = (temp>>7)&1
        self.F_ZERO = temp
        return 0
    
    
    def do_ROR(self, **kwargs):
        """
        Rotate one bit right
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        addrMode = kwargs['addrMode']
        
        if addrMode == CPU.OpData.ADDR_ACC:
            add = self.F_CARRY<<7
            self.F_CARRY = self.REG_ACC&1
            temp = (self.REG_ACC>>1)+add   
            self.REG_ACC = temp
        else:
            temp = self._load(addr)
            add = self.F_CARRY << 7
            self.F_CARRY = temp&1
            temp = (temp>>1)+add    
            self._write(addr, temp)

        self.F_SIGN = (temp>>7)&1
        self.F_ZERO = temp
        return 0
    
    def do_RTI(self, **kwargs):
        """
        Return from interrupt. Pull status and PC from stack
        Return: cycles to be added after this operation
        """
        temp = self._pull()
        self.F_CARRY     = (temp   )&1
        self.F_ZERO      = 1 if ((temp>>1)&1)==0 else 0
        self.F_INTERRUPT = (temp>>2)&1
        self.F_DECIMAL   = (temp>>3)&1
        self.F_BRK       = (temp>>4)&1
        self.F_NOTUSED   = (temp>>5)&1
        self.F_OVERFLOW  = (temp>>6)&1
        self.F_SIGN      = (temp>>7)&1

        self.REG_PC = self._pull()
        self.REG_PC += (self._pull()<<8)
        if self.REG_PC==0xFFFF:
            return 0

        self.REG_PC -= 1
        self.F_NOTUSED = 1
        return 0
        
    def do_RTS(self, **kwargs):
        """
        Return from subroutine. Pull PC from stack
        Return: cycles to be added after this operation
        """
        self.REG_PC = self._pull()
        self.REG_PC += (self._pull()<<8)
        
        #if self.REG_PC==0xFFFF:
        #    return 0 # return from NSF play routine:
        return 0
    
    def do_SBC(self, **kwargs):
        """
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        cycleAdd = kwargs['cycleAdd']
        addrMode = kwargs['addrMode']
        
        temp = self.REG_ACC-self._load(addr)-(1-self.F_CARRY)
        self.F_SIGN = (temp>>7)&1
        self.F_ZERO = temp&0xFF
        self.F_OVERFLOW = 1 if (((self.REG_ACC^temp)&0x80)!=0 and ((self.REG_ACC^self._load(addr))&0x80)!=0) else 0
        self.F_CARRY = 0 if (temp<0) else 1
        self.REG_ACC = (temp&0xFF)
        if not (addrMode == CPU.OpData.ADDR_POSTIDXIND):
            return cycleAdd
        return 0
        
    def do_SEC(self, **kwargs):
        """
        Set carry flag
        Return: cycles to be added after this operation
        """
        self.F_CARRY = 1
        return 0
    
    def do_SED(self, **kwargs):
        """
        Set decimal flag
        Return: cycles to be added after this operation
        """
        self.F_DECIMAL = 1
        return 0
    
    def do_SEI(self, **kwargs):
        """
        Set interrupt flag
        Return: cycles to be added after this operation
        """
        self.F_INTERRUPT = 1
        return 0
    
    def do_STA(self, **kwargs):
        """
        Store accumulator in memory
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        self._write(addr, self.REG_ACC)
        return 0
    
    def do_STX(self, **kwargs):
        """
        Store index X in memory
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        self._write(addr, self.REG_X)
        return 0
    
    def do_STY(self, **kwargs):
        """
        Store index Y in memory
        Return: cycles to be added after this operation
        """
        addr = kwargs['addr']
        self._write(addr, self.REG_Y)
        return 0
    
    def do_TAX(self, **kwargs):
        """
        Transfer accumulator to index X
        Return: cycles to be added after this operation
        """
        self.REG_X = self.REG_ACC
        self.F_SIGN = (self.REG_ACC>>7)&1
        self.F_ZERO = self.REG_ACC
        return 0
    
    def do_TAY(self, **kwargs):
        """
        Transfer accumulator to index Y
        Return: cycles to be added after this operation
        """
        self.REG_Y = self.REG_ACC
        self.F_SIGN = (self.REG_ACC>>7)&1
        self.F_ZERO = self.REG_ACC
        return 0
    
    def do_TSX(self, **kwargs):
        """
        Transfer stack pointer to index X:
        Return: cycles to be added after this operation
        """
        self.REG_X = (self.REG_SP-0x0100)
        self.F_SIGN = (self.REG_SP>>7)&1
        self.F_ZERO = self.REG_X
        return 0
    
    def do_TXA(self, **kwargs):
        """
        Transfer index X to accumulator:
        Return: cycles to be added after this operation
        """
        self.REG_ACC = self.REG_X
        self.F_SIGN = (self.REG_X>>7)&1
        self.F_ZERO = self.REG_X
        return 0
                    
    def do_TXS(self, **kwargs):
        """
        Transfer index X to stack pointer:
        Return: cycles to be added after this operation
        """
        self.REG_SP = (self.REG_X+0x0100)
        self._stackWrap()
        return 0
    
    def do_TYA(self, **kwargs):
        """
        Transfer index Y to accumulator:
        Return: cycles to be added after this operation
        """
        self.REG_ACC = self.REG_Y
        self.F_SIGN = (self.REG_Y>>7)&1
        self.F_ZERO = self.REG_Y
        return 0

    #def_do_DUMMY(self, **kwargs):

    def reset(self):
        self.cmdCount = 0
        self.mem = None
        self.mem = bytearray('\x00' * 0x10000)
        self.mem[:0x2000] = '\xFF' * 0x2000
        for p in range(4):
            offset = p * 0x800
            self.mem[offset + 0x008] = '\xF7'
            self.mem[offset + 0x009] = '\xEF'
            self.mem[offset + 0x00A] = '\xDF'
            self.mem[offset + 0x00F] = '\xBF'

        # CPU Registers
        self.REG_ACC = 0
        self.REG_X = 0
        self.REG_Y = 0
        # Stack Pointer
        self.REG_SP = 0x01FF
        # Program Counter
        self.REG_PC = 0x8000-1
        self.REG_PC_NEW = 0x8000-1
        # Status Register
        self.REG_STATUS = 0x28
        self.setStatus(0x28)
        
        # Flags
        self.F_CARRY = 0
        self.F_DECIMAL = 0
        self.F_INTERRUPT = 1
        self.F_INTERRUPT_NEW = 1
        self.F_OVERFLOW = 0
        self.F_SIGN = 0
        self.F_ZERO = 1
        self.F_NOTUSED = 1
        self.F_NOTUSED_NEW = 1
        self.F_BRK = 1
        self.F_BRK_NEW = 1
        self.palCnt = 0
        self.palEmu = False
        self.opdata = CPU.OpData().opdata
        self.cyclesToHalt = 0
        
        # Reset crash flag
        self.crash = False
        
        # Interrupts
        self.irqRequested = False
        self.irqType = None
    
    def emulate(self):
        temp = 0

        if self.irqRequested:
            temp = (self.F_CARRY)| \
                ((1 if (self.F_ZERO==0) else 0)<<1)| \
                (self.F_INTERRUPT<<2)| \
                (self.F_DECIMAL<<3)| \
                (self.F_BRK<<4)| \
                (self.F_NOTUSED<<5)| \
                (self.F_OVERFLOW<<6)| \
                (self.F_SIGN<<7)
            self.REG_PC_NEW = self.REG_PC
            self.F_INTERRUPT_NEW = self.F_INTERRUPT
            
            if self.irqType == CPU.IRQ_NORMAL:
                if self.F_INTERRUPT == 0:
                   self._doIrq(temp)
            elif self.irqType == CPU.IRQ_NMI:
                self._doNonMaskableInterrupt(temp)
            elif self.irqType == CPU.IRQ_RESET:
                self._doResetInterrupt()
                
            self.REG_PC = self.REG_PC_NEW
            self.F_INTERRUPT = self.F_INTERRUPT_NEW
            self.F_BRK = self.F_BRK_NEW
            self.irqRequested = False
        
        opinf = self.opdata[self.nes.mmap.load(self.REG_PC+1)]
        cycleCount = (opinf>>24)
        cycleAdd = 0
        
        # Find addr mode
        addrMode = (opinf>>8) & 0xFF
        
        # Increase PC by number of op bytes
        opaddr = self.REG_PC
        self.REG_PC += ((opinf>>16) & 0xFF)
        
        addr = 0
        #switch addrMode
        addr, cycleAdd = self.onAddrMode[addrMode](opaddr)
        
        #if addrMode == CPU.OpData.ADDR_ZP:
        #    # 0. Zero Page mode. Use the address given after the opcode, 
        #    # but without high byte.
        #    addr = self._load(opaddr+2)
        #elif addrMode == CPU.OpData.ADDR_REL:
        #    # 1. Relative mode
        #    addr = self._load(opaddr+2)
        #    if addr<0x80:
        #        addr += self.REG_PC
        #    else:
        #        addr += self.REG_PC-256
        #elif addrMode == CPU.OpData.ADDR_ABS:
        #    # 3. Absolute mode. Use the two bytes following the opcode as 
        #    # an address.
        #    addr = self._load16bit(opaddr+2)
        #elif addrMode == CPU.OpData.ADDR_ACC:
        #    # 4. Accumulator mode. The address is in the accumulator 
        #    # register.
        #    addr = self.REG_ACC
        #elif addrMode == CPU.OpData.ADDR_IMM:
        #    # 5. Immediate mode. The value is given after the opcode.
        #    addr = self.REG_PC
        #elif addrMode == CPU.OpData.ADDR_ZPX:
        #    # 6. Zero Page Indexed mode, X as index. Use the address given 
        #    # after the opcode, then add the
        #    # X register to it to get the final address.
        #    addr = (self._load(opaddr+2)+self.REG_X)&0xFF
        #elif addrMode == CPU.OpData.ADDR_ZPY:
        #    # 7. Zero Page Indexed mode, Y as index. Use the address given 
        #    # after the opcode, then add the
        #    # Y register to it to get the final address.
        #    addr = (self._load(opaddr+2)+self.REG_Y)&0xFF
        #elif addrMode == CPU.OpData.ADDR_ABSX:
        #    # 8. Absolute Indexed Mode, X as index. Same as zero page 
        #    # indexed, but with the high byte.
        #    addr = self._load16bit(opaddr+2)
        #    if((addr&0xFF00)!=((addr+self.REG_X)&0xFF00)):
        #        cycleAdd = 1
        #    addr += self.REG_X
        #elif addrMode == CPU.OpData.ADDR_ABSY:
        #    # 9. Absolute Indexed Mode, Y as index. Same as zero page 
        #    # indexed, but with the high byte.
        #    addr = self._load16bit(opaddr+2)
        #    if((addr&0xFF00)!=((addr+self.REG_Y)&0xFF00)):
        #        cycleAdd = 1
        #    addr += self.REG_Y
        #elif addrMode == CPU.OpData.ADDR_PREIDXIND:
        #    # 10. Pre-indexed Indirect mode. Find the 16-bit address 
        #    # starting at the given location plus
        #    # the current X register. The value is the contents of that 
        #    # address.
        #    addr = self._load(opaddr+2)
        #    if((addr&0xFF00)!=((addr+self.REG_X)&0xFF00)):
        #        cycleAdd = 1
        #    addr += self.REG_X
        #    addr &= 0xFF
        #    addr = self._load16bit(addr)
        #elif addrMode == CPU.OpData.ADDR_POSTIDXIND:
        #    # 11. Post-indexed Indirect mode. Find the 16-bit address 
        #    # contained in the given location
        #    # (and the one following). Add to that address the contents 
        #    # of the Y register. Fetch the value
        #    # stored at that adress.
        #    addr = self._load16bit(self._load(opaddr+2))
        #    if((addr&0xFF00)!=((addr+self.REG_Y)&0xFF00)):
        #        cycleAdd = 1
        #    addr += self.REG_Y
        #elif addrMode == CPU.OpData.ADDR_INDABS:
        #    # 12. Indirect Absolute mode. Find the 16-bit address contained 
        #    # at the given location.
        #    addr = self._load16bit(opaddr+2); # Find op
        #    if addr < 0x1FFF:
        #        addr = self.mem[addr] + (self.mem[(addr & 0xFF00) | (((addr & 0xFF) + 1) & 0xFF)] << 8) # Read from address given in op
        #    else:
        #        addr = self.nes.mmap._load(addr) + (self.nes.mmap._load((addr & 0xFF00) | (((addr & 0xFF) + 1) & 0xFF)) << 8)

        addr &= 0xFFFF
        # ----------------------------------------------------------------------------------------------------
        # Decode & execute instruction:
        # ----------------------------------------------------------------------------------------------------

        # Jump table
        self.cmdCount += 1
        if (self.cmdCount % 10000 == 0):
            print "Cmd({0}): {1}".format(self.cmdCount, opinf&0xFF)
        #cmd = CPU.OpData.instname[opinf&0xFF]
        #cycleCount += self.callOp(cmd)(addr=addr, addrMode=addrMode, cycleAdd=cycleAdd, opaddr=opaddr)
        cycleCount += self.inst[opinf&0xFF](addr=addr, addrMode=addrMode, cycleAdd=cycleAdd, opaddr=opaddr)
        
        if self.palEmu:
            self.palCnt+=1
            if self.palCnt == 5:
                self.palCnt = 0
                cycleCount += 1
        
        self.nes.ppu.cycles = cycleCount * 3
        self.nes.ppu.emulateCycles()
        #if self.nes.opts.emulateSound:
        #    pass #TODO Sound emu
        
        return cycleCount
        
    def _load(self, addr):
        if addr < 0x2000:
            return self.mem[addr&0x7FF]
        else:
            return self.nes.mmap.load(addr)
    
    def _load16bit(self, addr):
        if addr < 0x1FFF:
            return (self.mem[addr&0x7FF] | (self.mem[(addr+1)&0x7FF] << 8))
        else:
            return (self.nes.mmap.load(addr) | (self.nes.mmap.load(addr+1) << 8))
    
    def _write(self, addr, val):
        if addr < 0x2000:
            self.mem[addr & 0x7FF] = val
        else:
            self.nes.mmap.write(addr, val)
    
    def requestIrq(self, type):
        if self.irqRequested:
            if type == CPU.IRQ_NORMAL:
                return
        
        self.irqRequested = True
        self.irqType = type
    
    def _push(self, value):
        self.nes.mmap.write(self.REG_SP, value)
        self.REG_SP -= 1
        self.REG_SP = 0x0100 | (self.REG_SP&0xFF)
        
    def _stackWrap(self):
        self.REG_SP = 0x0100 | (self.REG_SP&0xFF)
    
    def _pull(self):
        self.REG_SP += 1
        self.REG_SP = 0x0100 | (self.REG_SP&0xFF)
        return self.nes.mmap.load(self.REG_SP)
    
    def pageCrossed(self, addr1, addr2):
        return ((addr1&0xFF00) != (addr2&0xFF00))
    
    def haltCycles(self, cycles):
        self.cyclesToHalt += cycles

    def _doNonMaskableInterrupt(self, status):
        if((self.nes.mmap.load(0x2000) & 128) != 0): # Check whether VBlank Interrupts are enabled

            self.REG_PC_NEW += 1
            self._push((self.REG_PC_NEW>>8)&0xFF)
            self._push(self.REG_PC_NEW&0xFF)
            #self.F_INTERRUPT_NEW = 1
            self._push(status)

            self.REG_PC_NEW = self.nes.mmap.load(0xFFFA) | (self.nes.mmap.load(0xFFFB) << 8)
            self.REG_PC_NEW -= 1
    
    def _doResetInterrupt(self):
        self.REG_PC_NEW = self.nes.mmap.load(0xFFFC) | (self.nes.mmap.load(0xFFFD) << 8)
        self.REG_PC_NEW -= 1
    
    def _doIrq(self, status):
        self.REG_PC_NEW += 1
        self._push((self.REG_PC_NEW>>8)&0xFF)
        self._push(self.REG_PC_NEW&0xFF)
        self._push(status)
        self.F_INTERRUPT_NEW = 1
        self.F_BRK_NEW = 0

        self.REG_PC_NEW = self.nes.mmap.load(0xFFFE) | (self.nes.mmap.load(0xFFFF) << 8)
        self.REG_PC_NEW -= 1
        
    def getStatus(self):
        return (self.F_CARRY)\
                |(self.F_ZERO<<1)\
                |(self.F_INTERRUPT<<2)\
                |(self.F_DECIMAL<<3)\
                |(self.F_BRK<<4)\
                |(self.F_NOTUSED<<5)\
                |(self.F_OVERFLOW<<6)\
                |(self.F_SIGN<<7)
        
    def setStatus(self,st):
        self.F_CARRY     = (st   )&1
        self.F_ZERO      = (st>>1)&1
        self.F_INTERRUPT = (st>>2)&1
        self.F_DECIMAL   = (st>>3)&1
        self.F_BRK       = (st>>4)&1
        self.F_NOTUSED   = (st>>5)&1
        self.F_OVERFLOW  = (st>>6)&1
        self.F_SIGN      = (st>>7)&1
