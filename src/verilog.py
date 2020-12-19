class Base(object):
  def __init__(self):
    self.author = ""
    self.date = ""
    self.name = ""
    self.type = ""
    self.ports = {}
    self.port_number = 0
    self.parameters = {}
    self.parameter_number = 0
    self.wires = {}
    self.wire_number = 0
    self.regs = {}
    self.reg_number = 0

  def read_from_file(self, filename):
    pass
  
  def write_to_file(self, filename):
    with open(filename, "w") as fout:


class Module(object):
  def __init__(self):
    super().__init__()
  
  def read_from_file(self, filename):
    with open(filename, "r") as fin:
      pass

class Test(Base):
  def __init__(self):
    super().__init__()


class Function(Base):
  def __init__(self):
    super().__init__()