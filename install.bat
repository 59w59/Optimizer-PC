@echo off
echo ========================================
echo Windows Performance Optimizer v2.0
echo Instalador de Dependencias
echo ========================================
echo.

echo 🔄 Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python nao encontrado! Instale o Python primeiro.
    pause
    exit /b 1
)

echo.
echo 🔄 Instalando dependencias...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ✅ Dependencias instaladas com sucesso!
    echo.
    echo 📋 Para usar o otimizador:
    echo    1. Execute: python windows_optimizer.py
    echo    2. Ou crie executavel: python build_exe.py
    echo.
) else (
    echo.
    echo ❌ Erro na instalacao das dependencias!
    echo    Verifique sua conexao com a internet.
)

echo.
pause
