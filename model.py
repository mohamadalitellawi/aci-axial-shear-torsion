class Section:
  def __init__(self, width:float, height:float, cover:float,
  main_bar_dia:float, tran_bar_dia:float) -> None:
    self.width = width
    self.height = height
    self.cover = cover
    self.main_bar_dia = main_bar_dia
    self.tran_bar_dia = tran_bar_dia



class Actions:
  def __init__(self,f1,f2,f3,m1,m2,m3) -> None:
    self.f1 = f1
    self.f2 = f2
    self.f3 = f3
    self.m1 = m1
    self.m2 = m2
    self.m3 = m3

class Criteria:
  def __init__(self, fc,fy,fyt) -> None:
    self.fc = fc
    self.fy = fy
    self.fyt = fyt