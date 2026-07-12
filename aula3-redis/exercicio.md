# Exercícios Práticos de Redis

## Pré-requisitos

1.  Um banco de dados **Redis Stack** (inclui RedisJSON, RedisTimeSeries, RedisBloom, RediSearch). O plano gratuito do Redis Cloud (limite de 30 MB) é perfeito.
2.  Python 3.8+ com o pacote `redis`:

    ```
    pip install redis hiredis typing_extensions
    ```

3.  Execute o script de geração de dados `generate_data.py` (fornecido) **uma vez** para popular todas as chaves.

---

## Script de Geração de Dados

O script `generate_data.py` utiliza as variáveis de ambiente `REDIS_HOST`, `REDIS_PORT` e `REDIS_PASSWORD`. O total de memória utilizado fica seguramente abaixo de 30 MB.

Execute-o com:

```
export REDIS_HOST=seu-host-cloud
export REDIS_PORT=12345
export REDIS_PASSWORD=sua-senha
python generate_data.py
```

---

# Exercícios

Para cada pergunta, utilize a documentação do Redis para encontrar o comando apropriado. Escreva sua resposta baseada no resultado obtido.

## 1\. Strings

| #   | Pergunta                                                                               |
| --- | -------------------------------------------------------------------------------------- |
| 1   | Recupere o valor armazenado na chave `usuario:1000:nome`.                              |
| 2   | Qual é o comprimento (em bytes) do valor da string em `pagina:inicio:html`?            |
| 3   | Incremente o valor inteiro em `contador_visitantes` em 1 e depois leia o novo valor.   |
| 4   | Extraia e escreva os primeiros 31 caracteres da chave `frase`.                         |
| 5   | Aumente o número em `config:conexoes_maximas` em 200 e depois verifique o valor final. |

## 2\. Geoespacial

| #   | Pergunta                                                                                                                                          |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Recupere a longitude e a latitude do membro `estacao_10` no conjunto `postos_gasolina`.                                                           |
| 2   | Calcule a distância em quilômetros entre `estacao_10` e `estacao_25`.                                                                             |
| 3   | Encontre todas as estações em um raio de 2 km do ponto longitude -46.65, latitude -23.55. Quantas estações são retornadas e quais são seus nomes? |
| 4   | Entre as estações encontradas na pergunta 3, qual é a mais distante do centro?                                                                    |

## 3\. Hashes

| #   | Pergunta                                                                                                             |
| --- | -------------------------------------------------------------------------------------------------------------------- |
| 1   | Obtenha o nome do produto `1002` a partir de seu hash `produto:1002`.                                                |
| 2   | Recupere todos os campos e valores do hash `produto:1003`.                                                           |
| 3   | Busque tanto o preço quanto o estoque atual do produto `1001` em uma única operação.                                 |
| 4   | Reduza o estoque do produto `1001` em 5 (o estoque está armazenado como um inteiro). Qual é o novo valor do estoque? |
| 5   | O hash `produto:1002` contém um campo chamado `desconto`? (sim/não)                                                  |

## 4\. JSON

| #   | Pergunta                                                                                                               |
| --- | ---------------------------------------------------------------------------------------------------------------------- |
| 1   | Recupere o nome do funcionário armazenado na chave JSON `func:1`.                                                      |
| 2   | Qual é o salário do funcionário em `func:2`?                                                                           |
| 3   | Acrescente a habilidade `"Docker"` ao array `habilidades` de `func:1` e depois liste todas as habilidades de `func:1`. |
| 4   | Quantos campos de nível superior (chaves do objeto) o documento JSON `func:1` possui?                                  |
| 5   | Aumente o salário de `func:1` em 5000. Qual é o novo salário?                                                          |

## 5\. Listas

| #   | Pergunta                                                                                                                 |
| --- | ------------------------------------------------------------------------------------------------------------------------ |
| 1   | Descubra quantos elementos existem na lista `logins_recentes`.                                                           |
| 2   | Retorne o elemento no início (mais à esquerda) da lista `logins_recentes`.                                               |
| 3   | Recupere os últimos 5 elementos da lista `logins_recentes`.                                                              |
| 4   | Remova e retorne o primeiro elemento (mais à esquerda) de `logins_recentes` e depois verifique quantos elementos restam. |

## 6\. Conjuntos (Sets)

| #   | Pergunta                                                                                 |
| --- | ---------------------------------------------------------------------------------------- |
| 1   | Quantos membros o conjunto `tags:noticias` contém?                                       |
| 2   | A tag `redis` é um membro de `tags:noticias`?                                            |
| 3   | Liste todos os membros de `tags:artigo:1`.                                               |
| 4   | Encontre as tags que estão presentes tanto em `tags:artigo:1` quanto em `tags:artigo:2`. |
| 5   | Quais tags estão em `tags:artigo:1` mas **não** estão em `tags:artigo:2`?                |

## 7\. Conjuntos Ordenados (Sorted Sets)

| #   | Pergunta                                                                                                      |
| --- | ------------------------------------------------------------------------------------------------------------- |
| 1   | Determine o número de jogadores no `ranking`.                                                                 |
| 2   | Qual é a pontuação do `jogador_23`?                                                                           |
| 3   | Quando o ranking é ordenado da menor para a maior pontuação, qual é a posição (baseada em 0) do `jogador_23`? |
| 4   | Mostre os 5 melhores jogadores (pontuações mais altas), junto com suas pontuações.                            |
| 5   | Aumente a pontuação do `jogador_5` em 50 e depois encontre sua nova posição (da menor para a maior).          |

## 8\. Série Temporal (Time Series)

| #   | Pergunta                                                                                                                                                        |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Recupere o timestamp e o valor mais recentes da série temporal `sensor:temperatura`.                                                                            |
| 2   | Obtenha todos os pontos de dados que estão entre `2024-01-01T00:00:00` e `2024-01-01T03:01:40` (use timestamps em milissegundos). Quantos pontos existem?       |
| 3   | Calcule a temperatura média para cada intervalo de uma hora em `2024‑01‑01` (tamanho do intervalo 3.600.000 ms). Liste as médias dos três primeiros intervalos. |
| 4   | Obtenha metadados (tempo de retenção, tamanho do chunk, etc.) da série temporal `sensor:temperatura`.                                                           |

## 9\. Streams

### Consultando a stream pré-preenchida

Todas as perguntas se referem à chave de stream `pedidos` e ao grupo de consumidores `processadores` que foram criados pelo script de dados.

| #   | Pergunta                                                                                                                                                              |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Quantas mensagens a stream `pedidos` contém atualmente?                                                                                                               |
| 2   | Busque as primeiras 5 mensagens. Anote o menor (mais antigo) ID de mensagem.                                                                                          |
| 3   | Busque as últimas 5 mensagens (mais recentes).                                                                                                                        |
| 4   | Leia 3 mensagens do início da stream como consumidor `consumidor1` pertencente ao grupo `processadores`. Liste os valores do campo `pedido_id` dessas três mensagens. |
| 5   | Sem confirmar nenhuma mensagem, inspecione a lista de entradas pendentes para o grupo `processadores`. Quantas mensagens pendentes existem?                           |
| 6   | Confirme a **primeira** mensagem que você obteve na pergunta 4 e depois verifique a contagem de pendentes novamente. Ela diminuiu?                                    |

### Escreva seu próprio produtor e consumidor

Crie dois pequenos scripts (em Python, shell ou qualquer linguagem de sua preferência) que interajam com uma stream Redis.

> **Produtor** (`produtor.py`)

- Use uma nova chave de stream `pedidos:ao_vivo`.
- A cada segundo, adicione uma mensagem contendo os campos:  
  `pedido_id` (identificador único, ex. `VIVO-001`, `VIVO-002`, …),  
  `cliente_id` (escolhido aleatoriamente de um pequeno conjunto como `C-A`, `C-B`, `C-C`),  
  `valor` (decimal aleatório entre 30.0 e 600.0).
- Deixe o produtor executar indefinidamente (ou pare após 50 mensagens).

> **Consumidor** (`consumidor.py`)

- Crie um grupo de consumidores chamado `proc-ao-vivo` na stream `pedidos:ao_vivo` (trate o caso em que ele já existe).
- Leia novas mensagens conforme elas chegam, usando o nome de consumidor `trabalhador-1`.
- Para cada mensagem, imprima o `pedido_id` e o `valor`, e mantenha um total acumulado do `valor` por `cliente_id`. A cada 10 mensagens, imprima um resumo dos totais até o momento.
- Confirme cada mensagem após ela ter sido processada.

**Entregáveis:**

- Código fonte de ambos os scripts.
- Um breve log do terminal mostrando o produtor adicionando mensagens e o consumidor processando-as com os resumos periódicos.

## 10\. Busca Vetorial (Vector Search)

O script de geração de dados armazenou um vetor de consulta binário na chave `exercicio:vetor_consulta`. Um índice RediSearch chamado `filmes_idx` foi criado sobre os hashes `filme:*`, cada um contendo um `titulo`, um `ano` e um `embeddings` de 300 dimensões float32.

| #   | Pergunta                                                                                                                                                                                       |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Execute uma busca K-vizinhos-mais-próximos com `K=3` usando o vetor de consulta de `exercicio:vetor_consulta`. Qual é o título do filme cujo embedding está mais próximo do vetor de consulta? |
| 2   | Liste os títulos e as distâncias de similaridade dos três filmes mais próximos.                                                                                                                |
| 3   | (Bônus) Repita a busca com `K=5`. O filme mais próximo permanece o mesmo?                                                                                                                      |

> **Dica:** O vetor bruto pode ser usado diretamente no seu cliente. O índice suporta consultas KNN através do comando `FT.SEARCH`.

---

# Projeto de um Serviço Simples de Encurtador de URL

Projete um programa simples que gerencie a tradução entre uma URL longa e uma curta. O programa deve permitir três operações distintas:

- **Inserção:** o usuário fornece uma URL longa e obtém uma URL curta do sistema;
- **Consulta:** o usuário fornece uma URL curta e obtém uma URL longa do sistema, se existir;
- **Estatísticas:** o sistema fornece um conjunto de estatísticas sobre o serviço.

Para a operação de **Inserção**, o sistema:

- recebe como entrada uma string (ex: http://www.exmaple.br/id=1234&lang=pt);
- solicita a identificação do usuário (ex: email do usuário);
- verifica se a string já foi registrada;
- gera uma string aleatória composta por 6 letras minúsculas e números aleatórios (ex: rv4b6n);
- salva a associação entre as duas strings.

Para a operação de **Consulta**, o sistema:

- recebe como entrada uma string (curta);
- fornece a URL longa associada à string, se existir; caso contrário, retorna um erro;
- registra o número de vezes que uma string curta foi consultada.

Para as operações de **Estatísticas**, o sistema deve fornecer:

- o número de inserções feitas por cada usuário;
- o número médio de vezes que as URLs curtas foram consultadas.

_Fim dos exercícios_
