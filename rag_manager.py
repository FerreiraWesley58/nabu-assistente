import os
import json
import re
import numpy as np
import streamlit as st
from typing import List, Dict, Any, Tuple, Optional
from collections import Counter

class RAGManager:
    def __init__(self, qa_file: str = 'qa_pairs.json', max_documents: int = 3):
        self.qa_file = qa_file
        self.max_documents = max_documents
        self.qa_pairs = []
        self.keywords = []
        
        # Carregar dados existentes
        self._load_data()
        
        # Extrair keywords
        self.keywords = self._extract_keywords()
    
    def _load_data(self) -> None:
        try:
            if os.path.exists(self.qa_file):
                with open(self.qa_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and 'qa_pairs' in data:
                        self.qa_pairs = data['qa_pairs']
                    elif isinstance(data, list):
                        self.qa_pairs = data
                    else:
                        self.qa_pairs = []
            else:
                self.qa_pairs = []
        except Exception as e:
            st.warning(f"Erro ao carregar dados: {str(e)}")
            self.qa_pairs = []
    
    def _extract_keywords(self) -> List[Counter]:
        keywords = []
        for qa in self.qa_pairs:
            # Normalizar texto
            text = qa['question'].lower()
            # Remover pontuações
            text = re.sub(r'[^\w\s]', '', text)
            # Extrair palavras com mais de 3 caracteres
            words = [word for word in text.split() if len(word) > 3]
            # Contar frequência das palavras
            word_counts = Counter(words)
            keywords.append(word_counts)
        return keywords
    
    def _compute_similarity(self, query: str) -> List[float]:
        if not self.qa_pairs or not self.keywords:
            return []
        
        # Normalizar query
        query = query.lower()
        query = re.sub(r'[^\w\s]', '', query)
        query_words = [word for word in query.split() if len(word) > 3]
        
        if not query_words:
            return [0] * len(self.qa_pairs)
        
        # Contar frequência das palavras na query
        query_counts = Counter(query_words)
        
        # Calcular similaridade com cada documento
        similarities = []
        for doc_counts in self.keywords:
            if not doc_counts:
                similarities.append(0)
                continue
                
            # Calcular interseção de palavras
            intersection = sum((query_counts & doc_counts).values())
            # Calcular união de palavras
            union = sum(query_counts.values()) + sum(doc_counts.values()) - intersection
            
            # Similaridade de Jaccard ponderada
            if union > 0:
                similarities.append(intersection / union)
            else:
                similarities.append(0)
        
        return similarities
    
    def get_relevant_context(self, query: str, max_documents: int = 2) -> str:
        if not self.qa_pairs:
            return ""
        
        try:
            # Calcular similaridade com todos os documentos
            similarities = self._compute_similarity(query)
            
            if not similarities:
                return ""
                
            # Converter para array numpy para usar argsort
            similarities = np.array(similarities)
            
            # Pegar os top-k documentos mais relevantes
            top_k_indices = np.argsort(similarities)[-max_documents:][::-1]
            
            # Construir contexto
            context = ""
            for idx in top_k_indices:
                if similarities[idx] > 0.1:  # Threshold para similaridade
                    qa = self.qa_pairs[idx]
                    context += f"Pergunta: {qa['question']}\nResposta: {qa['answer']}\n\n"
            
            return context.strip()
        except Exception as e:
            st.warning(f"Erro ao obter contexto relevante: {str(e)}")
            # Fallback: retornar primeiro documento se existir
            if self.qa_pairs:
                qa = self.qa_pairs[0]
                return f"Pergunta: {qa['question']}\nResposta: {qa['answer']}"
            return ""
    
    def get_answer(self, query: str) -> List[Dict[str, Any]]:
        if not self.qa_pairs:
            return []
        
        try:
            # Calcular similaridade com todos os documentos
            similarities = self._compute_similarity(query)
            
            if not similarities:
                return []
                
            # Converter para array numpy para usar argsort
            similarities = np.array(similarities)
            
            # Pegar os top-k documentos mais relevantes
            top_k_indices = np.argsort(similarities)[-self.max_documents:][::-1]
            
            # Retornar resultados
            results = []
            for idx in top_k_indices:
                if similarities[idx] > 0.1:  # Threshold para similaridade
                    qa = self.qa_pairs[idx]
                    results.append({
                        'question': qa['question'],
                        'answer': qa['answer'],
                        'category': qa.get('category', 'geral'),
                        'similarity': float(similarities[idx])
                    })
            
            # Se não encontrou nada, retornar resposta padrão
            if not results and self.qa_pairs:
                qa = self.qa_pairs[0]
                results.append({
                    'question': qa['question'],
                    'answer': "Desculpe, não encontrei uma resposta específica para sua pergunta. Tente reformular ou perguntar sobre outro tema.",
                    'category': qa.get('category', 'geral'),
                    'similarity': 0.1
                })
                
            return results
        except Exception as e:
            st.warning(f"Erro ao obter resposta: {str(e)}")
            # Fallback: retornar resposta genérica
            return [{
                'question': query,
                'answer': "Desculpe, estou enfrentando dificuldades técnicas. Tente novamente mais tarde.",
                'category': 'erro',
                'similarity': 0.0
            }]
  
    def add_qa_pair(self, question: str, answer: str, category: str = 'geral') -> bool:
        try:
            # Adicionar novo par de QA
            new_qa = {
                'question': question,
                'answer': answer,
                'category': category
            }
            self.qa_pairs.append(new_qa)
            
            # Atualizar keywords para o novo par
            self.keywords = self._extract_keywords()
            
            # Salvar dados
            with open(self.qa_file, 'w', encoding='utf-8') as f:
                json.dump(self.qa_pairs, f, ensure_ascii=False, indent=4)
                
            return True
        except Exception as e:
            st.warning(f"Erro ao adicionar par de QA: {str(e)}")
            return False