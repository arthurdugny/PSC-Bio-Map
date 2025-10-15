from skimage import io
from matplotlib import pyplot as plt
from skimage.feature import canny
from skimage.exposure import equalize_hist

from skimage.exposure import rescale_intensity
import numpy as np
from skimage.measure import label, regionprops, regionprops_table
import pandas as pd
import matplotlib.pyplot as plt



img = io.imread(r"C:\Users\Babo\Documents\Polytechnique\PSC\Vidéo 1\images\NS_Left_20151216_102151_000.jpg",as_gray = True)

#img2 = equalize_hist(img, mask=None)
v_min, v_max = np.percentile(img, (0.2, 90))

img2 = rescale_intensity(img, in_range=(v_min, v_max))

edge_canny = canny(img2,sigma = 3)
plt.imshow(edge_canny)
#plt.show()


#tirer les données
label_img = label(edge_canny)
regions = regionprops(label_img)
props = regionprops_table(label_img,properties=('label', 'coords','perimeter'))
df=pd.DataFrame(props)
 
df = df.sort_values(by="perimeter") #on trie par ordre croissant des perimètres les lignes du tableau
df = df.tail(2) # on garde les deux dernières = celles d'intérêt

#tri des valeurs selon l'abcsisse croissante:
df['coords'][0] = df['coords'][0][df['coords'][0][:,1].argsort()] # mais pas content
df['coords'][1] = df['coords'][1][df['coords'][1][:,1].argsort()]

## #Extraire les coordonnées de la première composante connexe
##coords = df.iloc[0]["coords"]

## #Trier les coordonnées par abscisse croissante (x = colonne)
##coords_sorted = sorted(coords, key=lambda c: c[1])

## #Remettre à jour dans le DataFrame si besoin
##df.at[df.index[0], "coords"] = coords_sorted

#df.loc[0,"coords"]=   df['coords'][0][df['coords'][0][:,1].argsort()]
'''for k in range (2):
    arr = df['coords'][k]
    arr = arr[arr[:,1].argsort()]
    df.loc[k, 'coords'] = arr'''
    
lx = []
ly = []
lx2 = []
ly2 = []
#contrôle visuel

coordon = df.head(1)['coords'].iloc[0]
    
for k in range (coordon.shape[0]):
    ly.append(coordon[k][0])
    lx.append(coordon[k][1])
    
coordon2 = df.tail(1)['coords'].iloc[0]
    
for k in range (coordon2.shape[0]):
    ly2.append(coordon2[k][0])
    lx2.append(coordon2[k][1])
    
plt.plot(lx,ly,'b.')
plt.plot(lx2,ly2,'r.')
plt.plot(271,57,'*')


plt.show()
    
    
    