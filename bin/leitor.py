import pandas as pd


def readVectorQuest():
    questoes = pd.read_csv('data/questoes.txt', delimiter=';')

    vetorQuestoes = []

    for i in range(0, len(questoes['NU_ANO'])):
        vetorQuestoes.append(
            {'ano': questoes['NU_ANO'][i], 'vet_tipo': list(map(int, questoes['VET_TIPO'][i].split(',')))})

    return vetorQuestoes


def readDictQuest():
    dicionario = pd.read_csv('data/dicionario.txt', delimiter=';')

    vetorDicionario = []

    for i in range(0, len(dicionario['NUMERO'])):
        vetorDicionario.append(
            {'id': dicionario['NUMERO'][i], 'nome': dicionario['NOME_TIPO'][i], 'sigla': dicionario['SIGLA'][i]})

    return vetorDicionario