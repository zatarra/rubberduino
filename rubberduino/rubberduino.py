# coding=utf-8
import json
import sys
import os
from optparse import OptionParser

''' 
Simple Rubber Ducky script converter by David Gouveia <david.gouveia [_at_] gmail.com
This script contains a a custom symbol mappings that should work ok for PT keyboard. Feel free to create your own and replace the "symbol_ids" accordingly.
'''

class RubberDuino(object):
  ''' DEFAULT DELAY IS SET TO 200 '''
  DEFAULT_DELAY = "200"

  functions = ['ALT', 'GUI', 'CTRL', 'CONTROL', 'SHIFT', 'WINDOWS', 'COMMAND', 'MENU', 'ESC', 'ESCAPE', 'END', 'SPACE', 'TAB', 'PRINTSCREEN', 'ENTER', 'UPARROW', 'UP', 'DOWNARROW', 'DOWN', 'LEFTARROW', 'LEFT', 'RIGHTARROW', 'RIGHT', 'CAPSLOCK', 'DELETE', 'DEL', "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12" ]

  mappings = ['KEY_LEFT_ALT', 'KEY_LEFT_GUI', 'KEY_LEFT_CTRL', 'KEY_LEFT_CTRL', 'KEY_LEFT_SHIFT', 'KEY_LEFT_GUI', 'KEY_LEFT_GUI', '229', 'KEY_ESC', 'KEY_ESC', 'KEY_END', '\' \'', 'KEY_TAB', '206', 'KEY_RETURN', 'KEY_UP_ARROW', 'KEY_UP_ARROW', 'KEY_DOWN_ARROW', 'KEY_DOWN_ARROW', 'KEY_LEFT_ARROW', 'KEY_LEFT_ARROW', 'KEY_RIGHT_ARROW', 'KEY_RIGHT_ARROW', 'KEY_CAPS_LOCK', 'KEY_DELETE', 'KEY_DELETE', "KEY_F1", "KEY_F2", "KEY_F3", "KEY_F4", "KEY_F5", "KEY_F6", "KEY_F7", "KEY_F8", "KEY_F9", "KEY_F10", "KEY_F11", "KEY_F12" ]

  symbol_ids = {' ':32, '!':33, '^':34, '#':35, '$':36, '%':37, '/':38, '~':39, ')':40, '=':41, '(':42, '*':43, ',':44, "'":45, '.':46, '-':47, '0':48, '1':49, '2':50, '3':51, '4':52, '5':53, '6':54, '7':55, '8':56, '9':57, '':58, 'ç':59, ';':60, '+':61, ':':62, '_':63, '"':64, 'A':65, 'B':66, 'C':67, 'D':68, 'E':69, 'F':70, 'G':71, 'H':72, 'I':73, 'J':74, 'K':75, 'L':76, 'M':77, 'N':78, 'O':79, 'P':80, 'Q':81, 'R':82, 'S':83, 'T':84, 'U':85, 'V':86, 'W':87, 'X':88, 'Y':89, 'Z':90, 'º':91,"\\":92, '´':93, '&':94, '?':95, '<':96, 'a':97, 'b':98, 'c':99, 'd':100, 'e':101, 'f':102, 'g':103, 'h':104, 'i':105, 'j':106, 'k':107, 'l':108, 'm':109, 'n':110, 'o':111, 'p':112, 'q':113, 'r':114, 's':115, 't':116, 'u':117, 'v':118, 'w':119, 'x':120, 'y':121, 'z':122, 'ª':123, '|':124, '`':125, '>':126}

  sketch = '''#include <Keyboard.h>
// Rubber ducky script converter developed by: David Gouveia <david.gouveia [_at_] gmail.com>
// https://www.davidgouveia.net

void setup(){
  Keyboard.begin();

%s
  Keyboard.end();
}

void type(int key){
  Keyboard.press(key);
  delay(50);
  Keyboard.release(key);
}

void loop(){}
'''

  def  __init__(self):
    ''' INITIALIZE FUTURE OPTIONS '''

  def convertString(self, string):
    ''' Some characters are not correctly encoded when using the print() function. '''
    output = []
    for i in list(string):
      if i in self.symbol_ids:
        output.append("Keyboard.write(" + str(self.symbol_ids[i]) + ");")
      else:
        output.append("Keyboard.write(" + str(ord(i)) + ");")

      output.append("delay(10);")
    return "\n".join(output)

  def convert(self, script):
    instructions = []
    for l in script.split("\n"):
      original = l
      l = l.strip().split()
      if l == []:
        instructions.append("");
      elif l[0] == "STRING":
        #instructions.append('Keyboard.print("' + '  ' + original.lstrip("STRING").replace("'", '"') + '");')
        instructions.append(self.convertString(original.lstrip("STRING").replace("'", '"')))
        instructions.append("delay(" + self.DEFAULT_DELAY  + ");")
      elif l[0] == "DELAY":
        instructions.append("delay(" + " ".join(l[1:]) + ");")
      elif l[0] == "REM":
        instructions.append("// " + " ".join(l[1:]))
      elif l[0] == "DEFAULT_DELAY":
        self.DEFAULT_DELAY=l[1]
      else:
        if len(l) > 1:
          for i in l:
            if i in self.functions:
              instructions.append("Keyboard.press(" + self.mappings[self.functions.index(i)] + ");")
            elif len(i) == 1:
              instructions.append("Keyboard.press(" + str(ord(i)) + ");")
            else:
              instructions.append("Keyboard.press(" + i + ");")
            instructions.append("delay(" + self.DEFAULT_DELAY  + ");")

          instructions.append("Keyboard.releaseAll();")
        else:
          if l[0] in self.functions:
            instructions.append("type(" + self.mappings[self.functions.index(l[0])] + ");")
          else:
            instructions.append("type(" + l[0] + ");")
          instructions.append("delay(" + self.DEFAULT_DELAY  + ");")
     
    return self.sketch % "\n".join(["  " + x for x in instructions])



if __name__ == "__main__":
  parser = OptionParser(usage="usage: %prog -i filename",
                        version="%prog 1.0")
  parser.add_option("-i", "--ifile",
                    dest="filename",                  
                    help="Rubber ducky script to be converted")
  parser.add_option("-o", "--outfile",
                    action="store", # optional because action defaults to "store"
                    dest="outfile",
                    default="out.c",
                    help="Output file",)
  (options, args) = parser.parse_args()

  if options.filename == None:
      parser.error("Usage: %s -i <file to convert> -o <output file>")
  else:
    filename = options.filename
    outfile = options.outfile
    print "[SYS] Loading payload: ", filename
    with open(filename, "r") as r:
      data = RubberDuino().convert(r.read())
      print "[SYS] Payload converted: %s Lines" % len(data.split("\n"))
      with open(outfile, "w") as o:
        print "[SYS] Writting to file... ", outfile
        o.write(data)
      sys.exit(0)
 