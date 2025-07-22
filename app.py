import os
# Forçar o uso da CPU antes de importar o PyTorch ou SentenceTransformer
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TORCH_DEVICE"] = "cpu"

import streamlit as st
import requests
import json
import time
import random
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from background_animation import add_background_animation
from rag_manager import RAGManager

# Configuração da página com tema personalizado (DEVE ser a primeira chamada Streamlit)
st.set_page_config(
    page_title="Nabu - Assistente Corporativo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Adicionar animação de fundo (reduzida para melhor performance)
add_background_animation(particle_count=10)  # Reduzido para 10 partículas

# Inicializar o RAG Manager com cache otimizado
@st.cache_resource(ttl=3600)  # Cache por 1 hora
def get_rag_manager():
    return RAGManager(max_documents=2)

rag_manager = get_rag_manager()

# Aplicar CSS personalizado
st.markdown("""
<style>
    /* Tema principal com mais cores */
    :root {
        --primary-color: #4a6bff;
        --secondary-color: #6c757d;
        --accent-color-1: #ff6b6b;
        --accent-color-2: #4ecdc4;
        --accent-color-3: #ffd166;
        --accent-color-4: #a06cd5;
        --background-color: #f8f9fa;
        --text-color: #212529;
    }
    
    /* Estilo geral com gradiente mais colorido */
    .stApp {
        background: none !important;
    }
    
    /* Cabeçalho com gradiente mais vibrante */
    .main .block-container h1 {
        background: linear-gradient(90deg, #4a6bff, #6a11cb, #ff6b6b, #4ecdc4);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-align: center;
        animation: fadeIn 1.5s ease-in-out, gradientFlow 8s ease infinite;
        position: relative;
        z-index: 1;
    }
    
    /* Animação do gradiente */
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Cards com cores mais vibrantes */
    .stCard {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        z-index: 1;
    }
    
    .stCard:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Botões com gradiente colorido */
    .stButton > button {
        background: linear-gradient(90deg, #4a6bff, #6a11cb, #ff6b6b);
        background-size: 200% 200%;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        animation: gradientFlow 5s ease infinite;
        position: relative;
        z-index: 1;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(74, 107, 255, 0.4);
    }
    
    /* Sidebar com gradiente mais colorido */
    .css-1d391kg, .css-12oz5g7 {
        background: linear-gradient(180deg, #2c3e50 0%, #1a2530 50%, #0f172a 100%);
        color: white;
        position: relative;
        z-index: 1;
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    /* Animações */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Mensagens de chat com cores mais vibrantes */
    .stChatMessage {
        animation: fadeIn 0.5s ease-in-out;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .stChatMessage [data-testid="stChatMessageContent"] {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Input de chat com borda colorida */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        position: relative;
        z-index: 1;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4a6bff;
        box-shadow: 0 0 0 2px rgba(74, 107, 255, 0.2);
    }
    
    /* Seletor de modelo com estilo colorido */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        backdrop-filter: blur(10px);
        position: relative;
        z-index: 1;
    }
    
    /* Spinner com cor mais vibrante */
    .stSpinner > div {
        border-top-color: #4a6bff;
    }
    
    /* Ajuste para garantir que o conteúdo fique sobre a animação */
    .main .block-container {
        position: relative;
        z-index: 1;
    }
</style>

<!-- Adicionar partículas -->
<div class="particles" id="particles"></div>

<script>
    // Criar partículas
    function createParticles() {
        const container = document.getElementById('particles');
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 10 + 's';
            container.appendChild(particle);
        }
    }
    
    // Executar quando o documento estiver carregado
    document.addEventListener('DOMContentLoaded', createParticles);
</script>
""", unsafe_allow_html=True)

# Função para verificar se o modelo está disponível
def check_model_availability(model_name):
    try:
        response = requests.get(f"http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return any(model["name"] == model_name for model in models)
        return False
    except:
        return False

# Função para obter lista de modelos disponíveis
def get_available_models():
    try:
        response = requests.get(f"http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
        return []
    except:
        return []

# Inicialização do modelo Ollama otimizado
@st.cache_resource(ttl=3600)  # Cache por 1 hora
def get_ollama_model(model_name="mistral"):
    try:
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        return Ollama(
            model=model_name,
            callback_manager=callback_manager,
            base_url="http://localhost:11434",
            temperature=0.3,  # Reduzido para respostas mais diretas
            num_ctx=512,      # Reduzido o contexto para melhor performance
            num_thread=4,     # Otimizado para 4 threads
            stop=["\n\n", "Human:", "Assistant:"]  # Adicionado stops para respostas mais curtas
        )
    except Exception as e:
        st.warning(f"Erro ao inicializar o modelo Ollama: {str(e)}")
        return None

# Cache de respostas frequentes
@st.cache_data(ttl=3600)  # Cache por 1 hora
def get_cached_response(query):
    return None  # Implementar cache de respostas frequentes se necessário

# Função principal de chat otimizada
def chat_with_rag(user_input, model_name="mistral"):
    try:
        # Obter respostas relevantes do RAG
        rag_results = rag_manager.get_answer(user_input)
        
        if not rag_results:
            return "Desculpe, não encontrei informações específicas sobre sua pergunta. Pode reformular ou perguntar sobre outro tema?"
        
        # Usar a resposta mais relevante
        best_match = rag_results[0]
        
        # Se a similaridade for muito baixa, pedir para reformular (threshold reduzido para 0.2)
        if best_match['similarity'] < 0.2:
            return "Sua pergunta não está muito clara. Pode reformular ou ser mais específico?"
        
        # Retornar a resposta direta do RAG
        return best_match['answer']
    except Exception as e:
        st.error(f"Erro ao processar sua pergunta: {str(e)}")
        return "Desculpe, estou enfrentando dificuldades técnicas. Por favor, tente novamente mais tarde ou reformule sua pergunta."

# Verificar se o Ollama está rodando
try:
    response = requests.get("http://localhost:11434/api/tags")
    if response.status_code == 200:
        ollama_running = True
    else:
        ollama_running = False
        st.error(f"O servidor Ollama retornou código de status {response.status_code}. Por favor, verifique se o servidor está funcionando corretamente.")
        st.warning("Continuando sem o Ollama. Algumas funcionalidades podem não estar disponíveis.")
except Exception as e:
    ollama_running = False
    st.error(f"Não foi possível conectar ao servidor Ollama: {str(e)}")
    st.warning("Continuando sem o Ollama. Algumas funcionalidades podem não estar disponíveis.")

# Verificar modelos disponíveis
available_models = get_available_models()
if not available_models:
    st.warning("Nenhum modelo encontrado no Ollama. Por favor, baixe um modelo com 'ollama pull mistral' ou outro modelo de sua preferência.")
    available_models = ["mistral"]  # Usar um modelo padrão para continuar
    st.warning("Continuando com o modelo padrão. Algumas funcionalidades podem não estar disponíveis.")

# Título e descrição com animação
st.markdown("<h1>🤖 Nabu - Seu Assistente Corporativo</h1>", unsafe_allow_html=True)

# Cards de funcionalidades com cores mais vibrantes
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="stCard" style="border-left: 5px solid #4a6bff;">
        <h3 style="color: #4a6bff;">📋 Processos Internos</h3>
        <p>Consulte informações sobre procedimentos, políticas e diretrizes da empresa.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stCard" style="border-left: 5px solid #ff6b6b;">
        <h3 style="color: #ff6b6b;">👥 Recursos Humanos</h3>
        <p>Obtenha informações sobre benefícios, políticas de RH e desenvolvimento profissional.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stCard" style="border-left: 5px solid #4ecdc4;">
        <h3 style="color: #4ecdc4;">📈 Plano de Carreira</h3>
        <p>Conheça as oportunidades de crescimento e desenvolvimento dentro da empresa.</p>
    </div>
    """, unsafe_allow_html=True)

# Seleção de modelo na barra lateral
with st.sidebar:
    st.markdown("<h2 style='color: #4a6bff;'>⚙️ Configurações</h2>", unsafe_allow_html=True)
    
    model_name = st.selectbox(
        "Selecione o modelo a ser usado:",
        available_models,
        index=0 if "mistral" in available_models else 0
    )
    
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #ff6b6b;'>📊 Estatísticas</h3>", unsafe_allow_html=True)
    
    # Estatísticas simuladas
    if "message_count" not in st.session_state:
        st.session_state.message_count = 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Mensagens", st.session_state.message_count, delta=random.randint(1, 5))
    with col2:
        st.metric("Modelo Atual", model_name)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #4ecdc4;'>ℹ️ Sobre o Nabu</h3>", unsafe_allow_html=True)
    st.markdown("""
    O Nabu é um assistente virtual especializado em processos corporativos.
    Ele pode ajudar você a encontrar informações sobre:
    - Políticas da empresa
    - Procedimentos internos
    - Dúvidas sobre RH
    - Informações sobre carreira
    - E muito mais!
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #ffd166;'>💡 Dicas</h3>", unsafe_allow_html=True)
    st.markdown("""
    - Seja específico em suas perguntas
    - Você pode perguntar sobre qualquer processo interno
    - O Nabu está sempre aprendendo e melhorando
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #a06cd5;'>🔧 Instalação do Ollama</h3>", unsafe_allow_html=True)
    st.markdown("""
    Se você ainda não instalou o Ollama:
    1. Baixe do site oficial: https://ollama.ai/download
    2. Instale e execute o Ollama
    3. Baixe um modelo: `ollama pull mistral` (ou outro modelo)
    4. Inicie o servidor: `ollama serve`
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Área de chat com animação
st.markdown("<h2 style='color: #4a6bff;'>💬 Chat com o Nabu</h2>", unsafe_allow_html=True)

# Inicializar histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # Mensagem de boas-vindas
    welcome_message = """
    Olá! Eu sou o Nabu, seu assistente virtual corporativo. Estou aqui para ajudar você com informações sobre:
    
    - **Processos internos** da empresa
    - **Recursos Humanos** e políticas
    - **Recrutamento** e seleção
    - **Informativos** importantes
    - **Plano de carreira** e desenvolvimento
    
    Como posso ajudar você hoje?
    """
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# Exibir mensagens anteriores com animação
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário com estilo personalizado
if prompt := st.chat_input("Digite sua pergunta aqui..."):
    # Adicionar mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.message_count += 1
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gerar resposta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = chat_with_rag(prompt, model_name)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.message_count += 1
            except Exception as e:
                st.error(f"Desculpe, ocorreu um erro: {str(e)}")
                st.info("Certifique-se de que o Ollama está rodando localmente na porta 11434.")

# Adicionar botão para limpar o histórico
if st.button("Limpar Histórico de Chat"):
    st.session_state.messages = []
    st.session_state.message_count = 0
    st.rerun()

# Adicionar rodapé
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.7); border-radius: 10px;">
    <p>Desenvolvido por Wesley Ferreira | Nabu - Assistente Virtual Corporativo</p>
</div>
""", unsafe_allow_html=True)