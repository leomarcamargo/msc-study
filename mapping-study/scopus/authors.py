
print "This script builds an adjacent matrix of authors"
print "that published papers together"
print "The input CSV file must contain a list of columns"
print "where the first column is the paper id and the remaining" 
print "columns contain a list of authors for the given paper" 
 


fname = raw_input("Enter the file name: ")

with open(fname) as f:
    content = f.readlines()

content = [x.strip() for x in content]

# builds an inverted-index for the authors. 

count = 0
authors = {} 

for data in content:
    s = data.split(";")
    s = [x.strip() for x in s] 
    for i in range(1, len(s)):
       if(not(authors.has_key(s[i]))):
           authors[s[i]] = (count, 1)
           count = count + 1 
       else:
           (key, papers) = authors[s[i]] 
           authors[s[i]] = (key, papers + 1)

# builds the graph of co-authors. 
graph = [] 

# allocates the space for the graph. initially, each cell 
# of the adjacency matrix equals zero. 
for i in range(0, len(authors)):
    graph.append([])
    for j in range(0, len(authors)):
        graph[i].append(0)

for data in content: 
    s = data.split(";")
    s = [x.strip() for x in s] 
    for i in range(1, len(s)-1):
        for j in range(i+1, len(s)):
            idx1 = authors[s[i]][0]
            idx2 = authors[s[j]][0]
            if(idx1 < idx2):
              tmp = idx1
              idx1 = idx2
              idx2 = tmp
            graph[idx1][idx2] = graph[idx1][idx2] + 1
            # graph[idx2][idx1] = graph[idx2][idx1] + 1 
            
# print the file with the name of the authors. 
for key, value in authors.iteritems():
    print "%d, \"%s\", %d" %(value[0],key, value[1])


print("from, to, weight")
for i in range(0, len(authors)):
    for j in range(0, len(authors)):
        if(graph[i][j] > 0):
            print "%d, %d, %d" %(i, j, graph[i][j])
