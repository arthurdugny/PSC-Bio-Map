from skimage import io
from matplotlib import pyplot as plt
from skimage.feature import canny


from skimage.exposure import rescale_intensity
import numpy as np
from skimage.measure import label, regionprops, regionprops_table
import panda as pd

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
    
    edge_canny = canny(img2,sigma = 3)
    plt.imshow(edge_canny)
    plt.show()
    
    
    #tirer les données
    label_img = label(edge_canny)
    regions = regionprops(label_img)
    props = regionprops_table(label_img,properties=('label', 'coords','perimeter'))
    
    donnees[k]=props #on enregistre les tableaux dans le dictionnaire
    
df=pd.DataFrame(donnees)