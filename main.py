import os
import matplotlib.pyplot as plt

# TODO preparar o arquivo de pré processamento no futuro
#import preProcessamentoBCC # USADO PARA OS ANOS < 2010
from bin import leitor, filtra_arquivos, baixa_bases_de_dados, cria_diretorios, gera_graficos_geral, \
    le_entrada_terminal, gera_graficos_especificos

if __name__ == '__main__':
    cria_diretorios.diretorios_graficos()
    cria_diretorios.diretorios_tabelas()
    cria_diretorios.diretorios_microdados()


    '''
    LEITOR
    area que le os arquivos que contem os temas das questões e seus dicionarios
    '''
    vectorQuest = leitor.readVectorQuest()
    vectorDict = leitor.readDictQuest()

    '''
    DOWNLOAD
    area responsavel pelo download dos microdados do enade (todos que estiverem no cabeçalho)
    '''

    microdado_cabecalhos_padrao_pasta = baixa_bases_de_dados.compara_cabecalhos_e_baixa()

    '''
    PRE PROCESSAMENTO
    pre processamento dos microdados para que o sistema funcione corretamente para anos que não seguem
    o padrão instituido pelo enade (neste caso referente a BCC)
    '''
    # preProcessamentoBCC.processa_BCC_2008()
    # preProcessamentoBCC.processa_BCC_2005()

    co_grupo, co_curso = le_entrada_terminal.informa_grupo_e_curso()

    filtra_arquivos.filtrado_para_csv(microdado_cabecalhos_padrao_pasta, vectorQuest, co_grupo)

    '''
    GRAFICOS DE QUANTIDADE DE TEMAS
    '''
    gera_graficos_geral.quantidadeTema(vectorQuest, vectorDict, (os.getcwd() + '/graficos/GraficosQuantidade/'))

    '''
    GRAFICOS DE PERCENTUAL DE ACERTOS
    '''
    for vec in vectorQuest:
        gera_graficos_geral.percentualAcertos(vectorQuest,
                                              vectorDict,
                                              "tabelas/dados_filtrados.csv",
                                              vec['ano'],
                                              (os.getcwd() + '/graficos/GraficosPercentualAcertos/' + str(vec['ano'])))

    '''
    GRAFICOS DE FACILIDADE
    '''
    totalFacilidade = {
        'Muito Dificil': 0,
        'Dificil': 0,
        'Medio': 0,
        'Facil': 0,
        'Muito Facil': 0
    }

    totalFacilidadeQuantidade = []

    for vec in vectorQuest:
        parcialFacilidade, results = gera_graficos_geral.indiceFacilidade(vectorQuest, "tabelas/dados_filtrados.csv", vec['ano'], (os.getcwd() + '/graficos/GraficosFacilidade/' + str(vec['ano'])))
        totalFacilidade['Muito Dificil'] += parcialFacilidade['Muito Dificil']
        totalFacilidade['Dificil'] += parcialFacilidade['Dificil']
        totalFacilidade['Medio'] += parcialFacilidade['Medio']
        totalFacilidade['Facil'] += parcialFacilidade['Facil']
        totalFacilidade['Muito Facil'] += parcialFacilidade['Muito Facil']
        totalFacilidadeQuantidade.append(results)

    gera_graficos_geral.facilidadePercentual(totalFacilidadeQuantidade, vectorDict, (os.getcwd() + '/graficos/GraficosFacilidadePercentual/'))

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle("Indice de facilidade Total")

    for atributo, valor in totalFacilidade.items():
        bar = ax.bar(atributo, valor, color='tab:blue')
        ax.bar_label(bar, fmt='{:,.0f}')

    plt.savefig(os.getcwd() + '/graficos/GraficosFacilidade/Total')

    '''
    GRAFICOS DE DISCRIMINAÇÃO
    '''
    totalDiscriminacao = {
        'Muito Bom': 0,
        'Bom': 0,
        'Medio': 0,
        'Fraco': 0
    }

    totalDiscriminacaoQuantidade = []
    vecParcialDiscriminacao = []

    for vec in vectorQuest:
        parcialDiscriminacao, pontoBisserial = gera_graficos_geral.grafico_de_discriminacao(vectorQuest,
                                                                                            'tabelas/dados_filtrados.csv', vec['ano'], (os.getcwd() + '/graficos/GraficosDiscriminacao/' + str(vec['ano'])))

        vecParcialDiscriminacao.append(parcialDiscriminacao)

        totalDiscriminacao['Muito Bom'] += parcialDiscriminacao['Muito Bom']
        totalDiscriminacao['Bom'] += parcialDiscriminacao['Bom']
        totalDiscriminacao['Medio'] += parcialDiscriminacao['Medio']
        totalDiscriminacao['Fraco'] += parcialDiscriminacao['Fraco']
        totalDiscriminacaoQuantidade.append(pontoBisserial)

    vecParcialDiscriminacao.reverse()

    discriminacaoPercentualGeral, siglasGeral = gera_graficos_geral.discriminacaoPercentual(totalDiscriminacaoQuantidade, vectorDict, (os.getcwd() + '/graficos/GraficosDiscriminacaoPercentual/'))

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle("Indice de Discriminação Total")

    for atributo, valor in totalDiscriminacao.items():
        bar = ax.bar(atributo, valor, color='tab:blue')
        ax.bar_label(bar, fmt='{:,.0f}')

    plt.savefig(os.getcwd() + '/graficos/GraficosDiscriminacao/Total')

    '''
    TABELAS DESCRITIVAS
    '''
    gera_graficos_geral.tabelaMediaDP(vectorQuest, "./tabelas/dados_filtrados.csv")

    '''
    GRÁFICOS ESPECÍFICOS DOS CURSOS ESCOLHIDO
    '''
    for x in co_curso:
        if x != -1:
            try:
                gera_graficos_especificos.especifico(vectorQuest, vectorDict,
                                                     totalDiscriminacaoQuantidade, "./tabelas/dados_filtrados.csv",
                                                     x, totalFacilidadeQuantidade,
                                                     vecParcialDiscriminacao, discriminacaoPercentualGeral,
                                                     siglasGeral)

            except OSError as e:
                print(str(e) + '\nDetalhes:\nErro no seguinte valor informado:\n' + str(x))
