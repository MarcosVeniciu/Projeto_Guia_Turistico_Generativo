# Projeto Guia Turistico Generativo
Projeto de Desenvolvimento da disciplina CCF726 - Engenharia de Aprendizado de Máquina. Envolvendo a customização de um modelo de IA generativa.
# Definição e escolha do problema
## Ideia
Usar um modelo de IA generativa como o TinyLlama para auxiliar viajantes na pesquisa por hoteis na cidade de Cabo frio no Rio de Janeiro. O sistema terá como funcionalidade principal
a recomendação de hoteis de acordo com as caracteristicas informadas pelo usuario.
## Modelo
O modelo de IA utilizado será o TinyLlama da Meta, ele funcionaria como um question answering, onde o ususario entrará com a pergunta e o modelo responderá com base em um
conjunto de documentos que contera a resposta para a pergunta do usuario.

## Dados
Os dados serão ser coletados usando crawler e datasets do ministerio do turismo, como:
* lista de hoteis em cada cidade, disponiveis no https://dados.turismo.gov.br/dataset/
* O crawler pode ser usado para coleta de dados mais detalhados como preço dos hoteis no site do Booking.com.
* Documento gerados a partir de paginas html

Os dados seriam limitados a cidade de Cabo Frio no Rio de Janeiro.

## Dataset
### Documentos Sobre os Hoteis
Através das informações coletadas sobre os hoteis, seram criados documentos descrevendo as informações celetadas. De modo que esses documentos serão usados para alimentar o Retrieval-Augmented Generation (RAG). Que será usado para fornecer o contexto da pergunta do usuario e gerar a resposta para as perguntas.
Para cada hotel terá um documento.

### Conjunto de Treinamento
Como a quantidade de hoteis coletados não é muito grande. 
Para realizar o fine-tuning do modelo será usado um dataset sintético. Onde as perguntas e respostas serão geradas por um modelo de LLM o Llama 3, para que o modelo usado para responder as perguntas possa aprender que tipo de pergunta esperar e como responder.
Desse modo foi gerardo um dataset com 28397 perguntas.
A perguntas usadas no dataset tem 3 categorias: 
* Positive Responses: São as perguntas onde existe um contexto valido e o hotel possui o que o usuario esta buscando, como piscina, spar, etc.
* Descriptive Negative Responses: São as pergunta onde exite um ocntexto valido, mas o hotel não possui o que o usuario esta buscando, então na resposta o modelo informa que o hotel não possui o que o usuario quer, mas apresenta os outro recursos do hotel.
* No Context Responses: São as pergunda onde não existe um contexto valido, o que siginfica que não possui nenhum documento no rag com o nome do hotel buscado. 

![image](https://github.com/MarcosVeniciu/Projeto_Guia_Turistico_Generativo/assets/42542651/e44a2333-136c-4c7c-aa26-39e3effc7c9a)

Sendo o datast dividido em:
Total: 28008
Positive Responses: 10246
No Context Responses: 6132
Descriptive Negative Responses: 11630

Ao considerar o contexto, pergunta e resposta, são 20008 perguntas unicas, mas ao considerar cada um deles separadamente havera repetições, pois um mesmo contexto pode ter sido usado para perguntas diferentes.

#### Prompt usado
Para gerar as perguntas foi utilizado dois prompts:
Um para gerar as perguntas em que a respota esta no ocntexto e um para as perguntas que a resposta não tem no contexto, mas o modelo deve gerar uma resposta apresentando os outros recursos disponiveis no hotel.

prompt para as perguntas em que a respota esta no ocntexto
prompt = """**Objective:** Generate a comprehensive list of questions and answers to assist tourists in choosing hotels, covering different cities and types of accommodation.

**Rules:**
1. Generate text in the format of context, questions, and answers, as per the provided example.
2. The questions must be clear, concise, and objective.
3. The context should contain the hotel name, the city name, and a description of the relevant features needed to answer the question.
4. The answers should be descriptive and contain only the information present in the context.
5. Format: The context should be identified by **Context:**, the questions identified by **Question:**, and the answers by **Answer:**
6. Cities: Any city
7. Important features:
Accommodation Types: Hotels: Apartments, Private Accommodation Rooms, Guest Houses, Hostels, Bed and Breakfasts, Villas
Amenities: Parking, Free Wi-Fi access, Family rooms, Pets allowed, Non-smoking rooms, Pool, 24-hour reception, Airport transfer, Restaurant, Room service, Wheelchair accessible, Fitness center, Spa and wellness center, Electric vehicle charging station
Additional Features: Hot tub, Air conditioning, Sea view, Kitchen, Kitchenette, Bathtub, Washing machine, Towels, Flat-screen TV, Refrigerator, Bed linen, Private pool, Balcony, Television, Shower, Desk, Minibar, Hairdryer, Heating, Toilet paper, Safe, Electric kettle, Socket near the bed
Location: Within 1 km
Activities: Beach, Hiking, Diving, Fishing, Sauna

8. Quantity: Generate 20 questions with answers as per the example.

Example:
**Context 1:** Hotel Fasano, São Paulo. This luxury hotel, located in the Jardins neighborhood, offers elegant accommodations with stunning city views. The hotel features a pool, spa and wellness center, gourmet restaurant, fitness center, and 24-hour reception.
**Question 1:** Does Hotel Fasano have a pool available for guests?
**Answer 1:** Yes, Hotel Fasano has a pool available for guests, providing a space for leisure and relaxation with incredible city views.

**Context 2:** Beachliner Hotel, New Jersey. This contemporary hotel, located in the Jardins neighborhood, offers designer accommodations with views of Ibirapuera Park. The hotel features a pool, restaurant, fitness center, and wheelchair accessibility.
**Question 2:** Does  Beachliner Hotel  have facilities for guests with reduced mobility?
**Answer 2:** Yes,  Beachliner Hotel  has wheelchair accessibility, ensuring comfort and convenience for guests with reduced mobility.
"""



prompt para as perguntas que a resposta não tem no contexto, mas o modelo deve gerar uma resposta apresentando os outros recursos disponiveis no hotel
prompt = """**Objective:** Generate a comprehensive list of questions and answers, covering different cities and types of accommodation. Questions should not have a direct answer in context. They should only be questions for which answers are not available in context and that require reasoning or go beyond the information provided, ensuring informative answers even when no direct answer is available.

**Rules:**

1. Generate text in context, question and answer format.

2. Questions must be clear, concise, objective and without a direct answer in context.

3. The context must contain the hotel name, the city name, and a description of the relevant features. But it must NOT have the characteristic that answers the question, or that is relevant to the question.

4. Answers must be informative and useful, presenting the other attractions available at the hotel:
   Questions without a direct answer in context.:
     - Recognize what is missing and suggest related amenities or alternatives.
     - Highlight other relevant features that may be of interest to the guest.
5. Format: The context must be identified by **Context:**, the questions identified by **Question:** and the answers by **Answer:**

6. Cities: Any city

7. Important features:
Accommodation Types: Hotels: Apartments, Private Accommodation Rooms, Guest Houses, Hostels, Bed and Breakfasts, Villas
Amenities: Parking, Free Wi-Fi access, Family rooms, Pets allowed, Non-smoking rooms, Pool, 24-hour reception, Airport transfer, Restaurant, Room service, Wheelchair accessible, Fitness center, Spa and wellness center, Electric vehicle charging station
Additional Features: Hot tub, Air conditioning, Sea view, Kitchen, Kitchenette, Bathtub, Washing machine, Towels, Flat-screen TV, Refrigerator, Bed linen, Private pool, Balcony, Television, Shower, Desk, Minibar, Hairdryer, Heating, Toilet paper, Safe, Electric kettle, Socket near the bed
Location: Within 1km
Activities: Beach, Hiking, Diving, Fishing, Sauna

8. Quantity: Generate 4 questions with answers according to examples.

Examples:

**Context 1:** Hotel Oasis, Rio de Janeiro. This beachfront hotel offers comfortable rooms with balconies and stunning ocean views. The hotel has a swimming pool, restaurant with bar and free Wi-Fi.
**Question 1:** Does Hotel Oasis have a gym available to guests?
**Answer 1:** Although Hotel Oasis does not have an on-site gym, it does offer a refreshing pool and a communal lounge with a relaxing atmosphere, perfect for unwinding after a day exploring Rio.

**Context 2:** Cozy Mountain Lodge, Colorado. This rustic lodge in the mountains offers cabins with fireplaces and a cozy atmosphere. The chalet features a hot tub, on-site ski rental and a shared lounge with a fireplace.
**Question 2:** Does Cozy Mountain Lodge offer in-room dining services?
**Answer 2:** Cozy Mountain Lodge does not offer in-room dining services. However, the accommodation has a fully equipped kitchen in each cabin, allowing you to prepare your own meals with the convenience of in-room dining.

**Context 3:** City Central Apartments, London. These modern, fully equipped apartments are located in the heart of London, close to many attractions. Apartments feature a washing machine, fully equipped kitchen and free Wi-Fi.
**Question 3:** Is there a spa available at City Central Apartments?
**Answer 3:** Although City Central Apartments does not have an on-site spa, it does offer guests easy access to a variety of nearby spas and wellness centers in the heart of London. You can relax and rejuvenate with a range of treatments and services within a short walk or drive.

**Context 4:** Hotel Costa del Sol, Barcelona. This modern hotel is located near the beach and offers comfortable rooms with balconies and stunning ocean views. The hotel features a swimming pool, restaurant with bar, and free Wi-Fi.

**Question 4:** Does Hotel Costa del Sol offer any activities for children?
**Answer 4:** While Hotel Costa del Sol does not have specific kids' clubs or programs, the hotel's beachfront location provides plenty of opportunities for family fun in the sun. You can also take a short walk to nearby attractions like Barceloneta Beach and Port Vell.

**Context 5:** Villa Vita, Milan. This luxurious villa offers private pools and stunning views of the city skyline. The villa features a fitness center, spa, and free Wi-Fi.

**Question 5:** Is there a laundry service available at Villa Vita?
**Answer 5:** Although Villa Vita does not have an on-site laundry facility, you can easily access nearby laundromats or ask the hotel staff for assistance with washing your clothes. The villa also provides towels and linens for your convenience.
"""

#### Retrieval-Augmented Generation (RAG)
Para a contrução do Retrieval-Augmented Generation (RAG), a apartir dos nomes dos hoteis encontrado na cidade de Cabo frio, foi realizada um busca na internet em sites de hoteis. Foram usados dois sitem como base de dados, o booking.com e o almosafer.com.
Apos recuperar uma lista com os links das paginas,foi realizado o download das paginas html. as paginas foram convertidas para pdf e foi extraido o texto presente neles.
Para melhorar a qulidade do texto, removendo palavras mau formatadas e simbolos aleatorios foi usado um modelo de sumariazação para extrair as informações mais relevantes dos texto.
os textos estavam em varios idiomas, então todos foram traduzidos para o ingles, que é o idioma em que o modelo foi treinado.
Então esses textos foram salvos em arquivos txt para serem lidos pelo RAG.
Como todos os documentos são referenstes a hoteis e eles possuem muitas informações em comum, frequentemente o RAG retornava documentos referentes a hoteis diferenstes, justamente por terem muito em comum.
Para resolver esse problema alem da busca por similaridade, foi aplicado um filtro, que selecionava apenas os documentos referente ao hotel buscado.
Para isso na pergunta do usuario é usado um modelo para identificar o nome do hotel, que sera usado no filtro.

## treinamento do Modelo
O modelo foi treinado usando como base o tinyllama que é um modelo com 1B de parâmetros, ele foi treinado por um todal de 150 epocas, com um batch size de 64. e um total de 66.450 pasos.
