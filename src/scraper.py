import requests
import pandas as pd
import time

# CONFIGURAÇÕES DA API
# URL base da API Remotive para busca de vagas remotas
API_URL = "https://remotive.com/api/remote-jobs"
# Termo de busca fixo para filtrar vagas de Data Engineering
QUERY   = "data engineer"

def coletar_vagas_remotive():
    """
    Coleta vagas de Data Engineer da API Remotive.
    
    Retorna:
        Lista de dicionários contendo informações estruturadas das vagas
    """
    # Parâmetros da requisição:
    # - search: termo de busca (data engineer)
    # - limit: máximo de resultados (200 é o máximo permitido pela API)
    params  = {"search": QUERY, "limit": 200}
    
    # Headers para simular um navegador e evitar bloqueios
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # Faz a requisição GET com timeout de 10 segundos para evitar hanging
    resp    = requests.get(API_URL, params=params, headers=headers, timeout=10)

    # Verifica se a requisição foi bem-sucedida (código 200)
    if resp.status_code != 200:
        raise RuntimeError(f"Erro {resp.status_code} na API")

    # Extrai a lista de vagas do JSON de resposta (padrão: campo "jobs")
    jobs = resp.json().get("jobs", [])
    
    # Estrutura os dados relevantes de cada vaga em um formato padronizado
    registros = []
    for job in jobs:
        registros.append({
            "titulo"    : job["title"],          # Título da vaga
            "empresa"   : job["company_name"],   # Nome da empresa
            "local"     : job["candidate_required_location"],  # Localização requerida
            "pub_date"  : job["publication_date"],  # Data de publicação
            "descricao" : job["description"],     # Descrição completa
            "url"       : job["url"],            # Link para a vaga
        })
    return registros

def main():
    """Função principal que orquestra a coleta e armazenamento das vagas"""
    print("Coletando vagas da Remotive...")
    
    # Coleta as vagas usando a função definida
    vagas = coletar_vagas_remotive()
    print(f"Total de vagas coletadas: {len(vagas)}")

    # Converte a lista de vagas para DataFrame pandas
    df = pd.DataFrame(vagas)
    
    # Salva os dados brutos em CSV:
    # - UTF-8-Sig para compatibilidade com Excel
    # - Sem índice numérico adicional
    df.to_csv("data/vagas_brutas.csv", index=False, encoding="utf-8-sig")
    print("CSV salvo em data/vagas_brutas.csv")

if __name__ == "__main__":
    # Ponto de entrada do script - executa a função main()
    # quando o arquivo é rodado diretamente (não importado como módulo)
    main()