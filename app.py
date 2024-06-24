from flask import Flask, request, jsonify
from langchain_community.llms import Ollama
from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate
import gradio as gr

from transformers import pipeline
import unicodedata
from googletrans import Translator
import pickle
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

template="""[INST] example Context: Hotel Costa del Sol, Barcelona. This modern hotel is located near the beach and offers comfortable rooms with balconies and stunning ocean views. The hotel features a swimming pool, restaurant with bar, and free Wi-Fi.
example Question: Is there a gift shop or convenience store available at Hotel Costa del Sol?
example Answer: Although Hotel Costa del Sol does not have an on-site gift shop, the hotel's location near La Rambla and Barceloneta Beach provides easy access to various shops, cafes, and restaurants. You can also take advantage of the hotel's 24-hour reception desk for any assistance with local amenities or recommendations.

example Context:
example Question: Is there free Wi-Fi Beachfront Paradise in Chicago?
example Answer: I don't know the hotel you are looking for, please provide a hotel in Cabo Frio, Rio de Janeiro, Brazil.

example Context: Hotel Fasano, Paris. This luxury hotel offers elegant accommodations with stunning city views. The hotel features a pool, spa and wellness center, gourmet restaurant, fitness center, and 24-hour reception.
example Question: Does Hotel Fasano have a pool available for guests?
example Answer: Yes, Hotel Fasano, Paris features a stunning rooftop pool available for guests. This pool offers breathtaking panoramic views, creating a serene and picturesque setting for relaxation and leisure. Guests can take a refreshing dip or lounge by the poolside while enjoying the beautiful surroundings.

Context:{context}
Question: {question} [/INST]\n"""



llm = LlamaCpp(
    model_path="FP16.gguf",
    temperature=0.3,
    max_tokens=2048,
    top_p=1,
    n_ctx=2048,
    #stop=["[/INST]"],
 # Verbose is required to pass to the callback manager
)

prompt = PromptTemplate.from_template(template)
chain = (prompt | llm)


# Carregar os documentos divididos
with open('Documentos/Chunks_RAG/documents_chunks_20-06-2024.pkl', 'rb') as f:
    docs = pickle.load(f)
print(len(docs))


# Criar embeddings
model_path = "sentence-transformers/all-MiniLM-l6-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_path, model_kwargs={'device': 'cpu'}, encode_kwargs={'normalize_embeddings': False})
db = FAISS.from_documents(docs, embeddings)

# Função para buscar com filtro
def buscar_com_filtro(query, filtro_hotel_name, k=4):
    # Função de filtro que verifica o hotel_name nos metadados
    def filtro(doc):
      return filtro_hotel_name in doc.metadata.get("hotel_name", "")

    # Realizar a busca e filtrar os resultados
    resultados_brutos = db.similarity_search(query, k=k)
    #print(len(resultados_brutos))
    resultados_filtrados = [doc for doc in resultados_brutos if filtro(doc)]

    return resultados_filtrados





model_name = "deepset/tinyroberta-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)


pergunta = "What is the name of the hotel?"

def get_hotel_name(texto):  
    QA_input = {
      'question': pergunta,
      'context': texto
    }
    res = nlp(QA_input)
    
    return res['answer']

def limpar_texto(texto):
  texto = texto.replace('[^\w\s]', '') # Remover caracteres especiais
  texto = texto.lower() # Converter para minúsculas
  return unicodedata.normalize('NFKD', texto).encode('ascii', errors='ignore').decode('utf-8') # Normalizes and removes accents from the text.

def translate_text(text, dest):
    translator = Translator()
    translation = translator.translate(text, dest=dest)
    return translation.text



def fn_chain(context, question):
    return chain.invoke({"context": context, "question":question}).split("[/INST]\n")[1] + ";"


def rag(question):
    filtro_hotel_name = get_hotel_name(question)
    retrieved_docs = buscar_com_filtro(limpar_texto(question), limpar_texto(filtro_hotel_name), k=8)
    real_context = ". ".join([doc.page_content for doc in retrieved_docs])
    return fn_chain(real_context, question)


def get_llm_answer(question):
    question = translate_text(question, 'en')
    resposta = rag(question)
    resposta = translate_text(resposta, 'pt')
    return resposta



# Gradio interface
iface = gr.Interface(
    fn=get_llm_answer,
    inputs=gr.Textbox(lines=2, placeholder="Enter your question here..."),
    outputs="text",
    title="Pesquisa por hoteis em Cabo Frio Rio de Janeiro",
    description="Faça perguntas sobre recursos disponiveis em hoteis como piscina, spa, academie e restaurantes.",
)

# Launch the app
iface.launch(server_name = "0.0.0.0", 
    server_port= 5000)
