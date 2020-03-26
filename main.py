# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 22:17:58 2020

@author: lucas
"""
from knn.KNNClassificator import KNNClassificator
import copy

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
    knn = KNNClassificator()
    print("Carregar Imagens")
    images = openImages()
    train = copy.deepcopy(images)
    print("Dividir entre Treino e Teste")
    test, label = knn.crossValidation(train)
    print("Treinar Modelo")
    knn.fit(train, 9)
    print("Prever Categoria de Imagens")
    knn.predict(test,label,9)
    print("Fim")
    
    
if __name__ =="__main__":
    main()