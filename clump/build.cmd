@echo off

:: Version
set VERSION=1.0.1

::Set personal Path to the Apps:
set PythonEXE=D:\Mess\Python24\python.exe
set SevenZipEXE=D:\Mess\Progra~1\SevenZip\7z.exe
set UpxEXE=D:\Windows\upx.exe
set NSIS=D:\Mess\Progra~1\NSIS\makensis.exe

::Check existance of files
if not exist clump.py           call FileNotFound clump.py
if not exist %PythonEXE%        call FileNotFound %PythonEXE%
if not exist %SevenZipEXE%      call FileNotFound %SevenZipEXE%
if not exist %UpxEXE%           call FileNotFound %UpxEXE%

::Write the Py2EXE-Setup File
call :MakeSetupFile >"clump_EXESetup.py"

::Compile the Python-Script
%PythonEXE% -OO "clump_EXESetup.py" py2exe
if not "%errorlevel%"=="0" (
        echo Py2EXE Error!
        pause
        goto eof
)

:: Delete the Py2EXE-Setup File
del "clump_EXESetup.py"

:: Copy the Py2EXE Results to the SubDirectory and Clean Py2EXE-Results
rd build /s /q
xcopy dist\*.* "clump_EXE\" /d /y /s
rd dist /s /q

:: Compress the files
call :CompressFiles
call :Package
echo.
echo.
echo Done: "clump_EXE\"
echo.
pause
goto eof

:: Compression
:CompressFiles
        cd clump_EXE\
        %UpxEXE% --best *.*
		cd..
goto eof

:: Package
:Package
		del clumpsetup-%VERSION%.exe
		del clump-%VERSION%.zip

		%NSIS% clumpsetup.nsi
		%SevenZipEXE% a clump-%VERSION%.zip clump.py clump.ico docs\*
goto eof

:: Generate the setup file
:MakeSetupFile
        echo.
        echo from distutils.core import setup
        echo import py2exe
        echo.
        echo setup (
        echo    windows = [{
        echo       "script"         : "clump.py",
        echo       "icon_resources" : [(1, "clump.ico")]
        echo    }],
        echo    options = {
        echo       "py2exe": {
        echo          "packages" : ["encodings"],
        echo          "optimize" : 2,
        echo          "compressed" : 1,
		echo 		  "bundle_files" : 2,
        echo       }
        echo    },
		echo    data_files = [(
		echo       "" , ["clump.ico",]
		echo    )],
        echo    zipfile = None)
        echo.
goto eof

:: Errors
:FileNotFound
        echo.
        echo Error, File not found:
        echo [%1]
        echo.
        echo Check Path in %~nx0???
        echo.
        pause
        exit
goto eof

:eof