import os
import numpy as np
import matplotlib.pyplot as plt
from bin.processamento import algoritmos

def grafico_discriminacao(dicDiscriminacao, vectorQuest, filename, ano: int, save_path, curso, cont):
    discriminacao = algoritmos.indice_de_discriminacao(vectorQuest, filename, ano)

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle("Indice de Discriminação " + str(ano))

    x = np.arange(4)  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()

    bars1 = ax.bar(x - width / 2, discriminacao.values(), width, color='tab:blue', label='Discriminação ' + str(curso))
    bars2 = ax.bar(x + width / 2, dicDiscriminacao[cont].values(), width, color='tab:red', label='Geral')

    ax.bar_label(bars1, fmt='{:,.0f}', padding=3)
    ax.bar_label(bars2, fmt='{:,.0f}', padding=3)

    ax.set_title('Índice de discriminação ' + str(ano))
    ax.set_xticks(x, discriminacao.keys())

    ax.legend()
    fig.tight_layout()

    plt.savefig(save_path)
    plt.close()

def grafico_discriminacao_percentual(discriminacaoPercentualGeral, siglasGeral, vectorDict, save_path, totalDiscriminacaoEspecifica, curso):
    for sigla, discriminacaoQtde in siglasGeral.items():
        discriminacaoTotal = sum(discriminacaoQtde)
        discriminacaoMedia = [0, 0, 0, 0, 0]
        
        for i in range(0, len(discriminacaoQtde)):
            if (discriminacaoTotal > 0):
                discriminacaoMedia[i] = (discriminacaoQtde[i] / discriminacaoTotal) * 100

        fig, ax = plt.subplots(figsize=(8, 5))
        fig.suptitle("Gráfico de Tema por Discriminacao")

        i = 0
        for discriminacaoParcial, num in discriminacaoPercentualGeral.items():
            barh1 = ax.barh(discriminacaoParcial, discriminacaoMedia[i], color='tab:blue', label='Discriminação ' + str(curso))
            ax.bar_label(barh1, fmt='{:,.0f}%')
            i += 1

        ax.set_title(sigla)

        plt.savefig(save_path + sigla)
        plt.close()

    i = 0
    for discriminacaoParcial, num in discriminacaoPercentualGeral.items():
        discriminacaoQtdeTotal = 0
        for siglaParcial, qtde in siglasGeral.items():
            discriminacaoQtdeTotal += qtde[i]

        fig, ax = plt.subplots(figsize=(8, 5))
        fig.suptitle("Gráfico de Discriminacao por Tema")

        for siglaParcial, qtde in siglasGeral.items():
            media = 0
            if (discriminacaoQtdeTotal > 0):
                media = (qtde[i] / discriminacaoQtdeTotal) * 100
            barh = ax.barh(siglaParcial, media, color='tab:blue')
            ax.bar_label(barh, fmt='{:,.0f}%')
        i += 1
        ax.set_title(discriminacaoParcial)

        plt.savefig(save_path + discriminacaoParcial)
        plt.close()

def especifico(vectorQuest, vectorDict,
               totalDiscriminacaoQuantidade, filename, # ATRIBUTO filename = "filtrado.csv"
               curso, totalFacilidadeQuantidade,
               vecParcialDiscriminacao, discriminacaoPercentualGeral,
               siglasGeral):
    '''
    Função principal responsável por receber o vetor de cursos e processar
    seus respectivos gráficos individualmente
    '''
    # 1452

    totalDiscriminacao = {
        'Muito Bom': 0,
        'Bom': 0,
        'Medio': 0,
        'Fraco': 0
    }

    cont = len(vecParcialDiscriminacao) - 1
    totalDiscriminacaoQuantidadeEspecifica = []

    for vec in vectorQuest:
        parcialDiscriminacao, pontoBisserial = grafico_discriminacao(vecParcialDiscriminacao, vectorQuest, 'dados_especificos_filtrados.csv', vec['ano'], (os.getcwd() + '/graficos/GraficosEspecificos/GraficosDiscriminacao/' + str(curso) + ' - ' + str(vec['ano'])), curso, cont)
        totalDiscriminacao['Muito Bom'] += parcialDiscriminacao['Muito Bom']
        totalDiscriminacao['Bom'] += parcialDiscriminacao['Bom']
        totalDiscriminacao['Medio'] += parcialDiscriminacao['Medio']
        totalDiscriminacao['Fraco'] += parcialDiscriminacao['Fraco']
        totalDiscriminacaoQuantidadeEspecifica.append(pontoBisserial)
        cont -= 1
    grafico_discriminacao_percentual(discriminacaoPercentualGeral, siglasGeral, vectorDict, (os.getcwd() + '/graficos/GraficosEspecificos/GraficosDiscriminacaoPercentual/' + str(curso) + ' - ' + str(vec['ano'])), totalDiscriminacaoQuantidadeEspecifica, str(curso))

    #ProcessamentoGraficos.percentualAcertos(vectorQuest, vectorDict, 'dados_especificos_filtrados.csv', vec['ano'], (os.getcwd() + '/graficos/GraficosEspecificos/GraficosPercentualAcertos/' + str(curso) + ' - ' + str(vec['ano'])))
    #ProcessamentoGraficos.indiceFacilidade(vectorQuest, 'dados_especificos_filtrados.csv', vec['ano'], (os.getcwd() + '/graficos/GraficosEspecificos/GraficosFacilidade/' + str(curso) + ' - ' + str(vec['ano'])))
    #ProcessamentoGraficos.facilidadePercentual(totalFacilidadeQuantidade, vectorDict, (os.getcwd() + '/graficos/GraficosEspecificos/GraficosFacilidadePercentual/' + str(curso) + ' - ' + str(vec['ano'])))
    #ProcessamentoGraficos.quantidadeTema(vectorQuest, vectorDict, (os.getcwd() + '/graficos/GraficosEspecificos/GraficosQuantidade/' + str(curso) + ' - ' + str(vec['ano'])))

