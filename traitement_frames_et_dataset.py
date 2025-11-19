from skimage import io
from matplotlib import pyplot as plt
from skimage.feature import canny
from skimage.util import crop
from skimage.exposure import rescale_intensity

from skimage.measure import label, regionprops, regionprops_table
import pandas as pd
import numpy as np

## Bas = 0, Haut = 1

# S'ASSURER DE NE PAS AVOIR LE FICHIER OUVERT AVANT DE RUN SINON LE PROGRAMME POURRA PAS CHANGER LE FICHIER CSV
# TROUVER UN MOYEN D'AJOUTER DANS LE .CSV SANS AVOIR A TOUT RERUN SINON C'EST INSUPPORTABLE

dataset = pd.DataFrame([])

compteur_patient = 1
compteur_frame = 1

#Ouverture des N = 10 vidéos à analyser
for j in range(1,3):
    for nom_video in ["S_0","M_0"]:
        if j<10:
            nom_video = nom_video + "0" + str(j)
        else:
            nom_video = nom_video + "10"
    
        nb_photo = 139
        
        '''RENSEIGNER CHEMIN DES IMAGES'''
        nom_photo = fr"C:\Users\zhang\OneDrive\Documents\_Tom\Polytechnique\2A\PSC\Vidéos 1\{nom_video}\{nom_video}_"
    
        #Ouverture de chaque frame 
        for k in range (1,nb_photo+1):
            if k<10:
                nom_de_photo = nom_photo + '00'+str(k)+".jpg"
            elif 10<=k and k<100:
                nom_de_photo = nom_photo + '0'+str(k)+".jpg"
            else:
                nom_de_photo = nom_photo + str(k)+".jpg"
            
            img = io.imread(nom_de_photo,as_gray = True)
            
            #on coupe les côtés des images
            img = crop(img,((18,18),(40,30)), copy=False, order='K') 
            
            #traitement de l'image
            v_min, v_max = np.percentile(img, (0.2, 90))
            img2 = rescale_intensity(img, in_range=(v_min, v_max))
            edge_canny = canny(img2,sigma = 2.9)
            
            #plt.imshow(img)
            plt.imshow(edge_canny)
            #plt.show()
            
            
            #Tirer les données
            label_img = label(edge_canny)
            #regions = regionprops(label_img)
            props = regionprops_table(label_img,properties=('label', 'coords','perimeter'))
            df=pd.DataFrame(props)
            
            df = df.sort_values(by="perimeter") #on trie par ordre croissant des perimètres les lignes du tableau
            df = df.tail(2) # on garde les deux dernières = celles d'intérêt
    
    
            #tri des coordonnées des points selon l'abcsisse croissante:
                
            #Extraire les coordonnées de la première composante connexe
            coords = df.iloc[0]["coords"]
            coords2 = df.iloc[1]["coords"]
            n1 = len(coords)
            n2 = len(coords2)
            #Trier les coordonnées par abscisse croissante (x = colonne)
            coords_sorted = sorted(coords, key=lambda c: c[1])
            coords_sorted2 = sorted(coords2, key=lambda c: c[1])
            
            #Remettre à jour dans le DataFrame si besoin
            if coords_sorted[n1//2][0] > coords_sorted2[n2//2][0] :
                df.at[df.index[0], "coords"] = coords_sorted
                df.at[df.index[1], "coords"] = coords_sorted2
            else :
                df.at[df.index[0], "coords"] = coords_sorted2
                df.at[df.index[1], "coords"] = coords_sorted
            
            #contrôle visuel
            coordon = df.head(1)['coords'].iloc[0]
    
            """SI PERIMETRE SORT TROP DE LA MOYENNE DES 3 DERNIERS, POP; algo qui enleve les images foireuses"""
    
            lx = []
            ly = []
            lx2 = []
            ly2 = []
            
            for k in range (len(coordon)):
                ly.append(coordon[k][0])
                lx.append(coordon[k][1])
                
            coordon2 = df.tail(1)['coords'].iloc[0]
                
            for k in range (len(coordon2)):
                ly2.append(coordon2[k][0])
                lx2.append(coordon2[k][1])
                
            plt.plot(lx,ly,'b.')
            plt.plot(lx2,ly2,'r.')
        
            plt.show()
            
            ## AJOUT DANS LE DATASET
                
            ## Perimeter : On doit faire attention aux frames où les CC sont inversées
            
            if coords_sorted[n1//2][0] > coords_sorted2[n2//2][0] :
                perimeter_bas = df.at[df.index[0], "perimeter"]
                perimeter_haut = df.at[df.index[1], "perimeter"]
            else :
                perimeter_bas = df.at[df.index[1], "perimeter"]
                perimeter_haut = df.at[df.index[0], "perimeter"]
    
            temp_dict_bas = {"CC_id": "CC_"+ str(compteur_patient) + "_" + str(compteur_frame) + "_b", 
                         "coords" :  coords_sorted,
                         "perimeter" : perimeter_bas}
            temp_df_bas = pd.DataFrame([temp_dict_bas])
            
            temp_dict_haut = {"CC_id": "CC_"+ str(compteur_patient) + "_" + str(compteur_frame) + "_h", 
                         "coords" :  coords_sorted,
                         "perimeter" : perimeter_haut}
            temp_df_haut = pd.DataFrame([temp_dict_haut])
            
            dataset = pd.concat([dataset,temp_df_haut])
            dataset = pd.concat([dataset,temp_df_bas])
            
            # Incrémentation du compteur de frame
            compteur_frame += 1
        
        # Incrémentation du compteur de patients
        compteur_frame = 1
        compteur_patient += 1


'''EXPORT EN CSV'''
dataset.to_csv(r"C:\Users\zhang\OneDrive\Documents\_Tom\Polytechnique\2A\PSC\dataset_test.csv", index=False)

