import numpy as np
from scapy.all import *
from numpy import binary_repr
from sklearn.decomposition import PCA
from sklearn import preprocessing, svm
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

np.set_printoptions(threshold=np.nan)
features = []
for i in range(1,34):
 with open ('outside_normal_1/feature'+str(i), 'rb') as fp:
    feature = pickle.load(fp)
 for i in range(0,len(feature)):
  features.append(feature[i])
    #print(sess['TCP 203.143.57.80:80 > 121.199.228.88:46593'].summary())
#for k, v in sess.iteritems():
#  print k
#  print v.summary()
#  print('---------------------------------')
print(features)
preprocessing.scale(features)
pca = PCA(n_components=8)
pca.fit(features)
features_r = pca.transform(features)
#print(features_r)

#Kmeans clustering is used to model the normal behaviour of the data. the number of clusters are
#selected on the basis of average silhouette value
n_clusters=3
clusterer = KMeans(n_clusters=n_clusters)
cluster_labels = clusterer.fit_predict(features_r)

# The silhouette_score gives the average value for all the samples.
# This gives a perspective into the density and separation of the formed
# clusters
silhouette_avg=0
for i in range(1,10):
 silhouette_avg = silhouette_avg+ silhouette_score(features_r,cluster_labels,sample_size=10000)
print(silhouette_avg/100)
#print(len(clusterer.cluster_centers_))
features_new = [] #will hold 'n_cluster' number of features which represent the distance of features_r from the cluster centers
for temp in features_r:
    feature_temp=[]
    for center in clusterer.cluster_centers_:
        dist = np.linalg.norm(temp - center)
        feature_temp.append(dist)
    features_new.append(feature_temp)
print(features_new[0])
#Use features_new to train a one class SVM on normal sessions only
clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
clf.fit(features_new)

#Pickle the SVM to a file
with open('Outside_Normal_SVM', 'wb') as fp:
    pickle.dump(clf, fp)

with open('Normal_clusters', 'wb') as fp:
    pickle.dump(clusterer, fp)