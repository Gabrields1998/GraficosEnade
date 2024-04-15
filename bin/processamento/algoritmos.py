import pandas as pd
import numpy as np

def indice_de_discriminacao(vectorQuest, filename, ano: int):
    arq_filtrado = pd.read_csv(filename)
    vet_respostas = arq_filtrado[(arq_filtrado['NU_ANO'] == ano)]
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

    return discriminacao

def indice_de_discriminacao_percentual(discriminacaoPercentualGeral, siglasGeral, vectorDict, save_path, totalDiscriminacaoEspecifica, curso):
    siglas = {}
    for dicionario in vectorDict:
        siglas[dicionario['sigla']] = [0, 0, 0, 0]  # Muito Bom, Bom, Medio, Fraco
        discriminacao = {
            'Muito Bom': 0,
            'Bom': 0,
            'Medio': 0,
            'Fraco': 0
        }

        for ano in totalDiscriminacaoEspecifica:
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
        siglas[dicionario['sigla']] = [discriminacao['Muito Bom'], discriminacao['Bom'],
                                       discriminacao['Medio'], discriminacao['Fraco']]

    for sigla, discriminacaoQtde in siglas.items():
        discriminacaoTotal = sum(discriminacaoQtde)
        discriminacao_media = [0, 0, 0, 0, 0]
        for i in range(0, len(discriminacaoQtde)):
            if (discriminacaoTotal > 0):
                discriminacao_media[i] = (discriminacaoQtde[i] / discriminacaoTotal) * 100

    return discriminacao, discriminacao_media, siglas

def obter_vetor_acertos(vetor_quest, arquivo, ano):
    arq_filtrado = pd.read_csv(arquivo)

    vet_respostas = arq_filtrado[(arq_filtrado['NU_ANO'] == ano)]

    questoes = []
    for quest in vetor_quest:
        if (quest["ano"] == ano):
            questoes = quest

    vet_resultado = []
    for i in range(0, len(questoes["vet_tipo"])):  # alterar questoes por tema
        flag = [questoes["vet_tipo"][i], 0, 0, 0]  # 0 = qual tema, 1 = acertos, 2 = erros, 3 = resto
        for resposta in vet_respostas["DS_VT_ACE_OCE"]:
            vet_res = []

            if (str(resposta) != 'nan'):
                for digito in str(resposta):
                    if (digito != 'Z'):
                        vet_res.append(int(digito))

                if (vet_res[i] == 1):
                    flag[1] += 1
                elif (vet_res[i] == 0):
                    flag[2] += 1
                else:
                    flag[3] += 1

        vet_resultado.append(flag)
    return vet_resultado