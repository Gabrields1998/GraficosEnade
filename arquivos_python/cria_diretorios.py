import os
import shutil


# Apaga todas as pastas com os gráficos processados
# e as cria novamente para uma nova execução

def diretorios_graficos():
    '''
    Cria os diretórios em que serão armazenados os gráficos
    '''
    dirNames = ['GraficosDiscriminacao', 'GraficosDiscriminacaoPercentual', 'GraficosFacilidade',
                'GraficosFacilidadePercentual', 'GraficosPercentualAcertos', 'GraficosQuantidade']

    if os.path.exists('graficos'):
        shutil.rmtree(r'graficos')
        os.mkdir('graficos')
        os.mkdir('graficos/GraficosEspecificos')

    else:
        os.mkdir('graficos')
        os.mkdir('graficos/GraficosEspecificos')

    for i in dirNames:
        os.mkdir(f'graficos/{i}')
        os.mkdir(f'graficos/GraficosEspecificos/{i}')

def diretorios_tabelas():
    '''
    Cria os diretórios em que serão armazenadas as tabelas
    utilizadas em parte do processamento dos gráficos
    '''
    if os.path.exists('tabelas'):
        shutil.rmtree(r'tabelas')
        os.mkdir('tabelas')
    else:
        os.mkdir('tabelas')

def diretorios_microdados():
    if (not os.path.exists('microdados')):
        os.mkdir('microdados')