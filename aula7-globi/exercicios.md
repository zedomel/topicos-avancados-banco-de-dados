# Lista de Exercícios - Consultas Cypher no GloBI

**Instruções:** Utilize o banco de dados Neo4j do GloBI fornecido para executar as consultas Cypher abaixo. Responda cada questão com base nos resultados obtidos. Preste atenção à sintaxe e aos detalhes do esquema do grafo.

---

## Parte 1 - Consultas Básicas

### Questão 1
**Enunciado:** Liste todas as espécies que estão presentes no banco de dados. Exiba apenas os 10 primeiros resultados com o nome científico de cada uma. Quantas espécies existem no total?

**Dica:** Utilize `MATCH` para encontrar nós do tipo `SPECIES` e `RETURN` para exibir a propriedade `name`.


### Questão 2
**Enunciado:** Encontre a espécie com o nome "Homo sapiens". Quais são as suas propriedades?

### Questão 3
**Enunciado:** Liste todos os tipos de interação (ex: "preysOn", "pollinates") presentes no banco de dados. Quantos tipos diferentes existem?

---

## Parte 2 - Filtros e Condições

### Questão 4
**Enunciado:** Encontre todas as interações do tipo "preysOn" que ocorreram no hemisfério sul. Quantas interações desse tipo foram encontradas? Listar as 10 primeiras interações.

### Questão 5
**Enunciado:** Liste as 10 espécies que servem de alimento (tipo "eats") pelo "Homo sapiens". Exiba o nome da espécie e a localização da interação, se disponível.

### Questão 6
**Enunciado:** Encontre todos os polinizadores (interações do tipo "pollinates") da planta "Coffea arabica". Exiba o nome do polinizador e a fonte dos dados (`source`).

### Questão 7
**Enunciado:** Liste as interações que possuem uma referência contendo a palavra "doi". Exiba o nome das duas espécies envolvidas, o tipo de interação e a referência.


---

## Parte 3 - Ordenação e Limitação

### Questão 8
**Enunciado:** Quais são as 5 espécies com o maior número de interações (considerando tanto como fonte quanto como alvo)? Exiba o nome da espécie e a contagem total de interações.

**Dica:** Utilize `MATCH` para encontrar todos os relacionamentos `INTERACTS_WITH` que envolvem uma espécie, agrupe por espécie e ordene pela contagem.


### Questão 9
**Enunciado:** Liste as 10 interações mais recentes (com base na propriedade `date`). Exiba as espécies envolvidas, o tipo de interação e a data.

**Dica:** Ordene pela propriedade `date` em ordem decrescente.


---

## Parte 4 - Agregações

### Questão 10
**Enunciado:** Quantas interações do tipo "parasiteOf" existem no banco de dados?


### Questão 11
**Enunciado:** Para cada tipo de interação, calcule o número total de ocorrências. Exiba o tipo e a contagem, ordenados da maior para a menor.

**Dica:** Utilize `GROUP BY` (implícito no Cypher com `RETURN` e funções de agregação).


### Questão 12
**Enunciado:** Encontre a espécie que possui a maior quantidade de interações como predador (tipo "preysOn"). Exiba o nome da espécie e o número de presas.

**Dica:** Modele o padrão `(predator:SPECIES)-[:INTERACTS_WITH {type: "preysOn"}]->(prey:SPECIES)` e agrupe por predador.


### Questão 13
**Enunciado:** Liste as 5 espécies com o maior número de interações únicas (distintas) como fonte. Exiba o nome da espécie e a contagem.

**Dica:** Utilize `COUNT(DISTINCT ...)` para contar interações únicas.


---

## Parte 5 - Caminhos e Relacionamentos

### Questão 14
**Enunciado:** Encontre todos os caminhos de até 3 relacionamentos entre "Homo sapiens" e "Panthera tigris". Exiba os caminhos encontrados.

**Dica:** Utilize `MATCH p = (a:SPECIES {name: "Homo sapiens"})-[:INTERACTS_WITH*1..3]-(b:SPECIES {name: "Panthera tigris"}) RETURN p`.


### Questão 15
**Enunciado:** Qual é o caminho mais curto entre "Homo sapiens" e "Escherichia coli"? Exiba os nós e relacionamentos do caminho.

**Dica:** Utilize a função `shortestPath`.


### Questão 16
**Enunciado:** Encontre todas as espécies que estão conectadas a "Homo sapiens" por exatamente 2 relacionamentos (ou seja, espécies que interagem com espécies que interagem com humanos). Exiba o nome dessas espécies.

**Dica:** Utilize `[:INTERACTS_WITH*2]`.


---

## Parte 6 - Consultas Avançadas

### Questão 17
**Enunciado:** Liste os 10 pares de espécies que compartilham o maior número de interações em comum (por exemplo, espécies que interagem com as mesmas outras espécies). Exiba os nomes das duas espécies e a contagem de interações compartilhadas.

**Dica:** Esta consulta é complexa. Considere encontrar, para cada espécie, o conjunto de espécies com as quais ela interage e, em seguida, calcular a interseção entre esses conjuntos.


### Questão 18
**Enunciado:** Crie uma consulta que retorne a "rede" de interações de uma espécie específica (por exemplo, "Vespa velutina"), incluindo todas as espécies com as quais ela interage diretamente e as interações entre essas espécies (subgrafo). Como você faria para visualizar essa rede?


### Questão 19
**Enunciado:** Quantas espécies não possuem nenhuma interação registrada no banco de dados?

**Dica:** Utilize `OPTIONAL MATCH` para encontrar espécies que não têm relacionamentos `INTERACTS_WITH`.


### Questão 20 (Desafio)
**Enunciado:** Identifique a cadeia alimentar mais longa (em número de relacionamentos) presente no banco de dados. Exiba a cadeia completa.

**Dica:** Esta é uma consulta desafiadora. Considere usar `MATCH p = (start:SPECIES)-[:INTERACTS_WITH*]->(end:SPECIES) WHERE NOT (end)-[:INTERACTS_WITH]->() RETURN p ORDER BY length(p) DESC LIMIT 1` para encontrar o caminho mais longo que termina em um nó sem saída.

---

### Questão 21

**Enunciado**: Refaça os cálculos do slide "Cobertura dos Dados (2014)" mas considerando o ano de 2026.

## Entrega

Ao final, os alunos devem entregar um arquivo contendo:

1.  **As respostas para cada questão**, incluindo a consulta Cypher utilizada e o resultado obtido (ou uma descrição do resultado).
2.  **Comentários** sobre as consultas, dificuldades encontradas e aprendizados.

---