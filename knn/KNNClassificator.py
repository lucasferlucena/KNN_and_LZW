# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 22:17:58 2020

@author: lucas
"""
import random
import copy

class KNNClassificator():
    def __init__(self):
        #Inicializa todos os Dicionário das 40 Classes com a tabela ASCII
        ascii_table = {}
        for i in range(256):
            ascii_table[i] = bytes([ord(chr(i))])

        self.dicionario = [copy.deepcopy(ascii_table) for _ in range(40)]
        #Inicializa o State [0 Significa que o dicionário pode ser alterado | 1 Significa que não]
        self.state = 0        


    def fit(self, images, k):
        #Primeiramente, define que o state como 0, para que o dicionário possa ser alterado
        self.state = 0   
        print("Treino K = "+ str(k))
        #No primeiro for é escolhido uma pessoa por vez
        for person in range(len(images)):
            print("Treinamento Pessoa :" +str(person+1))
            #E em seguida é selecionado uma imagem por vez desse pessoa
            for image in range(len(images[person])):
                #E cada imagem é comprimida para alimentar um único dicionário pertencente a esta pessoa
                self.LZWCompression(images[person][image], k, self.dicionario[person])


    def predict(self, images, label, k):   
        #Primeiramente, define que o state como 1, para que o dicionário não possa ser alterado, se mantendo estático
        self.state = 1 
        
        predictions = []
        #Selecionamos cada uma das pessoas 
        for person in range(len(images)):
            compressionRates = []
            print("Predict pessoa:"+str(person+1))
            #E então comprimimos ela com cada um dos dicionários já calculados no durante o treino
            for category in range(len(self.dicionario)):
                #E salvamos cada um dos resultados obtidos a cada dicionario em uma lista
                compressionRates.append(self.LZWCompression(images[person], k, self.dicionario[category]))                
            
            #No final selecionamos o resultado com a menor quantidade de indices nesta lista final com o predict de cada pessoa
            predictions.append(compressionRates.index(sorted(compressionRates)[0]))

        count = 0
        for i in range(len(label)):
            #comparamos o predict com o ground truth
            if label[i] == predictions[i]:
                count += 1
        #E com base na comparação anterior, calculamos a acurácia
        print("Acertou "+ str(count*100/len(label)) + "%" + " com K = " + str(k))



    def crossValidation(self, images):
        randomImages = []
        label = []

        for i in range(len(images)):
            #Escolhe aleatoriamente uma das imagens de cada pessoa
            index = random.choice(range(len(images[i])))
            #E divide entre treino(images) e teste(randomImages)
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
 

 pessoa 3
 2000, 3000, 12000000, 5000,.....

 pe