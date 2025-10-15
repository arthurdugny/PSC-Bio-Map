

import subprocess
import os


## Extraction des frames, vidéo par vidéo

'''BIEN RENOMMER LES FICHIERS AVANT !'''

'''RENSEIGNER :
    - LE RANGE DES IMAGES A TRAITER
    - L'ETAT DU PATIENT (malade, sain, unknown)
    - LE CHEMIN D'ACCES VERS LES VIDEOS'''

for k in range (2,11): 
    
    if k < 10 :
        video_path = r"C:chemin\M_00"+str(k)+".avi"
        output_folder = r"C:chemin\M_00"+str(k)
    elif k <= 10 < 100 : 
        video_path = r"C:chemin\M_0"+str(k)+".avi"
        output_folder = r"C:chemin\M_0"+str(k)
        
    else :
        video_path = r"C:chemin\M_"+str(k)+".avi"
        output_folder = r"C:chemin\M_"+str(k)

    
    os.makedirs(output_folder, exist_ok=True)
    
    
    # Récupérer le nom de la vidéo sans extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # Construire le pattern de nommage des images
    output_pattern = os.path.join(output_folder, f"{video_name}_%03d.jpg")
    
    # Commande FFmpeg : extraire toutes les frames
    cmd = [
        "ffmpeg",
        "-i", video_path,
        output_pattern
    ]
    
    # Exécution de la commande
    subprocess.run(cmd)