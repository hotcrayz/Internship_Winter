
import os
import numpy as np
import cv2
import fra_imgcluster
from matplotlib import pyplot as plt

DIR_NAME = 'Fra_Gray_Padding_Img_Input'

# Demo for clustering a set of 20 images using 'imgcluster' module.
# To be executed in the standalone mode by default. IP[y] Notebook requires some minor adjustments.

""" True (reference) labels for the provided images - defined manually according to the semantic
    meaning of images. For example: bear, raccoon and fox should belong to the same cluster.
    Please feel free to change the true labels according to your perception of these images  :-)
"""
TRUE_LABELS = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

if __name__ == "__main__":
    c = fra_imgcluster.do_cluster(DIR_NAME, algorithm='SIFT', print_metrics=True, labels_true=TRUE_LABELS)
    num_clusters = len(set(c))
    images = os.listdir(DIR_NAME)
	
    print(images)
	
    for n in range(num_clusters):
        print("\n --- Images from cluster #%d ---" % n)

        for i in np.argwhere(c == n):
           print(i)
           #print(images + i)
                #print("Image %s" &np.array(images[i]))
            
				#img = cv2.imread('%s/%s' % (DIR_NAME, images[i]))
                #print(img)
                #plt.axis('off')
                #plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                #plt.show()
