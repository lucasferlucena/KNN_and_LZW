# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 22:17:58 2020

@author: lucas
"""
from datetime import datetime


##FUNCÃO PARA CONVERTER OS INDICES DE INTEIRO PARA BYTES PASSANDO O NUMERO DE BITS QUE CADA INT IRÁ OCUPAR
def intToBin (inDict, k):
    output = ''
    zero = ''
    
    #CRIA STRING COM K '0's
    for i in range(k):
        zero += '0'
        
    #ADEQUA CADA UM DOS INDICES A FICAREM COM K BITS
    for input_index in inDict:
        aux = input_index
        bits_size = 0
        #CONVERTE O INDICE PARA BINÁRIO
        bin_input_index = str(bin(input_index))[2:]
        
        #CALCULA A QUANTIDADE DE BITS DO INDICE | EX.: 8 = '1000' = 4 BITS
        while (aux != 0):
            aux = int(aux/2)
            bits_size += 1
            
        if input_index == 0:
            bin_input_index = ''
        
        #TRANSFORMA O INDICES EM K BITS
        inDictBin = zero[bits_size:] + bin_input_index
        output += inDictBin
    
    #PREPARAÇÃO PARA SALVAR A STRING EM BYTES:
    #CALCULA QUANTOS BYTES SERÃO UTILIZADOS A PARTIR DA QUANTIDADE DE BITS(CHAR) DA STRING FINAL(output)
    total_bits = len(output)
    total_bytes = 0
    if ((total_bits%8) == 0):
        total_bytes = int(total_bits/8)
    else:
        total_bytes = int(total_bits/8) + 1
    
    #PREENCHE O FINAL DA STRING COM 0s PARA O TAMANHO TOTAL DELA SER MULTIPLO DE 8 E PODER SER SALVÁ-LA EM BYTES
    zero = ''
    for i in range(total_bytes*8 - total_bits):
        zero += '0'
        
    output = output + zero
    
    return int(output, 2).to_bytes(total_bytes, 'big')

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
def LZWCompression(file_name, k):
    indice = []
    table_size = 256
    MAX = 2**k
    #INICIALIZA TABELA ASCII
    ascii_table = {}
    for i in range(256):
        ascii_table[i] = bytes([ord(chr(i))])
    
    
    #ABRE O ARQUIVO E VAI LENDO BYTE A BYTE
    with open(file_name, "rb") as f:
        byte = f.read(1)
        s = b''
        while byte != b'':
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
                
            byte = f.read(1)
    
    #EXECUTA A FUNÇAO PARA TRANSFORMAR A LISTA DE INDICES INTEIRO EM BYTES
    byte_buffer = intToBin(indice,k)
    #SALVA EM ARQUIVO BINARIO
    f2 = open(file_name.split('.')[0]+'Ck'+str(k)+'.bin',"wb")
    f2.write(byte_buffer)
    f2.close()   
    
'''
currcode = read in a code;
    entry = translation of currcode from dictionary;
    output entry;
    ch = first char of entry;
    add ((translation of prevcode)+ch) to dictionary;
    prevcode = currcode;

'''
def LZWDecompression(file_name, k):
#INICIALIZA TABELA ASCII
    MAX = 2**k
    arraybyte = b''
    
    with open(file_name, "rb") as f:
        #ler byte
        byte = f.read(1)
        while byte != b"":
            arraybyte += byte
            byte = f.read(1)

    
    output = ''
    zero = '00000000'
    
    #TRANSFORMA O ARRAY DE BYTES EM ARRAY DE BITS DO TIPO STRING
    for input_index in arraybyte:
        aux = input_index
        bits_size = 0
        bin_input_index = str(bin(input_index))[2:]
        
        while (aux != 0):
            aux = int(aux/2)
            bits_size += 1
            
        if input_index == 0:
            bin_input_index = ''
            
        inDictBin = zero[bits_size:] + bin_input_index
        output += inDictBin

    
    #TRANFORMA O ARRAY DE BIT EM INTEIROS DE ACORDO COM O TAMANHO DE K
    indices = []
    for i in range (0, int(len(output)/k)):
        indices.append(int(output[i*k:i*k+k], 2))


    #PROCESSO DE DESCOMPRESSÃO:
    #INCIA A TABELA ASCII COMO DICIONARIO INICIAL
    ascii_table = {}
    for i in range(256):
        ascii_table[i] = bytes([ord(chr(i))])
    '''
    #DESCOMPRESSAO COM LZW
    table_size = 256
    prevcode = 0
    outputF = b''    
    for i in indices:
        entry = ascii_table[i]
        outputF += entry
        ch = bytes([ord(chr(ascii_table[i][0]))])
        if i != indices[0]:
            ascii_table[table_size] = ascii_table[prevcode] + ch
            table_size += 1
        
        prevcode = i
    '''
    table_size = len(ascii_table)
    ascii_table = ascii_table.copy()
    palavra = b''
    word = []
    s = b''
    i = 0
    byte = ascii_table[indices[i]]

    palavra += byte
    word.append(byte[0])
    i += 1

    while i < len(indices):
        s = byte
        if indices[i] >= len(ascii_table):
            teste = s+ascii_table[indices[0]]
            palavra += teste
            for j in range(len(teste)):
                word.append(teste[i])
            if table_size < MAX:
                ascii_table[table_size] = s + ascii_table[indices[0]]
                table_size += 1
            byte = ascii_table[indices[i]]
            i += 1
            continue
            
        byte = ascii_table[indices[i]]
        
        if getKeysByValue(ascii_table,byte) != -1:
            palavra += byte
            for j in range(len(byte)):
                word.append(byte[j])
            P = s
            C = byte[0:1]
            if table_size < MAX:
                ascii_table[table_size] = P+C
                table_size += 1
        else:
            P = s
            C = s[0:1]
            s = P + C
            if table_size < MAX:
                ascii_table[table_size] = P+C
                table_size += 1
        i += 1 
        
        
    #EXPORTA O EM BINÁRIO
    f2 = open(file_name.split('.')[0]+'FINALk'+str(k)+'.bin',"wb")
    f2.write(palavra)
    f2.close()  


def main():
    
    
    '''
    print("iniciando descompressão; k="+str(9)+"; "+datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    #LZWCompression('teste.txt',9)
    LZWDecompression('corpus16MBCk9.bin',9)
    print("final processo; k="+str(9)+"; "+datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    '''
    file_name = 'C:/Users/lucas/OneDrive/Documentos/iti/projeto-final/\orl_faces/s1/1.pgm'
    LZWCompression(file_name,16)
    '''
    for i in range(16  , 17):
        print("iniciando compressão; k="+str(i)+"; "+datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        LZWCompression(file_name, i)
        #print("iniciando descompressão; k="+str(i)+"; "+datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        #LZWDecompression(file_name.split('.')[0]+'Ck'+str(i)+'.bin',i)
        print("final processo; k="+str(i)+"; "+datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    '''
    '''  
    file_name = 'mapa.mp4'
    for i in range(9, 17):
        print("iniciando compressão; k="+str(i)+"; "+datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        LZWCompression(file_name, i)
        print("iniciando descompressão; k="+str(i)+"; "+datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        LZWDecompression(file_name.split('.')[0]+'Ck'+str(i)+'.bin',i)
        print("final processo; k="+str(i)+"; "+datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
     '''
if __name__ =="__main__":
    main()