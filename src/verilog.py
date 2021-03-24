import os
import time

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
  print(get_signals_from_statement(statement))