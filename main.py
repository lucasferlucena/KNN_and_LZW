# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 22:17:58 2020

@author: lucas
"""
from knn.KNNClassificator import KNNClassificator
import copy
import time


#Função que permite abrir todas as imagens do dataset ORL e retorna uma lista de listas de bytes que representam essas imagens
def openImages():
    images= []
    for i in range(1,41):
        imagesTemp = []
        for j in range(1,11):
            with open("orl_faces/s"+str(i)+"/"+str(j)+".pgm", "rb") as binary_file:
                    imagesTemp.append(bytearray(binary_file.read()))
        images.append(imagesTemp)
        
    return images


def main():
    for i in range(9,17):
        #Função para medição de páginas
        start_time = time.time()
        #Inicia o classificador
        knn = KNNClassificator()
        print("Carregar Imagens")
        #Carrega as imagens
        images = openImages()
        train = copy.deepcopy(images)
        print("Dividir entre Treino e Teste")
        #Divide o dataset entre treino e imagem
        test, label = knn.crossValidation(train)
        print("Treinar Modelo")
        #Treinamento
        knn.fit(train, i)
        print("Prever Categoria de Imagens")
        #Teste
        knn.predict(test,label,i)
        print("Fim")
        #Medição do Tempo
        print("---K = "+str(i)+" %s segundos ---" % (time.time() - start_time))
    
    
if __name__ =="__main__":
    main()