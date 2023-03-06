// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@SCREEN
D=A

@CURRENT_POSITION
M=D

(KEYBOARD_CHECK)
@KBD
D=M
@WRITE_BLACK
D;JGT

@WRITE_WHITE
0;JMP

(WRITE_BLACK)
@24576 //16384 + ((512 * 256)/16) end of screen
D=M
@CURRENT_POSITION
D=D-M
@KEYBOARD_CHECK
D;JEQ

@CURRENT_POSITION
A=M
M=-1

@CURRENT_POSITION
D=M+1
@CURRENT_POSITION
M=D

@KEYBOARD_CHECK
0;JMP




(WRITE_WHITE)
@SCREEN
D=A-1

@CURRENT_POSITION
D=D-M
@KEYBOARD_CHECK
D;JEQ

@CURRENT_POSITION
A=M
M=0

@CURRENT_POSITION
D=M-1
@CURRENT_POSITION
M=D

@KEYBOARD_CHECK
0;JMP


@SCREEN
D=M
@Position //initial position to -1, if to 0 there will be a bug when whiten the screen
M=D

@KEYBOARD_CHECK
0;JMP



