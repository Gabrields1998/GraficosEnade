#Número de entrada
numero = 891110 

# Vetor para armazenar o numero convertido em 8 posições 
vetor_transformado = [0, 0, 0, 0, 0, 0, 0, 0] 

# Convertendo o número para o vetor.
for i in range(8): 
	if (numero != 0): 
		vetor_transformado[7 - i] = int(numero % 10) 
		numero = int(numero / 10) 
		
# Printando o vetor transformado
print (vetor_transformado)