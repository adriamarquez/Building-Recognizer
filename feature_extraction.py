# -*- coding: utf-8 -*-
import os
import src.get_local_features as get_local_features
import src.train_codebook as train_codebook
import src.compute_assignments as compute_assignments
import src.construct_bow_vector as construct_bow_vector
import matplotlib.pyplot as plt
import numpy as np
import pickle

ruta = os.path.dirname(os.path.abspath(__file__)) #obtenim la ruta del l'arxiu

#Entrenem el codebook i fem crides a get_local_features

nfiles = os.listdir(ruta + "/TerrassaBuildings900/train/images") #llistem tots els arxius de la carpeta 
descriptors = [] #inicialitzem el vector descriptors
for file in nfiles:
    ds = get_local_features("/TerrassaBuildings900/train/images/"+file) #obtenim els descriptors de cada imatge
    for feat in ds:
        descriptors.append(feat) #guardem tots els descriptors de totes les imatges
centroides,_ = train_codebook(12,descriptors) #calculem els centroides de les imatges
#plt.scatter(centroides[:,0],centroides[:,1]), plt.show()

# Compute assignments

nfiles_t = os.listdir(ruta+"/TerrassaBuildings900/train/images")
nfiles_v = os.listdir(ruta+"/TerrassaBuildings900/val/images")
descriptors = [] #Declarem el vector de descriptors
assig = [] #Declarem el vector d'assignacions

for file in nfiles_t: 
   dscrp = get_local_features("/TerrassaBuildings900/train/images"+file)
   descriptors.append(dscrp)
   centroide,_ = train_codebook(13,descriptors)
assig = compute_assignments(centroide,_,dscrp)

for file in nfiles_v:
   dscrp = get_local_features("/TerrassaBuildings900/val/images"+file)
   descriptors.append(dscrp)
assig = compute_assignments(centroide,_,dscrp)

#A continuació representarem la grafica amb els descriptors i els centroides mrcats amb color vermell
plt.scatter(descriptors[:,0],descriptors[:,1]),plt.scatter(centroide[:,0],centroide[:,1],color = 'r'),plt.show()
#Mes tard, mostrem per pantalla el vector d'assignacions separats amb comes
print", ".join(assig)

#constrium BoW

ruta = os.path.dirname(os.path.abspath(__file__)) # Definim la instrucció principal que busca la ruta absoluta del fitxer
IDs_file_T = open(ruta+"/files/outfile_train.txt", 'r') #obrim l'arxiu que conté les ids de les imatges d'entrenament
local_features_file_T = open(ruta + "/files/local_features_train.p",'w') #obrim l'arxiu en el que escriurem les caracteristiques
IDs_file_V = open(ruta+"/files/outfile_val.txt", 'r') #obrim l'arxiu que conté les ids de les imatges de validació
local_features_file_V = open(ruta + "/files/local_features_val.p",'w') #obrim l'arxiu en el que escriurem les caracteristiques
feat_vec = dict() #inicialitzem el diccionari buit
descriptors = [] #Declarem el vector de descriptors
assignments = [] #Declarem el vector d'assignacions

for line in IDs_file_T:
    BoW = np.zeros(1,100)#Generem el vector de paraules normalitzades.
    final = file.index("\n")
    dscrp = get_local_features("/TerrassaBuildings900/train/images"+file)
    descriptors.append(dscrp) #introduim el vector de descriptors
    centroide,_ = train_codebook(13,descriptors)
    assig = compute_assignments(centroide,_,dscrp,file,"train") #crida a la funció compute_assignments
    assignments.append(assig) #Insertem cada assignacio al vector de assignacions
    norm = construct_bow_vector(assig,centroide,_,dscrp,file,"train") #crida a la funció construct_bow_vector
    BoW.insert(norm) # insertem cada element normalitzat al vector BoW.
    feat_vec[line[0:final]] = BoW #Afegim al diccionari el vector de paraules normalitzades.
    pickle.dump(feat_vec, local_features_file_T) #Escribim el diccionari amb 'pickle'.
IDs_file_T.close() #Tanquem el directori on es trobaven les imatges d'entrenament.

for line in IDs_file_V:
    BoW = np.zeros(1,100)#Generem el vector de paraules normalitzades.
    final = file.index("\n")
    dscrp = get_local_features("/TerrassaBuildings900/val/images"+file)
    descriptors.append(dscrp)
    centroide,_ = train_codebook(13,descriptors)
    assig = compute_assignments(centroide,_,dscrp,file,"val") #crida a la funció compute_assignments
    assignments.append(assig) #Insertem cada assignacio al vector de assignacions
    norm = construct_bow_vector(assig,centroide,_,dscrp,file,"val")
    BoW.insert(norm) # insertem cada element normalitzat al vector BoW.
    feat_vec[line[0:final]] = BoW #Afegim al diccionari el vector de paraules normalitzades
    pickle.dump(feat_vec, IDs_file_V) #Escribim el diccionari amb 'pickle'
IDs_file_V.close() #Tanquem el directori on es trobaven les imatges de validació.