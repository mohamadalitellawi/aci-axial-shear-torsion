import math


from model import Section, Loads, Criteria

def main():
  section = Section(1700,400)
  criteria = Criteria()
  loads = Loads(400, 600, 290, 300,0,0)
  result = calculate_shear_torsion(loads,criteria,section,True)
  print(result)


SHEAR_TORSION_RESULT_HEADER = ["message", "Label", "Combination" ,"Ratio", "MainBar Count", "StrLegsX", "StrLegsY"]



def calculate_shear(loads:Loads,criteria:Criteria,section:Section, x_dir = True):
  Nu = loads.f1 * 1000
  phi = criteria.phi_shear

  if x_dir:
    Vu = abs( loads.f3 ) * 1000
    bw = section.height
    d = section.dx()
  else:
    Vu = abs( loads.f2 ) * 1000
    bw = section.width
    d = section.dy()
  phi_Vc_comp = phi * 0.17 * (1 + Nu / (14 * section.Ag())) * math.sqrt(criteria.fc) * bw * d
  phi_Vc_tens = phi * 0.17 * (1 + Nu / (3.5 * section.Ag())) * math.sqrt(criteria.fc) * bw * d

  if Nu >= 0:
    phi_Vc = phi_Vc_comp
  else:
    phi_Vc = phi_Vc_tens if phi_Vc_tens > 0 else 0
  
  Av = (Vu - phi_Vc) / (phi * criteria.fyt * d) * section.stirrups_spacing
  Av = max(Av, 0)

  phi_Vs = phi * Av * criteria.fyt * d / section.stirrups_spacing
  phi_Vn = phi_Vc + phi_Vs
  Vu_max = phi_Vc + phi * 0.66 * math.sqrt(criteria.fc) * bw * d

  vu_max = Vu_max / (bw * d)
  vu = Vu / (bw * d)

  Av_min_x = max(
    0.062 * math.sqrt(criteria.fc ) * section.height / criteria.fyt, 
    0.35 * section.height / criteria.fyt
  ) * section.stirrups_spacing 

  Av_min_y = max(
    0.062 * math.sqrt(criteria.fc ) * section.width / criteria.fyt, 
    0.35 * section.width / criteria.fyt
  ) * section.stirrups_spacing 

  Av_min = Av_min_x if x_dir else Av_min_y

  return (Av, vu, vu_max, Av_min)


def calculate_torsion(loads:Loads,criteria:Criteria,section:Section):
  Acp = section.Ag()
  Pcp = 2 * (section.width + section.height)
  Nu = loads.f1 * 1000
  Tu = abs(loads.m1) * 1000 * 1000
  phi = criteria.phi_shear

  Tth = 0.083 * math.sqrt(criteria.fc) * ( Acp**2 / Pcp ) * math.sqrt(1 + Nu / ( 0.33 * section.Ag() * math.sqrt(criteria.fc)))
  Tcr = 0.33 * math.sqrt(criteria.fc) * ( Acp**2 / Pcp ) * math.sqrt(1 + Nu / ( 0.33 * section.Ag() * math.sqrt(criteria.fc)))

  vu_torsion = Tu * section.Ph() / (1.7 * section.Aoh() ** 2)

  At = Tu * section.stirrups_spacing / (phi * 2 * section.Ao() * criteria.fyt)
  Al = Tu * section.Ph() / (phi * 2 * section.Ao() * criteria.fy )
  Al_min = min(
    0.42 * math.sqrt(criteria.fc) * Acp / criteria.fyt - At/section.stirrups_spacing * section.Ph() * criteria.fyt / criteria.fy,
    0.42 * math.sqrt(criteria.fc) * Acp / criteria.fyt - 0.175 * section.width / criteria.fyt * section.Ph() * criteria.fyt / criteria.fy
  )
  Al = max(Al, Al_min)

  return (At,Al,vu_torsion,Tth,Tcr)


def calculate_shear_torsion(loads:Loads,criteria:Criteria,section:Section, x_dir = True):
  message = ""
  if x_dir:
    Av_x, vu_x, vu_max_x, Av_min_x = calculate_shear(loads,criteria,section, True)
  else:
    Av_x, vu_x, vu_max_x, Av_min_x = (0,0,0,0)

  Av_y, vu_y, vu_max_y, Av_min_y = calculate_shear(loads,criteria,section, False)
  
  At,Al,vu_torsion,Tth,Tcr = calculate_torsion(loads,criteria,section)

  vu_max = round(min(vu_max_x, vu_max_y),3)
  vu = round(math.sqrt(vu_torsion ** 2 + vu_x ** 2 + vu_y ** 2),3)
  if vu > vu_max:
    message =  f"increase section size {vu=} > {vu_max=}"
  else:
    message = f"Success {vu=} <= {vu_max=}"
  ratio = round(vu/vu_max,3)
  n_main_bar = math.ceil(4 * Al / (math.pi * section.main_bar_dia ** 2 ))

  Av_x_total = Av_x + 2 * At
  Av_x_total = max(Av_x_total, Av_min_x)
  n_x_legs = math.ceil(4 * Av_x_total / (math.pi * section.stirrups_bar_dia ** 2))

  Av_y_total = Av_y + 2 * At
  Av_y_total = max(Av_y_total, Av_min_y)
  n_y_legs = math.ceil(4 * Av_y_total / (math.pi * section.stirrups_bar_dia ** 2))

  return (message,loads.label,loads.combination , ratio, n_main_bar, n_x_legs, n_y_legs)


if __name__ == "__main__":
  main()