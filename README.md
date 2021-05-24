# Hack Machine Language Assembler

HackAssembler is an Assembler program that translates programs written in the symbolic Hack assembly language into binary code.

This was done as part of course [nand2tetris](http://www.nand2tetris.org), Specifically [project 06](https://www.nand2tetris.org/project06).

## Resources

This program was written in reference to the [Chapter 6](https://b1391bd6-da3d-477d-8c01-38cdf774495a.filesusr.com/ugd/44046b_b73759b866b249a0b3a715bf5a18f668.pdf) of book [The Elements of Computing Systems](https://www.amazon.com/Elements-Computing-Systems-Building-Principles/dp/0262640686/ref=ed_oe_p), By [Noam Nisan](http://www.cs.huji.ac.il/~noam/) and [Shimon Schocken](http://www.shimonschocken.com/) .MIT Press

## Usage

For running the gui
```
$ python src/gui.py
```
Then select the file needed and click 'Run' to convert into binary.

For using just the command line
```
$ python src/assembler.py <file_path>
```

> Note: .hack file is generated in the same directory as the input file. 



