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
                # TODO modularizar

                # DOCUMENTAR

    except:
        print("Erro ao extrair o arquivo ZIP " + nome_do_arquivo + '!')

    try:
        os.remove(caminho + '/' + fileZip)
    except FileNotFoundError:
        print("O arquivo ZIP não foi encontrado no caminho especificado!")

def compara_cabecalhos_e_baixa():
    '''
    CABEÇALHO
    dicionario utilizado para facilitar o controle do sistema
    '''
    microdado_cabecalhos = [
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

    microdado_cabecalhos_padrao_pasta = [
        {'nome': 'microdados_Enade_2021_LGPD', 'ano': 2021},
        {'nome': 'microdados_Enade_2019_LGPD', 'ano': 2019},
        {'nome': 'microdados_Enade_2018_LGPD', 'ano': 2018},
        {'nome': 'microdados_Enade_2017_LGPD', 'ano': 2017},
        {'nome': 'microdados_Enade_2016_LGPD', 'ano': 2016},
        {'nome': 'microdados_Enade_2015_LGPD', 'ano': 2015},
        {'nome': 'microdados_Enade_2014_LGPD', 'ano': 2014},
        {'nome': 'microdados_Enade_2013_LGPD', 'ano': 2013},
        {'nome': 'microdados_Enade_2012_LGPD', 'ano': 2012},
        {'nome': 'microdados_Enade_2011_LGPD', 'ano': 2011},
        {'nome': 'microdados_Enade_2010_LGPD', 'ano': 2010},
        {'nome': 'microdados_Enade_2009_LGPD', 'ano': 2009},
        {'nome': 'microdados_Enade_2008_LGPD', 'ano': 2008},
        {'nome': 'microdados_Enade_2007_LGPD', 'ano': 2007},
        {'nome': 'microdados_Enade_2006_LGPD', 'ano': 2006},
        {'nome': 'microdados_Enade_2005_LGPD', 'ano': 2005},
        {'nome': 'microdados_Enade_2004_LGPD', 'ano': 2004}]

    diretorio_atual = os.listdir('microdados')

    diretorio_atual_padrao_cabecalho = diretorio_atual
    for i in range(len(diretorio_atual_padrao_cabecalho)):
        diretorio_atual_padrao_cabecalho[i] = diretorio_atual_padrao_cabecalho[i].replace('Enade', 'enade')
        if diretorio_atual_padrao_cabecalho[i].endswith('21_LGPD'):
            diretorio_atual_padrao_cabecalho[i] = diretorio_atual_padrao_cabecalho[i].replace('_LGPD', '')
        elif diretorio_atual_padrao_cabecalho[i].endswith('11_LGPD'):
            diretorio_atual_padrao_cabecalho[i] = diretorio_atual_padrao_cabecalho[i].replace('_LGPD', '')
        elif diretorio_atual_padrao_cabecalho[i].endswith('10_LGPD'):
            diretorio_atual_padrao_cabecalho[i] = diretorio_atual_padrao_cabecalho[i].replace('_LGPD', '')
        elif diretorio_atual_padrao_cabecalho[i].endswith('09_LGPD'):
            diretorio_atual_padrao_cabecalho[i] = diretorio_atual_padrao_cabecalho[i].replace('_LGPD', '')
        elif diretorio_atual_padrao_cabecalho[i].endswith('08_LGPD'):
            diretorio_atual_padrao_cabecalho[i] = diretorio_atual_padrao_cabecalho[i].replace('_LGPD', '')
        elif diretorio_atual_padrao_cabecalho[i].endswith('07_LGPD'):
            diretorio_atual_padrao_cabecalho[i] = diretorio_atual_padrao_cabecalho[i].replace('_LGPD', '')
        elif diretorio_atual_padrao_cabecalho[i].endswith('06_LGPD'):
            diretorio_atual_padrao_cabecalho[i] = diretorio_atual_padrao_cabecalho[i].replace('_LGPD', '')
        elif diretorio_atual_padrao_cabecalho[i].endswith('05_LGPD'):
            diretorio_atual_padrao_cabecalho[i] = diretorio_atual_padrao_cabecalho[i].replace('_LGPD', '')
        elif diretorio_atual_padrao_cabecalho[i].endswith('04_LGPD'):
            diretorio_atual_padrao_cabecalho[i] = diretorio_atual_padrao_cabecalho[i].replace('_LGPD', '')
    # Código temporário enquanto os padrões dos arquivos do governo forem essa porcaria

    for cabeçalho in microdado_cabecalhos:
        if cabeçalho['nome'] not in diretorio_atual_padrao_cabecalho:
            baixa_e_extrai('https://download.inep.gov.br/microdados/' + cabeçalho['nome'] + '.zip',
                                                cabeçalho['nome'])

    return microdado_cabecalhos_padrao_pasta