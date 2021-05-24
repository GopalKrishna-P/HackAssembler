import sys
from parser import *
from code import *
from symboltable import *

class assembler():
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_file = self._outfile()
        self.symbol_addr = 1
        self.symbols = symbolTable()

    def _outfile(self):
        if self.input_file.endswith( '.asm' ):
            return self.input_file.replace( '.asm', '.hack' )
        else:
            return self.input_file + '.hack'

    def primary_pass(self):
        file_parser = parser(self.input_file)
        cur_address = 0
        while file_parser.has_more_commands():
            file_parser.advance()
            cmd = file_parser.command_type()
            if cmd == file_parser.A_COMMAND or cmd == file_parser.C_COMMAND:
                cur_address += 1
            elif cmd == file_parser.L_COMMAND:
                self.symbols.add_entry( file_parser.symbol(), cur_address )

    def secondary_pass(self):
        file_parser = parser(self.input_file)
        hackfile = open( self.output_file, 'w' )
        code_gen = code()
        while file_parser.has_more_commands():
            file_parser.advance()
            cmd = file_parser.command_type()
            if cmd == file_parser.A_COMMAND:
                hackfile.write( code_gen.gen_a(self._get_address(file_parser.symbol())) + '\n' )
            elif cmd == file_parser.C_COMMAND:
                hackfile.write( code_gen.gen_c(file_parser.dest(), file_parser.comp(), file_parser.jmp()) + '\n' )
            elif cmd == file_parser.L_COMMAND:
                pass
        hackfile.close()

    def _get_address(self, symbol):
        if symbol.isdigit():
            return symbol
        else:
            if not self.symbols.contains(symbol):
                self.symbols.add_entry(symbol, self.symbol_addr)
                self.symbol_addr += 1
            return self.symbols.get_address(symbol)

    def assemble(self):
        self.primary_pass()
        self.secondary_pass()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python Assembler.py Program.asm")
    else:
        asm_file = sys.argv[1]

    hack_assembler = assembler(asm_file)
    hack_assembler.assemble()
