from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import math

def grafico_horizontal(dataframe, modo="dark"):

    # Configuração de cores baseada no modo selecionado
    if modo == "dark":
        face, txt_color = "#0D0D0D", "white"  # Fundo preto e texto branco
    else:
        face, txt_color = "white", "black"    # Fundo branco e texto preto

    # Cria figura com tamanho personalizado e cor de fundo
    plt.figure(figsize=(10, 6), facecolor=face)
    ax = plt.gca()  # Obtém o eixo atual

    # Cor azul padrão para as barras (tom moderno)
    blue_600 = "#2563EB"
    
    # Cria as barras horizontais
    bars = ax.barh(
        dataframe["skill"],   # Nomes das skills no eixo Y
        dataframe["qtd"],     # Quantidades no eixo X
        color=blue_600,       # Cor uniforme das barras
        edgecolor="none",     # Remove bordas das barras
    )

    # Adiciona os valores dentro das barras (alinhados à direita)
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width - width * 0.02,  # Posição X (95% da largura da barra)                     
            bar.get_y() + bar.get_height() / 2,  # Centralizado verticalmente
            f"{int(width)}",       # Valor formatado como inteiro
            va="center",           # Alinhamento vertical centralizado
            ha="right",            # Alinhamento horizontal à direita
            color=txt_color,       # Cor do texto conforme o modo
            fontsize=8,            # Tamanho compacto mas legível
            fontweight="bold",     # Texto em negrito para melhor contraste
        )

    # Configuração inteligente dos ticks do eixo X
    max_val = dataframe["qtd"].max()
    step = 10 if max_val > 50 else 5  # Passo maior para escalas amplas                 
    tick_vals = list(range(0, math.ceil(max_val / step) * step + step, step))

    # Aplica os ticks e formatação do eixo X
    ax.set_xticks(tick_vals)
    ax.set_xticklabels(tick_vals, color=txt_color)
    ax.tick_params(axis="y", colors=txt_color)  # Cor dos labels do eixo Y

    # Remove todas as bordas do gráfico (estilo minimalista)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(False)  # Remove linhas de grid

    # Garante que o fundo do gráfico combine com o tema
    ax.set_facecolor(face)
    plt.tight_layout()  # Ajuste automático de layout

    # Salva a figura com alta qualidade
    out = Path("output") / f"grafico_{modo}_custom.png"
    out.parent.mkdir(exist_ok=True)  # Cria diretório se não existir
    plt.savefig(out, dpi=300, facecolor=face)  # Alta resolução (300dpi)
    plt.close()  # Fecha a figura para liberar memória
    print(f"[OK] {out} criado!")

# CARREGAMENTO E PREPARAÇÃO DOS DADOS
data_path = Path("output") / "skills_top.csv"
df = (
    pd.read_csv(data_path)
      .head(15)               # Considera apenas as top 15 skills
      .sort_values("qtd")     # Ordena por quantidade (para gráfico crescente)
)

# GERAÇÃO DOS GRÁFICOS
grafico_horizontal(df, modo="dark")   # Versão tema escuro
grafico_horizontal(df, modo="light")  # Versão tema claro