@echo off
title Caderno de Leads — TM Sempre Tecnologia
chcp 65001 > nul
cls
echo =======================================================
echo   📒 CADERNO DE LEADS & SALES COCKPIT
echo   TM Sempre Tecnologia
echo =======================================================
echo.
cd /d "%~dp0"

echo [1/2] Abrindo Caderno de Leads no navegador...
start "" http://localhost:3333

echo [2/2] Iniciando servidor local em http://localhost:3333...
echo Pressione Ctrl+C para encerrar o servidor.
echo.
python server.py
pause
