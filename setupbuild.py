from cx_Freeze import setup, Executable

exe=Executable(
     # script="汕头市残联康复业务系统.py",
     script="kfpro.py",
     base="Win32Gui",
     icon="images\login.ico"
     )
includefiles=["images\login.png", "images\splash.png", "msvcr100.dll", "MSVCP100.dll", "sqldrivers\qsqlmysql4.dll"]
includes=[]
excludes=[]
packages=[]
setup(
     version = "1.0",
     description = "康复业务系统",
     author = "iefan",
     name = "康复业务系统",
     options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
     executables = [exe]
     )