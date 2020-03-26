#FUNÇÃO PARA ACHAR CHAVE DA TABELA ASCII PASSA O VALOR COMO PARÂMETRO
def getKeysByValue(dictOfElements, valueToFind):
  listOfItems = dictOfElements.items()
  for item  in listOfItems:
    if item[1] == valueToFind:
      return item[0]
  return  -1
    
##COMPRESSOR
'''
  *     PSEUDOCODE
  1     Initialize table with single character strings
  2     P = first input character
  3     WHILE not end of input stream
  4          C = next input character
  5          IF P + C is in the string table
  6            P = P + C
  7          ELSE
  8            output the code for P
  9          add P + C to the string table
  10           P = C
  11         END WHILE
  12    output code for P 
'''

#INICIALIZA TABELA ASCII
ascii_table = {}
for i in range(256):
    ascii_table[i] = bytes([ord(chr(i))])


def LZWCompression(image, k):
    indice = []
    table_size = len(ascii_table)
    MAX = 2**k
  
    
    #ABRE O ARQUIVO E VAI LENDO BYTE A BYTE
    firstRound = True
    for pixel in image:
        if(firstRound):
            byte = bytes([ord(chr(pixel))])
            s = b''
    
        #VERIFICA SE O BYTE ANTERIOR + O BYTE ATUAL ESTÁ NO DICIONÁRIO
        index = getKeysByValue(ascii_table,s+byte)
        
        #SE SIM, ELE IRÁ SOMAR OS DOIS BYTES E LER UM NOVO BYTE
        if index != -1:
            s += byte
        #CASO CONTRÁRIO, ELE CODIFICA O BYTE ANTERIOR PARA A SAÍDA
        else:
            indice.append(getKeysByValue(ascii_table,s))
            #E SALVA O BYTE ANTERIOR + O BYTE ATUAL NO DICIONÁRIO, CASO O TAMANHO DO DICIONÁRIO PERMITA
            if table_size < MAX:
                ascii_table[table_size] = s + byte
                table_size += 1
            #ATUALIZA O BYTE ANTERIOR COM O BYTE ATUAL
            s = byte
            
        byte = bytes([ord(chr(pixel))])
        
        firstRound = False
    
    return len(indice)
    
        
def openImages():
    images= []
    for i in range(1,41):
        imagesTemp = []
        for j in range(1,11):
            with open("orl_faces/s"+str(i)+"/"+str(j)+".pgm", "rb") as binary_file:
                    imagesTemp.append(bytearray(binary_file.read()))
        images.append(imagesTemp)
        
    return images


images2 = openImages()

len(images[0])


LZWCompression(images[0][3], 16)


lista = []

dicionarios = [ascii_table for _ in range(40)]



train = images2[:]

lista = 0


lista = [1,5,7,6,23,7,5]

b = list.index(list.sort()[0])

sorted(lista)[0]

lista.sort()[0]


import random
def crossValidation(images):
    randomImages = []
    label = []
    
    for i in range(len(images)):
        index = random.choice(range(len(images[i])))
        randomImages.append(images[i].pop(index))
        label.append(i)
        
    return randomImages, label
        
teste, label = crossValidation(train)












