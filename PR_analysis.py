import xlwt
import os
import nltk

def intersect(a, b):
	return list(set(a) & set(b))
	
files=[x for x in os.listdir(os.getcwd()+"/Output") if "_output" in x]
glo=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
for File in files:
	targetFile=""
	for ch in File:
		if ch=="_":
			break
		else:
			targetFile=targetFile+ch
	
	target=open(os.getcwd()+"/clusters _summarized(2)/"+targetFile)
	summary1=nltk.word_tokenize((target.readline()[:-1]).lower())
	summary2=nltk.word_tokenize((target.readline()[:-1]).lower())
	
	print(File)
	length_summary1=len(summary1)
	print("K: "+str(summary1))
	length_summary2=len(summary2)
	print("P: "+str(summary2))
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
		p1=intersect(s,summary1)
		p2=intersect(s,summary2)
		length_p1=len(p1)
		length_p2=len(p2)
		length_s=len(s)
		precision=((length_p1/length_s)+(length_p2/length_s))/2
		recall=((length_p1/length_summary1)+(length_p2/length_summary2))/2
		
		try:
			f_measure=(2*precision*recall)/(precision+recall)
		except:
			f_measure=0
		sheet1.write(counter,0,base)
		sheet1.write(counter,1,str("{0:.2f}".format(precision*100))+"%")
		sheet1.write(counter,2,str("{0:.2f}".format(recall*100)+"%"))
		sheet1.write(counter,3,str("{0:.2f}".format(f_measure*100)+"%"))
		
		glo[counter-1][0]=glo[counter-1][0]+float("{0:.2f}".format(precision*100))
		glo[counter-1][1]=glo[counter-1][1]+float("{0:.2f}".format(recall*100))
		glo[counter-1][2]=glo[counter-1][2]+float("{0:.2f}".format(f_measure*100))
		
		base=base+1
		counter=counter+1
		
		s=(output.readline()[:-1]).lower()
		s=((s.split("::"))[-1])[1:]
		s=nltk.word_tokenize(s)
		
	#print("\n\n")
	#k=input()
	book.save("Results/%s_results.xls" % targetFile)
	
#creating final output file
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1",cell_overwrite_ok=True)

sheet1.write(0,0,"Base")
sheet1.write(0,1,"Precision")
sheet1.write(0,2,"Recall")
sheet1.write(0,3,"F-measure")

for i in range(0,9):
	sheet1.write(i+1,0,i+2)
	for j in range(0,3):
		glo[i][j]=glo[i][j]/len(files)
		sheet1.write(i+1,j+1,str("{0:.2f}".format(glo[i][j]))+"%")
		
book.save("Final Results.xls")
