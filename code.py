from skimage import io
from matplotlib import pyplot as plt
from skimage.feature import canny


from skimage.exposure import rescale_intensity
import numpy as np
from skimage.measure import label, regionprops, regionprops_table
import pandas as pd

nb_photo = 107
nom_photo = r"C:\Users\Babo\Documents\Polytechnique\PSC\Vidéo 1\images\NS_Left_20151216_102151_"
donnees = {}


for k in range (nb_photo):
    if k<10:
        nom_de_photo = nom_photo + '00'+str(k)+".jpg"
    elif 10<=k and k<100:
        nom_de_photo = nom_photo + '0'+str(k)+".jpg"
    else:
        nom_de_photo = nom_photo + str(k)+".jpg"
    
    img = io.imread(nom_de_photo,as_gray = True)
    
    #img2 = equalize_hist(img, mask=None)
    v_min, v_max = np.percentile(img, (0.2, 90))
    
    img2 = rescale_intensity(img, in_range=(v_min, v_max))
    
    edge_canny = canny(img2,sigma = 2.9)
    plt.imshow(edge_canny)
    #plt.show()
    
    
    
    #tirer les données
    label_img = label(edge_canny)
    regions = regionprops(label_img)
    props = regionprops_table(label_img,properties=('label', 'coords','perimeter'))
    df=pd.DataFrame(props)
    
    df = df.sort_values(by="perimeter") #on trie par ordre croissant des perimètres les lignes du tableau
    df = df.tail(2) # on garde les deux dernières = celles d'intérêt
    
    #s'assurer des l'ordre des lignes
    
    
    
    #contrôle visuel
    coordon = df.head(1)['coords'].iloc[0]
    
    lx = []
    ly = []
    lx2 = []
    ly2 = []
    
    for k in range (coordon.shape[0]):
        ly.append(coordon[k][0])
        lx.append(coordon[k][1])
        
    coordon2 = df.tail(1)['coords'].iloc[0]
        
    for k in range (coordon2.shape[0]):
        ly2.append(coordon2[k][0])
        lx2.append(coordon2[k][1])
        
    plt.plot(lx,ly,'b.')
    plt.plot(lx2,ly2,'r.')


    plt.show()
    
