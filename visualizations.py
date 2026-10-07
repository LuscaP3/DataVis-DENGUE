import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_hex
from matplotlib.patches import Patch
from matplotlib.colors import to_rgb


def diverging_bar_chart(titulo, dados_categoria_a, rotulo_a, cor_a, contagem_total_a, dados_categoria_b, rotulo_b, cor_b, contagem_total_b, intervalos, categorias, rotulo_eixo_y, arquivo = None):

    maior_valor = min(dados_categoria_a + dados_categoria_b)
    menor_valor = max(dados_categoria_a + dados_categoria_b)

    nova_origem = (maior_valor + menor_valor) / 2

    novos_dados_categoria_a = list(map(lambda x: -(x * 100) / contagem_total_a, dados_categoria_a))
    novos_dados_categoria_b = list(map(lambda x:  (x * 100) / contagem_total_b, dados_categoria_b))

    fig, ax = plt.subplots()

    ax.barh(range(0,len(dados_categoria_a)), novos_dados_categoria_a, left = nova_origem - 0.5, height = 0.7, color = cor_a, label = rotulo_a, zorder = 2)
    ax.barh(range(0,len(dados_categoria_b)), novos_dados_categoria_b, left = nova_origem + 0.5, height = 0.7, color = cor_b, label = rotulo_b, zorder = 2)


    particoes = 100 / intervalos
    porcentagens = []
    valor_atual = -100
    while valor_atual <= 100:
        porcentagens.append(valor_atual)
        valor_atual = valor_atual + particoes

    xticks_labels = list(map(lambda x: abs(x), porcentagens))
    xticks = list(map(lambda x: nova_origem + x, porcentagens))

    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks_labels, rotation=0, ha='center')

    qtd_linhas = len(dados_categoria_a)

    ax.set_yticks(list(range(0, qtd_linhas)))
    ax.set_yticklabels(categorias, rotation=0, ha='right')

    for i in range(0, qtd_linhas):
        ax.plot([xticks[0], xticks[-1]], [i,i], dashes=[20, 10], linewidth = 0.25, color = "#6B6B6B", zorder = 1)


    ax.set_ylabel(rotulo_eixo_y, ha='center', va='center')

    ax.legend()

    plt.title(titulo)

    if arquivo is not None:
        fig.savefig(arquivo, dpi = 300, bbox_inches = 'tight')
        plt.close(fig)
    else:
        plt.show()

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #


def mapa_de_calor(grupos, categorias, valores, totais, cor_max, cor_min, arquivo = None):
    gradiente = LinearSegmentedColormap.from_list(
        "meu_gradiente",
        [cor_min, cor_max]
    )

    maior_valor = max(valor for linha in valores for valor in linha)

    fig, ax = plt.subplots()

    for i in range(len(categorias)):
        for j in range(0, len(grupos)):
            ax.bar([j], [0.95], bottom = i, width = 0.75, color = to_hex(gradiente(valores[j][i] / totais[j])), label = 'rotulo_a', zorder = 2)


    ax.set_xticks(range(0, len(grupos)))
    ax.set_xticklabels(grupos, rotation=0, ha='center')

    ax.set_yticks(list(map(lambda x: x + 0.5, list(range(0, len(categorias))))))
    ax.set_yticklabels(categorias, rotation=0, ha='right')

    if arquivo is not None:
        fig.savefig(arquivo, dpi = 300, bbox_inches = 'tight')
        plt.close(fig)
    else:
        plt.show()


    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #

def mosaic_plot(titulo, dados, grupos, categorias, cores, tamanho_fonte = 10, fonte_minima = 7, rotulos_externos = True, arquivo = None):

    totais = []

    for i in dados:
        totais.append(sum(i))

    fig, ax = plt.subplots()

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # tamanho do eixo em pontos (1 pt = 1/72 polegada), para saber se o texto cabe
    largura_ax_pt = ax.get_position().width * fig.get_figwidth() * 72
    altura_ax_pt = ax.get_position().height * fig.get_figheight() * 72

    larguras = []
    alturas = []

    for i in dados:
        larguras.append((sum(i) * 100) / sum(totais))

    for i in range(0, len(grupos)):
        temp = []
        for j in range(0, len(dados[i])):
            temp.append((dados[i][j] * 100) / sum(dados[i]))
        alturas.append(temp)

    posicao_x = 0

    posicoes_grupos = []

    fora = []   # porcentagens que não couberam dentro do bloco

    for i in range(0, len(grupos)):

        base = 0

        largura_pt = larguras[i] / 100 * largura_ax_pt

        for j in range(0, len(dados[i])):

            ax.bar(
                [posicao_x + larguras[i] / 2],
                [alturas[i][j]],
                bottom = base,
                width = larguras[i],
                color = cores[j],
                edgecolor = 'white',
                linewidth = 1.5,
                label = categorias[j] if i == 0 else None
            )

            if alturas[i][j] > 0:

                texto = '<1%' if alturas[i][j] < 0.5 else f'{alturas[i][j]:.0f}%'

                altura_pt = alturas[i][j] / 100 * altura_ax_pt

                r, g, b = to_rgb(cores[j])

                luminosidade = 0.299 * r + 0.587 * g + 0.114 * b

                rotacao = None
                fonte = tamanho_fonte

                # 1) na horizontal, diminuindo a fonte até a mínima
                for f in range(tamanho_fonte, fonte_minima - 1, -1):
                    if largura_pt >= 0.7 * f * len(texto) + 4 and altura_pt >= 1.2 * f + 2:
                        rotacao = 0
                        fonte = f
                        break

                # 2) na vertical (girado 90 graus)
                if rotacao is None:
                    for f in range(tamanho_fonte, fonte_minima - 1, -1):
                        if largura_pt >= 1.2 * f + 4 and altura_pt >= 0.7 * f * len(texto) + 2:
                            rotacao = 90
                            fonte = f
                            break

                if rotacao is not None:

                    ax.text(
                        posicao_x + larguras[i] / 2,
                        base + alturas[i][j] / 2,
                        texto,
                        ha = 'center',
                        va = 'center',
                        rotation = rotacao,
                        fontsize = fonte,
                        color = 'black' if luminosidade > 0.6 else 'white',
                        zorder = 3
                    )

                elif rotulos_externos:

                    # 3) não coube de jeito nenhum: vai para a margem direita, com uma linha
                    fora.append((posicao_x + larguras[i] / 2, base + alturas[i][j] / 2, texto))

            base = base + alturas[i][j]

        posicoes_grupos.append(posicao_x + larguras[i] / 2)

        posicao_x = posicao_x + larguras[i]

    if arquivo is not None:
        fig.savefig(arquivo, dpi = 300, bbox_inches = 'tight')
        plt.close(fig)
    else:
        plt.show()

    # rótulos externos, de baixo para cima, empurrando para cima quando ficariam sobrepostos
    fora.sort(key = lambda item: item[1])

    espacamento = (1.3 * 8) / altura_ax_pt * 100

    ultimo_y = None

    for x, y, texto in fora:

        y_texto = y if ultimo_y is None else max(y, ultimo_y + espacamento)

        ax.annotate(
            texto,
            xy = (x, y),
            xytext = (101, y_texto),
            ha = 'left',
            va = 'center',
            fontsize = 8,
            annotation_clip = False,
            arrowprops = dict(arrowstyle = '-', relpos = (0, 0.5), color = 'black', linewidth = 0.7, shrinkA = 2, shrinkB = 0),
            zorder = 4
        )

        ultimo_y = y_texto

    ax.set_xticks(posicoes_grupos)
    ax.set_xticklabels(grupos)

    ax.legend(loc = 'center left', bbox_to_anchor = (1.09 if fora else 1.01, 0.5), frameon = False)

    plt.title(titulo)

    if arquivo is not None:
        fig.savefig(arquivo, dpi = 300, bbox_inches = 'tight')
        plt.close(fig)
    else:
        plt.show()


    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #

def barras_empilhadas(titulo, grupos, dados_grupo, descrição, cores, tamanho_fonte = 9, arquivo = None):

    fig, ax = plt.subplots()

    porcentagens = []   # (x, y do centro do segmento, altura em %, índice da cor)

    for i in range(0, len(dados_grupo)):

        total = sum(dados_grupo[i])

        if total == 0:
            continue

        base = 0

        for j in range(0, len(dados_grupo[i])):

            altura = (dados_grupo[i][j] * 100) / total

            ax.bar([i], [altura], width = 0.9, bottom = base, color = cores[j], edgecolor = 'white', zorder = 2)

            porcentagens.append((i, base + altura / 2, altura, j))

            base = base + altura

    ax.set_xlim(-0.5, len(grupos) - 0.5)
    ax.set_ylim(0, 100)

    ax.set_xticks(list(range(0, len(grupos))))
    ax.set_xticklabels(grupos, rotation = 0, ha = 'center')

    ax.set_yticks([0, 100])
    ax.set_yticklabels(["", ""], rotation = 0, ha = 'right')

    # legenda na mesma ordem visual do empilhamento (de cima para baixo)
    legenda = []

    for j in range(0, len(descrição)):
        legenda.append(Patch(facecolor = cores[j], label = descrição[j]))

    plt.legend(handles = legenda[::-1], bbox_to_anchor = (1.05, 1), loc = 'upper left')
    plt.title(titulo)

    fig.tight_layout()

    # tamanho do eixo em pontos (1 pt = 1/72 polegada), para saber se o texto cabe
    largura_ax_pt = ax.get_position().width * fig.get_figwidth() * 72
    altura_ax_pt = ax.get_position().height * fig.get_figheight() * 72

    largura_barra_pt = 0.9 / len(grupos) * largura_ax_pt

    for x, y, altura, j in porcentagens:

        texto = f'{altura:.0f}%' if altura >= 10 else f'{altura:.1f}%'.replace('.', ',')

        altura_segmento_pt = altura / 100 * altura_ax_pt

        # se o texto não couber no segmento, não escreve
        if altura_segmento_pt < 1.2 * tamanho_fonte + 2 or largura_barra_pt < 0.7 * tamanho_fonte * len(texto) + 4:
            continue

        r, g, b = to_rgb(cores[j])

        luminosidade = 0.299 * r + 0.587 * g + 0.114 * b

        ax.text(x, y, texto, ha = 'center', va = 'center', fontsize = tamanho_fonte, color = 'black' if luminosidade > 0.6 else 'white', zorder = 3)

    
    if arquivo is not None:
        fig.savefig(arquivo, dpi = 300, bbox_inches = 'tight')
        plt.close(fig)
    else:
        plt.show()