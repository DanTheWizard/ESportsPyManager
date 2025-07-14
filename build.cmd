@echo off
cd /d "%~dp0"



REM 0 - Build only the -s version
REM 1 - Build only the -h version
REM 2 - Build both -s and -h version
REM | - Show what command would run
set hidden=2

REM python script to build
set file="%~dp0\app.py"

REM Set EXE Icon
set exe_icon="%~dp0\src\appicon.ico"

set USERNAME="DanTheWizard"


REM Get the Version from the Python script
for /f "delims=" %%A in ('python -c "from src.logo import app_version; print(app_version)"') do (
    set "VERSION=%%A"
)


REM This will create a output folder with the EXE built in there
set "python=%~dp0\.venv\Scripts\python.exe"
set "pre_args=-m PyInstaller --clean --hidden-import=tkinter --add-data="%~dp0\.env;." --onefile"
set "post_args=--i %exe_icon% %file% --version-file=..\..\versionfile.txt  --distpath %~dp0\output --workpath %~dp0\output\build_src --specpath %~dp0\output\build_src"


%python% -c "import pyinstaller_versionfile; pyinstaller_versionfile.create_versionfile(output_file='versionfile.txt', version='%VERSION%', company_name='%USERNAME%', file_description='PyAppManager', internal_name='PyAppManager', legal_copyright='%USERNAME%', original_filename='PyAppManager-%VERSION%.exe', product_name='PyAppManager', translations=[0, 1200])"


REM -s version for a shown window, -h version for hidden window (no output console)
if %hidden%==0 (
     %python% %pre_args% --name app-s-%VERSION%.exe %post_args%
) else if %hidden%==1 (
    %python% %pre_args% --name app-h-%VERSION%.exe %post_args% --noconsole
) else if %hidden%==2 (
    %python% %pre_args% --name app-s-%VERSION%.exe %post_args%
    %python% %pre_args% --name app-h-%VERSION%.exe %post_args% --noconsole
) else (
    echo %python% %pre_args% --name app-s.exe %post_args%
)

exit
