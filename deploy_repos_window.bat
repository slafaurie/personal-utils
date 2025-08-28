@echo off
setlocal enabledelayedexpansion

title Master Deployment Script

echo ========================================
echo   Master Deployment Script
echo ========================================
echo.
echo This script will pull from main and sync dependencies
echo for all configured repositories.
echo.
echo Deployment started at %date% %time%
echo.

:: Configuration: Add new repositories here
:: Format: "Repository Name|Repository Path"
set "REPO_1=cw-dags|%cd%\cw-dags"
set "REPO_2=cw-forecast|%cd%\cw-forecast"
set "REPO_3=cw-ingestion|%cd%\cw-ingestion"
REM set "REPO_4=cw-lakehouse|%cd%\cw-lakehouse"

:: Counter for total repositories
set "TOTAL_REPOS=3"

echo Found %TOTAL_REPOS% repositories to deploy:
for /L %%i in (1,1,%TOTAL_REPOS%) do (
    for /f "tokens=1,2 delims=|" %%a in ("!REPO_%%i!") do (
        echo   - %%a
    )
)
echo.

:: Initialize counters
set "SUCCESS_COUNT=0"
set "FAILED_COUNT=0"
set "SKIPPED_COUNT=0"

:: Process each repository
for /L %%i in (1,1,%TOTAL_REPOS%) do (
    for /f "tokens=1,2 delims=|" %%a in ("!REPO_%%i!") do (
        set "REPO_NAME=%%a"
        set "REPO_PATH=%%b"
        
        echo ========================================
        echo Processing: !REPO_NAME!
        echo Path: !REPO_PATH!
        echo.
        
        :: Check if directory exists
        if not exist "!REPO_PATH!" (
            echo ERROR: Directory does not exist!
            echo.
            set /a FAILED_COUNT+=1
        ) else (
            :: Check if it's a git repository
            cd /d "!REPO_PATH!"
            git status >nul 2>&1
            if errorlevel 1 (
                echo WARNING: Not a git repository, skipping...
                echo.
                set /a SKIPPED_COUNT+=1
            ) else (
                :: Pull from main
                echo Pulling from origin/main...
                git pull origin main
                if errorlevel 1 (
                    echo ERROR: Git pull failed!
                    echo.
                    set /a FAILED_COUNT+=1
                ) else (
                    :: Check if uv.toml or pyproject.toml exists for dependency sync
                    if exist "uv.toml" (
                        echo Syncing dependencies with uv...
                        uv sync
                        if errorlevel 1 (
                            echo WARNING: uv sync failed, but continuing...
                        )
                    ) else if exist "pyproject.toml" (
                        echo Syncing dependencies with uv...
                        uv sync
                        if errorlevel 1 (
                            echo WARNING: uv sync failed, but continuing...
                        )
                    ) else (
                        echo No uv.toml or pyproject.toml found, skipping dependency sync
                    )
                    
                    echo SUCCESS: !REPO_NAME! deployed successfully
                    echo.
                    set /a SUCCESS_COUNT+=1
                )
            )
        )
    )
)

:: Summary
echo ========================================
echo           DEPLOYMENT SUMMARY
echo ========================================
echo.
echo Successful: %SUCCESS_COUNT%/%TOTAL_REPOS%
if %FAILED_COUNT% gtr 0 (
    echo Failed: %FAILED_COUNT%/%TOTAL_REPOS%
)
if %SKIPPED_COUNT% gtr 0 (
    echo Skipped: %SKIPPED_COUNT%/%TOTAL_REPOS%
)
echo.
echo Deployment completed at %date% %time%

:: Pause if there were any failures
if %FAILED_COUNT% gtr 0 (
    echo.
    echo Some deployments failed. Press any key to exit...
    pause >nul
) else (
    echo.
    echo All deployments completed successfully!
    timeout /t 3 >nul
)

endlocal

REM echo.
REM echo Press any key to exit...
REM pause >nul 
