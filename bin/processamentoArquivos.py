import pandas as pd
import os


def accessCSVFiles(fileName: str, ano: int, co_grupo: int):
    print(fileName)

    # Entra na pasta DADOS dentro da pasta microdados_enade
    path = os.getcwd()
    os.chdir(path + '/' + fileName)
    lista_arquivos = os.listdir()
    data_path = path + '/' + fileName + '/' + lista_arquivos[0]
    os.chdir(data_path)

    # TESTE
    print('Lista de arquivos: ', lista_arquivos)
    print('Caminho: ' + path)
    print('Caminho dos dados: ' + data_path)

    # Abrindo o arquivo de entrada como CSV e lendo para o Pandas
    dfArq1 = pd.read_csv('microdados' + str(ano) + '_arq1.txt', delimiter=';')

    dfArq3 = pd.read_csv('microdados' + str(ano) + '_arq3.txt', delimiter=';',
                         dtype={"DS_VT_ACE_OFG": "Int64", "TP_PR_OB_CE": "Int64"})

    # Selecionando as colunas
    dfArq3_columns = dfArq3[['NU_ANO', 'CO_CURSO',
                             'NU_ITEM_OFG',
                             # 'NU_ITEM_OFG_Z', 'NU_ITEM_OFG_X', 'NU_ITEM_OFG_N', prova de 2013 não possui
                             'NU_ITEM_OCE',
                             # 'NU_ITEM_OCE_Z', 'NU_ITEM_OCE_X', 'NU_ITEM_OCE_N', prova de 2013 não possui
                             'DS_VT_GAB_OFG_FIN', 'DS_VT_ESC_OFG', 'DS_VT_ACE_OFG',
                             'DS_VT_GAB_OCE_FIN', 'DS_VT_ESC_OCE', 'DS_VT_ACE_OCE',
                             'TP_PRES', 'TP_PR_GER', 'TP_PR_OB_FG', 'TP_PR_DI_FG',
                             'TP_PR_OB_CE', 'TP_PR_DI_CE', 'NT_CE']]

    df1_filtered = pd.DataFrame()

    # provas realizadas antes de 2010 possuem subarea
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

    dfArq3_columns_filtered = dfArq3_columns[
        (dfArq3_columns['CO_CURSO'].isin(unique_co_cursos)) & (dfArq3_columns['TP_PR_OB_CE'] != 556) & (
                    dfArq3_columns['TP_PR_OB_CE'] != 888) & (dfArq3_columns['TP_PR_OB_CE'] != 889) & (
                    dfArq3_columns['TP_PR_OB_CE'] != 222) & (dfArq3_columns['TP_PR_OB_CE'] != 334)]
    dfArq3_columns_filtered['DS_VT_ACE_OCE'].dropna(axis=0, inplace=True)
    dfArq3_columns_filtered['NT_CE'].fillna(0, inplace=True)

    if (ano == 2005):
        dfArq3_columns_filtered = dfArq3_columns_filtered[dfArq3_columns_filtered.DS_VT_ACE_OCE.str.contains(r'^Z.*Z$')]

    os.chdir(path)

    # escreve o arquivo CSV
    return dfArq3_columns_filtered