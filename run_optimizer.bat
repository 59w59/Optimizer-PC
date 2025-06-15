@echo off
echo ========================================
echo Windows Performance Optimizer v2.0
echo ========================================
echo.
echo ⚠️  AVISO: Execute como Administrador para melhores resultados!
echo.
pause
cd /d "%~dp0"
if exist "dist\WindowsOptimizer.exe" (
    echo 🚀 Iniciando otimizador...
    dist\WindowsOptimizer.exe
) else (
    echo ❌ Executável não encontrado!
    echo    Execute primeiro: python build_exe.py
)
pause
