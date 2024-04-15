import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bin.processamento import algoritmos


def quantidadeTema(questoes, dicionario, save_path):
    quantidade_disciplinas = len(dicionario)

    disciplinas_sigla = []
    for dic in dicionario:
        disciplinas_sigla.append(dic['sigla'])

    vetQuestTotal = []

    for quest in questoes:
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.suptitle("Gráfico da Quantidade questões por tema")

        vetQuestTotal += quest['vet_tipo']

        flag = quest['vet_tipo']
        qtd_por_tema = []
        for i in range(1, quantidade_disciplinas + 1):
            qtd_por_tema.append(flag.count(i))

        for i in range(0, quantidade_disciplinas):
            barh = ax.barh(disciplinas_sigla[i], qtd_por_tema[i], color='tab:blue')
            ax.bar_label(barh, fmt='{:,.0f}')

        ax.set_title(str(quest['ano']))
        plt.savefig(save_path)
        plt.close()

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle("Gráfico da Quantidade questões por tema")

    qtd_por_tema_total = []
    for i in range(1, quantidade_disciplinas + 1):
        qtd_por_tema_total.append(vetQuestTotal.count(i))

    for i in range(0, quantidade_disciplinas):
        barh = ax.barh(disciplinas_sigla[i], qtd_por_tema_total[i], color='tab:blue')
        ax.bar_label(barh, fmt='{:,.0f}')
    ax.set_title('Total')

    plt.savefig(save_path + str('Total'))
    plt.close()

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle("Percentual total de questões por tema")

    qtde_total = 0
    for qtde in qtd_por_tema_total:
        qtde_total += qtde
    for i in range(0, quantidade_disciplinas):
        bar = ax.bar(disciplinas_sigla[i], (qtd_por_tema_total[i] / qtde_total) * 100, color='tab:blue')
        ax.bar_label(bar, fmt='{:,.0f}%')

    with open(file='dados_dos_graficos/qtdTema.csv', mode='w') as file:
        for column in disciplinas_sigla:
            file.write(column + ';')

        file.writelines('\n')

        for disc in qtd_por_tema_total:
            file.write(str(disc) + ';')

        file.close()

    plt.savefig(save_path + 'TotalPorcentagem')
    plt.close()


def percentualAcertos(vectorQuest, vectorDict, filename, ano: int, save_path):
    category_names = ['Acertos', 'Erros']

    vet_resultado = algoritmos.obter_vetor_acertos(vectorQuest, filename, ano)

    results = {}
    for dic in vectorDict:
        somaFinal = [0, 0]  # 0 = acertos, 1 = erros
        for parcial in vet_resultado:
            if (parcial[0] == dic['id']):
                somaFinal[0] += parcial[1]
                somaFinal[1] += parcial[2]

        mediaAcertos = 0
        mediaErros = 0
        total = somaFinal[0] + somaFinal[1]
        if (total != 0):
            mediaAcertos = (somaFinal[0] / total) * 100
            mediaErros = (somaFinal[1] / total) * 100
        results[dic['sigla']] = [mediaAcertos, mediaErros]

    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['PRGn'](
        np.linspace(0.85, 0.15, data.shape[1]))

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.invert_yaxis()
    # ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    ax.set_title(str(ano))
    ax.set_xlabel("%")
    ax.set_ylabel("Tema")

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, fmt='{:,.0f}%', label_type='center', color=text_color)

    ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    with open(file='dados_dos_graficos/acertos.csv', mode='w') as file:
        for column in results.keys():
            file.write(column + ';')

        file.writelines('\n')

        for vec in data:
            file.write(str(vec[0]) + ';')

        file.close()

    plt.savefig(save_path)
    plt.close()


def indiceFacilidade(vectorQuest, filename, ano: int, save_path):
    vet_resultado = algoritmos.obter_vetor_acertos(vectorQuest, filename, ano)

    results = {}
    j = 0
    for parcial in vet_resultado:
        j += 1

        mediaAcertos = 0
        mediaErros = 0
        total = parcial[1] + parcial[2]
        disciplina = parcial[0]

        if (total != 0):
            mediaAcertos = (parcial[1] / total) * 100
            mediaErros = (parcial[2] / total) * 100
        results[j] = [mediaAcertos, mediaErros, disciplina]

    facilidade = {
        'Muito Dificil': 0,
        'Dificil': 0,
        'Medio': 0,
        'Facil': 0,
        'Muito Facil': 0
    }

    for atributo, valor in results.items():
        if (valor[0] != 0):
            if (round(valor[0]) <= 15):
                facilidade['Muito Dificil'] += 1
            elif (round(valor[0]) >= 16 and round(valor[0]) <= 40):
                facilidade['Dificil'] += 1
            elif (round(valor[0]) >= 41 and round(valor[0]) <= 60):
                facilidade['Medio'] += 1
            elif (round(valor[0]) >= 61 and round(valor[0]) <= 85):
                facilidade['Facil'] += 1
            elif (round(valor[0]) >= 86):
                facilidade['Muito Facil'] += 1

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle("Indice de facilidade " + str(ano))

    for atributo, valor in facilidade.items():
        bar = ax.bar(atributo, valor, color='tab:blue')
        ax.bar_label(bar, fmt='{:,.0f}')

    plt.savefig(save_path)
    plt.close()

    return facilidade, results


def facilidadePercentual(totalAcertos, vectorDict, save_path):
    siglas = {}
    for dicionario in vectorDict:
        siglas[dicionario['sigla']] = [0, 0, 0, 0, 0]  # muito dificil, dificil, medio, facil, muito facil
        facilidade = {
            'Muito Dificil': 0,
            'Dificil': 0,
            'Medio': 0,
            'Facil': 0,
            'Muito Facil': 0
        }

        for ano in totalAcertos:
            for atributo, valor in ano.items():
                if (dicionario['id'] == valor[2]):
                    if (valor[0] != 0):
                        if (round(valor[0]) <= 15):
                            facilidade['Muito Dificil'] += 1
                        elif (round(valor[0]) >= 16 and round(valor[0]) <= 40):
                            facilidade['Dificil'] += 1
                        elif (round(valor[0]) >= 41 and round(valor[0]) <= 60):
                            facilidade['Medio'] += 1
                        elif (round(valor[0]) >= 61 and round(valor[0]) <= 85):
                            facilidade['Facil'] += 1
                        elif (round(valor[0]) >= 86):
                            facilidade['Muito Facil'] += 1
        siglas[dicionario['sigla']] = [facilidade['Muito Dificil'], facilidade['Dificil'], facilidade['Medio'],
                                       facilidade['Facil'], facilidade['Muito Facil']]

    for sigla, facilidadeQtde in siglas.items():
        facilidadeTotal = sum(facilidadeQtde)
        facilidadeMedia = [0, 0, 0, 0, 0]
        for i in range(0, len(facilidadeQtde)):
            if (facilidadeTotal > 0):
                facilidadeMedia[i] = (facilidadeQtde[i] / facilidadeTotal) * 100

        fig, ax = plt.subplots(figsize=(8, 5))
        fig.suptitle("Gráfico de Tema por Facilidade")

        i = 0
        for facilidadeParcial, num in facilidade.items():
            barh = ax.barh(facilidadeParcial, facilidadeMedia[i], color='tab:blue')
            ax.bar_label(barh, fmt='{:,.0f}%')
            i += 1
        ax.set_title(sigla)

        plt.savefig(save_path)
        plt.close()

    i = 0
    for facilidadeParcial, num in facilidade.items():
        facilidadeQtdeTotal = 0
        for siglaParcial, qtde in siglas.items():
            facilidadeQtdeTotal += qtde[i]

        fig, ax = plt.subplots(figsize=(8, 5))
        fig.suptitle("Gráfico de Facilidade por Tema")

        for siglaParcial, qtde in siglas.items():
            media = 0
            if (facilidadeQtdeTotal > 0):
                media = (qtde[i] / facilidadeQtdeTotal) * 100
            barh = ax.barh(siglaParcial, media, color='tab:blue')
            ax.bar_label(barh, fmt='{:,.0f}%')
        i += 1
        ax.set_title(facilidadeParcial)

        plt.savefig(os.getcwd() + '/graficos/GraficosFacilidadePercentual/' + facilidadeParcial)
        plt.close()


def grafico_de_discriminacao(vectorQuest, filename, ano: int, save_path):
    arq_filtrado = pd.read_csv(filename)
    # Recebe o arquivo filtrado com os dados

    vet_respostas = arq_filtrado[(arq_filtrado['NU_ANO'] == ano)]
    # Filtra o arquivo para que o vetor de respostas receba apenas as linhas
    # do ano determinado

    vet_respostas = vet_respostas.reset_index(0)

    cr_linha = np.average(vet_respostas['NT_CE'])

    sr = np.std(vet_respostas['NT_CE'])

    questoes = []
    for quest in vectorQuest:
        if (quest["ano"] == ano):
            questoes = quest

    vet_ponto_bisserial = []
    for i in range(0, len(questoes["vet_tipo"])):  # alterar questoes por tema
        vet_ca_linha = []
        acertaram = 0
        j = 0
        for resposta in vet_respostas["DS_VT_ACE_OCE"]:
            vet_res = []

            if (str(resposta) != 'nan'):
                for digito in str(resposta):
                    if (digito != 'Z'):
                        vet_res.append(int(digito))

                if (vet_res[i] == 1):
                    vet_ca_linha.append(vet_respostas['NT_CE'][j])
                    acertaram += 1
            j += 1
        ca_linha = 0
        if (len(vet_ca_linha) != 0):
            ca_linha = np.average(vet_ca_linha)

        p = 0
        if (len(vet_respostas["DS_VT_ACE_OCE"]) > 0):
            p = acertaram / len(vet_respostas["DS_VT_ACE_OCE"])

        q = 1 - p

        r_pb = ((ca_linha - cr_linha) / sr) * np.sqrt(p / q)

        vet_ponto_bisserial.append([questoes["vet_tipo"][i], r_pb])

    discriminacao = {
        'Muito Bom': 0,
        'Bom': 0,
        'Medio': 0,
        'Fraco': 0
    }

    for valor in vet_ponto_bisserial:
        if (valor[1] != 0):
            if (valor[1] <= 0.19):
                discriminacao['Muito Bom'] += 1
            elif (valor[1] > 0.19 and valor[1] <= 0.29):
                discriminacao['Bom'] += 1
            elif (valor[1] > 0.29 and valor[1] <= 0.39):
                discriminacao['Medio'] += 1
            elif (valor[1] > 0.39):
                discriminacao['Fraco'] += 1

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle("Indice de Discriminação " + str(ano))

    for atributo, valor in discriminacao.items():
        bar = ax.bar(atributo, valor, color='tab:blue')
        ax.bar_label(bar, fmt='{:,.0f}')

    plt.savefig(save_path)
    plt.close()

    return discriminacao, vet_ponto_bisserial


def discriminacaoPercentual(totalDiscriminacao, vectorDict, save_path):
    siglas = {}
    for dicionario in vectorDict:
        siglas[dicionario['sigla']] = [0, 0, 0, 0]  # Muito Bom, Bom, Medio, Fraco
        discriminacao = {
            'Muito Bom': 0,
            'Bom': 0,
            'Medio': 0,
            'Fraco': 0
        }

        for ano in totalDiscriminacao:
            for valor in ano:
                if (dicionario['id'] == valor[0]):
                    if (valor[1] > 0):
                        if (valor[1] <= 0.19):
                            discriminacao['Muito Bom'] += 1
                        elif (valor[1] > 0.19 and valor[1] <= 0.29):
                            discriminacao['Bom'] += 1
                        elif (valor[1] > 0.29 and valor[1] <= 0.39):
                            discriminacao['Medio'] += 1
                        elif (valor[1] > 0.39):
                            discriminacao['Fraco'] += 1
        siglas[dicionario['sigla']] = [discriminacao['Muito Bom'], discriminacao['Bom'], discriminacao['Medio'],
                                       discriminacao['Fraco']]

    for sigla, discriminacaoQtde in siglas.items():
        discriminacaoTotal = sum(discriminacaoQtde)
        discriminacaoMedia = [0, 0, 0, 0, 0]
        for i in range(0, len(discriminacaoQtde)):
            if (discriminacaoTotal > 0):
                discriminacaoMedia[i] = (discriminacaoQtde[i] / discriminacaoTotal) * 100

        fig, ax = plt.subplots(figsize=(8, 5))
        fig.suptitle("Gráfico de Tema por Discriminacao")

        i = 0
        for discriminacaoParcial, num in discriminacao.items():
            barh = ax.barh(discriminacaoParcial, discriminacaoMedia[i], color='tab:blue')
            ax.bar_label(barh, fmt='{:,.0f}%')
            i += 1
        ax.set_title(sigla)

        plt.savefig(save_path + sigla)
        plt.close()

    i = 0
    for discriminacaoParcial, num in discriminacao.items():
        discriminacaoQtdeTotal = 0
        for siglaParcial, qtde in siglas.items():
            discriminacaoQtdeTotal += qtde[i]

        fig, ax = plt.subplots(figsize=(8, 5))
        fig.suptitle("Gráfico de Discriminacao por Tema")

        for siglaParcial, qtde in siglas.items():
            media = 0
            if (discriminacaoQtdeTotal > 0):
                media = (qtde[i] / discriminacaoQtdeTotal) * 100
            barh = ax.barh(siglaParcial, media, color='tab:blue')
            ax.bar_label(barh, fmt='{:,.0f}%')
        i += 1
        ax.set_title(discriminacaoParcial)

        plt.savefig(save_path + discriminacaoParcial)
        plt.close()

        return discriminacao, siglas

def tabelaMediaDP(vectorQuest, filename):
    arq_filtrado = pd.read_csv(filename)

    anos = []
    for quest in vectorQuest:
        anos.append(quest['ano'])

    path = os.getcwd()
    os.chdir(path + '/tabelas')

    medias = []
    desvioPadrao = []
    qtdeAlunosValidos = []
    for ano in anos:
        arq_anual = arq_filtrado[(arq_filtrado['NU_ANO'] == ano)]
        medias.append(np.average(arq_anual['NT_CE']))
        desvioPadrao.append(np.std(arq_anual['NT_CE']))
        qtdeAlunosValidos.append(len(arq_anual))

    dados = {
        'Ano': anos,
        'Alunos validos': qtdeAlunosValidos,
        'Media': medias,
        'Desvio Padrão': desvioPadrao
    }

    tabela = pd.DataFrame(dados)
    tabela.to_csv('Amostra_descritiva.csv')

    os.chdir(path)