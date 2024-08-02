def informa_grupo_e_curso():
    # INFORMADO PELO USUÁRIO
    # RECEBE UM CÓDIGO DE GRUPO DE CURSOS (Ex.: Ciências da Computação, Eng. Civil, etc.)

    co_grupo = int(input("Digite o código do grupo desejado:\nBCC - 4004\n>> "))
    co_curso = []

    # RECEBE DO USUÁRIO CÓDIGOS DE CURSOS ESPECÍFICOS PARA OBTER INFORMAÇÕES SOBRE O MESMO
    # (Ex.: Ciêcias da Computação ~do Câmpus de Campo Mourão~)
    print("Digite o código do curso cuja intenção é comparar com os cursos das demais instituições (-1 para nenhum):")

    while True:
        try:
            valor = int(input('>> '))

            if (valor == -1):
                return co_grupo, co_curso
            else:
                co_curso.append(valor)
                print("Deseja adicionar mais um curso específico? (-1 para parar)")

        except:
            print('Erro!\nValor inválido! Tente novamente!')