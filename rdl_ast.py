class Component():
  def __init__(self, comptype, name, content):
    self.comptype = comptype
    self.name = name
    self.content = content

  def pprint(self):
    msg = "comp %s %s\n" % (self.comptype, self.name)
    for i in self.content:
      msg += i.pprint()
      msg += "\n"
    return msg

class ComponentInst():
  def __init__(self, comptype, instname, content):
    self.comptype = comptype
    self.instname = instname
    self.content = content

  def pprint(self):
    msg = "comp %s %s\n" % (self.comptype, self.instname)
    for i in self.content:
      msg += i.pprint()
      msg += "\n"
    return msg

class Property():
  def __init__(self, name, value):
    self.name = name
    self.value = value

  def pprint(self):
    return "prop %s = %s" % (self.name, self.value)
