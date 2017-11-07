import xlwt
import os
import nltk

def intersect(a, b):
	return list(set(a) & set(b))
	
files=[x for x in os.listdir(os.getcwd()+"/Output") if "_output" in x]

for File in files:
	targetFile=""
	for ch in File:
		if ch=="_":
			break
		else:
			targetFile=targetFile+ch
	
	target=open(os.getcwd()+"/clusters_summarized/"+targetFile)
	summary=nltk.word_tokenize((target.readline()[:-1]).lower())
	length_summary=len(summary)
	print(summary)
	target.close()
	
	book = xlwt.Workbook(encoding="utf-8")
	sheet1 = book.add_sheet("Sheet 1",cell_overwrite_ok=True)
	
	counter=0
	sheet1.write(counter,0,"Base")
	sheet1.write(counter,1,"Precision")
	sheet1.write(counter,2,"Recall")
	sheet1.write(counter,3,"F-measure")
	counter=counter+1
	
	output=open(os.getcwd()+"/Output/"+File)
	
	base=2
	s=(output.readline()[:-1]).lower()
	s=((s.split("::"))[-1])[1:]
	s=nltk.word_tokenize(s)
	
	while(s!=[]):
		p=intersect(s,summary)
		length_p=len(p)
		length_s=len(s)
		precision=length_p/length_s
		recall=length_p/length_summary
		f_measure=(2*precision*recall)/(precision+recall)
		
		sheet1.write(counter,0,base)
		sheet1.write(counter,1,str(precision*100)+"%")
		sheet1.write(counter,2,str(recall*100)+"%")
		sheet1.write(counter,3,str(f_measure*100)+"%")
		
		base=base+1
		counter=counter+1
		
		s=(output.readline()[:-1]).lower()
		s=((s.split("::"))[-1])[1:]
		s=nltk.word_tokenize(s)
		
	#print("\n\n")
	#k=input()
	book.save("Results/%s_results.xls" % targetFile)