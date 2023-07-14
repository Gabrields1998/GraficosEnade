import requests
import zipfile
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import preprocessamentoBCC as ppBCC

def downloadAndExtractZip(url: str, filename: str):
    # Nome do arquivo ZIP após o download
    fileZip = filename + '.zip'

    print(fileZip)

    # Faz o download do arquivo
    response = requests.get(url, verify=False)

    # Abre o arquivo e escreve os dados binários no mesmo
    with open(fileZip, 'wb') as file:
        file.write(response.content)

    # Extrai o conteúdo do arquivo ZIP
    try:
        with zipfile.ZipFile(fileZip, 'r') as zip_ref:
            zip_ref.extractall('.')
            # Renomeia o arquivo para o nome que vem no .zip
            os.rename(zip_ref.namelist()[0][:-1], filename)
    except:
        print("Não foi possivel extrair o arquivo ZIP " + filename + '!')

    try:
        os.remove(fileZip)
    except FileNotFoundError:
        print("O arquivo ZIP não foi encontrado no caminho especificado!")

def readVectorQuest():
    questoes = pd.read_csv('questoes.txt', delimiter=';')

    vetorQuestoes = []

    for i in range (0, len(questoes['NU_ANO'])):
        vetorQuestoes.append({"ano": questoes['NU_ANO'][i], 'vet_tipo': list(map(int, questoes['VET_TIPO'][i].split(',')))})
    
    return vetorQuestoes

def readDictQuest():
    dicionario = pd.read_csv('dicionario.txt', delimiter=';')

    vetorDicionario = []

    for i in range (0, len(dicionario['NUMERO'])):
        vetorDicionario.append({"id": dicionario['NUMERO'][i], 'nome': dicionario['NOME_TIPO'][i],  'sigla': dicionario['SIGLA'][i]})
    
    return vetorDicionario
        
def accessCSVFiles(fileName: str, ano: int, co_grupo: int):
    print(fileName)

    # Entra na pasta DADOS dentro da pasta microdados_enade
    path = os.getcwd() 
    os.chdir(path + '\\' + fileName)
    lista_arquivos = os.listdir() 
    data_path = path + '\\' + fileName + '\\' + lista_arquivos[1]
    os.chdir(data_path)

    # Abrindo o arquivo de entrada como CSV e lendo para o Pandas
    dfArq1 = pd.read_csv('microdados' + str(ano) + '_arq1.txt', delimiter=';')

    dfArq3 = pd.read_csv('microdados' + str(ano) + '_arq3.txt', delimiter=';', dtype={"DS_VT_ACE_OFG": "Int64", "TP_PR_OB_CE": "Int64"})

    # Selecionando as colunas
    dfArq3_columns = dfArq3[['NU_ANO', 'CO_CURSO', 
                         'NU_ITEM_OFG', #'NU_ITEM_OFG_Z', 'NU_ITEM_OFG_X', 'NU_ITEM_OFG_N', prova de 2013 não possui
                         'NU_ITEM_OCE', #'NU_ITEM_OCE_Z', 'NU_ITEM_OCE_X', 'NU_ITEM_OCE_N', prova de 2013 não possui
                         'DS_VT_GAB_OFG_FIN', 'DS_VT_ESC_OFG', 'DS_VT_ACE_OFG',
                         'DS_VT_GAB_OCE_FIN', 'DS_VT_ESC_OCE', 'DS_VT_ACE_OCE',
                         'TP_PRES', 'TP_PR_GER', 'TP_PR_OB_FG', 'TP_PR_DI_FG',
                         'TP_PR_OB_CE', 'TP_PR_DI_CE', 'NT_CE']]
    df1_filtered = pd.DataFrame()
    
    #provas realizadas antes de 2010 possuem subarea
    # if(ano >= 2010):
    dfArq1_columns = dfArq1[['NU_ANO', 'CO_CURSO', 'CO_GRUPO']]
    # filtra o DataFrame de acordo com o ano e o código do grupo passado
    df1_filtered = dfArq1_columns[(dfArq1_columns['NU_ANO'] == ano) & (dfArq1_columns['CO_GRUPO'] == co_grupo)]
    # else:
    #     dfArq1_columns = dfArq1[['NU_ANO', 'CO_CURSO', 'CO_GRUPO', 'CO_SUBAREA']]
    #     # filtra o DataFrame de acordo com o ano e o código do grupo passado
    #     df1_filtered = dfArq1_columns[(dfArq1_columns['NU_ANO'] == ano) & (dfArq1_columns['CO_SUBAREA'] == co_subarea)]
    
    # obtém os CO_CURSOS únicos das linhas encontradas
    unique_co_cursos = df1_filtered["CO_CURSO"].unique()

    # filtra o DataFrame de acordo com a lista de CO_CURSOS obtida anteriormente
    # 556 = Participação com resultado desconsiderado pela Aplicadora**
    # 889 = Prova não realizada por problemas administrativos**

    dfArq3_columns_filtered = dfArq3_columns[(dfArq3_columns['CO_CURSO'].isin(unique_co_cursos)) & (dfArq3_columns['TP_PR_OB_CE'] != 556) & (dfArq3_columns['TP_PR_OB_CE'] != 888) & (dfArq3_columns['TP_PR_OB_CE'] != 889) & (dfArq3_columns['TP_PR_OB_CE'] != 222) & (dfArq3_columns['TP_PR_OB_CE'] != 334)]
    dfArq3_columns_filtered['DS_VT_ACE_OCE'].dropna(axis=0, inplace=True)
    dfArq3_columns_filtered['NT_CE'].fillna(0, inplace=True)
    if(ano == 2005):
        dfArq3_columns_filtered = dfArq3_columns_filtered[dfArq3_columns_filtered.DS_VT_ACE_OCE.str.contains(r'^Z.*Z$')]
    
    os.chdir(path)

    # escreve o arquivo CSV
    return dfArq3_columns_filtered

def getVetAcertos(vectorQuest, filename, ano):
    arq_filtrado = pd.read_csv(filename)
    
    vet_respostas = arq_filtrado[(arq_filtrado['NU_ANO'] == ano)]
    
    questoes = []
    for quest in vectorQuest:
        if(quest["ano"] == ano):
            questoes = quest

    vet_resultado = []
    for i in range (0, len(questoes["vet_tipo"])): #alterar questoes por tema
        flag = [questoes["vet_tipo"][i], 0, 0, 0] # 0 = qual tema, 1 = acertos, 2 = erros, 3 = resto
        for resposta in vet_respostas["DS_VT_ACE_OCE"]:
            vet_res = []

            if(str(resposta) != 'nan'):
                for digito in str(resposta):
                        if(digito != 'Z'):
                            vet_res.append(int(digito))

                if(vet_res[i] == 1):
                    flag[1] += 1
                elif(vet_res[i] == 0):
                    flag[2] += 1
                else:
                    flag[3]+=1

        vet_resultado.append(flag)
    return vet_resultado 

def quantidadeTema(questoes, dicionario):

    quantidade_disciplinas = len(dicionario)
    
    disciplinas_sigla = []
    for dic in dicionario:
        disciplinas_sigla.append(dic['sigla'])
    
    vetQuestTotal = []

    for quest in questoes:
        fig, ax = plt.subplots(figsize=(8,5))
        fig.suptitle("Gráfico da Quantidade questões por tema")

        vetQuestTotal+=quest['vet_tipo']

        flag = quest['vet_tipo']
        qtd_por_tema = []
        for i in range(1, quantidade_disciplinas + 1):
            qtd_por_tema.append(flag.count(i))

        for i in range(0, quantidade_disciplinas):
            barh = ax.barh(disciplinas_sigla[i], qtd_por_tema[i], color = 'tab:blue')
            ax.bar_label(barh, fmt='{:,.0f}')

        ax.set_title(str(quest['ano']))
        plt.savefig(os.getcwd() + '\\GraficosQuantidade\\' + str(quest['ano']))

    fig, ax = plt.subplots(figsize=(8,5))
    fig.suptitle("Gráfico da Quantidade questões por tema")
    
    qtd_por_tema_total = []
    for i in range(1, quantidade_disciplinas + 1):
        qtd_por_tema_total.append(vetQuestTotal.count(i))

    for i in range(0, quantidade_disciplinas):
        barh = ax.barh(disciplinas_sigla[i], qtd_por_tema_total[i], color = 'tab:blue')
        ax.bar_label(barh, fmt='{:,.0f}')
    ax.set_title('Total')

    plt.savefig(os.getcwd() + '\\GraficosQuantidade\\' + str('Total'))
    
    fig, ax = plt.subplots(figsize=(8,5))
    fig.suptitle("Percentual total de questões por tema")
    
    qtde_total = 0
    for qtde in qtd_por_tema_total:
        qtde_total+=qtde
    for i in range(0, quantidade_disciplinas):
        bar = ax.bar(disciplinas_sigla[i], (qtd_por_tema_total[i]/qtde_total)*100, color = 'tab:blue')
        ax.bar_label(bar, fmt='{:,.0f}%')

    plt.savefig(os.getcwd() + '\\GraficosQuantidade\\' + 'TotalPorcentagem')

def percentualAcertos(vectorQuest, vectorDict, filename, ano: int):
    category_names = ['Acertos', 'Erros']

    vet_resultado = getVetAcertos(vectorQuest, filename, ano)

    results = {}
    for dic in vectorDict:
        somaFinal = [0, 0] # 0 = acertos, 1 = erros
        for parcial in vet_resultado:
            if(parcial[0] == dic['id']):
                somaFinal[0] += parcial[1]
                somaFinal[1] += parcial[2]
        
        mediaAcertos = 0
        mediaErros = 0
        total = somaFinal[0]+somaFinal[1]
        if(total != 0):
            mediaAcertos = (somaFinal[0]/total) * 100
            mediaErros = (somaFinal[1]/total) * 100
        results[dic['sigla']] = [mediaAcertos, mediaErros]

    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['PRGn'](
        np.linspace(0.85, 0.15, data.shape[1]))

    fig, ax = plt.subplots(figsize=(8,5))

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
    
    plt.savefig(os.getcwd() + '\\GraficosPercentualAcertos\\' + str(ano))

def indiceFacilidade(vectorQuest, filename, ano: int):
    vet_resultado = getVetAcertos(vectorQuest, filename, ano)
    
    results = {}
    j=0
    for parcial in vet_resultado:
        j+=1
    
        mediaAcertos = 0
        mediaErros = 0
        total = parcial[1] + parcial[2]
        disciplina = parcial[0]

        if(total != 0):
            mediaAcertos = (parcial[1]/total) * 100
            mediaErros = (parcial[2]/total) * 100
        results[j] = [mediaAcertos, mediaErros, disciplina]
    
    facilidade = {
        'Muito Dificil': 0,
        'Dificil': 0,
        'Medio': 0,
        'Facil': 0,
        'Muito Facil': 0
    }

    for atributo, valor in results.items():
        if(valor[0] != 0):
            if(round(valor[0]) <= 15):
                facilidade['Muito Dificil'] += 1
            elif(round(valor[0]) >= 16 and round(valor[0]) <= 40):
                facilidade['Dificil'] += 1
            elif(round(valor[0]) >= 41 and round(valor[0]) <= 60):
                facilidade['Medio'] += 1
            elif(round(valor[0]) >= 61 and round(valor[0]) <= 85):
                facilidade['Facil'] += 1
            elif(round(valor[0]) >= 86):
                facilidade['Muito Facil'] += 1

    fig, ax = plt.subplots(figsize=(8,5))
    fig.suptitle("Indice de facilidade " + str(ano))
    
    for atributo, valor in facilidade.items():
        bar = ax.bar(atributo, valor, color = 'tab:blue')
        ax.bar_label(bar, fmt='{:,.0f}')

    plt.savefig(os.getcwd() + '\\GraficosFacilidade\\' + str(ano))
    
    return facilidade, results

def facilidadePercentual(totalAcertos, vectorDict):
    siglas = {}
    for dicionario in vectorDict:
        siglas[dicionario['sigla']] = [0, 0, 0, 0, 0] #muito dificil, dificil, medio, facil, muito facil
        facilidade = {
            'Muito Dificil': 0,
            'Dificil': 0,
            'Medio': 0,
            'Facil': 0,
            'Muito Facil': 0
        }

        for ano in totalAcertos:
            for atributo, valor in ano.items():
                if(dicionario['id'] == valor[2]):
                    if(valor[0] != 0):
                        if(round(valor[0]) <= 15):
                            facilidade['Muito Dificil'] += 1
                        elif(round(valor[0]) >= 16 and round(valor[0]) <= 40):
                            facilidade['Dificil'] += 1
                        elif(round(valor[0]) >= 41 and round(valor[0]) <= 60):
                            facilidade['Medio'] += 1
                        elif(round(valor[0]) >= 61 and round(valor[0]) <= 85):
                            facilidade['Facil'] += 1
                        elif(round(valor[0]) >= 86):
                            facilidade['Muito Facil'] += 1
        siglas[dicionario['sigla']] = [facilidade['Muito Dificil'], facilidade['Dificil'], facilidade['Medio'], facilidade['Facil'], facilidade['Muito Facil']]

    for sigla, facilidadeQtde in siglas.items():
        facilidadeTotal = sum(facilidadeQtde)
        facilidadeMedia = [0, 0, 0, 0, 0]
        for i in range(0, len(facilidadeQtde)):
            if(facilidadeTotal > 0):
                facilidadeMedia[i] = (facilidadeQtde[i] / facilidadeTotal) * 100

        fig, ax = plt.subplots(figsize=(8,5))
        fig.suptitle("Gráfico de Tema por Facilidade")
        
        i = 0
        for facilidadeParcial, num in facilidade.items():
            barh = ax.barh(facilidadeParcial, facilidadeMedia[i], color = 'tab:blue')
            ax.bar_label(barh, fmt='{:,.0f}%')
            i+=1
        ax.set_title(sigla)

        plt.savefig(os.getcwd() + '\\GraficosFacilidadePercentual\\' + sigla)

    
    i = 0
    for facilidadeParcial, num in facilidade.items():
        facilidadeQtdeTotal = 0
        for siglaParcial, qtde in siglas.items():
            facilidadeQtdeTotal += qtde[i]

        fig, ax = plt.subplots(figsize=(8,5))
        fig.suptitle("Gráfico de Facilidade por Tema")
        
        for siglaParcial, qtde in siglas.items():
            media = 0
            if(facilidadeQtdeTotal > 0):
                media = (qtde[i] / facilidadeQtdeTotal) * 100
            barh = ax.barh(siglaParcial, media, color = 'tab:blue')
            ax.bar_label(barh, fmt='{:,.0f}%')
        i+=1
        ax.set_title(facilidadeParcial)

        plt.savefig(os.getcwd() + '\\GraficosFacilidadePercentual\\' + facilidadeParcial)

def indiceDiscriminacao(vectorQuest, filename, ano: int):
    arq_filtrado = pd.read_csv(filename)
    vet_respostas = arq_filtrado[(arq_filtrado['NU_ANO'] == ano)]
    vet_respostas = vet_respostas.reset_index(0)

    cr_linha = np.average(vet_respostas['NT_CE'])

    sr = np.std(vet_respostas['NT_CE'])

    questoes = []
    for quest in vectorQuest:
        if(quest["ano"] == ano):
            questoes = quest

    vet_ponto_bisserial = []
    for i in range (0, len(questoes["vet_tipo"])): #alterar questoes por tema
        vet_ca_linha = []
        acertaram = 0
        j = 0
        for resposta in vet_respostas["DS_VT_ACE_OCE"]:
            vet_res = []

            if(str(resposta) != 'nan'):
                for digito in str(resposta):
                        if(digito != 'Z'):
                            vet_res.append(int(digito))
                
                if(vet_res[i] == 1):
                    vet_ca_linha.append(vet_respostas['NT_CE'][j])
                    acertaram += 1
            j+=1
        ca_linha = 0
        if(len(vet_ca_linha) != 0):
            ca_linha = np.average(vet_ca_linha)

        p = 0
        if(len(vet_respostas["DS_VT_ACE_OCE"]) > 0):
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
        if(valor[1] != 0):
            if(valor[1] <= 0.19):
                discriminacao['Muito Bom'] += 1
            elif(valor[1] > 0.19 and valor[1] <= 0.29):
                discriminacao['Bom'] += 1
            elif(valor[1] > 0.29 and valor[1] <= 0.39):
                discriminacao['Medio'] += 1
            elif(valor[1] > 0.39):
                discriminacao['Fraco'] += 1

    fig, ax = plt.subplots(figsize=(8,5))
    fig.suptitle("Indice de Discriminação " + str(ano))

    for atributo, valor in discriminacao.items():

        bar = ax.bar(atributo, valor, color = 'tab:blue')
        ax.bar_label(bar, fmt='{:,.0f}')

    plt.savefig(os.getcwd() + '\\GraficosDiscriminacao\\' + str(ano))

    return discriminacao, vet_ponto_bisserial

def discriminacaoPercentual(totalDiscriminacao, vectorDict):
    siglas = {}
    for dicionario in vectorDict:
        siglas[dicionario['sigla']] = [0, 0, 0, 0] #Muito Bom, Bom, Medio, Fraco
        discriminacao = {
            'Muito Bom': 0,
            'Bom': 0,
            'Medio': 0,
            'Fraco': 0
        }
    
        for ano in totalDiscriminacao:
            for valor in ano:
                if(dicionario['id'] == valor[0]):
                    if(valor[1] > 0):
                        if(valor[1] <= 0.19):
                            discriminacao['Muito Bom'] += 1
                        elif(valor[1] > 0.19 and valor[1] <= 0.29):
                            discriminacao['Bom'] += 1
                        elif(valor[1] > 0.29 and valor[1] <= 0.39):
                            discriminacao['Medio'] += 1
                        elif(valor[1] > 0.39):
                            discriminacao['Fraco'] += 1
        siglas[dicionario['sigla']] = [discriminacao['Muito Bom'], discriminacao['Bom'], discriminacao['Medio'], discriminacao['Fraco']]

    for sigla, discriminacaoQtde in siglas.items():
        discriminacaoTotal = sum(discriminacaoQtde)
        discriminacaoMedia = [0, 0, 0, 0, 0]
        for i in range(0, len(discriminacaoQtde)):
            if(discriminacaoTotal > 0):
                discriminacaoMedia[i] = (discriminacaoQtde[i] / discriminacaoTotal) * 100

        fig, ax = plt.subplots(figsize=(8,5))
        fig.suptitle("Gráfico de Tema por Discriminacao")
        
        i = 0
        for discriminacaoParcial, num in discriminacao.items():
            barh = ax.barh(discriminacaoParcial, discriminacaoMedia[i], color = 'tab:blue')
            ax.bar_label(barh, fmt='{:,.0f}%')
            i+=1
        ax.set_title(sigla)

        plt.savefig(os.getcwd() + '\\GraficosDiscriminacaoPercentual\\' + sigla)
    
    i = 0
    for discriminacaoParcial, num in discriminacao.items():
        discriminacaoQtdeTotal = 0
        for siglaParcial, qtde in siglas.items():
            discriminacaoQtdeTotal += qtde[i]

        fig, ax = plt.subplots(figsize=(8,5))
        fig.suptitle("Gráfico de Discriminacao por Tema")
        
        for siglaParcial, qtde in siglas.items():
            media = 0
            if(discriminacaoQtdeTotal > 0):
                media = (qtde[i] / discriminacaoQtdeTotal) * 100
            barh = ax.barh(siglaParcial, media, color = 'tab:blue')
            ax.bar_label(barh, fmt='{:,.0f}%')
        i+=1
        ax.set_title(discriminacaoParcial)

        plt.savefig(os.getcwd() + '\\GraficosDiscriminacaoPercentual\\' + discriminacaoParcial)

def tabelaMediaDP(vectorQuest, filename):

    arq_filtrado = pd.read_csv(filename)

    anos = []
    for quest in vectorQuest:
        anos.append(quest['ano'])

    path = os.getcwd() 
    os.chdir(path + '\\Tabelas')

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

def main():

    """
    CABEÇALHO
    dicionario utilizado para facilitar o controle do sistema
    """
    microdadoCabeçalhos = [
        {'nome': 'microdados_enade_2021', 'ano': 2021},
        {'nome': 'microdados_enade_2019_LGPD', 'ano': 2019},
        {'nome':  'microdados_enade_2018_LGPD', 'ano': 2018},
        {'nome': 'microdados_enade_2017_LGPD', 'ano': 2017},
        {'nome':  'microdados_enade_2016_LGPD', 'ano': 2016},
        {'nome': 'microdados_enade_2015_LGPD', 'ano': 2015},
        {'nome': 'microdados_enade_2014_LGPD', 'ano': 2014},
        {'nome': 'microdados_enade_2013_LGPD', 'ano': 2013}, 
        {'nome': 'microdados_enade_2012_LGPD', 'ano': 2012},
        {'nome': 'microdados_enade_2011', 'ano': 2011}, 
        {'nome': 'microdados_enade_2010', 'ano': 2010}, 
        {'nome': 'microdados_enade_2009', 'ano': 2009}, 
        {'nome': 'microdados_enade_2008', 'ano': 2008}, 
        {'nome': 'microdados_enade_2007', 'ano': 2007}, 
        {'nome': 'microdados_enade_2006', 'ano': 2006}, 
        {'nome': 'microdados_enade_2005', 'ano': 2005}, 
        {'nome': 'microdados_enade_2004', 'ano': 2004}]

    diretorioAtual = os.listdir()

    """
    LEITOR
    area que le os arquivos que contem os temas das questões e seus dicionarios
    """
    vectorQuest = readVectorQuest()
    vectorDict = readDictQuest()

    """
    DOWNLOAD
    area responsavel pelo download dos microdados do enade (todos que estiverem no cabeçalho)
    """
    for cabeçalho in microdadoCabeçalhos:
        if cabeçalho['nome'] not in diretorioAtual:
            downloadAndExtractZip('https://download.inep.gov.br/microdados/' + cabeçalho['nome'] + '.zip', cabeçalho['nome'])

    """
    PRE PROCESSAMENTO
    pre processamento dos microdados para que o sistema funcione corretamente para anos que não seguem
    o padrão instituido pelo enade (neste caso referente a BCC)
    """
    ppBCC.processa_BCC_2008()
    ppBCC.processa_BCC_2005()

    """
    FILTRAGEM
    area onde os arquivos são filtrados e unidos em um unico arquivo filtrado.csv
    eles são filtrados por grupo e por alunos que realmente fizeram a prova
    """
    co_grupo = int(input("Digite o código do grupo desejado: "))

    arq_filtrado = pd.DataFrame()

    for dic in microdadoCabeçalhos:
        for vec in vectorQuest:
            if dic['ano'] == vec['ano']: 
                arq_filtrado = pd.concat([arq_filtrado, accessCSVFiles(dic['nome'], dic['ano'], co_grupo)], ignore_index = True)
    arq_filtrado.to_csv("filtrado.csv")
    
    """
    GRAFICOS DE QUANTIDADE DE TEMAS
    """
    quantidadeTema(vectorQuest, vectorDict)
    
    """
    GRAFICOS DE PERCENTUAL DE ACERTOS
    """
    for vec in vectorQuest:
        percentualAcertos(vectorQuest, vectorDict, "filtrado.csv", vec['ano'])

    """
    GRAFICOS DE FACILIDADE
    """
    totalFacilidade = {
        'Muito Dificil': 0,
        'Dificil': 0,
        'Medio': 0,
        'Facil': 0,
        'Muito Facil': 0
    }

    totalFacilidadeQuantidade = []

    for vec in vectorQuest:
        parcialFacilidade, results = indiceFacilidade(vectorQuest, "filtrado.csv", vec['ano'])
        totalFacilidade['Muito Dificil'] += parcialFacilidade['Muito Dificil']
        totalFacilidade['Dificil'] += parcialFacilidade['Dificil']
        totalFacilidade['Medio'] += parcialFacilidade['Medio']
        totalFacilidade['Facil'] += parcialFacilidade['Facil']
        totalFacilidade['Muito Facil'] += parcialFacilidade['Muito Facil']
        totalFacilidadeQuantidade.append(results)

    facilidadePercentual(totalFacilidadeQuantidade, vectorDict)

    fig, ax = plt.subplots(figsize=(8,5))
    fig.suptitle("Indice de facilidade Total")
    
    for atributo, valor in totalFacilidade.items():
        bar = ax.bar(atributo, valor, color = 'tab:blue')
        ax.bar_label(bar, fmt='{:,.0f}')

    plt.savefig(os.getcwd() + '\\GraficosFacilidade\\Total')

    """
    GRAFICOS DE DISCRIMINAÇÃO
    """
    totalDiscriminacao = {
        'Muito Bom': 0,
        'Bom': 0,
        'Medio': 0,
        'Fraco': 0
    }

    totalDiscriminacaoQuantidade = []
    for vec in vectorQuest:
        parcialDiscriminacao, pontoBisserial = indiceDiscriminacao(vectorQuest, "filtrado.csv", vec['ano'])
        totalDiscriminacao['Muito Bom'] += parcialDiscriminacao['Muito Bom']
        totalDiscriminacao['Bom'] += parcialDiscriminacao['Bom']
        totalDiscriminacao['Medio'] += parcialDiscriminacao['Medio']
        totalDiscriminacao['Fraco'] += parcialDiscriminacao['Fraco']
        totalDiscriminacaoQuantidade.append(pontoBisserial)

    discriminacaoPercentual(totalDiscriminacaoQuantidade, vectorDict)
    
    fig, ax = plt.subplots(figsize=(8,5))
    fig.suptitle("Indice de Discriminação Total")
    
    for atributo, valor in totalDiscriminacao.items():

        bar = ax.bar(atributo, valor, color = 'tab:blue')
        ax.bar_label(bar, fmt='{:,.0f}')

    plt.savefig(os.getcwd() + '\\GraficosDiscriminacao\\Total')
    
    """
    TABELAS DESCRITIVAS
    """

    tabelaMediaDP(vectorQuest, "filtrado.csv")

if __name__ == "__main__":
    main()


