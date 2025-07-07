@echo off

REM 0 - Build only the -s version
REM 1 - Build only the -h version
REM 2 - Build both -s and -h version
REM | - Show what command would run
set hidden=2

REM python script to build
set file="%~dp0\app.py"

REM Set EXE Icon
set exe_icon="%~dp0\src\appicon.ico"

REM This will create a output folder with the EXE built in there
set "python=%~dp0\.venv\Scripts\python.exe"
set "pre_args=-m PyInstaller --clean --paths=%~dp0\src --hidden-import=tkinter --add-data="%~dp0\.env;." --onefile"
set "post_args=--i %exe_icon% %file% --distpath %~dp0\output --workpath %~dp0\output\build_src --specpath %~dp0\output\build_src"



REM -s version for a shown window, -h version for hidden window (no output console)
if %hidden%==0 (
     %python% %pre_args% --name app-s.exe %post_args%
) else if %hidden%==1 (
    %python% %pre_args% --name app-h.exe %post_args% --noconsole --hide-console=hide-early
) else if %hidden%==2 (
    %python% %pre_args% --name app-s.exe %post_args%
    %python% %pre_args% --name app-h.exe %post_args% --noconsole --hide-console=hide-early
) else (
    echo %python% %pre_args% --name app-s.exe %post_args%
)

exit
