from google.genai import types, Client
from sklearn.metrics.pairwise import cosine_similarity
from numpy import array, zeros, argmax
from dotenv import load_dotenv
from os import environ

class model:

    cliente = None
    response_base = None
    knowledge_embeddings = None

    def __init__(self, base, response):
        load_dotenv()

        self.cliente = Client(api_key=environ.get('API_KEY'))

        self.knowledge_base = base

        self.response_base = response

        # Gerar embeddings para a base de conhecimento
        self.knowledge_embeddings = []

        knowledge_response = self.cliente.models.embed_content(model="gemini-embedding-001", contents=self.knowledge_base, config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")).embeddings
        for embedding in knowledge_response:
            self.knowledge_embeddings.append(embedding.values)
        self.knowledge_embeddings = array(self.knowledge_embeddings)

    def answer_question(self, user_question):
        try:
            question_embedding = array(self.cliente.models.embed_content(model="gemini-embedding-001", contents=[user_question], config=types.EmbedContentConfig(task_type="QUESTION_ANSWERING")).embeddings[0].values).reshape(1, -1)
            print(len(self.knowledge_base))
            similarities = zeros((len(self.knowledge_base), 1))
            for index, embedding in enumerate(self.knowledge_embeddings):
                similarities[index] = cosine_similarity(question_embedding, embedding.reshape(1, -1))[0, 0]

            max_similaritie = argmax(similarities)
            max_index = int(max_similaritie)
            if similarities[max_index] < 0.75:
                raise Exception("No similarity")
            most_similar_text = self.response_base[max_index]

            # 4. Apresentar a resposta
            print(f"Resposta mais provável (similaridade: {max_similaritie:.4f}): {most_similar_text}")
            return most_similar_text
        except Exception as e:
            print(f"Ocorreu um erro ao processar a pergunta: {e}")
            print("Não foi possível encontrar uma resposta.")
            return None

base = [
            "Qual é a capital da França?",
            "Quem escreveu 'Dom Quixote'?",
            "Qual o país que tem a forma de uma bota?",
            "Qual é a cidade luz?",
            "Qual o nome do autor de 'Cem Anos de Solidão'?"
           # "Quais projetos com IA fez?",
           # ""
        ]
response = [
        "A capital da França é Paris.",
        "Miguel de Cervantes escreveu 'Dom Quixote'.",
        "A Itália é o país que tem a forma de uma bota.",
        "Paris é conhecida como a Cidade Luz.",
        "Gabriel García Márquez é o autor de 'Cem Anos de Solidão'."
        ]
# Testando o sistema
#embeded = model(base, response)
#embeded.answer_question("Onde fica a Torre Eiffel?")
#embeded.answer_question("Qual a principal cidade francesa?")
#embeded.answer_question("Quem foi o autor de 'Don Quijote'?")
#embeded.answer_question("Qual o livro de cem anos de solidao?")
#embeded.answer_question("Qual a capital da Alemanha?")