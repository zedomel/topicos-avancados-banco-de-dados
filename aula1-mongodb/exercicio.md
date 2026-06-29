# Laboratório de MongoDB com Atlas Sample Data (sample_mflix)

## 1. Contexto do laboratório

Você foi contratado como analista de dados de uma plataforma de streaming de filmes.  
Sua tarefa é explorar o **banco de dados `sample_mflix` do MongoDB Atlas**, que contém informações sobre filmes, cinemas, usuários e comentários, para responder perguntas de negócio usando consultas e agregações em MongoDB.

Documentação oficial do dataset `sample_mflix`:  
[https://www.mongodb.com/pt-br/docs/atlas/sample-data/sample-mflix/](https://www.mongodb.com/pt-br/docs/atlas/sample-data/sample-mflix/)

Este laboratório é totalmente prático: cada questão pede que você escreva **consultas ou pipelines de agregação** para obter respostas específicas.  
Em algumas questões você também deverá propor e testar **índices** e analisar planos de execução com `explain()`.

---

## 2. Pré‑requisitos

- Conhecimentos básicos de:
  - Modelo de documentos do MongoDB.
  - Comandos `find()`, operadores de filtro, projeção e ordenação.
  - Pipeline de agregação (`$match`, `$group`, `$project`, `$sort`, `$lookup`, `$unwind`, etc.).
  - Conceitos de índice e leitura de `explain()`.

- Acesso a um cluster MongoDB Atlas com os **datasets de amostra carregados**, incluindo o banco `sample_mflix`.

Página de sample data do Atlas (como carregar os datasets de exemplo):  
[https://www.mongodb.com/docs/atlas/sample-data/](https://www.mongodb.com/docs/atlas/sample-data/)

---

## 3. Estrutura do banco `sample_mflix` (visão geral)

O banco de dados `sample_mflix` inclui, entre outras, as seguintes coleções principais:

- `movies`: informações gerais sobre filmes.
- `comments`: comentários de usuários sobre filmes.
- `theaters`: informações sobre cinemas (localização, endereço, etc.).
- `users`: dados básicos de usuários.

Documentação detalhada do sample_mflix (em inglês e português):  
[https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/](https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/)  
[https://www.mongodb.com/pt-br/docs/atlas/sample-data/sample-mflix/](https://www.mongodb.com/pt-br/docs/atlas/sample-data/sample-mflix/)

A seguir, uma visão simplificada de campos relevantes (nem todos os campos estão listados):

### 3.1. Coleção `movies`

Exemplos de campos importantes (veja o schema real com `db.movies.findOne()`):

- `_id`: identificador interno (ObjectId).
- `title`: título do filme (string).
- `year`: ano de lançamento (number).
- `runtime`: duração em minutos (number).
- `genres`: lista de gêneros (array de strings).
- `countries`: lista de países de produção (array de strings).
- `directors`: lista de diretores (array de strings).
- `cast`: lista de atores (array de strings).
- `plot`: sinopse/descrição (string).
- `rated`: classificação indicativa (string, ex.: "PG-13").
- `imdb`: subdocumento com campos como:
  - `rating`: nota média (number).
  - `votes`: quantidade de votos (number).
- `awards`: subdocumento com informações sobre prêmios e indicações (por exemplo, número de vitórias e nomeações).

> Observação: verifique o schema exato da sua instância usando `db.movies.findOne()` em Atlas ou Compass.

### 3.2. Coleção `comments`

Campos principais:

- `_id`: identificador interno.
- `movie_id`: referência para `_id` do filme correspondente (ObjectId).
- `name`: nome do usuário que comentou.
- `email`: e‑mail do usuário.
- `text`: texto do comentário.
- `date`: data/hora do comentário (ISODate).

### 3.3. Coleção `theaters`

Campos principais:

- `_id`: identificador interno.
- `theaterId`: identificador numérico/textual do cinema.
- `location`: subdocumento de localização, incluindo:
  - `address` (rua, cidade, estado, etc.).
  - `geo`: coordenadas geográficas (GeoJSON).
- Outros metadados do cinema.

---

## 4. Regras gerais do exercício

1. Para **cada questão**, escreva:
   - A consulta ou pipeline de agregação.
   - Uma breve explicação do raciocínio (por que usou cada estágio/operador).
   - Se aplicável, índices sugeridos e análise do `explain()`.

2. Sempre que possível:
   - Utilize **pipeline de agregação** para perguntas que envolvam agrupamentos, ordenações complexas ou cálculos.
   - Pense em **eficiência**: não apenas obtenha a resposta, mas considere se sua consulta escala para grandes volumes.

3. Não modifique os dados permanentemente, a menos que a questão peça explicitamente (este laboratório é focado em leitura, não em escrita).

---

## 5. Parte A – Consultas básicas em `movies`

### Q1. Filmes recentes (pós‑2010)

Liste os **10 filmes mais recentes** (maior `year`) lançados após 2010, mostrando:

- título,
- ano,
- nota `imdb.rating`.

Ordene por ano decrescente e, em caso de empate, por `imdb.rating` decrescente.

**Tarefas:**

- Escrever uma consulta `find()` com:
  - filtro por `year > 2010`,
  - projeção dos campos relevantes,
  - ordenação,
  - `limit(10)`.

---

### Q2. Filmes longos com prêmios

Encontre filmes com:

- `runtime` maior que 140 minutos,
- **pelo menos um prêmio** (com base nos campos em `awards`, como número de vitórias ou indicações).

Mostre:

- título,
- runtime,
- resumo de prêmios (campo de `awards` que julgar mais relevante).

**Tarefas:**

- Escrever uma consulta que filtre por `runtime > 140` e por algum atributo em `awards`.
- Justificar como inferiu “pelo menos um prêmio” olhando o schema ou um exemplo de documento.

---

### Q3. Filmes por gênero e rating

Para um gênero específico (por exemplo, `"Drama"`), exiba os filmes desse gênero com:

- título,
- ano,
- `imdb.rating`.

Ordene por `imdb.rating` decrescente e limite a 20 resultados.

**Tarefas:**

- Escrever a consulta `find()` com filtro em `genres` (array).
- Explicar a diferença entre usar `genres: "Drama"` vs operadores de array mais avançados (como `$in`).

---

### Q4. Filmes por país e intervalo de anos

Para um país escolhido (por exemplo, `"Brazil"` ou `"USA"`), liste os filmes produzidos nesse país entre 1990 e 2010 (inclusive).  
Mostre título, ano e países (`countries`).

**Tarefas:**

- Consulta com filtro de intervalo em `year` e inclusão do país em `countries`.
- Ordenar os resultados por ano crescente.

---

### Q5. Busca por palavra‑chave na sinopse

Encontre filmes cuja sinopse (`plot`) contém uma determinada palavra‑chave (por exemplo, `"war"`, `"love"`, `"science"`).

**Versão básica:**

- Usar um filtro simples com regex.

**Versão avançada (opcional):**

- Criar um índice de texto em `title` e `plot`, e usar uma consulta `$text`.

**Tarefas:**

- Fornecer ambas versões (regex e `$text`).
- Comentar vantagens e desvantagens de cada abordagem.

---

## 6. Parte B – Agregações em `movies`

### Q6. Anos com mais lançamentos

Calcule quantos filmes foram lançados em cada ano e retorne os **10 anos com maior número de filmes**.

**Tarefas:**

- Pipeline de agregação com:
  - `$match` (opcional, se quiser restringir a um intervalo),
  - `$group` por `year` para contar,
  - `$sort` por contagem decrescente,
  - `$limit(10)`.

---

### Q7. Média de rating por gênero

Calcule a **média de `imdb.rating` por gênero**, considerando apenas filmes que possuem rating definido.

**Tarefas:**

- Usar `$unwind` em `genres` para tratar arrays.
- Agrupar por gênero com `$group` e calcular média.
- Ordenar os gêneros por média decrescente.

---

### Q8. Diretores mais produtivos

Encontre os **10 diretores** com maior número de filmes no catálogo.

**Tarefas:**

- `$unwind` em `directors`.
- `$group` por diretor contando filmes.
- `$sort` por contagem decrescente, `limit(10)`.
- Propor uma métrica adicional (por exemplo, média de rating por diretor).

---

### Q9. Países mais presentes

Liste os países que aparecem com maior frequência na produção de filmes (independente do ano).

**Tarefas:**

- `$unwind` em `countries`.
- `$group` por país contando filmes.
- Ordenar por contagem decrescente.
- Comentar resultados (quais países dominam o catálogo).

---

### Q10. Duração média por década

Defina “década” a partir do ano (por exemplo, 1990–1999 = década 1990).

Calcule a **duração média (`runtime`) por década**.

**Tarefas:**

- Criar um campo “decada” em `$project` usando uma fórmula (ex.: `year - (year % 10)`).
- Agrupar por década com `$group`.
- Calcular média de `runtime` e ordenar por década crescente.

---

## 7. Parte C – Arrays, joins e comentários (`comments`)

### Q11. Quantidade de gêneros distintos

Use `$unwind` em `genres` para descobrir **quantos gêneros distintos** existem na coleção `movies`.

**Tarefas:**

- `$unwind` em `genres`.
- `$group` por `genres` para obter lista de gêneros únicos.
- `$count` ou `$group` adicional para obter total de gêneros.

---

### Q12. Filmes com mais comentários

Utilizando `comments` e `movies`, encontre os **20 filmes com maior número de comentários**.

**Tarefas:**

- Pipeline que comece em `comments`.
- `$group` por `movie_id` contando comentários.
- `$sort` por contagem decrescente.
- `$lookup` para buscar título em `movies` (join entre `comments.movie_id` e `movies._id`).
- Projeção final com título e número de comentários.

---

### Q13. “Hidden gems”: alta nota, poucos comentários

Defina “hidden gems” como filmes com:

- `imdb.rating` alto (por exemplo, ≥ 8),
- **poucos comentários** (por exemplo, menos de 5 comentários).

Encontre esses filmes.

**Tarefas:**

- Fazer join entre `movies` e `comments` via `$lookup`.
- Calcular número de comentários por filme.
- Filtrar por rating alto e poucos comentários.
- Ordenar por rating decrescente, mostrar título, rating e contagem de comentários.

---

### Q14. Densidade de comentários por ano

Para cada ano, calcule:

- número de filmes lançados,
- número total de comentários,
- **média de comentários por filme**.

**Tarefas:**

- Agregar comentários por `movie_id` e depois associar ao ano (via join com `movies`).
- Agrupar por `year`, contando filmes e somando comentários.
- Calcular média (`total_comentarios / qtd_filmes`) em `$project` ou `$addFields`.

---

## 8. Parte D – Desafios avançados em `movies` + `comments`

### Q15. Gênero com maior rating entre filmes populares

Defina “filmes populares” como aqueles com:

- `imdb.votes` ≥ 1000.

Entre esses filmes, encontre:

- o gênero com maior **média de `imdb.rating`**.

**Tarefas:**

- `$match` por `imdb.votes` ≥ 1000.
- `$unwind` em `genres`.
- `$group` por gênero calculando média de rating.
- Ordenar e pegar o primeiro gênero (melhor média).

---

### Q16. Crescimento de lançamentos por ano

Calcule o número de filmes lançados por ano e identifique anos em que houve **crescimento > 20%** em relação ao ano anterior.

**Tarefas:**

- `$group` por `year` contando filmes.
- Ordenar por `year` crescente.
- Usar `$setWindowFields` (se disponível na versão) ou algum artifício (ex.: `$group` + pós‑processamento ou `$function`) para comparar com o ano anterior.
- Filtrar anos com crescimento percentual acima do limiar.

---

### Q17. Top 5 filmes por ano

Para cada ano, liste os **5 filmes com maior `imdb.rating`**.

**Tarefas (opções):**

- Usar `$setWindowFields` com partição por `year` e ordenação por rating, filtrando `rank ≤ 5`.
- Ou agrupar por ano, ordenar filmes por rating e usar operador de slice / array para pegar top 5.
- Projeção final com ano, título e rating.

---

### Q18. Outliers de runtime vs rating

Encontre filmes com:

- runtime muito alto e rating baixo (por exemplo, `runtime ≥ 150` e `imdb.rating < 6`),  
  **ou**
- runtime muito baixo e rating alto (`runtime ≤ 80` e `imdb.rating ≥ 8`).

**Tarefas:**

- Escrever uma condição composta com `$or`.
- Projeção com título, runtime e rating.
- (Opcional) adicionar um campo “tipo_outlier” indicando qual dos dois casos o filme se enquadra.

---

### Q19. Relatório de densidade de filmes por ano

Monte um relatório que para cada ano mostre:

- número de filmes,
- média de rating,
- total de comentários,
- média de comentários por filme.

**Tarefas:**

- Combinar lógicas de Q6, Q14 e Q18.
- Pode começar agregando `movies` e juntando com dados agregados de `comments` por `movie_id`.
- Finalizar com um `$project` consolidando métricas.

---

## 9. Parte E – Índices e desempenho

Nesta parte, além de obter os resultados corretos, você deve pensar sobre **desempenho**.

### Q20. Índice para consultas por ano, gênero e rating

Proponha um índice para consultas frequentes do tipo:

> Buscar filmes de um dado gênero em um intervalo de anos, ordenados por `imdb.rating` decrescente.

**Tarefas:**

- Sugerir um índice composto (por exemplo, em `genres`, `year` e `imdb.rating`).
- Justificar a ordem dos campos no índice.
- Mostrar uma consulta de exemplo e o plano de execução `explain()` antes e depois de criar o índice.

---

### Q21. Comparando desempenho com e sem índice

Escolha uma consulta relativamente pesada (por exemplo, filtro por gênero + intervalo de anos + ordenação por rating) e:

1. Execute com **apenas índices default**.
2. Execute após criar um índice otimizado.

Compare:

- `executionStats.totalDocsExamined`,
- `executionStats.executionTimeMillis`.

**Tarefas:**

- Mostrar dois planos de execução.
- Comentar a diferença e impacto do índice.

---

### Q22. Índice composto para cast + rating

Suponha que você precise frequentemente buscar filmes em que um determinado ator (`cast`) participou e ordenar por `imdb.rating` desc.

Proponha um índice e teste.

**Tarefas:**

- Criar índice em `cast` e `imdb.rating` (pensar na ordem).
- Mostrar uma consulta exemplo.
- Explicar como o índice ajuda na ordenação e filtragem.

---

### Q23. Índice de texto para título e plot

Crie um índice de texto combinando `title` e `plot`.

Use esse índice para responder:

> “Quais filmes têm título ou sinopse fortemente relacionados a `<palavra-chave>`?”

Documentação sobre índices de texto (MongoDB manual):  
[https://www.mongodb.com/docs/manual/core/index-text/](https://www.mongodb.com/docs/manual/core/index-text/)

**Tarefas:**

- Criar o índice de texto (`db.movies.createIndex({ title: "text", plot: "text" })`).
- Executar uma consulta `$text` com `$search`.
- Ordenar por score de texto (`$meta: "textScore"`) e discutir os resultados.

---

## 10. Entregáveis

Para concluir o laboratório, o aluno deve entregar:

1. Um arquivo (ou repositório) com:
   - Todas as consultas `find()` e pipelines de agregação usados.
   - Scripts de criação de índices.
   - Comandos `explain()` relevantes (ou trechos dos planos de execução).

2. Um pequeno relatório (markdown ou PDF) com:
   - Explicação das principais decisões (por que escolheu certos índices, por que ordenou os estágios da agregação daquela forma).
   - Interpretação de alguns resultados de negócio:
     - Anos com mais lançamentos.
     - Gêneros com melhor performance média.
     - Países dominantes.
     - Exemplos de “hidden gems” encontrados.
