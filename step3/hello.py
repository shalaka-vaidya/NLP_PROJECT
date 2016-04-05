
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
	
