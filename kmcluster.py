import sys
sys.path.append("..")
import clusters as c
import word_cloud

def get_centroid(cluster, values):
    centroid = [0 for i in range(len(values[0]))]
    for i in cluster:
        for j in range(len(values[0])):
            centroid[j] += values[i][j]
    try:
        centroid = [int(centroid[i]/len(cluster)) for i in range(len(centroid))]
    except:
        centroid = [int(centroid[i] / (len(cluster)+1)) for i in range(len(centroid))]
    return centroid

def get_sse(cluster, values,dist_function):
    sse = 0
    for i in cluster:
        centroid = get_centroid(i,values)
        for j in i:
            sse += dist_function(values[j], centroid) **2
    return sse

def read_file(file_name):
    title = []
    datas = []

    f = open(file_name)

    for line in f:
        arr = line.rstrip().split(',')

        title.append((arr[0], arr[1]))
        datas.append([int(arr[i]) for i in range(2,8)])

    f.close()
    return title, datas

def bisect(clusters, values):
    if len(clusters) == 7:
        return clusters
    sse = None
    cluster_index = None
    initial= []
    for i in range(len(clusters)):
        cluster = clusters[i]
        current_sse = 0
        centroid = get_centroid(cluster, values)
        for country in cluster:
            current_sse += pow(c.cosine(values[country], centroid), 2)
        if sse is None or current_sse > sse:
            sse = current_sse
            cluster_index = i
    for index in clusters[cluster_index]:
        initial.append(index)
    new_clusters = c.kcluster([values[index] for index in clusters.pop(cluster_index)], distance=c.cosine, k=2)
    for cluster in new_clusters:
        for i in range(len(cluster)):
            cluster[i] = initial[cluster[i]]
    return bisect(clusters + new_clusters, values)

def output(countries, file_name):
    output = open(file_name, "w")
    output.write("['Country', 'Type'],\n")
    for i in range(len(countries)):
        cluster = countries[i]

        for country in cluster:
            output.write("['" + country + "', " + str(i) + "],\n")
    output.close()

    output.close()

def generate(clusters, values):
    f = open("dimensions_keywords.csv")
    lines = f.read().split('\n')
    k = []
    for i in range(len(lines)):
        if i == 0:
            continue
        k.append(lines[i].split(',')[1:])
    for j in range(len(clusters)):
        cluster = clusters[j]
        word = []
        centroid = get_centroid(cluster, values)
        for i in range(len(centroid)):
            if centroid[i] > 50:
                label = 0
            else:
                label = 1
            word += k[i][label].split(' ')
        d = {}
        for w in word:
            if w in d:
                d[w] += 1
            else:
                d[w] = 1
        word_counts = [(w, count/20) for w, count in d.items()]
        word_cloud.create_cloud("{}.png".format(str(j)), word_counts)
if __name__ == "__main__":
    num_clusters = 7

    country, values = read_file("processed_data.csv")

    cluster = c.kcluster(values, distance=c.cosine, k=num_clusters)
    nonempty_clusters = []
    countrys= []
    for i in range(num_clusters):
        if len(cluster[i]) == 0:
            continue
        nonempty_clusters.append(cluster[i])
        print('cluster {}:'.format(i + 1))
        print([country[r] for r in cluster[i]])
        countrys.append([country[r][1] for r in cluster[i]])

    print("Cosine SSE = " + str(get_sse(nonempty_clusters, values,c.cosine)))
    output(country,"country_clus.json")
    generate(cluster,values)
    #cluster = c.kcluster(values, distance=c.euclidean, k=num_clusters)
    #nonempty_clusters = []
    #for i in range(num_clusters):
        #if len(cluster[i]) == 0:
            #continue
        #nonempty_clusters.append(cluster[i])
        #print('cluster {}:'.format(i + 1))
        #print([country[r] for r in cluster[i]])
    #print("Euclidean SSE = " + str(get_sse(nonempty_clusters, values, c.euclidean)))

    #cluster = c.kcluster(values, distance=c.pearson, k=num_clusters)
    #nonempty_clusters = []
    #for i in range(num_clusters):
        #if len(cluster[i]) == 0:
        #    continue
        #nonempty_clusters.append(cluster[i])
        #print('cluster {}:'.format(i + 1))
        #print([country[r] for r in cluster[i]])
    #print("Pearson SSE = " + str(get_sse(nonempty_clusters, values, c.pearson)))

    # cluster = bisect([list(range(len(values)))], values)
    # proper_clusters = []
    # for i in range(num_clusters):
    #     if len(cluster[i]) == 0:
    #         continue
    #
    #     proper_clusters.append(cluster[i])
    #     print('cluster {}:'.format(i + 1))
    #     print([country[r] for r in cluster[i]])
    #
    # print("Bisect SSE: " + str(get_sse(proper_clusters, values,c.cosine)))