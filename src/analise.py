import pandas as pd
import re
from collections import Counter
from pathlib import Path

# 1) CARREGAMENTO DOS DADOS BRUTOS
# Lê o arquivo CSV contendo as vagas extraídas pelo scraper
# O arquivo está localizado em data/vagas_brutas.csv
CSV_PATH = Path("data") / "vagas_brutas.csv"
df = pd.read_csv(CSV_PATH)

# 2) DEFINIÇÃO DAS HABILIDADES A SEREM RASTREADAS
# Lista de skills tecnológicas relevantes para análise
# Organizadas por categorias:
# - Linguagens de programação
# - Bancos de dados e SQL
# - Big Data/Processamento
# - Ferramentas de ETL/Orquestração
# - Cloud Computing
# - Infraestrutura como código/Contêineres
SKILLS = [
    "python", "java", "scala", "c#", ".net",
    "sql", "postgresql", "mysql", "snowflake", "bigquery",
    "spark", "pyspark", "hadoop", "kafka",
    "airflow", "dbt",
    "aws", "gcp", "azure", "s3", "redshift", "glue",
    "docker", "kubernetes", "terraform",
]

# OTIMIZAÇÃO: Pré-compilação das expressões regulares
# Cria um dicionário onde cada skill tem seu padrão regex correspondente
# \b garante que estamos pegando palavras inteiras
# re.I faz a busca ser case insensitive
patterns = {skill: re.compile(rf"\b{re.escape(skill)}\b", re.I) for skill in SKILLS}

# 3) PROCESSAMENTO E CONTAGEM DE SKILLS
# Inicializa um contador para acumular as ocorrências
contagem = Counter()

# Itera por cada descrição de vaga (tratando valores nulos)
for desc in df["descricao"].fillna(""):
    texto = desc.lower()  # Normaliza para minúsculas
    # Verifica cada skill contra o texto da descrição
    for skill, pattern in patterns.items():
        if pattern.search(texto):  # Busca eficiente usando regex pré-compilado
            contagem[skill] += 1  # Incrementa o contador para a skill encontrada

# 4) ORGANIZAÇÃO DOS RESULTADOS
# Converte o Counter para um DataFrame pandas
# Ordena as skills pela frequência (decrescente)
skills_df = (
    pd.DataFrame(contagem.items(), columns=["skill", "qtd"])
      .sort_values("qtd", ascending=False)
)

# 5) PERSISTÊNCIA DOS DADOS PROCESSADOS
# Define o caminho de saída e cria o diretório se necessário
OUTPUT_CSV = Path("output") / "skills_top.csv"
OUTPUT_CSV.parent.mkdir(exist_ok=True)  # Garante que o diretório existe

# Salva o DataFrame como CSV (com codificação UTF-8-Sig para Excel)
skills_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

# 6) FEEDBACK DE EXECUÇÃO
# Exibe um preview das 15 skills mais citadas
print("Skills mais citadas (top 15):")
print(skills_df.head(15).to_string(index=False))
# Informa o local onde o arquivo foi salvo
print(f"\nArquivo salvo em {OUTPUT_CSV.resolve()}")