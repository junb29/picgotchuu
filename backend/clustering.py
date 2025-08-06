import numpy as np
from sklearn.cluster import KMeans

def cluster_embeddings(embeddings, n_clusters):
    
    X = np.vstack(embeddings)
    
    kmeans = KMeans(n_clusters = n_clusters, random_state = 42, n_init = "auto")
    labels = kmeans.fit_predict(X)
    
    return labels