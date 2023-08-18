import os
import pandas as pd
import matplotlib.pyplot as plt

#import preProcessamentoBCC # USADO PARA OS ANOS < 2010
import getDatabases
import createDir
from processamento import processamentoGraficos
import processamentoArquivos
import leitor

if __name__ == '__main__':

    # Preparação do ambiente, apagando as informações antigas e
    # recriando as pastas onde ficarão as novas informações.

    createDir.graphicsDir()
    createDir.tablesDir()

    """
        CABEÇALHO
        dicionario utilizado para facilitar o controle do sistema
    """

    microdadoCabeçalhos = [
        {'nome': 'microdados_enade_2021', 'ano': 2021},
        {'nome': 'microdados_enade_2019_LGPD', 'ano': 2019},
        {'nome': 'microdados_enade_2018_LGPD', 'ano': 2018},
        {'nome': 'microdados_enade_2017_LGPD', 'ano': 2017},
        {'nome': 'microdados_enade_2016_LGPD', 'ano': 2016},
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

    # MICRODADOS QUE ESTÃO DANDO PROBLEMA
    '''{'nome': 'microdados_enade_2009', 'ano': 2009},
        {'nome': 'microdados_enade_2008', 'ano': 2008}, 
        {'nome': 'microdados_enade_2007', 'ano': 2007}, 
        {'nome': 'microdados_enade_2006', 'ano': 2006}, 
        {'nome': 'microdados_enade_2005', 'ano': 2005}, 
        {'nome': 'microdados_enade_2004', 'ano': 2004}]'''

    diretorioAtual = os.listdir()
    print('Diretório atual: ', diretorioAtual)

    """
    LEITOR
    area que le os arquivos que contem os temas das questões e seus dicionarios
    """
    vectorQuest = leitor.readVectorQuest()
    vectorDict = leitor.readDictQuest()

    """
    DOWNLOAD
    area responsavel pelo download dos microdados do enade (todos que estiverem no cabeçalho)
    """
    for cabeçalho in microdadoCabeçalhos:
        if cabeçalho['nome'] not in diretorioAtual:
            getDatabases.downloadAndExtractZip('https://download.inep.gov.br/microdados/' + cabeçalho['nome'] + '.zip',
                                  cabeçalho['nome'])

    """
    PRE PROCESSAMENTO
    pre processamento dos microdados para que o sistema funcione corretamente para anos que não seguem
    o padrão instituido pelo enade (neste caso referente a BCC)
    """
    # preProcessamentoBCC.processa_BCC_2008()
    # preProcessamentoBCC.processa_BCC_2005()

    """
    FILTRAGEM
    area onde os arquivos são filtrados e unidos em um unico arquivo filtrado.csv
    eles são filtrados por grupo e por alunos que realmente fizeram a prova
    """
    co_grupo = int(input("Digite o código do grupo desejado:\nBCC - 4004\n>> "))

    arq_filtrado = pd.DataFrame()

    for dic in microdadoCabeçalhos:
        for vec in vectorQuest:
            if dic['ano'] == vec['ano']:
                arq_filtrado = pd.concat([arq_filtrado, processamentoArquivos.accessCSVFiles(dic['nome'], dic['ano'], co_grupo)],
                                         ignore_index=True)
    arq_filtrado.to_csv("filtrado.csv")

    """
    GRAFICOS DE QUANTIDADE DE TEMAS
    """
    processamentoGraficos.quantidadeTema(vectorQuest, vectorDict)

    """
    GRAFICOS DE PERCENTUAL DE ACERTOS
    """
    for vec in vectorQuest:
        processamentoGraficos.percentualAcertos(vectorQuest, vectorDict, "filtrado.csv", vec['ano'])

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
        parcialFacilidade, results = processamentoGraficos.indiceFacilidade(vectorQuest, "filtrado.csv", vec['ano'])
        totalFacilidade['Muito Dificil'] += parcialFacilidade['Muito Dificil']
        totalFacilidade['Dificil'] += parcialFacilidade['Dificil']
        totalFacilidade['Medio'] += parcialFacilidade['Medio']
        totalFacilidade['Facil'] += parcialFacilidade['Facil']
        totalFacilidade['Muito Facil'] += parcialFacilidade['Muito Facil']
        totalFacilidadeQuantidade.append(results)

    processamentoGraficos.facilidadePercentual(totalFacilidadeQuantidade, vectorDict)

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle("Indice de facilidade Total")

    for atributo, valor in totalFacilidade.items():
        bar = ax.bar(atributo, valor, color='tab:blue')
        ax.bar_label(bar, fmt='{:,.0f}')

    plt.savefig(os.getcwd() + '/graphics/GraficosFacilidade/Total')

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
        parcialDiscriminacao, pontoBisserial = processamentoGraficos.indiceDiscriminacao(vectorQuest, "filtrado.csv", vec['ano'])
        totalDiscriminacao['Muito Bom'] += parcialDiscriminacao['Muito Bom']
        totalDiscriminacao['Bom'] += parcialDiscriminacao['Bom']
        totalDiscriminacao['Medio'] += parcialDiscriminacao['Medio']
        totalDiscriminacao['Fraco'] += parcialDiscriminacao['Fraco']
        totalDiscriminacaoQuantidade.append(pontoBisserial)

    processamentoGraficos.discriminacaoPercentual(totalDiscriminacaoQuantidade, vectorDict)

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle("Indice de Discriminação Total")

    for atributo, valor in totalDiscriminacao.items():
        bar = ax.bar(atributo, valor, color='tab:blue')
        ax.bar_label(bar, fmt='{:,.0f}')

    plt.savefig(os.getcwd() + '/graphics/GraficosDiscriminacao/Total')

    """
    TABELAS DESCRITIVAS
    """

    processamentoGraficos.tabelaMediaDP(vectorQuest, "filtrado.csv")