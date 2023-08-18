import os


# Apaga todas as pastas com os gráficos processados
# e as cria novamente para uma nova execução

def graphicsDir():

    dirNames = ['GraficosDiscriminacao', 'GraficosDiscriminacaoPercentual', 'GraficosFacilidade',
                    'GraficosFacilidadePercentual', 'GraficosPercentualAcertos', 'GraficosQuantidade', ]

    if os.path.exists('graphics'):
        os.system('rm -rf graphics')
        os.mkdir('graphics')
    else:
        os.mkdir('graphics')

    for i in dirNames:
        os.mkdir(f'graphics/{i}')

def tablesDir():

    if os.path.exists('tables'):
        os.system('rm -rf tables')
        os.mkdir('tables')
    else:
        os.mkdir('tables')