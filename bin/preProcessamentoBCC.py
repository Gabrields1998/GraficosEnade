import os
import numpy as np
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

    dfArq1 = pd.read_csv('microdados2008_arq1.txt', delimiter=';')

    dfArq1['CO_GRUPO'] = dfArq1['CO_SUBAREA'].apply(define_grupo_2008)

    dfArq1.to_csv('microdados2008_arq1.txt', sep=';', index = 0)

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

    dfArq1 = pd.read_csv('microdados2005_arq1.txt', delimiter=';')

    dfArq1['CO_GRUPO'] = dfArq1['CO_GRUPO'].apply(define_grupo_2005)

    dfArq1.to_csv('microdados2005_arq1.txt', sep=';', index=0)

    os.chdir(path)