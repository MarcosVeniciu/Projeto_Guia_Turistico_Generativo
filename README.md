# Projeto Guia Turistico Generativo
Projeto de Desenvolvimento da disciplina CCF726 - Engenharia de Aprendizado de Máquina. Envolvendo a customização de um modelo de IA generativa.
# Definição e escolha do problema
## Ideia
Usar um modelo de IA generativa como o Lhama 2 para auxiliar viajantes na pesquisa e planejamento de viagens turísticas. O sistema terá duas funcionalidades principais:
1. Recomendação de destinos: A IA recomendará cidades para o usuário.
2. Informações sobre cidades e pontos turísticos: O usuário poderá pesquisar por informações sobre cidades e pontos turísticos.

## Modelo
O modelo de IA utilizado será o LLaMA 2 da Meta, ele funcionaria como um chat.

## Dados
Os dados serão ser coletados usando crawler e datasets do ministerio do turismo, como:
* hoteis, parques aquaticos, restaurantes, acampamentos, locadora de veiculos, disponiveis no https://dados.turismo.gov.br/dataset/
* O crawler pode ser usado para coleta de dados mais detalhados como preço dos hoteis no site do TripAdvisor

Os dados seriam limitados a algumas cidades que tenham foco em turismo, e alguns tipos específicos de pontos turisticos para simplificar a coleta de dados.
