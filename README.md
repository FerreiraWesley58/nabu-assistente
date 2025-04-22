# Nabu - Assistente Virtual Inteligente

Nabu é um assistente virtual inteligente desenvolvido para ajudar usuários com suas tarefas diárias, respondendo perguntas e fornecendo suporte personalizado.

## Requisitos

- Python 3.8 ou superior
- Ollama (para execução local dos modelos de linguagem)
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/nabu.git
cd nabu
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Inicie o servidor Ollama (se ainda não estiver rodando):
```bash
ollama serve
```

5. Instale o modelo Mistral (se ainda não estiver instalado):
```bash
ollama pull mistral
```

## Uso

1. Inicie a aplicação:
```bash
streamlit run app.py
```

2. Acesse a interface web em: http://localhost:8501

3. Comece a interagir com o Nabu através do chat!

## Recursos

- Interface moderna e responsiva
- Animações de fundo interativas
- Suporte a múltiplos modelos de linguagem
- Histórico de conversas
- Personalização de aparência

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contribuições

Contribuições são bem-vindas! Por favor, sinta-se à vontade para abrir issues ou enviar pull requests.

## Contato

Para dúvidas ou sugestões, entre em contato através do GitHub. 