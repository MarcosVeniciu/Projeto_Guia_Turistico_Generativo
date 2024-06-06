# Projeto Guia Turistico Generativo
Projeto de Desenvolvimento da disciplina CCF726 - Engenharia de Aprendizado de Máquina. Envolvendo a customização de um modelo de IA generativa.
# Definição e escolha do problema
## Ideia
Usar um modelo de IA generativa como o Lhama 2 para auxiliar viajantes na pesquisa e planejamento de viagens turísticas. O sistema terá como funcionalidade principal
a recomendação de hoteis de acordo com as caracteristicas informadas pelo usuario.
## Modelo
O modelo de IA utilizado será o LLaMA 2 da Meta, ele funcionaria como um question answering, onde o ususario entrará com a pergunta e o modelo responderá com base em um
conjunto de documentos que contera a resposta para a pergunta do usuario.

## Dados
Os dados serão ser coletados usando crawler e datasets do ministerio do turismo, como:
* lista de hoteis em cada cidade, disponiveis no https://dados.turismo.gov.br/dataset/
* O crawler pode ser usado para coleta de dados mais detalhados como preço dos hoteis no site do Booking.com.

Os dados seriam limitados a cidade de Cabo Frio no Rio de Janeiro.

## Dataset
### Documentos Sobre os Hoteis
Através das informações coletadas sobre os hoteis, seram criados documentos descrevendo as informações celetadas. De modo que esses documentos serão usados para alimentar o 
Retrieval-Augmented Generation (RAG). Que será usado para fornecer o contexto da pergunta do usuario e gerar a resposta para as perguntas.
Para cada hotel terá um documento.

### Conjunto de Treinamento
Como a quantidade de hoteis coletados não é muito grande. 
Para realizar o fine-tuning do modelo será usado um dataset sintético. Onde as perguntas e respostas serão geradas por um modelo de LLM o Llama 3, para que o modelo usado para responder 
as perguntas possa aprender que tipo de pergunta esperar e como responder.
Desse modo foi gerardo um dataset com 3184 perguntas.
#### Prompt usado
Para gerar as perguntas foi utilizado um prompt padão:

"""Objetivo: Gerar uma lista abrangente de perguntas e respostas para auxiliar turistas na escolha de hotéis no Brasil, abrangendo diferentes cidades e tipos de acomodação.
Regras:
1. Gere texto no formato de perguntas e respostas, semelhante ao exemplo fornecido.
2. As perguntas devem ser claras, concisas e objetivas.
3. As respostas devem ser informativas, completas e relevantes para a pergunta.
4. Use uma linguagem natural e amigável. Mantenha a formatação consistente em todo o texto.
5. Formato: Perguntas identificadas por  **Pergunta:** e Respostas por **Resposta:**
Idioma: Português brasileiro.
6. Abordagem:
	-Considerar a relevância turística de cada cidade e seus principais atrativos.
	-Incluir diferentes tipos de hotéis, desde luxuosos até econômicos, e opções para diversos gostos e orçamentos.
	-Enfatizar informações relevantes para os turistas, como localização, preços, horários, acessibilidade, comodidades, recursos, etc.
	-Destacar hotéis com características únicas ou que oferecem experiências especiais.
	- incluir uma ou mais das caractesristicas importantes
7. Cidades: Qualquer cidade brasileira
8. Caracteristicas importantes:
Tipo de Acomodação: Hotéis: Apartamentos, Quartos em Acomodações Particulares, Casas de hóspedes, Hostel, Alojamentos de Acomodação e Pequeno-almoço, Villas, Barcos
Casas e apartamentos completos: Casas de Férias, Casas de Campo
Comodidades: Estacionamento, Acesso Wi-Fi gratuito, Quartos familiares, Animais de estimação admitidos, Quartos para não fumadores, Piscina, Receção disponível 24 horas,
Transfer (aeroporto), Restaurante, Serviço de quartos, Acessibilidade para cadeira de rodas, Centro de fitness, Spa e centro de bem-estar, Posto de carga para veículos elétricos
Características Adicionais: Banheira de hidromassagem, Ar condicionado, Vista mar, Cozinha, Cozinha/kitchenette, Banheira, Máquina de lavar roupa, Toalhas,Televisão de ecrã plano, Frigorífico,
Roupa de cama, Piscina privada, Varanda, Televisão, Duche, Secretária, Minibar, Secador de cabelo, Aquecimento, Papel higiénico, Cofre, Chaleira elétrica, Tomada perto da cama
Localização: A menos de 1 km
Atividades: Praia, Caminhadas, Mergulho, Pesca, Sauna
9. Quantidade: Gere em portuges 500 perguntas com respostas conforme o exemplo.

Exemplos de perguntas e respostas:

**Pergunta 1:** Quais hotéis em São Paulo oferecem vista panorâmica da cidade?
**Resposta:** São Paulo oferece diversas opções de hotéis com vista panorâmica da cidade, desde hotéis luxuosos como o Hotel Fasano São Paulo e o Rosewood São Paulo, até opções mais econômicas como o Melia Paulista e o Novotel São Paulo Centro. A escolha ideal dependerá do seu orçamento e das suas preferências em relação à localização, serviços e comodidades.
**Pergunta 2:** Quais hotéis em Rio de Janeiro são ideais para casais em lua de mel?
**Resposta:** O Rio de Janeiro oferece diversos hotéis românticos perfeitos para casais em lua de mel, como o Belmond Copacabana Palace, o Fasano Rio de Janeiro e o Santa Teresa Rio MGallery by Sofitel. Esses hotéis oferecem serviços personalizados, ambientes elegantes e vistas deslumbrantes da cidade ou da praia.
**Pergunta 3:** Quais hotéis em Salvador oferecem experiências autênticas da cultura afro-brasileira?
**Resposta:** Salvador é rica em cultura afro-brasileira, e diversos hotéis oferecem a oportunidade de vivenciar essa cultura de perto, como o Hotel Vila Galé Salvador, o Fera Palace Hotel e o Pestana Rio Branco Hotel. Esses hotéis oferecem decoração afro, culinária típica e atividades culturais como capoeira e aulas de culinária.
**Pergunta 4:** Quais hotéis em Brasília são ideais para quem viaja a negócios?
**Resposta:** Brasília oferece diversos hotéis modernos e bem equipados para quem viaja a negócios, como o Grand Hyatt Brasília, o Meliá Brasília e o Windsor Brasília Hotel. Esses hotéis oferecem salas de conferência, Wi-Fi gratuito e serviços de business center.
**Pergunta 5:** Quais hotéis em Florianópolis são perfeitos para quem busca relaxamento à beira-mar?
**Resposta:** Florianópolis é conhecida por suas belas praias, e diversos hotéis oferecem experiências relaxantes à beira-mar, como o Sofitel Guarujá Jurerê, o Laguna Ingleses Hotel e o Mercure Florianópolis Norte. Esses hotéis oferecem acesso direto à praia, spa, piscinas e serviços de lazer.
**Pergunta 6:** Quais hotéis em Fortaleza são ideais para quem busca diversão e aventura?
**Resposta:** Fortaleza oferece diversas opções de hotéis para quem busca diversão e aventura, como o Vila Galé Fortaleza, o Beach Park Acqua Resort e o Hotel Gran Marquise. Esses hotéis oferecem parques aquáticos, atividades de praia, esportes aquáticos e vida noturna agitada.
**Pergunta 7:** Quais hotéis em Curitiba oferecem experiências ecológicas?
**Resposta:** Curitiba é conhecida por seu foco em sustentabilidade, e diversos hotéis oferecem experiências ecológicas, como o Pestana Curitiba, o Hotel Bourbon Curitiba Convention Center e o Hotel Pestana Curitiba. Esses hotéis utilizam práticas sustentáveis.
"""
#### Sobre o dataset gerado
Como a quantidade de perguntas geradas foram muito grande, ocorreu de algumas perguntas serem repetidas algumas vezes, porém as respostas não eram exatamente iguais.
![image](https://github.com/MarcosVeniciu/Projeto_Guia_Turistico_Generativo/assets/42542651/2f64b2a5-c15b-4fc5-9112-31a4236816f3)

## treinamento do Modelo
