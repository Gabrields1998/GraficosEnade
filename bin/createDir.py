import os
import shutil


# Apaga todas as pastas com os gráficos processados
# e as cria novamente para uma nova execução

def graphicsDir():

    dirNames = ['GraficosDiscriminacao', 'GraficosDiscriminacaoPercentual', 'GraficosFacilidade',
                'GraficosFacilidadePercentual', 'GraficosPercentualAcertos', 'GraficosQuantidade']

    if os.path.exists('graphics'):
        shutil.rmtree(r'graphics')
        os.mkdir('graphics')
        os.mkdir('graphics/GraficosEspecificos')

    else:
        os.mkdir('graphics')
        os.mkdir('graphics/GraficosEspecificos')

    for i in dirNames:
        os.mkdir(f'graphics/{i}')
        os.mkdir(f'graphics/GraficosEspecificos/{i}')

def tablesDir():

    if os.path.exists('tables'):
        shutil.rmtree(r'tables')
        os.mkdir('tables')
    else:
        os.mkdir('tables')