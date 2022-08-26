class Section:
  def __init__(self, width = 1700, height = 500, cover=30,
                main_bar_dia=25, stirrups_bar_dia=14,
                stirrups_spacing = 150 ) -> None:
    self.width = width
    self.height = height
    self.cover = cover
    self.main_bar_dia = main_bar_dia
    self.stirrups_bar_dia = stirrups_bar_dia
    self.stirrups_spacing = stirrups_spacing

  def print_section_inputdata(self,print_header = False):
    if print_header:
      print("Width, Height, Concrete Cover, Main Bar Diameter, Stirrups Bar Diamater, Stirrups Bar Spacing")
    print(f"{self.width},{self.height},{self.cover},{self.main_bar_dia},{self.stirrups_bar_dia},{self.stirrups_spacing}")

  def parse_manual_data(self,data_row):
    self.width = float(data_row[0].strip())
    self.height = float(data_row[1].strip())
    self.cover = float(data_row[2].strip())
    self.main_bar_dia = float(data_row[3].strip())
    self.stirrups_bar_dia = float(data_row[4].strip())
    self.stirrups_spacing = float(data_row[5].strip())

  def xo (self):
    return self.width - 2 * self.cover
  def yo (self):
    return self.height - 2 * self.cover
  def Aoh (self):
    return self.xo() * self.yo()
  def Ph (self):
    return 2 * (self.xo() + self.yo())
  def Ao (self):
    return 0.85 * self.Aoh()
  def dx (self):
    return self.width - self.cover - self.stirrups_bar_dia - 0.5 * self.main_bar_dia
  def dy (self):
    return self.height - self.cover - self.stirrups_bar_dia - 0.5 * self.main_bar_dia
  def Ag(self):
    return self.width * self.height
  def max_spacing(self):
    spacing = [
      16 * self.main_bar_dia,
      48 * self.stirrups_bar_dia,
      self.width,
      self.height,
      600,
      0.5 * self.dx(),
      0.5 * self.dy()
    ]
    return min(spacing)


class Loads:
  def __init__(self,f1=0.0,f2=0.0,f3=0.0,m1=0.0,m2=0,m3=0.0,combination = None,label = None,casetype = "Combination", x=0,y=0,z=0) -> None:
    self.f1 = f1  # Positive is Compression
    self.f2 = f2
    self.f3 = f3
    self.m1 = m1
    self.m2 = m2
    self.m3 = m3
    self.x = x
    self.y = y
    self.z = z
    self.label = label
    self.combination = combination
    self.casetype = casetype

  def print_shear_design_forces(self,print_header = False):
    if print_header:
      print(f"F1,F2,F3,M1")
    print(f"{self.f1},{self.f2},{self.f3},{self.m1}")

  def parse_manual_data(self,data_row):
    self.f1 = float(data_row[0].strip())
    self.f2 = float(data_row[1].strip())
    self.f3 = float(data_row[2].strip())
    self.m1 = float(data_row[3].strip())

  def parse_excel_data(self, data_row):
    self.label = data_row[0]
    self.combination = data_row[1]
    self.casetype = data_row[2]
    self.f1 = float(data_row[3])
    self.f2 = float(data_row[4])
    self.f3 = float(data_row[5])
    self.m1 = float(data_row[6])
    self.m2 = float(data_row[7])
    self.m3 = float(data_row[8])
    self.x = float(data_row[9])
    self.y = float(data_row[10])
    self.z = float(data_row[11])



class Criteria:
  def __init__(self, fc = 40.0,fy = 420.0,fyt = 400.0, phi_shear = 0.75) -> None:
    self.fc = fc
    self.fy = fy
    self.fyt = fyt
    self.phi_shear = phi_shear

  def print_inputdata(self,print_header = False):
    if print_header:
      print("FC, FY, FYT (stirrups), Phi shear")
    print(f"{self.fc},{self.fy},{self.fyt},{self.phi_shear}")

  def parse_manual_data(self,data_row):
    self.fc = float(data_row[0].strip())
    self.fy = float(data_row[1].strip())
    self.fyt = float(data_row[2].strip())
    self.phi_shear = float(data_row[3].strip())
