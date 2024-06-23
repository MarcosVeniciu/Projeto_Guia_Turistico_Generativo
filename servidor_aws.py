from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from transformers import logging, pipeline
import pickle
import unicodedata
import torch
import gradio as gr
from googletrans import Translator
from transformers.trainer_utils import get_last_checkpoint




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

# Função para formatar o texto de entrada
def format_text(context, question):
    formatted_text = (
                    f"example Context: {context_1}\n"
                    f"example Question: {question_1}\n"
                    f"example Answer: {answer_1}\n\n"
                    f"example Context: {context_2}\n"
                    f"example Question: {question_2}\n"
                    f"example Answer: {answer_2}\n\n"
                    f"example Context: {context_3}\n"
                    f"example Question: {question_3}\n"
                    f"example Answer: {answer_3}\n\n"
                    f"Context: {context}.\n"
                    f"Question: {question}")
    return limpar_texto(formatted_text)



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




# Ignore warnings
logging.set_verbosity(logging.CRITICAL)

project_dir = "checkpoint"

last_checkpoint = get_last_checkpoint(project_dir)
device = 0 if torch.cuda.is_available() else -1 # Definir o dispositivo, 0 para GPU
print(f"checkpoint usado: {last_checkpoint}")
# Run text generation pipeline with our next model
pipe = pipeline(task="text-generation", model=last_checkpoint, tokenizer=last_checkpoint, device=device)




from transformers import BitsAndBytesConfig, AutoModelForCausalLM, AutoTokenizer
compute_dtype = getattr(torch, "float16")

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=False,
)
base_model ='TinyLlama/TinyLlama_v1.1'
model = AutoModelForCausalLM.from_pretrained(base_model, quantization_config=quant_config, device_map={"": 0})

max_length = 2048 # valor usado no treinamento do tinyllama


tokenizer = AutoTokenizer.from_pretrained(base_model,
                                        trust_remote_code=True,
                                        max_length= max_length, 
                                        truncation=True)
    
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"



context_1 = ("Hotel Costa del Sol, Barcelona. This modern hotel is located near the beach and offers comfortable rooms with balconies and stunning ocean views. The hotel features a swimming pool, restaurant with bar, and free Wi-Fi.")
question_1 = ("Is there a gift shop or convenience store available at Hotel Costa del Sol?")
answer_1 = ("Although Hotel Costa del Sol does not have an on-site gift shop, the hotel's location near La Rambla and Barceloneta Beach provides easy access to various shops, cafes, and restaurants. You can also take advantage of the hotel's 24-hour reception desk for any assistance with local amenities or recommendations.")

context_2 =  (" ")
question_2 = ("Is there free Wi-Fi Beachfront Paradise in Chicago?")
answer_2 = ("I don't know the hotel you are looking for, please provide a hotel in Cabo Frio, Rio de Janeiro, Brazil.")

context_3 = ("Hotel Fasano, Paris. This luxury hotel offers elegant accommodations with stunning city views. The hotel features a pool, spa and wellness center, gourmet restaurant, fitness center, and 24-hour reception.")
question_3 = ("Does Hotel Fasano have a pool available for guests?")
answer_3 = ("Yes, Hotel Fasano, Paris features a stunning rooftop pool available for guests. This pool offers breathtaking panoramic views, creating a serene and picturesque setting for relaxation and leisure. Guests can take a refreshing dip or lounge by the poolside while enjoying the beautiful surroundings.")




from peft import get_peft_model
from peft import LoraConfig

lora_config = LoraConfig.from_pretrained('Modelo Lora/modelo_final')
llm_text_generation = get_peft_model(model, lora_config)

def llm(formatted_input):
    device = 0
    inputs = tokenizer(f"<s>[INST] {formatted_input} [/INST]\n", return_tensors="pt").to(device)
    outputs = llm_text_generation.generate(**inputs, max_new_tokens=70)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    #print(result)
    resposta = result.split("[/INST]\nanswer:")
    return resposta[1]
    
def rag(question):
    filtro_hotel_name = get_hotel_name(question)
    retrieved_docs = buscar_com_filtro(limpar_texto(question), limpar_texto(filtro_hotel_name), k=8)
    real_context = ". ".join([doc.page_content for doc in retrieved_docs])
    formatted_input = format_text(real_context, question)
    return llm(formatted_input)

# Define the Gradio interface
def get_llm_answer(question):
    question = translate_text(question, 'en')
    resposta = rag(question)
    resposta = translate_text(resposta, 'pt')
    return resposta

# Create a Gradio app interface
iface = gr.Interface(
  fn=get_llm_answer,
  inputs=gr.Textbox(lines=2, placeholder="Enter your question here..."),
  outputs="text",
  title="Pesquisa por hoteis em Cabo Frio Rio de Janeiro",
  description="Faça perguntas sobre recursos disponiveis em hoteis como piscina, spa, academie e restaurantes.",
)

# Launch the Gradio app
iface.launch(share=True, server_name = "0.0.0.0", server_port= 5000)