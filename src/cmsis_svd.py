import xml.dom.minidom
import json

class Object(object):
  def __init__(self, name, description):
    self.name = name
    self.description = description

class Base(Object):
  def __init__(self, derivedFrom, name, description, 
    access, modifiedWriteValues, readAction):
    super().__init__(name, description)
    self.derivedFrom = derivedFrom
    self.access = access
    self.modifiedWriteValues = modifiedWriteValues
    self.readAction = readAction

class Field(Base):
  def __init__(self, name, description, bitRange, 
    derivedFrom=None, access="write-read", modifiedWriteValues=None, readAction=None):
    super().__init__(derivedFrom, name, description, access, modifiedWriteValues, readAction)
    self.bitRange = bitRange

class FieldDim(Field):
  def __init__(self, name, description, bitRange, 
    access="write-read", modifiedWriteValues=None, readAction=None, derivedFrom=None, 
    dim=1, dimIncrement=1, dimIndex=[], dimArrayIndex=[]):
    super().__init__(name, description, bitRange,
    derivedFrom, access, modifiedWriteValues, readAction)
    self.dim = dim
    self.dimIncrement = dimIncrement
    self.dimIndex = dimIndex
    self.dimArrayIndex = dimArrayIndex
  def FieldDim_to_Field_array(self):
    fields = []
    
    return fields

class Register(Base):
  def __init__(self, name, description, addressOffset, size, 
    derivedFrom=None, access="read-write", modifiedWriteValues=None, readAction=None,
    protection=None, resetValue=0x00000000, resetMask=0xFFFFFFFF):
    super().__init__(derivedFrom, name, description, access, modifiedWriteValues, readAction)
    self.addressOffset = addressOffset
    self.size = size
    self.protection = protection
    self.resetValue = resetValue
    self.resetMask = resetMask
    self.fields = []
  
  def add_Field(self, field):
    self.fields.append(field)

class RegisterDim(Register):
  def __init__(self, name, description, addressOffset, size, 
    derivedFrom=None, access="read-write", modifiedWriteValues=None, readAction=None,
    protection=None, resetValue=0x00000000, resetMask=0xFFFFFFFF,
    dim=1, dimIncrement=1, dimIndex=[], dimArrayIndex=[]):
    super().__init__(name, description, addressOffset, size, 
    derivedFrom, access, modifiedWriteValues, readAction,
    protection, resetValue, resetMask)
    self.dim = dim
    self.dimIncrement = dimIncrement
    self.dimIndex = dimIndex
    self.dimArrayIndex = dimArrayIndex
  def RegisterDim_to_Register_array(self):
    registers = []
    
    return registers
    

class Peripheral(Base):
  def __init__(self, derivedFrom, name, description, access, modifiedWriteValues, readAction):
    super().__init__(derivedFrom, name, description, access, modifiedWriteValues, readAction)
    self.registers = []
  def add_register(self, register):
    self.registers.append(field)

class CPU(Object):
  def __init__(self, name, revision, endian, mpuPresent, fpuPresent):
    super().__init__(name, None)
    self.revision = revision
    self.endian = endian
    self.mpuPresent = mpuPresent
    self.fpuPresent = fpuPresent
  def __str__(self):
    return " ".join([self.name, self.revision, self.endian, self.mpuPresent, self.fpuPresent])

def cpu_parse(root):
  name = None
  revision = None
  endian = None
  mpuPresent = None
  fpuPresent = None
  nodes = root.getElementsByTagName("name")[0]
  for node in nodes.childNodes:
    if node.nodeType == node.ELEMENT_NODE:
      if node.tagName == "name":
        name = node.childNodes[0].data
      elif node.tagName == "revision":
        revision = node.childNodes[0].data
      elif node.tagName == "endian":
        endian = node.childNodes[0].data
      elif node.tagName == "mpuPresent":
        mpuPresent = node.childNodes[0].data
      elif node.tagName == "fpuPresent":
        fpuPresent = node.childNodes[0].data
  return CPU(name, revision, endian, mpuPresent, fpuPresent)

class Device(Object):
  def __init__(self, vendor, vendorID, name, series, version, description, licenseText, headerSystemFilename, headerDefinitionsPrefix, 
    addressUnitBits, width=32, size=32, access="read-write", resetValue=0x00000000, resetMask=0xFFFFFFFF):
    super().__init__(name, description)
    self.vendor = vendor
    self.vendorID = vendorID
    self.series = series
    self.version = version
    self.licenseText = licenseText
    self.headerSystemFilename = headerSystemFilename
    self.headerDefinitionsPrefix = headerDefinitionsPrefix
    self.addressUnitBits = addressUnitBits
    self.width = width
    self.size = size
    self.access = access
    self.resetValue = resetValue
    self.resetMask = resetMask
  def __str__(self):
    return " ".join([self.vendor, self.vendorID, self.name, self.series, self.version, self.description, self.licenseText, 
    self.headerSystemFilename, self.headerDefinitionsPrefix, 
    self.addressUnitBits, self.width, self.size, self.access, self.resetValue, self.resetMask])

def device_parse(root):
  vendor = None
  vendorID = None
  name = None
  series = None
  version = None
  description = None
  licenseText = None
  headerSystemFilename = None
  headerDefinitionsPrefix = None
  cpu = None
  addressUnitBits = None
  width = 32
  size = 32
  access = "read-write"
  resetValue = 0x00000000
  resetMask = 0xFFFFFFFF
  for node in root.childNodes:
    if node.nodeType == node.ELEMENT_NODE:
      if node.tagName == "vendor":
        vendor = node.childNodes[0].data
      elif node.tagName == "vendorID":
        vendorID = node.childNodes[0].data
      elif node.tagName == "name":
        name = node.childNodes[0].data
      elif node.tagName == "series":
        series = node.childNodes[0].data
      elif node.tagName == "version":
        version = node.childNodes[0].data
      elif node.tagName == "description":
        description = node.childNodes[0].data
      if node.tagName == "licenseText":
        licenseText = node.childNodes[0].data
      elif node.tagName == "headerSystemFilename":
        headerSystemFilename = node.childNodes[0].data
      elif node.tagName == "headerDefinitionsPrefix":
        headerDefinitionsPrefix = node.childNodes[0].data
      elif node.tagName == "addressUnitBits":
        addressUnitBits = node.childNodes[0].data
      elif node.tagName == "width":
        width = node.childNodes[0].data
      elif node.tagName == "size":
        size = node.childNodes[0].data
      elif node.tagName == "access":
        access = node.childNodes[0].data
      elif node.tagName == "resetValue":
        resetValue = node.childNodes[0].data
      elif node.tagName == "resetMask":
        resetMask = node.childNodes[0].data
  return Device(vendor, vendorID, name, series, version, description, licenseText, headerSystemFilename, headerDefinitionsPrefix, 
    addressUnitBits, width, size, access, resetValue, resetMask)
      

def CMSIS_OBJECTS(object):
  def __init__(self, cpu, device):
    self.cpu = cpu
    self.device = device
    self.periperals = []
  def add_register(self, periperal):
    self.periperals.append(periperal)

def cmsis_svd_parse(svd_file):
  dom = xml.dom.minidom.parse(svd_file)
  root = dom.documentElement
  device = device_parse(root)
  cpu = cpu_parse(root)
  return CMSIS_OBJECTS(cpu, device)

if __name__ == "__main__":
  cmsis_svd_parse("../data/CMSDK_CM3.svd")