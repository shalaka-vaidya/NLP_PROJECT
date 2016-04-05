import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#removing stop words
stop_words= set(stopwords.words("english"))
testVar = raw_input("Enter input data file name: ")
p=open(testVar,'r')
s=p.read()
p.close()
s=s.split('\n')
k=len(s)  #k-1:no of docs
count=0   #count:no of docs in class +
p=open('output','w')
#s[i] gives sentence
for i in range(0,k-1):
	sent=""
	t=s[i].split(']')
	if '+' in t[0]:
		count=count+1
	st=t[0]+']'+" "
	m=t[1].lower()
	m=m.split()
	for x in m:
		if x.isalpha():
			sent=sent+x+" "
	words = word_tokenize(sent)
	sent=""
	for w in words:
		if not w in stop_words:
			st=st+w+" "
	st=st+"\n"
	p.write(st)
	
p.close()	
#print count
#vocabulary from input
fopen = open("output","r")
s=fopen.read()
fopen.close()
sp=s.split()
stp=[]
for w in sp:
	if w.isalpha():
		if sp.count(w)>1:
			if not w in stp:
				stp.append(w)
			
fopen=open("vocabulary.txt","w")
for x in stp:
	fopen.write(x+"\n")

fopen.close()

n=len(stp) # |v| = n
probpos=count/(k-1)
probneg=1-probpos

fopen = open("output","r")
s=fopen.read()
fopen.close()
fopen=open("vocabulary.txt","r")
text=fopen.read()
fopen.close()
text=text.rstrip('\n').split('\n')
s=s.rstrip('\n').split('\n')
cp=0
np=0
#print len(s),s[600].split('[+]')
#total words for each class
for step in s:
	if '+' in step:
		cp=cp+len(step.split())-1
	else:
		np=np+len(step.split())-1
	
#calculating probs for each class and storing
cpp=0
npp=0
resp=dict()
resn=dict()
for t in text:
	for w in s:
		if '+' in w and t in w:
			cpp=cpp+1
		elif t in w:
			npp=npp+1
			
	prob=(cpp+1.0)/(cp+n)		
	resp[t]=prob
	prob=(npp+1.0)/(np+n)
	resn[t]=prob
	npp=0
	cpp=0
	
	
#print len(resp),len(resn)		
result=[resp,resn]
pickle.dump( result, open( "pickle_pack", "wb" ) )		
		
		
#d1, d2 = pickle.load(open("pickle_pack", "rb"))	
#print d1["lasted"],d2["lasted"]	
				
							
			
