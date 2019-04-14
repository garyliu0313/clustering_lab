import kmcluster
import clusters
import word_cloud

country,data = kmcluster.read_file("processed_data.csv")

#for i in ['min', 'max']:
clust=clusters.hcluster(data,distance=clusters.cosine, inter_dis=max)
print(clust)
print ('cosine similarity')
