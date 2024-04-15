import os
import pandas as pd

def define_grupo_2008(num):
    if(num == 4001):
        return 4004
    return num

def processa_BCC_2008():
    # Entra na pasta DADOS dentro da pasta microdados_enade
    path = os.getcwd()
    os.chdir(path + '\\microdados_enade_2008')
    lista_arquivos = os.listdir()
    data_path = path + '\\microdados_enade_2008\\' + lista_arquivos[1]
    os.chdir(data_path)

    df_arq = pd.read_csv('microdados2008_arq1.txt', delimiter=';')

    df_arq['CO_GRUPO'] = df_arq['CO_SUBAREA'].apply(define_grupo_2008)

    df_arq.to_csv('microdados2008_arq1.txt', sep=';', index = 0)

    os.chdir(path)

def define_grupo_2005(num):
    if(num == 40):
        return 4004
    return num

def processa_BCC_2005():
    # Entra na pasta DADOS dentro da pasta microdados_enade
    path = os.getcwd()
    os.chdir(path + '\\microdados_enade_2005')
    lista_arquivos = os.listdir()
    data_path = path + '\\microdados_enade_2005\\' + lista_arquivos[1]
    os.chdir(data_path)

    df_arq = pd.read_csv('microdados2005_arq1.txt', delimiter=';')

    df_arq['CO_GRUPO'] = df_arq['CO_GRUPO'].apply(define_grupo_2005)

    df_arq.to_csv('microdados2005_arq1.txt', sep=';', index=0)

    os.chdir(path)