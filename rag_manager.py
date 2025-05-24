import json
from typing import Dict, List, Tuple, Any
from sentence_transformers import SentenceTransformer
import numpy as np
import streamlit as st
import torch

class RAGManager:
    def __init__(self, max_documents: int = 2):  # Reduzido para 2 documentos
        self.max_documents = max_documents
        self.model = self._load_model()
        self.qa_pairs = self._load_qa_pairs()
        self.embeddings = self._compute_embeddings()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
    
    @staticmethod
    @st.cache_resource(ttl=3600)  # Cache por 1 hora
    def _load_model():
        model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda' if torch.cuda.is_available() else 'cpu')
        model.max_seq_length = 128  # Reduzir tamanho máximo da sequência
        return model
    
    def _load_qa_pairs(self) -> List[Dict[str, str]]:
        try:
            with open('qa_pairs.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('qa_pairs', [])
        except:
            return []
    
    def _compute_embeddings(self) -> np.ndarray:
        if not self.qa_pairs:
            return np.array([])
        
        # Computar embeddings em batch com tamanho otimizado
        texts = [qa['question'] for qa in self.qa_pairs]
        return self.model.encode(texts, show_progress_bar=False, batch_size=32)
    
    def get_relevant_context(self, query: str, max_documents: int = 2) -> str:
        if not self.qa_pairs:
            return ""
        
        # Computar embedding da query com batch
        query_embedding = self.model.encode([query], show_progress_bar=False, batch_size=1)[0]
        
        # Calcular similaridade com todos os documentos usando GPU se disponível
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Pegar os top-k documentos mais relevantes
        top_k_indices = np.argsort(similarities)[-max_documents:][::-1]
        
        # Construir contexto
        context = ""
        for idx in top_k_indices:
            if similarities[idx] > 0.3:  # Reduzido threshold para 0.3
                qa = self.qa_pairs[idx]
                context += f"Pergunta: {qa['question']}\nResposta: {qa['answer']}\n\n"
        
        return context.strip()
    
    def get_answer(self, query: str) -> List[Dict[str, Any]]:
        if not self.qa_pairs:
            return []
        
        # Computar embedding da query com batch
        query_embedding = self.model.encode([query], show_progress_bar=False, batch_size=1)[0]
        
        # Calcular similaridade com todos os documentos usando GPU se disponível
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Pegar os top-k documentos mais relevantes
        top_k_indices = np.argsort(similarities)[-self.max_documents:][::-1]
        
        # Retornar resultados
        results = []
        for idx in top_k_indices:
            if similarities[idx] > 0.3:  # Reduzido threshold para 0.3
                qa = self.qa_pairs[idx]
                results.append({
                    'question': qa['question'],
                    'answer': qa['answer'],
                    'category': qa['category'],
                    'similarity': float(similarities[idx])
                })
        
        return results

    def add_qa_pair(self, question: str, answer: str, category: str) -> None:
        self.qa_pairs.append({
            'question': question,
            'answer': answer,
            'category': category
        })
        self.embeddings = self._compute_embeddings()
        
        with open('qa_pairs.json', 'w', encoding='utf-8') as f:
            json.dump({'qa_pairs': self.qa_pairs}, f, ensure_ascii=False, indent=4) 