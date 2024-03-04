import os
import requests
import zipfile
import py7zr


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
        try:
            with zipfile.ZipFile(fileZip, 'r') as zip_ref:
                zip_ref.extractall('.')
                # Renomeia o arquivo para o nome que vem no .zip
                os.rename(zip_ref.namelist()[0][:-1], filename)

        except:
            with py7zr.SevenZipFile(fileZip, 'r') as zip_ref:
                zip_ref.extractall('.')
                archives = zip_ref.getnames()
                # Renomeia o arquivo para o nome que vem no .zip
                os.renames(archives[0].split('/')[0], filename)

                # DOCUMENTAR

    except:
        print("Erro ao extrair o arquivo ZIP " + filename + '!')

    try:
        os.remove(fileZip)
    except FileNotFoundError:
        print("O arquivo ZIP não foi encontrado no caminho especificado!")