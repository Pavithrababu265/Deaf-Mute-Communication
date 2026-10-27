@echo off
echo Requesting Admin Privileges...

NET SESSION >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo Admin privileges confirmed.
    
    echo Opening Port 5000 (Web Client)...
    netsh advfirewall firewall add rule name="EchoHandsWeb" dir=in action=allow protocol=TCP localport=5000
    
    echo Opening Port 5555 (TCP Relay)...
    netsh advfirewall firewall add rule name="EchoHandsRelay" dir=in action=allow protocol=TCP localport=5555
    
    echo.
    echo Firewall rules added! 
    echo Please RESTART the application now.
    pause
) ELSE (
    echo.
    echo ##########################################
    echo #  ERROR: PLEASE RUN AS ADMINISTRATOR    #
    echo ##########################################
    echo.
    echo Right-click this file > Run as Administrator
    pause
)
