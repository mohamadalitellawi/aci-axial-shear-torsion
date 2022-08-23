class Section:
  def __init__(self, width, height, cover=30,
                main_bar_dia=25, stirrups_bar_dia=14,
                stirrups_spacing = 150 ) -> None:
    self.width = width
    self.height = height
    self.cover = cover
    self.main_bar_dia = main_bar_dia
    self.stirrups_bar_dia = stirrups_bar_dia
    self.stirrups_spacing = stirrups_spacing

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
  def __init__(self,f1,f2,f3,m1,m2,m3) -> None:
    self.f1 = f1  # Positive is Compression
    self.f2 = f2
    self.f3 = f3
    self.m1 = m1
    self.m2 = m2
    self.m3 = m3

class Criteria:
  def __init__(self, fc = 40.0,fy = 420.0,fyt = 400.0, phi_shear = 0.75) -> None:
    self.fc = fc
    self.fy = fy
    self.fyt = fyt
    self.phi_shear = phi_shear