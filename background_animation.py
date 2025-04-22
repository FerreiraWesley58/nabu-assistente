import streamlit as st

def add_background_animation():
    """
    Adiciona uma animação de fundo interativa à aplicação Streamlit.
    """
    st.markdown("""
    <style>
        /* Animação de fundo interativa */
        .background-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
            pointer-events: none;
        }
        
        .gradient-sphere {
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.5;
            animation: float 15s ease-in-out infinite;
        }
        
        .sphere-1 {
            width: 300px;
            height: 300px;
            background: linear-gradient(135deg, #4a6bff, #6a11cb);
            top: 10%;
            left: 10%;
            animation-delay: 0s;
        }
        
        .sphere-2 {
            width: 250px;
            height: 250px;
            background: linear-gradient(135deg, #ff6b6b, #ffd166);
            top: 60%;
            left: 70%;
            animation-delay: -5s;
        }
        
        .sphere-3 {
            width: 200px;
            height: 200px;
            background: linear-gradient(135deg, #4ecdc4, #a06cd5);
            top: 30%;
            left: 50%;
            animation-delay: -10s;
        }
        
        @keyframes float {
            0% {
                transform: translate(0, 0) scale(1);
            }
            25% {
                transform: translate(50px, 30px) scale(1.1);
            }
            50% {
                transform: translate(0, 50px) scale(1);
            }
            75% {
                transform: translate(-30px, 20px) scale(0.9);
            }
            100% {
                transform: translate(0, 0) scale(1);
            }
        }
        
        /* Efeito de partículas - usando CSS puro */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }
        
        .particle {
            position: absolute;
            width: 5px;
            height: 5px;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            animation: float-particle 10s linear infinite;
        }
        
        .particle:nth-child(1) { left: 10%; top: 20%; animation-delay: 0s; }
        .particle:nth-child(2) { left: 20%; top: 40%; animation-delay: 1s; }
        .particle:nth-child(3) { left: 30%; top: 60%; animation-delay: 2s; }
        .particle:nth-child(4) { left: 40%; top: 80%; animation-delay: 3s; }
        .particle:nth-child(5) { left: 50%; top: 10%; animation-delay: 4s; }
        .particle:nth-child(6) { left: 60%; top: 30%; animation-delay: 5s; }
        .particle:nth-child(7) { left: 70%; top: 50%; animation-delay: 6s; }
        .particle:nth-child(8) { left: 80%; top: 70%; animation-delay: 7s; }
        .particle:nth-child(9) { left: 90%; top: 90%; animation-delay: 8s; }
        .particle:nth-child(10) { left: 15%; top: 75%; animation-delay: 9s; }
        .particle:nth-child(11) { left: 25%; top: 85%; animation-delay: 10s; }
        .particle:nth-child(12) { left: 35%; top: 15%; animation-delay: 11s; }
        .particle:nth-child(13) { left: 45%; top: 25%; animation-delay: 12s; }
        .particle:nth-child(14) { left: 55%; top: 35%; animation-delay: 13s; }
        .particle:nth-child(15) { left: 65%; top: 45%; animation-delay: 14s; }
        .particle:nth-child(16) { left: 75%; top: 55%; animation-delay: 15s; }
        .particle:nth-child(17) { left: 85%; top: 65%; animation-delay: 16s; }
        .particle:nth-child(18) { left: 95%; top: 75%; animation-delay: 17s; }
        .particle:nth-child(19) { left: 5%; top: 85%; animation-delay: 18s; }
        .particle:nth-child(20) { left: 15%; top: 95%; animation-delay: 19s; }
        
        @keyframes float-particle {
            0% { transform: translateY(0) translateX(0); opacity: 0; }
            50% { opacity: 0.8; }
            100% { transform: translateY(-100vh) translateX(100vw); opacity: 0; }
        }
        
        /* Efeito de brilho */
        .spotlight {
            position: absolute;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.1) 0%, rgba(0, 0, 0, 0) 50%);
            opacity: 0.5;
            pointer-events: none;
            z-index: -1;
        }
        
        /* Ajustes para o conteúdo principal */
        .main .block-container {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-top: 2rem;
            margin-bottom: 2rem;
            padding: 2rem;
        }
    </style>
    
    <!-- Adicionar animação de fundo -->
    <div class="background-animation">
        <div class="gradient-sphere sphere-1"></div>
        <div class="gradient-sphere sphere-2"></div>
        <div class="gradient-sphere sphere-3"></div>
        <div class="spotlight"></div>
    </div>
    
    <!-- Adicionar partículas - usando CSS puro -->
    <div class="particles">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
    </div>
    """, unsafe_allow_html=True) 