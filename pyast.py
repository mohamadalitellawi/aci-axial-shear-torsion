
from doctest import OutputChecker
from model import Section, Loads, Criteria
from sheetmanager import SheetManager
import sheartorsioncalculations as ast_calc

class ASTApp:
  pass

  def __init__(self):
    self.username = ""
    self.section = Section()
    self.loads = Loads()
    self.criteria = Criteria()
    self.sm : SheetManager = None



  def startup(self):        
    # print the greeting at startup
    self.greeting()

    # ask the user for their name
    self.username = input("What is your name? ")
    print(f"Welcome, {self.username}!")
    print()
    
  def greeting(self):
    print("-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-")
    print("~~~~~~ Welcome to Axial-Shear-Torsion! ~~~~~~")
    print("-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-")
    print()

  def menu_header(self):
    print("--------------------------------")
    print("Please make a selection:")
    print("(M): repeat this Menu")

    print("(D): Define Criteria")
    print("(A): Add Section")

    print("(C): calculate from manual data")
    print("(E): Calculate from excel sheet data (Section Cut sap results)")

    print("(X): eXit program")

  def menu_error(self):
    print("That's not a valid selection. Please try again.")

  def goodbye(self):
    print("-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~")
    print(f"Thanks for using PyAST, {self.username}!")
    print("-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~")

  def menu(self):
    self.menu_header()

    # get the user's selection and act on it. This loop will
    # run until the user exits the app
    selection = ""
    while (True):
      selection = input("Selection? ")

      if len(selection) == 0:
        self.menu_error()
        continue

      selection = selection.capitalize()
      if selection[0] == 'X':
        self.goodbye()
        break
      elif selection[0] == 'M':
        self.menu_header()
        continue

      elif selection[0] == 'A':
        print("\nAdd/Update Current Section [units mm]:")
        
        if self.section is None:
          self.section = Section()
        print(self.section.get_inputdata_str( print_header=True))

        # ask the user if they want to update the data
        doupdate = input("Update the Data? (y/n): ")
        doupdate = doupdate.capitalize()
        if (len(doupdate) > 0 and doupdate[0] == 'Y'):
          inputdata = input("Enter New data:\n")
          if inputdata.capitalize()[0] == "X": continue
          self.section.parse_manual_data(inputdata.split(","))
          print(self.section.get_inputdata_str())

        print("----------------------------------\n")
        continue



      elif selection[0] == 'D':
        print("\nDefine/Update Design Criteria [units mpa]:")
        
        if self.criteria is None:
          self.criteria = Criteria()
        print(self.criteria.get_inputdata_str( print_header=True))

        # ask the user if they want to update the data
        doupdate = input("Update the Data? (y/n): ")
        doupdate = doupdate.capitalize()
        if (len(doupdate) > 0 and doupdate[0] == 'Y'):
          inputdata = input("Enter New data:\n")
          if inputdata.capitalize()[0] == "X": continue
          self.criteria.parse_manual_data(inputdata.split(","))
          print(self.criteria.get_inputdata_str())

        print("----------------------------------\n")
        continue




      elif selection[0] == 'C':
        print("\nUpdate Shear Design Forces [units kN,m]:")
        if self.loads is None:
          self.loads = Loads()
        self.loads.print_shear_design_forces(print_header=True)

        # ask the user if they want to update the data
        doupdate = input("Update the Data? (y/n): ")
        doupdate = doupdate.capitalize()
        if (len(doupdate) > 0 and doupdate[0] == 'Y'):
          inputdata = input("Enter New data:\n")
          if inputdata.capitalize()[0] == "X": continue
          self.loads.parse_manual_data(inputdata.split(","))
          self.loads.print_shear_design_forces()
        
        print ("message,Label,Ratio,MainBar Count,StrLegsX,StrLegsY")
        print(ast_calc.calculate_shear_torsion(self.loads,self.criteria,self.section))
        print("----------------------------------\n")
        continue

      elif selection[0] == 'E':
        print("\nDefine/Update Excel file name and sheet name:")
        try:
          if self.sm is None:
            excelfilename = input("Enter Excel File Name: ")
            sheetname = input("Enter Sheet Name: ")
            self.sm = SheetManager(excelfilename,sheetname)
          self.sm.print_file_sheet_names()
          # ask the user if they want to update the data
          doupdate = input("Update the Data? (y/n): ")
          doupdate = doupdate.capitalize()
          if (len(doupdate) > 0 and doupdate[0] == 'Y'):
            excelfilename = input("Enter Excel File Name: ")
            if excelfilename.capitalize()[0] == "X": continue
            sheetname = input("Enter Sheet Name: ")
            self.sm = SheetManager(excelfilename,sheetname)
            self.sm.print_file_sheet_names()

          load_data = self.sm.get_loads()
          output_data = []
          output_data.append(["message", "Label", "Ratio", "MainBar Count", "StrLegsX", "StrLegsY"])
          for i, row in enumerate(load_data):
            self.loads.parse_excel_data(row)
            output_data.append(ast_calc.calculate_shear_torsion(self.loads,self.criteria,self.section))
          
          criteria_str = self.criteria.get_inputdata_str(with_title=True)
          section_str = self.section.get_inputdata_str(with_title=True)
          output_data.append(criteria_str.split(","))
          output_data.append(section_str.split(","))
          self.sm.create_output_sheet(output_data)

        except Exception as e:
          self.menu_error()
          raise e


  def run(self):
    # Execute the startup routine - ask for name, print greeting, etc
    self.startup()
    # Start the main program menu and run until the user exits
    self.menu()

if __name__ == "__main__":
    app = ASTApp()
    app.sm = SheetManager(r".\data\220825_section forces.xlsx",r"Section Cut Forces - Analysis")
    app.run()