REM CHATGPT CODE 
@echo off
setlocal

REM Check if running as administrator
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo Please run this script as an administrator.
    exit /b 1
)

REM Define variables
set WDK_URL=https://go.microsoft.com/fwlink/p/?LinkId=871629
set WDK_INSTALLER=wdksetup.exe
set WDK_PATH=C:\WDK
set DRIVER_PATH=C:\Path\To\Your\Driver
set DRIVER_NAME=MyDriver
set DRIVER_SYS=%DRIVER_PATH%\%DRIVER_NAME%.sys

REM Download and install WDK
echo Downloading WDK installer...
powershell -Command "Invoke-WebRequest -Uri %WDK_URL% -OutFile %WDK_INSTALLER%"

echo Installing WDK...
%WDK_INSTALLER% /quiet /installpath %WDK_PATH%

REM Compile the driver
echo Compiling the driver...
call "%WDK_PATH%\bin\setenv.cmd" /release /x64
call "%WDK_PATH%\bin\makebuild.cmd" /f "%DRIVER_PATH%\%DRIVER_NAME%.inf"

REM Load the driver
echo Loading the driver...
sc create %DRIVER_NAME% type= kernel start= demand binPath= %DRIVER_SYS%
sc start %DRIVER_NAME%

echo Driver loaded successfully.

endlocal
pause
