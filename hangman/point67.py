import re
import operator

b_count = {}
t_count = {}
q_count = {}
p_count = {}

with open('train','r') as f:
    for lin in f:
        line = lin.strip().decode('ascii',errors='ignore')
        for i in range(len(line)-1):
            if line[i:i+2] in b_count:
                b_count[line[i:i+2]] += 1
            else:
                b_count[line[i:i+2]] = 1
with open('train','r') as f:
    for lin in f:
        line = lin.strip().decode('ascii',errors='ignore')
        for i in range(len(line)-2):
            if line[i:i+3] in t_count:
                t_count[line[i:i+3]] += 1
            else:
                t_count[line[i:i+3]] = 1

with open('train','r') as f:
    for lin in f:
        line = lin.strip().decode('ascii',errors='ignore')
        for i in range(len(line)-3):
            if line[i:i+4] in q_count:
                q_count[line[i:i+4]] += 1
            else:
                q_count[line[i:i+4]] = 1

with open('train','r') as f:
    max_=1
    for lin in f:
        line = lin.strip().decode('ascii',errors='ignore')
        line = "["+line+"]"
        for i in range(len(line)-4):
            if line[i:i+5] in p_count:
                p_count[line[i:i+4]] += 1
                if p_count[line[i:i+4]]>max_:
                    max_ = p_count[line[i:i+4]]
            else:
                p_count[line[i:i+4]] = 1

with open('train','r') as f:
    for lin in f:
        line = lin.strip().decode('ascii',errors='ignore')
        line = "["+line+"]"
        for i in range(len(line)-4):
            if i==0 or i==len(line)-5:
                p_count[line[i:i+4]] = max_+1

def bi_gram(inp,ind,guesses):
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    r_dict = {}  
    for x in alpha:
        r_dict[x]=0
    tot=0
    use = []
    for x in alpha:
        if x not in guesses:
            use.append(x)
    l = []
    fn(inp,use,l)
    for x in l:
        if x[ind] in r_dict and x in b_count:
            r_dict[x[ind]]+= b_count[x]
            tot+=b_count[x]

    for k in r_dict:
        if tot > 1:
            r_dict[k]/=float(tot)
    return r_dict

def fn(st,guesses,l):
    if "_" in st:
        t = ""
        i=0
        while st[i]!='_':
            t += st[i]
            i+=1
        for c in guesses:
            fn(t+c+st[i+1:],guesses,l)
    else:
        l.append(st)
        return 

def tri_gram(inp,ind,guesses):
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    r_dict = {}  
    for x in alpha:
        r_dict[x]=0
    tot=0
    use = []
    for x in alpha:
        if x not in guesses:
            use.append(x)
    l = []
    fn(inp,use,l)
    for x in l:
        if x[ind] in r_dict and x in t_count:
            r_dict[x[ind]]+= t_count[x]
            tot+=t_count[x]

    for k in r_dict:
        if tot > 1:
            r_dict[k]/=float(tot)
    return r_dict


def quad_gram(inp,ind, guesses):
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    r_dict = {}  
    for x in alpha:
        r_dict[x]=0
    tot=0
    use = []
    for x in alpha:
        if x not in guesses:
            use.append(x)
    l = []
    fn(inp,use,l)
    for x in l:
        if x[ind] in r_dict and x in q_count:
            r_dict[x[ind]]+= q_count[x]
            tot+=q_count[x]

    for k in r_dict:
        if tot > 1:
            r_dict[k]/=float(tot)
    return r_dict


def pent_gram(inp,ind,guesses):
    alpha = 'abcdefghijklmnopqrstuvwxyz[]'
    r_dict = {}  
    for x in alpha:
        r_dict[x]=0
    tot=0
    use = []
    for x in alpha:
        if x not in guesses:
            use.append(x)
    l = []
    fn(inp,use,l)
    for x in l:
        if x[ind] in r_dict and x in p_count:
            r_dict[x[ind]]+= p_count[x]
            tot+=p_count[x]

    for k in r_dict:
        if tot > 1:
            r_dict[k]/=float(tot)
    return r_dict

def uni_gram(dataset, node, tree, k):
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    r_dict = {}    
    tot=0
    for word in dataset:
        for c in word:
            if c in r_dict:
                r_dict[c]+=1
            else:
                r_dict[c]=1
    
    r_dict = sorted(r_dict.items(), key=operator.itemgetter(1),reverse = True)
    if len(r_dict)==0:
        tree[node] = '&'
        return
    i = node/2
    par = []
    while i >= 1:
        par.append(tree[i])
        i = i/2
    r = 0
    while r_dict[r][0] in par:
        r+=1
    tree[node] = r_dict[r][0]
    if k < 5 :
        left = []
        right = []
        for x in dataset:
            if tree[node] in x:
                left.append(x)
            else:
                right.append(x)
        uni_gram(left, 2*node, tree, k+1)
        uni_gram(right, 2*node+1, tree, k+1)


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def hangman(t):
    solution=""
    maskedWord=""
    guesses={}
    wrongGuess=0
    solution = t
    num=len(solution)
    for j in range(0,num):
        maskedWord+='_'
    while True:
        c=guess_word(maskedWord,guesses)
        guesses[c]=1
        if c in solution:
            fin=find(solution,c)
            temp = ""
            for i in range(len(solution)):
                if i in fin:
                    temp+=c
                else:
                    temp+=maskedWord[i]
            maskedWord=temp
        else:
            wrongGuess+=1 
    
        if wrongGuess==8:
            global id
            print str(id)+','+maskedWord
            id+=1
            return maskedWord,guesses
        else:
            if '_' not in maskedWord:
                global id
                print str(id)+','+maskedWord
                id+=1
                return maskedWord,guesses

letters = 'aeioubcdfghjklmnpqrstvwxyz[]'

def guess_word(maskedWord, guesses):
    if len(guesses)< 6:
        i=1
        while i in tree and tree[i] in guesses:
            if tree[i] in maskedWord:
                i=2*i
            else:
                i=2*i+1
        if i in tree and tree[i]!='&':
            return tree[i]
        
    maskedWord = '[' + maskedWord + ']'
    count = {}
    for x in letters:
        count[x] = 0
    for i in range(0,len(maskedWord)):
        if maskedWord[i] != '_':
            continue
        prob = {}
        for x in letters:
            prob[x] = 0
        index = i-1
        while index >= 0 and  i - index <= 4 and maskedWord[index]!='_':
            index = index - 1
        jndex = i+1
        if index==-1:
            index=0
        
        while jndex < len(maskedWord) and jndex - i <= 4 and maskedWord[jndex]!='_':
            jndex = jndex + 1
        if jndex==len(maskedWord):
            jndex = i
        for j in range(index,i+1):
            for l in range(1,5) :
                if j+l >= i and j+l < len(maskedWord):
                    if '[' not in maskedWord[j:j+l+1] and ']' not in maskedWord[j:j+l+1] :
                        if l == 1 :
                            temp = bi_gram(maskedWord[j:j+2],i-j, guesses)
                            temp['['] = 0
                            temp[']'] = 0
                            for x in letters:
                                if 2*temp[x] > prob[x]:
                                    prob[x] = 2*temp[x]
                        if l == 2 and maskedWord[j:j+3].count('_') < 3:
                            temp = tri_gram(maskedWord[j:j+3],i-j, guesses)
                            temp['['] = 0
                            temp[']'] = 0
                            for x in letters:
                                if 3*temp[x] > prob[x]:
                                    prob[x] = 3*temp[x]
                        if l == 3 :
                            temp = quad_gram(maskedWord[j:j+4],i-j, guesses)
                            temp['['] = 0
                            temp[']'] = 0
                            g = 4 - len(find('_', maskedWord[j:j+l]))
                            for x in letters:
                                if g*temp[x] > prob[x]:
                                    prob[x] = g*temp[x]
                            
                    else:
                        if l == 4 and len(find('_', maskedWord[j:j+l+1])) < 2:
                            temp = pent_gram(maskedWord[j:j+5],i-j,guesses)
                            for x in letters:
                                if 10*temp[x] > prob[x]:
                                    prob[x] = 10*temp[x]
        if len(maskedWord) > 4 and maskedWord[-5:].count('_') < 2:
            temp = pent_gram(maskedWord[j:j+5],i-j,guesses)
            for x in letters:
                if 10*temp[x] > prob[x]:
                    prob[x] = 10*temp[x]
            
        for x in prob:
            count[x] = count[x] + prob[x]

    count = sorted(count.items(), key=operator.itemgetter(1), reverse=True)

    for x in count:
        if x[0] not in guesses:
            return x[0]

def iterative_levenshtein(s, t, costs=(1, 1, 1)):
    rows = len(s)+1
    cols = len(t)+1
    deletes, inserts, substitutes = costs
    
    dist = [[0 for x in range(cols)] for x in range(rows)]
    for row in range(1, rows):
        dist[row][0] = row * deletes
    for col in range(1, cols):
        dist[0][col] = col * inserts
        
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = substitutes
            dist[row][col] = min(dist[row-1][col] + deletes,
                                 dist[row][col-1] + inserts,
                                 dist[row-1][col-1] + cost) # substitution
 
    return dist[row][col]

with open('test') as f:
    lines=f.readlines()
lines=[x.decode('ascii',errors='ignore').strip() for x in lines]
ans=[]
for i in range(1,len(lines)):
    var= lines[i].split(",")
    ans.append(var[1])

tree = {}
uni_gram(ans,1,tree,0)
    
sum_ = 0
f = 0
id=1
print 'Id,Prediction'
for t in ans:
    f+=1
    maskedWords,guesses = hangman(t)
    k = iterative_levenshtein(maskedWords, t)
    sum_ += k
            
sum_ = sum_/float(len(ans))
# print sum_

