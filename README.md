# Nabu - Assistente Virtual Inteligente

Nabu é um assistente virtual inteligente desenvolvido para ajudar usuários com suas tarefas diárias, respondendo perguntas e fornecendo suporte personalizado. O sistema utiliza uma abordagem de Recuperação Aumentada por Geração (RAG) baseada em palavras-chave para encontrar respostas relevantes para as perguntas dos usuários.

## Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Ollama (opcional - para execução local dos modelos de linguagem)

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

4. (Opcional) Para usar modelos de linguagem locais, inicie o servidor Ollama:
```bash
ollama serve
```

5. (Opcional) Instale o modelo Mistral para processamento local:
```bash
ollama pull mistral
```

**Nota:** O sistema funcionará mesmo sem o Ollama instalado, utilizando apenas o mecanismo de RAG baseado em palavras-chave.

## Uso

1. Inicie a aplicação:
```bash
streamlit run app.py
```

2. Acesse a interface web em: http://localhost:8501

3. Comece a interagir com o Nabu através do chat!

## Recursos

- Interface moderna e responsiva com animações de fundo interativas
- Sistema de RAG (Recuperação Aumentada por Geração) baseado em palavras-chave
- Funcionamento independente de GPU ou hardware especializado
- Tolerância a falhas (funciona mesmo sem o Ollama instalado)
- Suporte opcional a múltiplos modelos de linguagem via Ollama
- Histórico de conversas
- Personalização de aparência

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Arquitetura do Sistema

O Nabu utiliza uma arquitetura de Recuperação Aumentada por Geração (RAG) baseada em palavras-chave:

1. **Processamento de Texto**: O sistema extrai palavras-chave das perguntas e respostas armazenadas.

2. **Cálculo de Similaridade**: Quando uma nova pergunta é feita, o sistema calcula a similaridade entre as palavras-chave da pergunta e as palavras-chave das perguntas armazenadas usando uma métrica de similaridade de Jaccard ponderada.

3. **Recuperação de Contexto**: O sistema recupera as respostas mais relevantes com base na similaridade calculada.

4. **Geração de Resposta**: Se o Ollama estiver disponível, o sistema pode usar um modelo de linguagem para gerar uma resposta mais elaborada com base no contexto recuperado.

5. **Tolerância a Falhas**: O sistema funciona mesmo sem o Ollama, fornecendo respostas baseadas apenas no mecanismo de RAG.

## Contribuições

Contribuições são bem-vindas! Por favor, sinta-se à vontade para abrir issues ou enviar pull requests.

## Contato

Para dúvidas ou sugestões, entre em contato através do GitHub.