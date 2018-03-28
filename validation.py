#This script takes the validation data and feeds it through the SVM generated from normal data.
#The sesions classified as normal are use to build a final SVM

import numpy as np
from scapy.all import *
from numpy import binary_repr
from sklearn.decomposition import PCA
from sklearn import preprocessing, svm
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

np.set_printoptions(threshold=np.nan)

features = []
for i in range(1,31):
 with open ('outside_mix/feature'+str(i), 'rb') as fp:
    feature = pickle.load(fp)
 for i in range(0,len(feature)):
  features.append(feature[i])
print(features)

preprocessing.scale(features)
pca = PCA(n_components=8)
pca.fit(features)
features_r = pca.transform(features)

with open ('Outside_Normal_SVM', 'rb') as fp:
   clf = pickle.load(fp)

with open ('Normal_clusters', 'rb') as fp:
   clusterer = pickle.load(fp)
features_test = []
for temp in features_r:
    feature_temp=[]
    for center in clusterer.cluster_centers_:
        dist = np.linalg.norm(temp - center)
        feature_temp.append(dist)
    result = clf.predict([feature_temp])
    if result > 0:
     features_test.append(feature_temp)

clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
clf.fit(features_test)

with open('Outside_Final_SVM', 'wb') as fp:
    pickle.dump(clf, fp)

