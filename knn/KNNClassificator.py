# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 22:17:58 2020

@author: lucas
"""
import random
import copy

class KNNClassificator():
    def __init__(self):
        ascii_table = {}
        for i in range(256):
            ascii_table[i] = bytes([ord(chr(i))])

        self.dicionario = [copy.deepcopy(ascii_table) for _ in range(40)]
        self.state = 0        


    def fit(self, images, k):
        self.state = 0   

        for category in range(len(images)):
            print("Treinamento Pessoa :" +str(category+1))
            for person in range(len(images[category])):
                self.LZWCompression(images[category][person], k, self.dicionario[category])


    def predict(self, images, label, k):        
        self.state = 1 
        
        predictions = []

        for person in range(len(images)):
            compressionRates = []
            for category in range(len(self.dicionario)):
                print("pessoa:"+str(person+1)+" dicionario:"+str(category+1))
                compressionRates.append(self.LZWCompression(images[person], k, self.dicionario[category]))                
            
            predictions.append(compressionRates.index(sorted(compressionRates)[0]))

        count = 0
        for i in range(len(label)):
            if label[i] == predictions[i]:
                count += 1
            print ("Imagem da pessoa["+str(label[i]+1)+"] previu como sendo da pessoa ["+str(predictions[i]+1)+"]")
        
        print("Acertou "+ str(count*100/len(label)) + "%")



    def crossValidation(self, images):
        randomImages = []
        label = []

        for i in range(len(images)):
            index = random.choice(range(len(images[i])))
            randomImages.append(images[i].pop(index))
            label.append(i)
        
        return randomImages, label



    #FUNÇÃO PARA ACHAR CHAVE DA TABELA ASCII PASSA O VALOR COMO PARÂMETRO
    def getKeysByValue(self, dictOfElements, valueToFind):
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
    def LZWCompression(self, image, k, dictionary):
        indice = []
        table_size = len(dictionary)
        MAX = 2**k
    
        
        #ABRE O ARQUIVO E VAI LENDO BYTE A BYTE
        firstRound = True
        for pixel in image:
            if(firstRound):
                byte = bytes([ord(chr(pixel))])
                s = b''
        
            #VERIFICA SE O BYTE ANTERIOR + O BYTE ATUAL ESTÁ NO DICIONÁRIO
            index = self.getKeysByValue(dictionary,s+byte)
            
            #SE SIM, ELE IRÁ SOMAR OS DOIS BYTES E LER UM NOVO BYTE
            if index != -1:
                s += byte
            #CASO CONTRÁRIO, ELE CODIFICA O BYTE ANTERIOR PARA A SAÍDA
            else:
                indice.append(self.getKeysByValue(dictionary,s))
                #E SALVA O BYTE ANTERIOR + O BYTE ATUAL NO DICIONÁRIO, CASO O TAMANHO DO DICIONÁRIO PERMITA
                if table_size < MAX and self.state == 0:
                    dictionary[table_size] = s + byte
                    table_size += 1
                #ATUALIZA O BYTE ANTERIOR COM O BYTE ATUAL
                s = byte
                
            byte = bytes([ord(chr(pixel))])
            
            firstRound = False
        
        return len(indice)
 