import pickle
import math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from itertools import islice, izip
from collections import Counter

p=open('output','r')
s=p.read()
p.close()
count=[]
count1=[]
s=s.split('\n')
for k in s:
	if '[+]' in k:
		count.append(k)
	else:
		count1.append(k)
		
		
co=1
i=1
s=''
for k in count:
	if co==1:
		s=s+k+'\n'+count1[co]+'\n'
		co=co+1
	elif co%30==0 :	
		s=s+k+'\n'+count1[co-1]+'\n'
		m=open('hello'+str(i),'w')
		m.write(s)
		m.close()
		co=co+1
		i=i+1
		s=''
	else:	
		s=s+k+'\n'+count1[co]+'\n'
		co=co+1	
		
#cross fold validation
avscore=0.0
for i in range(1,11):
	sent=""
	for j in range(1,11):
		if j == i:
			continue
		else:
			fopen=open('hello'+str(j),'r')
			sent=sent+fopen.read()
			fopen.close()  
	
	sp=sent.split()
	stp=[]
	for w in sp:
		if w.isalpha():
			if sp.count(w)>1:
				if not w in stp:
					stp.append(w)
	stp1=[]
	words = re.findall('\w+', sent)	
	y=(Counter(zip(words,words[1:])))
	z=dict(y)
	#print z
	for key, value in z.iteritems():
		if(value>3):
			t=key[0]+' '+key[1]
			stp1.append(t)			
	#print len(stp1),len(stp)	
	fopen=open("vocabulary.txt","w")
	for x in stp:
		fopen.write(x+"\n")
	
	for x in stp1:
		fopen.write(x+"\n")
	fopen.close()
	n=len(stp)+len(stp1) # |v| = n
	probspos=0.5 #here in data used we have half chance for both classes
	probsneg=0.5 #alternative method to find for unequal classes done in 4th step
	fopen=open("vocabulary.txt","r")
	text=fopen.read()
	fopen.close()
	text=text.rstrip('\n').split('\n')
	s=sent.rstrip('\n').split('\n')
	cp=0
	np=0
	for step in s:
		if '+' in step:
			cp=cp+len(step.split())-1
		else:
			np=np+len(step.split())-1
	
	cpp=0
	npp=0 #training
	resp=dict()
	resn=dict()
	sn=sent.rstrip('\n').split('\n')

	for t in stp1:
		for w in sn:
			count=0
			tm=t.split()
			listw=w.split()
			#print listw
			wlen=len(listw)
			n=0
			wlen=wlen-1
			#print wlen
			while (n<wlen):
				#print tm[0] == listw[n],listw[n]
				if tm[0] == listw[n]:
					if tm[1] == listw[n+1]:
						count= count+1
			
				n=n+1
						
			if count > 0:
				if '+' in w:			
					cpp=cpp+count
				else:
					npp=npp+count
		
		prob=(cpp+1.0)/(cp+n)		
		resp[t]=prob
		prob=(npp+1.0)/(np+n)
		resn[t]=prob
		npp=0
		cpp=0
		
	npp=0
	cpp=0
	for t in stp:
		for w in sn:
			count=0
			listw=w.split()
			wlen=len(listw)
			n=0
			#print listw
			while(n<wlen):
				if(t==listw[n]):
					if (n<(wlen-1)):
						maps=t+" "+listw[n+1]
						if(maps not in stp1):
							count=count+1
						else:
							count=count+0	
							
					else:
						count=count+1
				n=n+1
			
			if count > 0:
				if '+' in w:			
					cpp=cpp+count
				else:
					npp=npp+count	
			
		prob=(cpp+1.0)/(cp+n)		
		resp[t]=prob
		prob=(npp+1.0)/(np+n)
		resn[t]=prob
		npp=0
		cpp=0 	
				
	
	result=[resp,resn]
	pickle.dump( result, open( "pickle_pack", "wb" ) )
	
	#testing
	fopen=open('hello'+str(i),'r')
	test=fopen.read()
	fopen.close()
	test=test.rstrip('\n').split('\n')
	d1, d2 = pickle.load(open("pickle_pack", "rb"))	
	tp=0
	tn=0
	for x in test:
		score2=0.0
		score1=0.0
		m=x.split()
		mlen=len(m)
		for k in range(1,mlen):
			if m[k] in text:
				score1=score1+math.log(d1[m[k]])
				score2=score2+math.log(d2[m[k]])
		
		for k in range(1,mlen-1):
			if m[k] in text:
				mstr=m[k]+" "+m[k+1]
				if mstr in text:
					score1=score1+math.log(d1[mstr])
					score2=score2+math.log(d2[mstr])
			
			
		if score1 > score2:
			if '+' in m[0]:
				tp=tp+1
		
		else:
			if '-' in m[0]:
				tn=tn+1
	
	avscore=avscore+(tp+tn)/0.6
	print "Accuracy for "+str(i)+"th part: "+str((tp+tn)/0.6)+"%"			


print "Overall accuracy: "+ str(avscore/10.0)+"%"
