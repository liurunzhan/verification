import xml.sax

class Field(object):
  def __init__(self):
    self.derivedFrom = None
    self.name = ""
    self.description = ""
    self.bitRange = []
    self.access = ""
    self.modifiedWriteValues = None
    self.readAction = None

class FieldDim(Field):
  def __init__(self):
    super().__init__()
    self.dim = 0
    self.dimIncrement = 0
    self.dimIndex = []
    self.dimArrayIndex = []

class Register(object):
  def __init__(self):
    self.derivedFrom = None
    self.name = ""
    self.description = ""
    self.addressOffset = 0
    self.size = 0
    self.access = ""
    self.protection = None
    self.resetValue = None
    self.resetMask = None
    self.fields = []

class RegisterDim(Register):
  def __init__(self):
    super().__init__()
    self.dim = None
    self.dimIncrement = 0
    self.dimIndex = []
    self.dimArrayIndex = []