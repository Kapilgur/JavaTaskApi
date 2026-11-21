@ECHO OFF
SETLOCAL
SET VERSION=3.9.11
IF "%MAVEN_USER_HOME%"=="" (SET CACHE=%USERPROFILE%\.m2) ELSE (SET CACHE=%MAVEN_USER_HOME%)
SET HOME_DIR=%CACHE%\wrapper\dists\apache-maven-%VERSION%
SET MAVEN=%HOME_DIR%\apache-maven-%VERSION%\bin\mvn.cmd
SET URL=https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/%VERSION%/apache-maven-%VERSION%-bin.zip
IF EXIST "%MAVEN%" GOTO RUN
IF NOT EXIST "%HOME_DIR%" MKDIR "%HOME_DIR%"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest '%URL%' -OutFile '%HOME_DIR%\maven.zip'; Expand-Archive -Force '%HOME_DIR%\maven.zip' '%HOME_DIR%'; Remove-Item '%HOME_DIR%\maven.zip'"
IF ERRORLEVEL 1 EXIT /B 1
:RUN
CALL "%MAVEN%" -f "%~dp0pom.xml" %*
ENDLOCAL
