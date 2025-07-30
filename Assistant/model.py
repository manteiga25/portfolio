from google.genai import types, Client
from sklearn.metrics.pairwise import cosine_similarity
from numpy import array, zeros, argmax
from dotenv import load_dotenv
from os import environ

class model:

    cliente = None
    knowledge_base = None
    response_base = None
    knowledge_embeddings = None

    num_responses = 0

    def __init__(self, base, response):
        load_dotenv()

        self.cliente = Client(api_key=environ.get('API_KEY'))

        self.knowledge_base = base

        self.response_base = response

        self.num_responses = len(response)

        # Gerar embeddings para a base de conhecimento
        self.knowledge_embeddings = []

        knowledge_response = self.cliente.models.embed_content(model="gemini-embedding-001", contents=self.knowledge_base, config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")).embeddings
        for embedding in knowledge_response:
            self.knowledge_embeddings.append(embedding.values)
        self.knowledge_embeddings = array(self.knowledge_embeddings)

    def answer_question(self, user_question):
        try:
            question_embedding = array(self.cliente.models.embed_content(model="gemini-embedding-001", contents=[user_question], config=types.EmbedContentConfig(task_type="QUESTION_ANSWERING")).embeddings[0].values).reshape(1, -1)
            similarities = zeros(self.num_responses, 1)
            for index, embedding in enumerate(self.knowledge_embeddings):
                similarities[index] = cosine_similarity(question_embedding, embedding.reshape(1, -1))[0, 0]

            max_similaritie = argmax(similarities)
            max_index = int(max_similaritie)
            if similarities[max_index] < 0.75:
                raise Exception("No similarity")
            most_similar_text = self.response_base[max_index]

            return most_similar_text
        except Exception:
            return None