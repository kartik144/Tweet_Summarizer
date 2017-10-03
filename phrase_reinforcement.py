from __future__ import print_function
import nltk
from time import time
from scipy.sparse import coo_matrix
from operator import itemgetter
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import networkx as nx
import matplotlib.pyplot as plt
def null_intersection(a,b):
	if(set(a) & set(b)) == set([]):
		return True
	else:
		return False

#n_samples = 145
root=""

print("Loading dataset...")
t0 = time()
file_tweet = open("/home/kartik144/Documents/CMS/4-1/CS F366/clusters/travelban","r")#"""("op.txt","r")"""
dataset=[]
s=file_tweet.readline()
while s !='':
	dataset.append(s.lower())
	s=file_tweet.readline()
file_tweet.close()
data_samples = dataset[:]##################################### list of tweets
print("done in %0.3fs." % (time() - t0))

# Inverted Index to find root
print("Generating IDF to find summary...")
t0 = time()
count_vec=CountVectorizer(ngram_range=(1,1),analyzer='word')
X_Train_counts=count_vec.fit_transform(data_samples)
X_name=count_vec.get_feature_names()
m,n=X_Train_counts.shape
cx=coo_matrix(X_Train_counts)
freq=[0 for i in range(0,n)]
for i,j,v in zip(cx.row, cx.col, cx.data):
    freq[j]+=v
words=[]
for i in range(0,n):
	words.append((X_name[i],freq[i]))
words=sorted(words,key=itemgetter(1))
root=words[-1][0]###################################################### Topic of summary / root node
print("done in %0.3fs.\nTopic of the Summary is '%s'" % (time() - t0,root))

# Inverted Index to build dictionary of frequencies of words
print("Generating IDF to build dictionary of the count of all words...")
t0=time()
count_vec=CountVectorizer(ngram_range=(1,1))
X_Train_counts=count_vec.fit_transform(data_samples)
X_name=count_vec.get_feature_names()
m,n=X_Train_counts.shape
cx=coo_matrix(X_Train_counts)
freq=[0 for i in range(0,n)]
for i,j,v in zip(cx.row, cx.col, cx.data):
    freq[j]+=v
words={}############################################################### Dictionary of words and their frequencies
for i in range(0,n):
	words.update({X_name[i]:freq[i]})
print("done in %0.3fs." % (time() - t0))

G=nx.DiGraph()
G.add_node((root,words[root]))
################################################################### Backward Pass
for data in data_samples:
	tokens=nltk.word_tokenize(data)
	edge_data=[]
	for x in range(len(tokens)-1,-1,-1):
	#	print(tokens[x],end=" ")
		if tokens[x] in words.keys():# and words[x]>1:
			edge_data.append((tokens[x],words[tokens[x]]))
	#	print()
	#print (data)
	#print(edge_data)
	if root in tokens:
		edges=[]
		j=0
		for i in range(0,len(edge_data)-1):
			if j==0 and edge_data[i]!=(root,words[root]):
				continue
			edges.append((edge_data[i],edge_data[i+1]))
			j=1
		
		#P=nx.DiGraph()
		for i in range(0,len(edges)):
			e1,e2=edges[i]
			n1,v1=e1
			n2,v2=e2
			if (edges[i] not in G) and (words[n1]>1 and words[n2]>1):
				G.add_edge(e1,e2)
		#G.add_edge(edge_data[i+1],(root,words[root]))
		#nx.draw_networkx(G,edge_color='g',arrows=True)
		#plt.show()
		
nx.draw_networkx(G,edge_color='g',arrows=True)
plt.show()

iterator=root
iterator_count=words[iterator]
graph_terminal=False
tweet_summary=[]
#tweet_summary.append((root,words[root]))
"""
print("Word=%s Count=%d"%(iterator,iterator_count))
for (n,v) in G.successors((iterator,iterator_count)):
	print("Word=%s Count=%d"%(n,v))
"""
while graph_terminal==False:
	#graph_terminal=True
	max_count=0
	max_word=""
	for (n,v) in G.successors((iterator,iterator_count)):
		if max_count<v  and n!=iterator:
			max_count=v
			max_word=n
			if ((n,v)  in tweet_summary):
				max_count=0
				max_word=""
				graph_termial=True
		#graph_terminal=False
	#print ("Word=%s Count=%d"%(max_word,max_count))
	tweet_summary.append((max_word,max_count))
	iterator=max_word
	iterator_count=max_count
	if iterator=="":
		graph_terminal=True
#print (tweet_summary)
for x in range(len(tweet_summary)-2,-1,-1):
	n,v=tweet_summary[x]
	print(n,end=" ")
print()
###################################################################### Forward Pass
for data in data_samples:
	tokens=nltk.word_tokenize(data)
	edge_data=[]
	for x in tokens:
		if x in words.keys():# and words[x]>1:
			edge_data.append((x,words[x]))
	if root in tokens:
		edges=[]
		j=0
		for i in range(0,len(edge_data)-1):
			if j==0 and edge_data[i]!=(root,words[root]):
				continue
			edges.append((edge_data[i],edge_data[i+1]))
			j=1
		
		#P=nx.DiGraph()
		for i in range(0,len(edges)):
			if edges[i] not in G:
				e1,e2=edges[i]
				G.add_edge(e1,e2)
		#G.add_edge(edge_data[i+1],(root,words[root]))
		#nx.draw_networkx(G,edge_color='g',arrows=True)
		#plt.show()
		
nx.draw_networkx(G,edge_color='g',arrows=True)
plt.show()

iterator=root
iterator_count=words[iterator]
graph_terminal=False
tweet_summary=[]
tweet_summary.append((root,words[root]))
"""
print("Word=%s Count=%d"%(iterator,iterator_count))
for (n,v) in G.successors((iterator,iterator_count)):
	print("Word=%s Count=%d"%(n,v))
"""
while graph_terminal==False:
	#graph_terminal=True
	max_count=0
	max_word=""
	for (n,v) in G.successors((iterator,iterator_count)):
		if max_count<v  and n!=iterator:
			max_count=v
			max_word=n
			if ((n,v)  in tweet_summary):
				max_count=0
				max_word=""
				graph_termial=True
		#graph_terminal=False
	#print ("Word=%s Count=%d"%(max_word,max_count))
	tweet_summary.append((max_word,max_count))
	iterator=max_word
	iterator_count=max_count
	if iterator=="":
		graph_terminal=True
	
for n,v in tweet_summary:
	print(n,end=" ")
print()