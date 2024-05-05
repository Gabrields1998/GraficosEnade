import os
import zipfile
import py7zr
import subprocess


def baixa_e_extrai(url: str, nome_do_arquivo: str):
    '''
    Função utilizada para realizar o download dos microdados do Enade
    e extraí-los para a pasta designada.
    '''
    # Nome do arquivo ZIP após o download e o caminho
    # relativo no qual será armazenado
    fileZip = nome_do_arquivo + '.zip'
    caminho = './microdados'

    print(fileZip)

    # Faz o download do arquivo
    try:
        subprocess.run(["wget", url, "--no-check-certificate", "-O", caminho + '/' + fileZip], check=True)
        print("Download concluído!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao baixar o arquivo: {e}")

    # Extrai o conteúdo do arquivo ZIP
    try:
        try:
            with zipfile.ZipFile(caminho + '/' + fileZip, 'r') as zip_ref:
                zip_ref.extractall(caminho)
                # Renomeia o arquivo para o nome que vem no .zip
                os.rename(zip_ref.namelist()[0][:-1], nome_do_arquivo)

        except:
            with py7zr.SevenZipFile(caminho + '/' + fileZip, 'r') as zip_ref:
                zip_ref.extractall(caminho)
                archives = zip_ref.getnames(caminho)
                # Renomeia o arquivo para o nome que vem no .zip
                os.renames(archives[0].split('/')[0], nome_do_arquivo)

                # DOCUMENTAR

    except:
        print("Erro ao extrair o arquivo ZIP " + nome_do_arquivo + '!')

    try:
        os.remove(caminho + '/' + fileZip)
    except FileNotFoundError:
        print("O arquivo ZIP não foi encontrado no caminho especificado!")