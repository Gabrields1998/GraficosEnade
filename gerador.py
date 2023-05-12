import requests
import zipfile
import os
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


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
    # alterar o nome de VET_TIPO para VET_TOPICO
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

    dfArq3 = pd.read_csv('microdados' + str(ano) + '_arq3.txt', delimiter=';', dtype={"DS_VT_ACE_OFG": "Int64"})

    # Selecionando as colunas
    dfArq1_columns = dfArq1[['NU_ANO', 'CO_CURSO', 'CO_GRUPO']]

    dfArq3_columns = dfArq3[['NU_ANO', 'CO_CURSO', 
                         'NU_ITEM_OFG', #'NU_ITEM_OFG_Z', 'NU_ITEM_OFG_X', 'NU_ITEM_OFG_N', prova de 2013 não possui
                         'NU_ITEM_OCE', #'NU_ITEM_OCE_Z', 'NU_ITEM_OCE_X', 'NU_ITEM_OCE_N', prova de 2013 não possui
                         'DS_VT_GAB_OFG_FIN', 'DS_VT_ESC_OFG', 'DS_VT_ACE_OFG',
                         'DS_VT_GAB_OCE_FIN', 'DS_VT_ESC_OCE', 'DS_VT_ACE_OCE',
                         'TP_PRES', 'TP_PR_GER', 'TP_PR_OB_FG', 'TP_PR_DI_FG',
                         'TP_PR_OB_CE', 'TP_PR_DI_CE']]

    # filtra o DataFrame de acordo com o ano e o código do grupo passado
    df1_filtered = dfArq1_columns[(dfArq1_columns['NU_ANO'] == ano) & (dfArq1_columns['CO_GRUPO'] == co_grupo)]

    # obtém os CO_CURSOS únicos das linhas encontradas
    unique_co_cursos = df1_filtered["CO_CURSO"].unique()

    # filtra o DataFrame de acordo com a lista de CO_CURSOS obtida anteriormente
    dfArq3_columns_filtered = dfArq3_columns[dfArq3_columns['CO_CURSO'].isin(unique_co_cursos)]

    # adiciona as outras colunas na tabela filtrada de acordo com a lista unica de CO_CURSOS
    # for row in unique_co_cursos:
    #     dfArq3_columns_filtered = pd.concat(dfArq3_columns_filtered, df1_filtered[df1_filtered['CO_CURSO'] == row])

    os.chdir(path)

    # escreve o arquivo CSV
    return dfArq3_columns_filtered

    #importante: trazer os outros campos do arquivo 1, eles são unicos por CO_CURSO
    #importante: filtrar retirando do database os alunos que não fizeram/vieram/colaram/... a prova
    #importante: pegar o paper e replicar as tabelas de la
    #importante: pegar a prova escrita e dividir em temas (ver os temas no paper)

def plotGraph(filename: str):
    print("questões objetivas da formação geral")
    dfArq3 = pd.read_csv(filename)
    
    nu_item_ofg = dfArq3['NU_ITEM_OFG'].unique()
    
    # Obtendo todos os valores de DS_VT_ACE_OFG
    vt_ace_ofg = dfArq3['DS_VT_ACE_OFG']
    print("tamanho vetor: " + str(nu_item_ofg[0]))
    print("tabela:")
    print(vt_ace_ofg)
    # Variáveis para acerto, erro e anulado
    acertos = 0
    erros = 0
    anulado = 0

    vt_ace_ofg_tranformado = []

    # Vetor para armazenar o numero convertido em 8 posições 
    vetor_transformado = [0] * nu_item_ofg[0]

    # Convertendo o número para o vetor.
    for numero in vt_ace_ofg:
        for i in range(nu_item_ofg[0]):
            if (numero != 0 and not math.isnan(numero)): 
                vetor_transformado[7 - i] = int(numero % 10) 
                numero = int(numero / 10) 
        vt_ace_ofg_tranformado.append(vetor_transformado)
        vetor_transformado = [0] * nu_item_ofg[0]     
    
    # Iterando cada valor do vetor
    for v in vt_ace_ofg_tranformado:
        if v[2] == 1:
            acertos += 1
        elif v[2] == 0:
            erros += 1
        else:
            anulado += 1
    
    # Calculando média dos acertos e erros
    media_acerto = acertos / len(vt_ace_ofg)
    media_erro = erros / len(vt_ace_ofg)

    # Construindo labels para o gráfico
    labels = ['Acertos', 'Erros']

    # Gráfico de barra simples
    plt.bar(labels, [media_acerto, media_erro])

    # Nomes para o eixo x
    plt.xlabel('Médias de acertos e erros na questão 3')
    # Nome para o eixo y
    plt.ylabel('Valores')
    # Título do gráfico
    plt.title('Gráfico de Acertos e Erros dos Alunos')

    # Exibindo o gráfico
    plt.show()

def quantidadeTema(questoes, dicionario):

    quantidade_disciplinas = len(dicionario)
    
    disciplinas_sigla = []
    for dic in dicionario:
        disciplinas_sigla.append(dic['sigla'])
    vetQuest = []

    for quest in questoes:
        vetQuest+=quest['vet_tipo']

    qtd_por_disciplina = []
    for i in range(1, quantidade_disciplinas + 1):
        qtd_por_disciplina.append(vetQuest.count(i))

    fig, ax = plt.subplots(figsize=(8,5))
    handles = []
    for i in range(0, quantidade_disciplinas):
        ax.bar(disciplinas_sigla[i], qtd_por_disciplina[i], color = ['black'], label = i)

    fig.legend(disciplinas_sigla, ncol=1, loc='upper right')
    ax.set_title("Gráfico de Barras da Quantidade de Disciplinas")
    ax.set_xlabel("Disciplina")
    ax.set_ylabel("Quantidade")


    # Sumario para cada disciplina
    # legenda = []
    # for key,value in data_dict.items():
    #     legenda.append(str(key) + " - " + str(value))

    # fig.legend(quantidade_disciplinas_sigla, legenda, loc='upper right')

    plt.show()

def main():
    # # não estão funcionando de 2009 para tras na minha maquina
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

    vectorQuest = readVectorQuest()
    vectorDict = readDictQuest()

    for cabeçalho in microdadoCabeçalhos:
        if cabeçalho['nome'] not in diretorioAtual:
            downloadAndExtractZip('https://download.inep.gov.br/microdados/' + cabeçalho['nome'] + '.zip', cabeçalho['nome'])

    co_grupo = int(input("Digite o código do grupo desejado: "))

    arq_filtrado = pd.DataFrame()

    for dic in microdadoCabeçalhos:
        for vec in vectorQuest:
            if dic['ano'] == vec['ano']: 
                arq_filtrado = pd.concat([arq_filtrado, accessCSVFiles(dic['nome'], dic['ano'], co_grupo)], ignore_index = True)
    arq_filtrado.to_csv("filtrado.csv")

    # plotGraph('arq_filtrado.csv')    
    quantidadeTema(vectorQuest, vectorDict)


if __name__ == "__main__":
    main()


