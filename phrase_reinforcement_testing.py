from __future__ import print_function
import nltk
from time import time
from scipy.sparse import coo_matrix
from operator import itemgetter
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph
import math
import os
from subprocess import check_call
import sys

def null_intersection(a,b):
	if(set(a) & set(b)) == set([]):
		return True
	else:
		return False

F=nx.DiGraph()
G=nx.DiGraph()
files=[x for x in os.listdir(os.getcwd()+"/clusters") if x[-1]!="~"]
#files=['travelban']

for i,x in enumerate(files):
	print(str(i)+". "+x)
print("Enter file number to summarize: ",end="")
File=files[int(input())]

#for File in files:
print("Processing file: %s" % File)
if File in files:
	file_output=open(os.getcwd()+"/Output/"+File+"_output.txt","w")
#print("Enter base for log calculation: ",end="")
#base=float(input())


root=""
file_tweet = open(os.getcwd()+"/clusters/"+File,"r")
dataset=[]
data_samples=[]
s=file_tweet.readline()
while s !='':
	data_samples.append(s.lower())
	dataset.append(s)
	s=file_tweet.readline()
file_tweet.close()##################################### list of tweets

# Inverted Index to find root
print("Generating IDF to find summary...")
t0 = time()
count_vec=CountVectorizer(ngram_range=(1,1),analyzer='word',stop_words="english")
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
freq.clear()
root=words[-1][0]###################################################### Topic of summary / root node
print("Topic of the Summary is '%s'" % root)

# Inverted Index to build dictionary of frequencies of words

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
freq.clear()
#print("Writing outputs to file ")
for base in range(2,11):
	G.clear()
	G.add_node((root,words[root],0,-1))
	################################################################### Backward Pass
	ident=1
	for index,data in enumerate(data_samples):
		tokens=nltk.word_tokenize(data)
		edge_data=[]
		count=1
		for x in range(len(tokens)-1,-1,-1):
		#	print(tokens[x],end=" ")
			if tokens[x]==root:
				edge_data.append((tokens[x],words[tokens[x]],0,-1))
				continue
			if tokens[x] in words:
				edge_data.append((tokens[x],words[tokens[x]]-count*math.log(words[tokens[x]],base),ident,index))
				count=count+1
			else:
				edge_data.append((tokens[x],0,ident,index))
				count=count+1
			ident=ident+1
		#	print()
		#print (data)
		#print(edge_data)
		if root in tokens:
			edges=[]
			j=0
			for i in range(0,len(edge_data)-1):
				if j==0 and edge_data[i]!=(root,words[root],0,-1):
					continue
				edges.append((edge_data[i],edge_data[i+1]))
				j=1

			#P=nx.DiGraph()
			for i in range(0,len(edges)):
				e1,e2=edges[i]
				if (edges[i] not in G):# and (words[n1]>1 and words[n2]>1):
					G.add_edge(e1,e2)
			#G.add_edge(edge_data[i+1],(root,words[root]))
			#nx.draw_networkx(G,edge_color='g',arrows=True)
			#plt.show()
			edges.clear()
		edge_data.clear()
	#nx.drawing.nx_pydot.write_dot(G,os.getcwd()+"/Graphs/"+File+"_backward.dot")	
	#print("Writing backward graph for file: %s \t base: %d" % (File,base))	
	#check_call(['dot','-Tps',os.getcwd()+"/Graphs/"+File+"_backward.dot",'-o',os.getcwd()+"/Graphs/"+File+"_backward.ps"])

	#nx.draw_networkx(G,edge_color='g',arrows=True)
	#plt.show()

	#iterator=root
	#iterator_count=words[iterator]

	#graph_terminal=False
	#tweet_summary=[]
	#tweet_summary.append((root,words[root]))
	"""
	print("Word=%s Count=%d"%(iterator,iterator_count))
	for (n,v) in G.successors((iterator,iterator_count)):
		print("Word=%s Count=%d"%(n,v))
	"""

			##REMOVE 
	"""	
	while graph_terminal==False:
		#graph_terminal=True
		#max_count=0
		#max_word=""
		count=0
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
	"""
	###################################################################### Forward Pass

	F.clear()
	F.add_node((root,words[root],0,-1))
	ident=1
	for index,data in enumerate(data_samples):
		tokens=nltk.word_tokenize(data)
		edge_data=[]
		count=1
		for x in tokens:
			if x==root:
				edge_data.append((x,words[x],0,-1))
				continue
			if x in words.keys():
				edge_data.append((x,words[x]-count*math.log(words[x],base),ident,index))
				count=count+1
			else:
				edge_data.append((x,0,ident,index))
				count=count+1
			ident=ident+1
		#print(edge_data)
		if root in tokens:
			edges=[]
			j=0
			for i in range(0,len(edge_data)-1):
				if j==0 and edge_data[i]!=(root,words[root],0,-1):
					continue
				edges.append((edge_data[i],edge_data[i+1]))
				j=1

			#P=nx.DiGraph()
			for i in range(0,len(edges)):
				if edges[i] not in G:
					e1,e2=edges[i]
					F.add_edge(e1,e2)
			#G.add_edge(edge_data[i+1],(root,words[root]))
			#nx.draw_networkx(G,edge_color='g',arrows=True)
			#plt.show()
			edges.clear()
		edge_data.clear()
	#nx.draw_networkx(G,edge_color='g',arrows=True)
	#plt.show()
	#nx.drawing.nx_pydot.write_dot(F,os.getcwd()+"/Graphs/"+File+"_forward.dot")
	#print("Writing forward graph for file: %s\t base: %d" % (File,base))		
	#check_call(['dot','-Tps',os.getcwd()+"/Graphs/"+File+"_forward.dot",'-o',os.getcwd()+"/Graphs/"+File+"_forward.ps"])

	#iterator=root
	#iterator_count=words[iterator]
	#graph_terminal=False
	#tweet_summary=[]
	#tweet_summary.append((root,words[root]))
	"""
	print("Word=%s Count=%d"%(iterator,iterator_count))
	for (n,v) in G.successors((iterator,iterator_count)):
		print("Word=%s Count=%d"%(n,v))
	"""
	max_count=0
	summaries_weights=[(-1*(sys.maxsize) -1) for x in range(0,len(data_samples))]

	for (n,v,const,index) in F.successors((root,words[root],0,-1)):
		summaries_weights[index]=v
		l=F.successors((n,v,const,index))
		while l!=[]:
			summaries_weights[index]=summaries_weights[index]+l[0][1]
			l=F.successors((l[0][0],l[0][1],l[0][2],l[0][3]))

		#summaries_forward.append((summary,count))
			#graph_terminal=False
		#print ("Word=%s Count=%d"%(max_word,max_count))
		#tweet_summary.append((max_word,max_count))
		#iterator=max_word
		#iterator_count=max_count
		#if iterator=="":
		#	graph_terminal=True

	#summaries_backward=[]
	for (n,v,const,index) in G.successors((root,words[root],0,-1)):
		summaries_weights[index]=summaries_weights[index]+v
		#summary=n+" "+root
		l=G.successors((n,v,const,index))
		while l!=[]:
			summaries_weights[index]=summaries_weights[index]+l[0][1]
			l=G.successors((l[0][0],l[0][1],l[0][2],l[0][3]))
		l.clear()
		#summaries_backward.append((summary,count))

	max_weight=(-1*(sys.maxsize) -1)
	final_summary=""
	for index,x in enumerate(summaries_weights):
		if x>max_weight:
			max_weight=x
			final_summary=dataset[index]

	#for index,x in enumerate(summaries_weights):
	#	print("Weight= "+str(x)+" \t "+data_samples[index])
	#print(final_summary)
	#print(".",end="")
	print("Writing output for file: %s\t base: %d" % (File,base))	
	file_output.write("Base:"+str(base)+" :: "+final_summary)

print("Done",end="\n\n")
file_output.close()
data_samples.clear()
dataset.clear()
summaries_weights.clear()
