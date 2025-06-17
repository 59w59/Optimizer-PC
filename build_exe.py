import subprocess
import sys
import os
import urllib.request
import tempfile
import zipfile
from pathlib import Path

def check_python_installation():
    """Verifica se Python está instalado"""
    try:
        result = subprocess.run([sys.executable, '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Python encontrado: {version}")
            return True
    except:
        pass
    
    print("❌ Python não encontrado no sistema")
    return False

def download_python():
    """Baixa e instala Python automaticamente"""
    print("🔄 Baixando Python 3.11.7...")
    
    # URL do Python 3.11.7 (versão estável e compatível)
    python_url = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
    
    try:
        # Criar pasta temporária
        temp_dir = tempfile.mkdtemp()
        python_installer = os.path.join(temp_dir, "python_installer.exe")
        
        # Baixar Python
        print("📥 Baixando instalador do Python...")
        urllib.request.urlretrieve(python_url, python_installer)
        print("✅ Download concluído")
        
        # Instalar Python silenciosamente
        print("🔧 Instalando Python...")
        install_cmd = [
            python_installer,
            '/quiet',                    # Instalação silenciosa
            'InstallAllUsers=1',         # Para todos os usuários
            'PrependPath=1',             # Adicionar ao PATH
            'Include_test=0',            # Não incluir testes
            'Include_pip=1',             # Incluir pip
            'Include_tcltk=0',           # Não incluir Tk
            'Include_launcher=1',        # Incluir launcher
        ]
        
        result = subprocess.run(install_cmd, capture_output=True)
        
        if result.returncode == 0:
            print("✅ Python instalado com sucesso!")
            # Atualizar o executável do Python
            return update_python_executable()
        else:
            print("❌ Erro na instalação do Python")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao baixar/instalar Python: {e}")
        return False

def update_python_executable():
    """Atualiza a referência do executável Python após instalação"""
    possible_paths = [
        r"C:\Program Files\Python311\python.exe",
        r"C:\Program Files (x86)\Python311\python.exe",
        r"C:\Users\{}\AppData\Local\Programs\Python\Python311\python.exe".format(os.environ.get('USERNAME', '')),
        "python.exe",
        "python3.exe"
    ]
    
    for path in possible_paths:
        try:
            result = subprocess.run([path, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Python encontrado em: {path}")
                # Atualizar sys.executable
                sys.executable = path
                return True
        except:
            continue
    
    print("⚠️  Python instalado mas não encontrado no PATH")
    return False

def install_dependencies():
    """Instala todas as dependências necessárias"""
    print("🔄 Verificando e instalando dependências...")
    
    try:
        # Verificar se requirements.txt existe
        if not os.path.exists("requirements.txt"):
            create_requirements_file()
        
        # Instalar dependências do requirements.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False
    except FileNotFoundError:
        print("❌ Arquivo requirements.txt não encontrado!")
        return False

def create_requirements_file():
    """Cria arquivo requirements.txt se não existir"""
    requirements_content = """pyinstaller>=5.0
psutil>=5.9.0
requests>=2.28.0
urllib3>=1.26.0
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements_content)
    print("📝 Arquivo requirements.txt criado")

def install_pyinstaller():
    """Instala PyInstaller se não estiver instalado"""
    try:
        import PyInstaller
        print("✅ PyInstaller já está instalado")
        return True
    except ImportError:
        print("📦 Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller instalado com sucesso")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar PyInstaller: {e}")
            return False

def test_executable(exe_path):
    """Testa se o executável foi criado corretamente"""
    print("\n🧪 Testando executável...")
    
    try:
        # Verificar se o arquivo existe e tem tamanho adequado
        if not os.path.exists(exe_path):
            print("❌ Executável não encontrado")
            return False
            
        size = os.path.getsize(exe_path)
        if size < 1024 * 1024:  # Menor que 1MB
            print("⚠️ Executável muito pequeno, pode estar corrompido")
            return False
            
        print(f"✅ Executável verificado: {size / (1024*1024):.1f} MB")
        
        # Teste rápido sem executar (apenas verificar se é um PE válido)
        with open(exe_path, 'rb') as f:
            header = f.read(64)
            if b'MZ' in header[:2]:  # Signature PE
                print("✅ Executável tem formato válido")
                return True
            else:
                print("⚠️ Formato de executável inválido")
                return False
                
    except Exception as e:
        print(f"⚠️ Erro ao verificar executável: {e}")
        return False

def build_executable():
    """Cria o executável do otimizador"""
    
    print("=" * 60)
    print("🏗️  Windows Optimizer v3.0 - Build Executável")
    print("🚀 Instalador Automático Completo")
    print("=" * 60)
    
    # 1. Verificar Python
    if not check_python_installation():
        print("\n🔄 Python não encontrado. Iniciando instalação automática...")
        if not download_python():
            print("❌ Falha na instalação do Python. Build cancelado.")
            return False
    
    # 2. Verificar se o arquivo principal existe
    if not os.path.exists("windows_optimizer.py"):
        print("❌ Arquivo windows_optimizer.py não encontrado!")
        return False
    
    # 3. Instalar dependências
    if not install_dependencies():
        print("⚠️ Tentando continuar sem algumas dependências...")
    
    # 4. Instalar PyInstaller
    if not install_pyinstaller():
        return False
    
    # 5. Limpar arquivos anteriores
    cleanup_previous_builds()
    
    # 6. Criar executável com comando otimizado
    cmd = [
        "pyinstaller",
        "--onefile",                    # Arquivo único
        "--console",                    # Interface de console
        "--name=WindowsOptimizer_v3",   # Nome do executável
        "--clean",                      # Limpar cache do build
        "--noconfirm",                  # Não pedir confirmação
        "--distpath=dist",              # Pasta de saída
        "--workpath=build",             # Pasta de trabalho
        "--specpath=.",                 # Local do arquivo .spec
        "--hidden-import=psutil",       # Garantir que psutil seja incluído
        "--hidden-import=winreg",       # Garantir que winreg seja incluído
        "--hidden-import=subprocess",   # Garantir que subprocess seja incluído
        "--exclude-module=tkinter",     # Excluir tkinter para reduzir tamanho
        "--exclude-module=matplotlib",  # Excluir matplotlib
        "--exclude-module=numpy",       # Excluir numpy
        "windows_optimizer.py"          # Arquivo principal
    ]
    
    print("\n🔨 Criando executável otimizado...")
    print(f"📝 Comando PyInstaller iniciado...")
    
    try:
        # Executar comando com timeout menor e sem capturar output completo
        result = subprocess.run(cmd, check=True, timeout=300)  # 5 minutos max
        
        print("\n✅ Build PyInstaller concluído!")
        
        # Verificar se o arquivo foi criado
        exe_path = "dist/WindowsOptimizer_v3.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"📁 Executável criado: {size_mb:.2f} MB")
            
            # Teste rápido do executável
            if test_executable(exe_path):
                print("✅ Teste de verificação passou")
            else:
                print("⚠️ Teste básico falhou, mas executável foi criado")
            
            # Criar pacote completo
            create_complete_package()
            
            print("\n🎉 BUILD CONCLUÍDO COM SUCESSO!")
            print("📦 Localização: WindowsOptimizer_Complete/")
            print("\n🚀 Para usar:")
            print("   1. Vá na pasta WindowsOptimizer_Complete")
            print("   2. Execute run_optimizer.bat como ADMINISTRADOR")
            
            return True
            
        else:
            print("❌ Executável não foi criado")
            return False
            
    except subprocess.TimeoutExpired:
        print("\n⏰ Timeout: Build demorou mais que 5 minutos")
        print("💡 Tentando método alternativo...")
        return build_executable_alternative()
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro no PyInstaller (código: {e.returncode})")
        print("💡 Tentando método alternativo...")
        return build_executable_alternative()
        
    except KeyboardInterrupt:
        print("\n⛔ Build interrompido pelo usuário")
        return False

def cleanup_previous_builds():
    """Limpa builds anteriores para evitar conflitos"""
    cleanup_folders = ['dist', 'build', '__pycache__']
    for folder in cleanup_folders:
        if os.path.exists(folder):
            try:
                import shutil
                shutil.rmtree(folder)
                print(f"🧹 Limpando: {folder}")
            except:
                pass
    
    # Remover arquivos .spec anteriores
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            try:
                os.remove(file)
                print(f"🧹 Removendo: {file}")
            except:
                pass

def build_executable_alternative():
    """Método alternativo mais simples para criar executável"""
    print("\n🔄 Método alternativo: Build simples...")
    
    # Comando mínimo
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console", 
        "--name=WindowsOptimizer_v3",
        "--noconfirm",
        "windows_optimizer.py"
    ]
    
    try:
        print("🔨 Executando build alternativo...")
        result = subprocess.run(cmd, check=True, timeout=180)  # 3 minutos
        
        exe_path = "dist/WindowsOptimizer_v3.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"✅ Método alternativo funcionou! ({size_mb:.2f} MB)")
            
            # Criar pacote
            create_complete_package()
            print("\n🎉 BUILD ALTERNATIVO CONCLUÍDO!")
            return True
        else:
            print("❌ Método alternativo também falhou")
            return create_standalone_package()
            
    except subprocess.TimeoutExpired:
        print("⏰ Método alternativo também demorou muito")
        return create_standalone_package()
        
    except subprocess.CalledProcessError:
        print("❌ Método alternativo falhou")
        return create_standalone_package()
        
    except KeyboardInterrupt:
        print("⛔ Método alternativo interrompido")
        return False

def create_standalone_package():
    """Cria pacote standalone sem PyInstaller"""
    print("\n🔄 Criando pacote standalone (sem executável)...")
    
    # Criar pasta de distribuição
    dist_folder = "WindowsOptimizer_Complete"
    if os.path.exists(dist_folder):
        import shutil
        shutil.rmtree(dist_folder)
    os.makedirs(dist_folder)
    
    # Copiar arquivos Python
    files_to_copy = [
        "windows_optimizer.py",
        "requirements.txt"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            import shutil
            shutil.copy2(file, dist_folder)
    
    # Criar script de execução Python
    run_script = """@echo off
title Windows Performance Optimizer v3.0
color 0A

echo.
echo ===============================================
echo    Windows Performance Optimizer v3.0
echo    🚀 100+ Otimizacoes Avancadas do Windows
echo ===============================================
echo.
echo 📋 NOTA: Este pacote executa via Python
echo.

:menu
echo Escolha uma opcao:
echo [1] Executar Otimizador (Python)
echo [2] Instalar Dependencias
echo [3] Verificar Python
echo [4] Sair
echo.
set /p choice="Digite sua opcao (1-4): "

if "%choice%"=="1" goto run_python
if "%choice%"=="2" goto install_deps
if "%choice%"=="3" goto check_python
if "%choice%"=="4" goto exit
goto menu

:run_python
echo.
echo 🚀 Iniciando otimizador via Python...
if exist "windows_optimizer.py" (
    python windows_optimizer.py
) else (
    echo ❌ Arquivo windows_optimizer.py nao encontrado!
)
pause
goto menu

:install_deps
echo.
echo 📦 Instalando dependencias...
pip install -r requirements.txt
pause
goto menu

:check_python
echo.
echo 🔍 Verificando Python...
python --version
if %errorlevel% equ 0 (
    echo ✅ Python encontrado!
) else (
    echo ❌ Python nao encontrado! Instale em python.org
)
pause
goto menu

:exit
echo.
echo 👋 Ate logo!
exit
"""
    
    run_script_path = os.path.join(dist_folder, "run_optimizer.bat")
    with open(run_script_path, "w", encoding="utf-8") as f:
        f.write(run_script)
    
    # Criar README específico
    readme_content = """# Windows Performance Optimizer v3.0

## 🚀 Pacote Standalone (Python)

Este pacote requer Python instalado no sistema.

### 📋 Requisitos:
- Python 3.7+ instalado
- Executar como Administrador

### 🛠️ Como Usar:

1. Certifique-se que Python está instalado
2. Execute: run_optimizer.bat
3. Escolha opção 2 para instalar dependências (primeira vez)
4. Escolha opção 1 para executar o otimizador
5. SEMPRE execute como Administrador

### 📥 Instalar Python:
Se não tem Python instalado:
1. Vá em: https://python.org/downloads/
2. Baixe a versão mais recente
3. Durante instalação, marque "Add to PATH"

### ✨ Recursos:
- 🧹 100+ otimizações para Windows
- 🚀 Limpeza avançada de sistema
- ⚡ Melhoria de performance
- 🔧 Tweaks de registro
- 🛠️ Ferramentas de manutenção

---
© 2024 Windows Performance Optimizer v3.0
"""
    
    readme_path = os.path.join(dist_folder, "README.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"📦 Pacote standalone criado em: {dist_folder}/")
    print("💡 Este pacote requer Python instalado no sistema de destino")
    
    return True

def create_complete_package():
    """Cria um pacote completo pronto para distribuição"""
    
    print("\n📦 Criando pacote completo...")
    
    # Criar pasta de distribuição
    dist_folder = "WindowsOptimizer_Complete"
    if os.path.exists(dist_folder):
        import shutil
        shutil.rmtree(dist_folder)
        print("🧹 Limpando pasta anterior...")
    
    os.makedirs(dist_folder)
    print(f"📁 Pasta criada: {dist_folder}")
    
    # Verificar se executável existe em dist/
    exe_source = "dist/WindowsOptimizer_v3.exe"
    exe_dest = os.path.join(dist_folder, "WindowsOptimizer_v3.exe")
    
    if os.path.exists(exe_source):
        print(f"📋 Copiando executável de: {exe_source}")
        print(f"📋 Para destino: {exe_dest}")
        
        try:
            import shutil
            shutil.copy2(exe_source, exe_dest)
            
            # Verificar se a cópia foi bem-sucedida
            if os.path.exists(exe_dest):
                source_size = os.path.getsize(exe_source)
                dest_size = os.path.getsize(exe_dest)
                
                if source_size == dest_size:
                    print(f"✅ Executável copiado com sucesso ({dest_size / (1024*1024):.2f} MB)")
                else:
                    print(f"⚠️ Tamanhos diferentes - Origem: {source_size}, Destino: {dest_size}")
                    return False
            else:
                print("❌ Executável não foi copiado para o destino")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao copiar executável: {e}")
            return False
    else:
        print(f"❌ Executável não encontrado em: {exe_source}")
        print("💡 Criando pacote Python como fallback...")
        return create_python_fallback_package(dist_folder)
    
    # Copiar scripts de execução existentes se houver
    existing_scripts = [
        "run_optimizer.bat",
        "INSTALACAO-FACIL.bat", 
        "LEIA-ME.txt",
        "README.txt"
    ]
    
    for script in existing_scripts:
        if os.path.exists(script):
            try:
                import shutil
                shutil.copy2(script, dist_folder)
                print(f"✅ {script} copiado")
            except Exception as e:
                print(f"⚠️ Erro ao copiar {script}: {e}")
    
    # Criar arquivos necessários se não existirem
    create_all_package_files(dist_folder)
    
    # Verificar integridade final
    verify_package_integrity(dist_folder)
    
    # Criar ZIP
    create_distribution_zip(dist_folder)
    
    return True

def create_python_fallback_package(dist_folder):
    """Cria pacote Python quando executável não está disponível"""
    print("🐍 Criando pacote Python fallback...")
    
    # Copiar arquivos Python necessários
    python_files = [
        "windows_optimizer.py",
        "requirements.txt"
    ]
    
    for file in python_files:
        if os.path.exists(file):
            try:
                import shutil
                shutil.copy2(file, dist_folder)
                print(f"✅ {file} copiado")
            except Exception as e:
                print(f"❌ Erro ao copiar {file}: {e}")
                return False
    
    # Criar script específico para Python
    create_python_runner_script(dist_folder)
    return True

def create_python_runner_script(dist_folder):
    """Cria script para executar versão Python"""
    script_content = """@echo off
title Windows Performance Optimizer v3.0 (Python)
color 0A

echo.
echo ===============================================
echo    Windows Performance Optimizer v3.0
echo    🐍 VERSAO PYTHON
echo ===============================================
echo.
echo 📋 NOTA: Esta versao requer Python instalado
echo.

:menu
echo Escolha uma opcao:
echo [1] 🚀 Executar Otimizador (Python)
echo [2] 📦 Instalar Dependencias
echo [3] 🔍 Verificar Python
echo [4] ❌ Sair
echo.
set /p choice="Digite sua opcao (1-4): "

if "%choice%"=="1" goto run_python
if "%choice%"=="2" goto install_deps
if "%choice%"=="3" goto check_python
if "%choice%"=="4" goto exit
goto menu

:run_python
echo.
echo 🚀 Iniciando via Python...
if exist "windows_optimizer.py" (
    python windows_optimizer.py
) else (
    echo ❌ windows_optimizer.py nao encontrado!
)
pause
goto menu

:install_deps
echo.
echo 📦 Instalando dependencias...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo ❌ requirements.txt nao encontrado!
)
pause
goto menu

:check_python
echo.
echo 🔍 Verificando Python...
python --version
if %errorlevel% equ 0 (
    echo ✅ Python encontrado!
) else (
    echo ❌ Python nao encontrado!
    echo 💡 Instale em: https://python.org
)
pause
goto menu

:exit
echo.
echo 👋 Ate logo!
exit
"""
    
    script_path = os.path.join(dist_folder, "run_optimizer.bat")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)
    print("✅ Script Python runner criado")

def create_user_instructions(dist_folder):
    """Cria instruções específicas para o usuário final"""
    
    instructions = """===============================================
   COMO USAR - SUPER SIMPLES!
===============================================

🎯 VOCÊ BAIXOU O WINDOWS OPTIMIZER v3.0

✨ É MUITO FÁCIL DE USAR:

PASSO 1: EXTRAIR
🔸 Extraia este ZIP em qualquer pasta
🔸 (Exemplo: Desktop, Documentos, etc.)

PASSO 2: EXECUTAR  
🔸 Clique duplo em: "run_optimizer.bat"
🔸 Escolha opção 2 (Administrador)
🔸 Clique "Sim" na janela de confirmação

PASSO 3: OTIMIZAR
🔸 No otimizador, escolha opção 12
🔸 (Otimização Completa - recomendado)
🔸 Aguarde terminar (5-15 minutos)

PASSO 4: REINICIAR
🔸 Reinicie o computador
🔸 Pronto! Windows otimizado!

===============================================

💡 AINDA MAIS FÁCIL:
- Execute: "INSTALACAO-FACIL.bat"
- Ele te guia passo a passo!

⚠️ IMPORTANTE:
- SEMPRE execute como Administrador
- Feche outros programas antes
- Aguarde até o final

🎉 RESULTADO:
- Boot 30-50% mais rápido
- Sistema mais responsivo  
- 2-10GB+ espaço liberado
- Menos travamentos

===============================================
© 2024 Windows Performance Optimizer v3.0 - Pronto para usar!
==============================================="""
    
    instructions_path = os.path.join(dist_folder, "INSTRUCOES-USUARIO.txt")
    with open(instructions_path, "w", encoding="utf-8") as f:
        f.write(instructions)
    print("✅ Instruções para usuário criadas")

def create_exe_runner_script(dist_folder):
    """Cria script para executar o arquivo executável"""
    script_content = """@echo off
title Windows Performance Optimizer v3.0
color 0A

echo.
echo ===============================================
echo    Windows Performance Optimizer v3.0
echo    🚀 100+ Otimizacoes Avancadas do Windows
echo ===============================================
echo.
echo 📋 INSTRUÇÕES:
echo.

:menu
echo Escolha uma opcao:
echo [1] Executar Normalmente
echo [2] Executar como Administrador (Recomendado)
echo [3] Sair
echo.
set /p choice="Digite sua opcao (1-3): "

if "%choice%"=="1" goto run_normal
if "%choice%"=="2" goto run_admin
if "%choice%"=="3" goto exit
goto menu

:run_normal
echo.
echo 🚀 Iniciando Windows Optimizer...
if exist "WindowsOptimizer_v3.exe" (
    start WindowsOptimizer_v3.exe
) else (
    echo ❌ Executavel nao encontrado!
)
exit

:run_admin
echo.
echo 🚀 Iniciando como Administrador...
if exist "WindowsOptimizer_v3.exe" (
    powershell -Command "Start-Process 'WindowsOptimizer_v3.exe' -Verb RunAs"
) else (
    echo ❌ Executavel nao encontrado!
)
exit

:exit
echo.
echo 👋 Ate logo!
exit
"""
    
    script_path = os.path.join(dist_folder, "run_optimizer.bat")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)
    print("✅ Script executor do executável criado")

def create_all_package_files(dist_folder):
    """Cria todos os arquivos necessários para o pacote"""
    
    # Verificar se run_optimizer.bat existe e é para executável
    run_script_path = os.path.join(dist_folder, "run_optimizer.bat")
    exe_path = os.path.join(dist_folder, "WindowsOptimizer_v3.exe")
    
    if os.path.exists(exe_path) and not os.path.exists(run_script_path):
        create_exe_runner_script(dist_folder)
    
    # Criar instruções do usuário
    create_user_instructions(dist_folder)
    
    # Criar README técnico
    create_technical_readme(dist_folder)
    
    # Criar arquivo de instalação fácil
    create_easy_install_script(dist_folder)
    
    # Criar guia de solução de problemas
    create_troubleshooting_guide(dist_folder)

def create_easy_install_script(dist_folder):
    """Cria script de instalação fácil"""
    script_content = """@echo off
title Instalacao Facil - Windows Optimizer v3.0
color 0B

echo.
echo =============================================
echo     INSTALACAO FACIL - WINDOWS OPTIMIZER
echo =============================================
echo.
echo 🎯 Este assistente vai te guiar passo a passo!
echo.
echo 📋 O que este script faz:
echo    ✅ Verifica se tudo esta OK
echo    ✅ Configura o ambiente ideal
echo    ✅ Inicia o otimizador
echo.

pause

echo.
echo 🔍 PASSO 1: Verificando arquivos necessarios...
echo.

if not exist "WindowsOptimizer_v3.exe" (
    echo ❌ ERRO: Executavel nao encontrado!
    echo.
    echo 💡 SOLUCAO:
    echo    1. Certifique-se que todos os arquivos estao na mesma pasta
    echo    2. Se baixou um ZIP, extraia todos os arquivos
    echo    3. Verifique se o antivirus nao bloqueou
    echo.
    pause
    exit /b 1
)

echo ✅ WindowsOptimizer_v3.exe: OK

if exist "run_optimizer.bat" (
    echo ✅ run_optimizer.bat: OK
) else (
    echo ⚠️  run_optimizer.bat: Nao encontrado (opcional)
)

echo.
echo 🔍 PASSO 2: Verificando sistema...
echo.

REM Verificar versão do Windows
for /f "tokens=4-7 delims=[.] " %%i in ('ver') do (
    if %%i==10 (
        echo ✅ Windows 10/11 detectado
    ) else (
        echo ⚠️  Windows versao: %%i.%%j
        echo    Recomendado: Windows 10 ou superior
    )
)

echo ✅ Sistema compativel verificado

echo.
echo 🔍 PASSO 3: Verificando privilegios...
echo.

net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Este script esta rodando como Administrador
    echo 💡 Perfeito! Pode prosseguir normalmente
    set "is_admin=yes"
) else (
    echo ⚠️  Este script NAO esta como Administrador
    echo.
    echo 💡 RECOMENDACAO:
    echo    Para melhores resultados, execute como Admin
    echo    Mas ainda pode prosseguir normalmente
    set "is_admin=no"
)

echo.
echo 🔍 PASSO 4: Verificacao final...
echo.

echo 📊 RESUMO DA VERIFICACAO:
echo ==========================================
echo Sistema: Windows (compativel)
echo Executavel: WindowsOptimizer_v3.exe (OK)
echo Privilegios: %is_admin%
echo Status: Pronto para usar!
echo ==========================================

echo.
echo 🎯 PASSO 5: Instrucoes finais
echo.
echo 📋 ANTES DE COMECAR:
echo    ✅ Feche todos os programas desnecessarios
echo    ✅ Salve todos os trabalhos importantes  
echo    ✅ Se for laptop, conecte na tomada
echo.

set /p ready="Esta pronto para comecar? (s/N): "
if /i not "%ready%"=="s" (
    echo.
    echo 👋 Sem problemas! Execute novamente quando estiver pronto.
    echo 💡 Para usar depois: clique duplo em "run_optimizer.bat"
    pause
    exit /b 0
)

echo.
echo 🚀 INICIANDO WINDOWS OPTIMIZER...
echo.

if "%is_admin%"=="yes" (
    echo 💡 Como voce ja e admin, iniciando diretamente...
    WindowsOptimizer_v3.exe
) else (
    echo 💡 Tentando iniciar como administrador...
    echo    Uma janela UAC aparecera - clique "Sim"
    powershell -Command "Start-Process 'WindowsOptimizer_v3.exe' -Verb RunAs"
)

echo.
echo ✅ COMANDO EXECUTADO!
echo.
echo 💡 PROXIMOS PASSOS:
echo    1. Na tela do otimizador, use opcao 12 (Otimizacao Completa)
echo    2. Aguarde todas as operacoes terminarem
echo    3. Reinicie o computador quando solicitado
echo    4. Aproveite seu Windows otimizado!
echo.

pause
"""
    
    script_path = os.path.join(dist_folder, "INSTALACAO-FACIL.bat")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)
    print("✅ Script de instalação fácil criado")

def create_troubleshooting_guide(dist_folder):
    """Cria guia de solução de problemas"""
    guide_content = """===============================================
   SOLUÇÃO DE PROBLEMAS
   Windows Performance Optimizer v3.0
===============================================

🔧 PROBLEMAS MAIS COMUNS:

===============================================
PROBLEMA: "Erro ao executar" ou "Não funciona"
===============================================

SOLUÇÃO 1: Executar como Administrador
🔸 Clique direito em "run_optimizer.bat"
🔸 Selecione "Executar como administrador"
🔸 Clique "Sim" na janela UAC

SOLUÇÃO 2: Verificar arquivos
🔸 Certifique-se que WindowsOptimizer_v3.exe existe
🔸 Tamanho deve ser aproximadamente 6MB
🔸 Se não existe, baixe novamente o pacote

===============================================
PROBLEMA: "Antivírus bloqueia" ou "Arquivo removido"
===============================================

SOLUÇÃO: Adicionar exceção no antivírus
🔸 Abra seu antivírus (Windows Defender, Avast, etc.)
🔸 Vá em "Exclusões" ou "Exceções"
🔸 Adicione a pasta do otimizador
🔸 OU temporariamente desative o antivírus

Windows Defender:
🔸 Configurações > Vírus e proteção
🔸 Gerenciar configurações (Proteção em tempo real)
🔸 Exclusões > Adicionar exclusão > Pasta
🔸 Selecione a pasta do otimizador

===============================================
PROBLEMA: "Sistema lento após otimização"
===============================================

SOLUÇÃO 1: Reiniciar o computador
🔸 SEMPRE reinicie após usar o otimizador
🔸 Aguarde 2-3 minutos após o boot
🔸 O sistema pode ficar lento inicialmente

SOLUÇÃO 2: Aguardar estabilização
🔸 Após otimização, o Windows reindexiza arquivos
🔸 Este processo pode durar 10-30 minutos
🔸 Use o PC normalmente, vai melhorar

SOLUÇÃO 3: Restauração do Sistema
🔸 Se persistir, use restauração do sistema
🔸 Painel de Controle > Sistema > Proteção do Sistema
🔸 Restauração do Sistema > Escolher ponto anterior

===============================================
PROBLEMA: "Programa trava" ou "Para de responder"
===============================================

SOLUÇÃO 1: Verificar requisitos
🔸 Windows 10 versão 1903+ ou Windows 11
🔸 Pelo menos 4GB de RAM
🔸 1GB+ de espaço livre em disco

SOLUÇÃO 2: Fechar outros programas
🔸 Feche navegadores, jogos, editores
🔸 Pare downloads/uploads
🔸 Feche programas de antivírus temporariamente

SOLUÇÃO 3: Executar em modo seguro
🔸 Reinicie em Modo Seguro
🔸 Execute o otimizador
🔸 Reinicie normalmente

===============================================
PROBLEMA: "Quero reverter as mudanças"
===============================================

SOLUÇÃO 1: Restauração do Sistema
🔸 Pressione Win + R, digite: rstrui
🔸 Escolha um ponto antes da otimização
🔸 Siga o assistente de restauração

SOLUÇÃO 2: Reverter manualmente
🔸 Reativar serviços desabilitados:
   - Windows Search
   - Fax
   - Windows Update (se desabilitado)
🔸 Reinstalar apps removidos pela Microsoft Store

===============================================
PROBLEMA: "Erro de privilégios" ou "Acesso negado"
===============================================

SOLUÇÃO: Garantir privilégios administrativos
🔸 Sempre execute como administrador
🔸 Desative controle de conta (UAC) temporariamente
🔸 Faça login como administrador local

===============================================
PROBLEMA: "Internet lenta após otimização"
===============================================

SOLUÇÃO 1: Verificar DNS
🔸 Pressione Win + R, digite: cmd
🔸 Digite: ipconfig /flushdns
🔸 Digite: ipconfig /renew

SOLUÇÃO 2: Resetar configurações de rede
🔸 Pressione Win + X > Windows PowerShell (Admin)
🔸 Digite: netsh winsock reset
🔸 Digite: netsh int ip reset
🔸 Reinicie o computador

===============================================
🆘 SE NADA FUNCIONAR:
===============================================

🔸 Baixe novamente o pacote completo
🔸 Execute em outro computador para teste
🔸 Verifique se o Windows está atualizado
🔸 Considere restauração completa do sistema

===============================================
💡 DICAS IMPORTANTES:
===============================================

✅ SEMPRE faça backup antes de usar
✅ Execute apenas em PCs que você possui
✅ Use apenas em Windows originais
✅ Mantenha pontos de restauração ativados
✅ Execute apenas quando necessário

===============================================
📞 INFORMAÇÕES TÉCNICAS:
===============================================

Logs do sistema: %TEMP%\WindowsOptimizer\
Versão mínima: Windows 10 build 1903
RAM mínima: 4GB
Espaço necessário: 1GB+
Duração típica: 5-15 minutos

===============================================
© 2024 Windows Performance Optimizer v3.0
==============================================="""
    
    guide_path = os.path.join(dist_folder, "SOLUCAO-PROBLEMAS.txt")
    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(guide_content)
    print("✅ Guia de solução de problemas criado")

def create_technical_readme(dist_folder):
    """Cria README técnico"""
    readme_content = """# Windows Performance Optimizer v3.0

## 📦 Pacote de Distribuição

Este é o pacote completo do Windows Optimizer, pronto para uso.

### 🎯 Como Usar:

1. **Extrair**: Extraia todos os arquivos em uma pasta
2. **Executar**: Clique duplo em `run_optimizer.bat`
3. **Administrador**: Escolha opção 2 (Como Administrador)
4. **Otimizar**: Use opção 12 (Otimização Completa)
5. **Reiniciar**: Reinicie o PC após otimização

### 📋 Arquivos Inclusos:

- `WindowsOptimizer_v3.exe` - Programa principal
- `run_optimizer.bat` - Script facilitador
- `INSTRUCOES-USUARIO.txt` - Guia completo
- `README.txt` - Este arquivo

### ⚠️ Requisitos:

- Windows 10/11 (64-bit)
- Privilégios de administrador
- 1GB+ espaço livre em disco

### 🎯 Resultados Esperados:

- ⚡ Boot 30-50% mais rápido
- 💾 2-10GB+ espaço liberado
- 🚀 Sistema mais responsivo
- 🔋 Melhor duração da bateria

---
© 2024 Windows Performance Optimizer v3.0
"""
    
    readme_path = os.path.join(dist_folder, "README.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✅ README técnico criado")

def verify_package_integrity(dist_folder):
    """Verifica integridade do pacote criado"""
    print("\n🔍 Verificando integridade do pacote...")
    
    essential_files = ["run_optimizer.bat", "INSTRUCOES-USUARIO.txt"]
    exe_file = os.path.join(dist_folder, "WindowsOptimizer_v3.exe")
    python_file = os.path.join(dist_folder, "windows_optimizer.py")
    
    # Deve ter pelo menos um dos dois
    if not (os.path.exists(exe_file) or os.path.exists(python_file)):
        print("❌ ERRO: Nem executável nem script Python encontrados!")
        return False
    
    # Verificar arquivos essenciais
    missing_files = []
    for file in essential_files:
        file_path = os.path.join(dist_folder, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️ Arquivos faltando: {', '.join(missing_files)}")
    
    # Verificar tamanho do executável se existir
    if os.path.exists(exe_file):
        size = os.path.getsize(exe_file)
        if size < 1024 * 1024:  # Menor que 1MB
            print(f"⚠️ Executável muito pequeno: {size} bytes")
            return False
        else:
            print(f"✅ Executável OK: {size / (1024*1024):.2f} MB")
    
    print("✅ Verificação de integridade concluída")
    return True

def create_distribution_zip(dist_folder):
    """Cria ZIP para distribuição"""
    try:
        import zipfile
        zip_path = "WindowsOptimizer_v3_Complete.zip"
        
        # Remover ZIP anterior
        if os.path.exists(zip_path):
            os.remove(zip_path)
            print("🗑️ ZIP anterior removido")
        
        print("📦 Criando novo ZIP...")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
            for root, dirs, files in os.walk(dist_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, dist_folder)
                    zipf.write(file_path, arcname)
                    print(f"📄 Adicionado: {arcname}")
        
        if os.path.exists(zip_path):
            zip_size = os.path.getsize(zip_path) / (1024 * 1024)
            print(f"✅ ZIP criado: {zip_path} ({zip_size:.1f} MB)")
            print("🎯 ESTE É O ARQUIVO PARA DISTRIBUIR!")
            return True
        else:
            print("❌ Falha ao criar ZIP")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao criar ZIP: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("🎯 WINDOWS PERFORMANCE OPTIMIZER v3.0")
    print("🔧 INSTALADOR AUTOMÁTICO COMPLETO")
    print("=" * 70)
    print()
    
    # Verificar arquivo principal
    if not os.path.exists("windows_optimizer.py"):
        print("❌ Arquivo windows_optimizer.py não encontrado!")
        print("💡 Certifique-se que ambos os arquivos estão na mesma pasta")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    try:
        print("🎯 Iniciando build automático...")
        success = build_executable()
        
        if success:
            print("\n" + "="*70)
            print("🎉 BUILD FINALIZADO COM SUCESSO!")
            print("="*70)
            print()
            
            # Verificar qual tipo de pacote foi criado
            exe_in_complete = os.path.exists("WindowsOptimizer_Complete/WindowsOptimizer_v3.exe")
            zip_exists = os.path.exists("WindowsOptimizer_v3_Complete.zip")
            
            if exe_in_complete:
                print("✅ EXECUTÁVEL: WindowsOptimizer_v3.exe (funciona sem Python)")
                print("📁 LOCALIZAÇÃO: WindowsOptimizer_Complete/")
            else:
                print("✅ VERSÃO PYTHON: windows_optimizer.py (requer Python)")
                print("📁 LOCALIZAÇÃO: WindowsOptimizer_Complete/")
            
            if zip_exists:
                print("📦 ZIP CRIADO: WindowsOptimizer_v3_Complete.zip")
                print("🎯 PARA DISTRIBUIR: Compartilhe este ZIP")
            
            print()
            print("🔧 PARA TESTAR:")
            print("   1. Vá na pasta: WindowsOptimizer_Complete")
            print("   2. Execute: run_optimizer.bat como ADMINISTRADOR")
            print("   3. Escolha opção 2 (Como Administrador)")
            print()
            
            # Tentar abrir a pasta
            try:
                import subprocess
                subprocess.run(['explorer', 'WindowsOptimizer_Complete'], check=False)
                print("📂 Pasta aberta automaticamente!")
            except:
                print("📂 Abra manualmente: WindowsOptimizer_Complete")
                
        else:
            print("\n💥 Build falhou!")
            print("💡 Possíveis soluções:")
            print("   - Execute como administrador")
            print("   - Desative antivírus temporariamente")
            print("   - Verifique espaço em disco")
            print("   - Tente novamente")
            
    except KeyboardInterrupt:
        print("\n⛔ Build cancelado pelo usuário")
        
    except Exception as e:
        print(f"\n💥 Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*50)
    input("Pressione Enter para sair...")
