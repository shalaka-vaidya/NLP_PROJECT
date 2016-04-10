import re
from itertools import islice, izip
from collections import Counter
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
	
words = re.findall('\w+', open('output').read())
y=(Counter(zip(words,words[1:])))
z=dict(y)

stp1=[]
for key, value in z.iteritems():
	if(value>2):
		t=key[0]+' '+key[1]
		stp1.append(t)

fopen=open("vocabulary.txt","w")
for x in stp:
	fopen.write(x+"\n")
	
for x in stp1:
	fopen.write(x+"\n")

fopen.close()
