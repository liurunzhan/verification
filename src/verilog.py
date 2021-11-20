import os
import time
from enum import Enum

class ObjectType(object):
  def __init__(self, name, value):
    self.name = name
    self.value = value

class Parameter(ObjectType):
  def __init__(self, name, value):
    super().__init__(name, value)

class Port(ObjectType):
  def __init__(self, type, name, width, value):
    super().__init__(name, value)
    self.type = type
    self.width = width

class Wire(ObjectType):
  def __init__(self, name, width, value):
    super().__init__(name, value)
    self.width = width

class Reg(ObjectType):
  def __init__(self, name, width, value):
    super().__init__(name, value)
    self.width = width

class BlockType(object):
  def __init__(self, name, type, ports, parameters, wires, regs, author="", date=""):
    self.author = author
    self.date = date if date != "" else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    self.name = name if name != "" else os.getlogin()
    self.type = type
    self.ports = ports
    self.parameters = parameters
    self.wires = wires
    self.regs = regs

  def read_from_file(self, filename):
    pass
  
  def write_to_file(self, filename):
    pass
		#with open(filename, "w") as fout:
			#pass

class Module(BlockType):
  def __init__(self, author="", date="", name="", type="", ports={}, parameters={}, wires={}, regs={}):
    super().__init__(author, date, name, type, ports, parameters, wires, regs)
  
  def read_from_file(self, filename):
    with open(filename, "r") as fin:
      pass

class Class(BlockType):
  def __init__(self):
    super().__init__()

class Test(BlockType):
  def __init__(self):
    super().__init__()


class Function(BlockType):
  def __init__(self):
    super().__init__()

class Interface(BlockType):
  def __init__(self):
    super().__init__()

class VerilogState(Enum):
	IDLE = 0 # Initial state
	VARIABLE = 1 # Variable name, starts from _, a-z, A-Z
	NUMBER = 2
	NUMBER_INTEGER = 200 # Number integer, starts from 0-9 and ends with 0-9
	NUMBER_INTEGER_BIN = 201 # Bibary
	NUMBER_INTEGER_OCT = 202 # Octal
	NUMBER_INTEGER_DEC = 203 # Decimal
	NUMBER_INTEGER_HEX = 204
	NUMBER_FLOAT = 210 # Float point number, starts from 0-9 and ends with 0-9
	STRING = 4 # String, starts from " and ends with "
	DOCUMENT = 5
	DOCUMENT_S = 51 # Single Document, starts from \\ and ends with "\n"
	DOCUMENT_D = 52 # Double Document, starts from \* and ends with *\
	MACRO = 6 # Macro, starts from `
	OPERATOR = 7
	ERROR = 10000


def verilog_parser(line):
	state = VerilogState.IDLE
	for i in range(len(line)):
		c = line[i]
		c_pre = line[i-1] if i > 0 else ""
		c_next = line[i+1] if i+1 < len(line) else ""
		if state == VerilogState.IDLE:
			if c == "_" or c.isalpha():
				state = VerilogState.VARIABLE
			elif c.isnumeric():
				state = VerilogState.NUMBER
			elif c == "'":
				state = VerilogState.NUMBER_INTEGER
			elif c == "\"":
				state = VerilogState.STRING
			elif c == "\\":
				if c_next == "\\":
					state = VerilogState.DOCUMENT_S
				elif c_next == "*":
					state = VerilogState.DOCUMENT_D
				else:
					state = VerilogState.OPERATOR
			elif c == "`":
				state = VerilogState.MACRO
			else:
				state = VerilogState.IDLE
		elif state == VerilogState.VARIABLE:
			if c == "_" or c.isalnum():
				state = VerilogState.VARIABLE
			elif c == " " or c == "\t" or c == "\r":
				state = VerilogState.IDLE
			else:
				state = VerilogState.OPERATOR
		elif state == VerilogState.NUMBER:
			if c == ".":
				state = VerilogState.NUMBER_FLOAT
			elif c == "'":
				state = VerilogState.NUMBER_INTEGER
			elif c.isnumeric():
				state = VerilogState.NUMBER
			elif c == "_":
				state = VerilogState.NUMBER if c_next.isnumeric() else VerilogState.ERROR
			elif c == " " or c == "\t" or c == "\r":
				state = VerilogState.IDLE
			elif c.isalpha():
				state = VerilogState.ERROR
			else:
				state = VerilogState.OPERATOR
		elif state == VerilogState.NUMBER_FLOAT:
			if c.isnumeric():
				state = VerilogState.NUMBER_FLOAT
			elif  c == "_":
				state = VerilogState.NUMBER if c_next.isnumeric() else VerilogState.ERROR
			elif c == " " or c == "\t" or c == "\r":
				state = VerilogState.IDLE
			elif c.isalpha() or c == ".":
				state = VerilogState.ERROR
			else:
				state = VerilogState.OPERATOR
		elif state == VerilogState.STRING:
			if c == "\"":
				state = VerilogState.IDLE
		elif state == VerilogState.DOCUMENT_S:
			if c == "\n":
				state = VerilogState.IDLE
		elif state == VerilogState.DOCUMENT_D:
			if c == "*" and c_next == "\\":
				state = VerilogState.IDLE
		elif state == VerilogState.NUMBER_INTEGER:
			if c == "b" or c == "B":
				state = VerilogState.NUMBER_INTEGER_BIN
			elif c == "d" or c == "D":
				state = VerilogState.NUMBER_INTEGER_DEC
			elif c == "o" or c == "O":
				state = VerilogState.NUMBER_INTEGER_OCT
			elif c == "h" or c == "H":
				state = VerilogState.NUMBER_INTEGER_HEX
			else:
				state = VerilogState.ERROR
		elif state == VerilogState.NUMBER_INTEGER_BIN:
			if c == "0" or c == "1":
				state = VerilogState.NUMBER_INTEGER_BIN
			elif c == "_":
				state = VerilogState.NUMBER_INTEGER_BIN if (c_next == "0" or c_next == "1") else VerilogState.ERROR
			elif c == " " or c == "\t" or c == "\r":
				state = VerilogState.IDLE
			elif c.isalpha():
				state = VerilogState.ERROR
			else:
				state = VerilogState.OPERATOR
		elif state == VerilogState.NUMBER_INTEGER_OCT:
			if c >= "0" or c <= "7":
				state = VerilogState.NUMBER_INTEGER_OCT
			elif c == "_":
				state = VerilogState.NUMBER_INTEGER_OCT if (c_next >= "0" or c_next <= "7") else VerilogState.ERROR
			elif c == " " or c == "\t" or c == "\r":
				state = VerilogState.IDLE
			elif c.isalpha():
				state = VerilogState.ERROR
			else:
				state = VerilogState.OPERATOR
		elif state == VerilogState.NUMBER_INTEGER_DEC:
			if c.isnumeric():
				state = VerilogState.NUMBER_INTEGER_DEC
			elif c == "_":
				state = VerilogState.NUMBER_INTEGER_DEC if c_next.isnumeric() else VerilogState.ERROR
			elif c == " " or c == "\t" or c == "\r":
				state = VerilogState.IDLE
			elif c.isalpha():
				state = VerilogState.ERROR
			else:
				state = VerilogState.OPERATOR
		elif state == VerilogState.NUMBER_INTEGER_HEX:
			if c.isnumeric() or (c >= "a" and c <= "f") or (c >= "A" and c <= "F"):
				state = VerilogState.NUMBER_INTEGER_HEX
			elif c == "_":
				state = VerilogState.NUMBER_INTEGER_HEX if (c_next.isnumeric() or (c_next >= "a" and c_next <= "f") or (c_next >= "A" and c_next <= "F")) else VerilogState.ERROR
			elif c == " " or c == "\t" or c == "\r":
				state = VerilogState.IDLE
			elif c.isalpha():
				state = VerilogState.ERROR
			else:
				state = VerilogState.OPERATOR
		elif state == VerilogState.MACRO:
			if c == "_" or c.isalnum():
				state = VerilogState.MACRO
			elif c == " " or c == "\t" or c == "\r":
				state = VerilogState.IDLE
			else:
				state = VerilogState.OPERATOR
		elif state == VerilogState.OPERATOR:
			if c == "_" or c.isalpha():
				state = VerilogState.VARIABLE
			elif c.isnumeric():
				state = VerilogState.NUMBER
			elif c == "'":
				state = VerilogState.NUMBER_INTEGER
			elif c == " " or c == "\t" or c == "\r":
				state = VerilogState.IDLE
			else:
				state = VerilogState.OPERATOR
		elif state == VerilogState.ERROR:
			break
		print("%s:%s" % (c, state))

# judge whether a sub-string matches a Verilog-type name or not
name_rule = {"_", ".", "[", "]"}

def match_verilog_name_rule(name, start):
  matched = True
  if not name[start].isalpha() and name[start] != "_":
    if name[start].isdigit():
      matched = False
    elif name[start] != "`":
      return False, 1
  length = 1
  bracket_flag = False
  for i in range(start+1, len(name)):
    if name[i].isalnum() or name[i] in name_rule or bracket_flag:
      length += 1
      if name[i] == "[":
        bracket_flag = True
      elif name[i] == "]":
        bracket_flag = False
    else:
      break
  return matched, length

# return a list of Verilog-type signals with their positions in a statement
def get_signals_from_statement(statement):
  signals = []
  i = 0
  while i < len(statement):
    matched, length = match_verilog_name_rule(statement, i)
    if matched:
      signals.append({statement[i:(i+length)] : i})
    i += length
  return signals

if __name__ == "__main__":
  statement = "`TOP.hclk.hclk&hclk&pclk[`TOP.width*8:0]+data[(`TOP.width*8)+1:0]"
  verilog_parser(statement)