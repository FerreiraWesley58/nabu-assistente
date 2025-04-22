@echo off
echo Iniciando o Nabu - Assistente Virtual Corporativo
echo.

REM Verificar se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python não encontrado. Por favor, instale o Python 3.8 ou superior.
    pause
    exit /b 1
)

REM Verificar se o Ollama está instalado
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ollama não encontrado. Por favor, instale o Ollama do site oficial: https://ollama.ai/download
    pause
    exit /b 1
)

REM Verificar se o servidor Ollama já está rodando
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo Servidor Ollama já está rodando.
) else (
    echo Verificando se a porta 11434 está em uso...
    netstat -ano | findstr :11434 >nul
    if %errorlevel% equ 0 (
        echo A porta 11434 já está em uso. Tentando encerrar o processo...
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :11434') do (
            taskkill /F /PID %%a >nul 2>&1
        )
        timeout /t 2 /nobreak >nul
    )
    
    echo Iniciando o servidor Ollama...
    start /b ollama serve
    echo Aguardando o servidor Ollama iniciar...
    timeout /t 5 /nobreak >nul
    
    REM Verificar novamente se o servidor iniciou
    curl -s http://localhost:11434/api/tags >nul 2>&1
    if %errorlevel% neq 0 (
        echo Não foi possível iniciar o servidor Ollama. Por favor, verifique se há outro processo usando a porta 11434.
        echo Você pode tentar encerrar manualmente o processo ou reiniciar o computador.
        pause
        exit /b 1
    )
)

REM Verificar se há modelos disponíveis
curl -s http://localhost:11434/api/tags | findstr "models" >nul
if %errorlevel% neq 0 (
    echo Nenhum modelo encontrado. Baixando o modelo Mistral...
    ollama pull mistral
)

REM Instalar dependências se necessário
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
    call venv\Scripts\activate
    echo Instalando dependências...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

REM Iniciar o Nabu
echo Iniciando o Nabu...
streamlit run app.py

pause 