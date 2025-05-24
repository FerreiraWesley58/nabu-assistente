import streamlit as st

def add_background_animation(particle_count: int = 10):
    """
    Adiciona uma animação de fundo com partículas otimizada.
    
    Args:
        particle_count (int): Número de partículas (padrão: 10)
    """
    st.markdown(f"""
    <style>
        /* Container de partículas */
        .particles {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
            will-change: transform;
        }}
        
        /* Partículas individuais */
        .particle {{
            position: absolute;
            width: 3px;
            height: 3px;
            background: rgba(74, 107, 255, 0.2);
            border-radius: 50%;
            animation: float 10s infinite linear;
            will-change: transform;
            transform: translateZ(0);
        }}
        
        /* Animação otimizada */
        @keyframes float {{
            0% {{
                transform: translateY(0) translateX(0);
                opacity: 0;
            }}
            50% {{
                opacity: 0.3;
            }}
            100% {{
                transform: translateY(-100vh) translateX(50px);
                opacity: 0;
            }}
        }}
        
        /* Ajuste para garantir que o conteúdo fique sobre a animação */
        .main .block-container {{
            position: relative;
            z-index: 1;
        }}
    </style>
    
    <div class="particles" id="particles"></div>
    
    <script>
        // Criar partículas otimizado
        function createParticles() {{
            const container = document.getElementById('particles');
            const fragment = document.createDocumentFragment();
            
            for (let i = 0; i < {particle_count}; i++) {{
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 5 + 's';
                fragment.appendChild(particle);
            }}
            
            container.appendChild(fragment);
        }}
        
        // Executar quando o documento estiver carregado
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', createParticles);
        }} else {{
            createParticles();
        }}
    </script>
    """, unsafe_allow_html=True) 