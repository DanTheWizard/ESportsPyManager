@echo off



set hidden=0

set file="app.py"
set manifest="%file%.xml"

    rem python -m PyInstaller --onefile --name app-s.exe --i "%public%\Icons\good.ico" %file%
    rem python -m PyInstaller --onefile --name app-h.exe --noconsole --i "%public%\Icons\good.ico" %file%

rem goto :eof

if %hidden%==0 (
    D:\PyAppKiller\.venv\Scripts\python.exe -m PyInstaller --clean --paths=src --onefile --name app-s.exe --i "%public%\Icons\good.ico" %file% --distpath ./output/dist --workpath ./output/build  --specpath ./output
) else (
    D:\PyAppKiller\.venv\Scripts\python.exe -m PyInstaller --clean --paths=src --onefile --name app-h.exe --noconsole --i "%public%\Icons\good.ico" %file% --distpath ./output/dist --workpath ./output/build  --specpath ./output
)


:EOF