import json
from typing import Dict, List, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RAGManager:
    def __init__(self, qa_file: str = "data/qa_database.json"):
        """
        Inicializa o gerenciador RAG.
        
        Args:
            qa_file (str): Caminho para o arquivo JSON com as perguntas e respostas
        """
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.qa_data = self._load_qa_data(qa_file)
        self.question_embeddings = None
        self._prepare_embeddings()
    
    def _load_qa_data(self, qa_file: str) -> List[Dict]:
        """
        Carrega os dados de Q&A do arquivo JSON.
        
        Args:
            qa_file (str): Caminho para o arquivo JSON
            
        Returns:
            List[Dict]: Lista de dicionários com perguntas e respostas
        """
        try:
            with open(qa_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data['qa_pairs']
        except FileNotFoundError:
            print(f"Arquivo {qa_file} não encontrado.")
            return []
        except json.JSONDecodeError:
            print(f"Erro ao decodificar o arquivo JSON {qa_file}.")
            return []
    
    def _prepare_embeddings(self) -> None:
        """
        Prepara os embeddings para todas as perguntas no banco de dados.
        """
        questions = [qa['question'] for qa in self.qa_data]
        self.question_embeddings = self.model.encode(questions)
    
    def find_similar_questions(self, query: str, threshold: float = 0.7) -> List[Tuple[int, float]]:
        """
        Encontra perguntas similares à consulta do usuário.
        
        Args:
            query (str): Pergunta do usuário
            threshold (float): Limiar de similaridade mínima
            
        Returns:
            List[Tuple[int, float]]: Lista de tuplas (índice, similaridade)
        """
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, self.question_embeddings)[0]
        
        # Encontra índices das perguntas mais similares acima do threshold
        similar_indices = [(i, sim) for i, sim in enumerate(similarities) if sim >= threshold]
        return sorted(similar_indices, key=lambda x: x[1], reverse=True)
    
    def get_answer(self, query: str, max_results: int = 3) -> List[Dict]:
        """
        Recupera as respostas mais relevantes para a pergunta do usuário.
        
        Args:
            query (str): Pergunta do usuário
            max_results (int): Número máximo de resultados a retornar
            
        Returns:
            List[Dict]: Lista de dicionários com perguntas e respostas relevantes
        """
        similar_questions = self.find_similar_questions(query)
        
        results = []
        for idx, similarity in similar_questions[:max_results]:
            qa_pair = self.qa_data[idx]
            results.append({
                'question': qa_pair['question'],
                'answer': qa_pair['answer'],
                'category': qa_pair['category'],
                'similarity': float(similarity)
            })
        
        return results

    def add_qa_pair(self, question: str, answer: str, category: str) -> None:
        """
        Adiciona um novo par de pergunta e resposta ao banco de dados.
        
        Args:
            question (str): Nova pergunta
            answer (str): Resposta correspondente
            category (str): Categoria da pergunta/resposta
        """
        self.qa_data.append({
            'question': question,
            'answer': answer,
            'category': category
        })
        self._prepare_embeddings()  # Atualiza os embeddings
        
        # Salva no arquivo
        with open('data/qa_database.json', 'w', encoding='utf-8') as f:
            json.dump({'qa_pairs': self.qa_data}, f, ensure_ascii=False, indent=4) 