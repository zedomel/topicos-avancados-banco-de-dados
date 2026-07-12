# generate_data.py
import os, random, time, struct
import redis
from redis.commands.json import JSON
from redis.commands.search.field import TextField, NumericField, VectorField
from redis.commands.search.index_definition import IndexDefinition, IndexType

HOST = os.getenv("REDIS_HOST", "localhost")
PORT = int(os.getenv("REDIS_PORT", 6379))
PASSWORD = os.getenv("REDIS_PASSWORD", "")

r = redis.Redis(host=HOST, port=PORT, password=PASSWORD, decode_responses=False)
json = r.json()

print("Conectado. Populando dados...")

# --- Strings ---
r.set("usuario:1000:nome", "Alice")
r.set("usuario:1000:email", "alice@exemplo.com")
r.set("config:conexoes_maximas", 1000)
r.set("contador_visitantes", 1000)
r.set("frase", "A única maneira de fazer um ótimo trabalho é amar o que você faz. - Steve Jobs")
r.set("pagina:inicio:html", "<html><head><title>Início</title></head><body>Bem-vindo!</body></html>")

# --- Geoespacial ---
estacoes = [("estacao_" + str(i), round(random.uniform(-23.50, -23.60), 6), round(random.uniform(-46.60, -46.70), 6))
            for i in range(50)]
for nome, lat, lon in estacoes:
    r.geoadd("postos_gasolina", values=(lon, lat, nome))

# --- Hashes ---
for pid, nome, preco, estoque, cat in [(1001, "Notebook", 3999.99, 50, "eletronicos"),
                                       (1002, "Mouse", 89.90, 200, "acessorios"),
                                       (1003, "Teclado", 249.90, 150, "acessorios")]:
    r.hset(f"produto:{pid}", mapping={"nome": nome, "preco": preco, "estoque": estoque, "categoria": cat})

# --- JSON ---
func1 = {"nome": "João Silva", "departamento": "Engenharia", "salario": 75000, "habilidades": ["Python", "Redis"]}
func2 = {"nome": "Maria Santos", "departamento": "Marketing", "salario": 68000, "habilidades": ["SEO", "Conteúdo"]}
json.set("func:1", "$", func1)
json.set("func:2", "$", func2)

# --- Listas ---
logins = [f"usuario_{random.randint(1000,9999)}" for _ in range(20)]
r.rpush("logins_recentes", *logins)

# --- Probabilístico (HyperLogLog, Bloom, Cuckoo) ---
for i in range(1000):
    ip = f"192.168.{random.randint(0,255)}.{random.randint(0,255)}"
    r.pfadd("visitantes_unicos", ip)
for i in range(300):
    ip = f"10.0.{random.randint(0,255)}.{random.randint(0,255)}"
    r.pfadd("pagina:hll", ip)

r.execute_command("BF.RESERVE", "nomes_usuarios", 0.01, 1000)
for usuario in ["alice", "bob", "charlie", "dave", "eve"]:
    r.execute_command("BF.ADD", "nomes_usuarios", usuario)

r.execute_command("CF.RESERVE", "emails", 1000)
for email in ["alice@exemplo.com", "bob@exemplo.com", "charlie@exemplo.com"]:
    r.execute_command("CF.ADD", "emails", email)

# --- Conjuntos (Sets) ---
tags_noticias = {"tecnologia", "politica", "esportes", "saude", "ciencia", "redis", "python", "ciencia_dados", "ia", "ml",
             "blockchain", "nuvem", "seguranca", "iot", "mobile", "web", "jogos", "design", "startup", "negocios"}
r.sadd("tags:noticias", *tags_noticias)
r.sadd("tags:artigo:1", "tecnologia", "ia", "python", "redis", "ciencia_dados", "nuvem")
r.sadd("tags:artigo:2", "tecnologia", "blockchain", "python", "seguranca", "nuvem")

# --- Conjuntos Ordenados (Sorted Sets) ---
for i in range(50):
    r.zadd("ranking", {f"jogador_{i}": random.randint(0, 10000)})

# --- Série Temporal (Time Series) ---
r.execute_command("TS.CREATE", "sensor:temperatura", "RETENTION", "0", "LABELS", "sensor_id", "1", "tipo", "temp")
inicio_ts = int(time.mktime(time.strptime("2024-01-01 00:00", "%Y-%m-%d %H:%M"))) * 1000
for i in range(1440):
    ts = inicio_ts + i * 60000
    val = round(random.uniform(20.0, 30.0), 2)
    r.execute_command("TS.ADD", "sensor:temperatura", ts, val)

# --- Streams ---
chave_stream = "pedidos"
for i in range(5000):
    r.xadd(chave_stream, {"pedido_id": f"PED-{1000+i}", "cliente_id": f"CLI-{random.randint(100,999)}",
                         "valor": round(random.uniform(30.0, 1500.0), 2)})
try:
    r.xgroup_create(chave_stream, "processadores", id="0", mkstream=True)
except:
    pass

# --- Busca Vetorial (Vector Search) ---
NOME_INDICE = "filmes_idx"
try:
    r.ft(NOME_INDICE).dropindex(delete_documents=True)
except:
    pass
campo_vetorial = VectorField("embeddings", "FLAT", {"TYPE": "FLOAT32", "DIM": 300, "DISTANCE_METRIC": "COSINE"})
esquema = (TextField("titulo"), NumericField("ano"), campo_vetorial)
r.ft(NOME_INDICE).create_index(esquema, definition=IndexDefinition(prefix=["filme:"], index_type=IndexType.HASH))

num_filmes = 1000
dim = 300
vetor_consulta = [random.random() for _ in range(dim)]
r.set("exercicio:vetor_consulta", struct.pack(f'{dim}f', *vetor_consulta))

for i in range(num_filmes):
    filme_id = f"filme:{i}"
    titulo = f"Filme_{i}"
    ano = 1990 + (i % 30)
    vec = [random.random() for _ in range(dim)]
    r.hset(filme_id, mapping={"titulo": titulo, "ano": ano, "embeddings": struct.pack(f'{dim}f', *vec)})

print("População de dados concluída.")
print("Vetor de consulta (hex) para o exercício KNN:")
hex_vec = r.get("exercicio:vetor_consulta").hex()
print(hex_vec[:80] + "...")
print("Todos os dados prontos para os exercícios.")