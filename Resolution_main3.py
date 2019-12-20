import sys
import copy
import time
from collections import OrderedDict


#returns the most simplified clauseA AND clauseB
def resolve(clauseA, clauseB): #return None if resolution is True
    if len(clauseA.split()) == 1 and len(clauseB.split()) == 1 and (clauseA == "~" + clauseB or clauseB == "~" + clauseA):
        return "Contradiction"
    litsA = clauseA.split()
    litsB = clauseB.split()
    allLits = []
    for lit in litsA:
        if lit not in allLits:
            allLits.append(lit)
    for lit in litsB:
        if lit not in allLits:
            allLits.append(lit)
    vars = []
    for lit in allLits:
        if lit[0] == "~":
            lit = lit[1:]
        if lit not in vars:
            vars.append(lit)
    unresolved = []
    reduced = 0
    for var in vars:
        negation = "~" + var
        if var not in allLits and negation not in allLits:
            raise Exception("Resolution error")
        elif var not in allLits and negation in allLits:
            unresolved.append(negation)
        elif var in allLits and negation not in allLits:
            unresolved.append(var)
        else: #var in allLits and negation in allLits, so eliminate that
            reduced += 1
    unresolved = sorted(unresolved)
    string = ""
    for lit in unresolved:
        string += lit + " "
    string
    unresolved = string
    if unresolved == "" or reduced > 1:
        return True
    elif len(unresolved.split()) == len(allLits):
        return None
    else:
        return unresolved[:-1]

start_time = time.time()

kbLines = open(sys.argv[1], "r").readlines()

goalClause = kbLines[-1]
kb = {}
for line in kbLines[:-1]:
    lits = sorted(line[:-1].split())
    string = ""
    for lit in lits:
        string += lit + " "
    string = string[:-1]
    kb.setdefault(string, None)
# NOT(A or B or C) ≡ Not(A) and Not(B) and Not(C)
goalClauseLits = goalClause.split()
for lit in goalClauseLits:
    if lit[0] == "~":
        kb.setdefault(lit[1:], None)
    else:
        kb.setdefault("~" + lit, None)
#print(kb)
i = 0
n = len(kb.items())
while i < n:
    for j in range(i):
        result = resolve(list(kb.keys())[i], list(kb.keys())[j])
        #print(i+1,j+1,result)
        if result == "Contradiction":
            kb.setdefault(result, (i+1, j+1))
            i = n
            break
        elif result == True:
            #print("Resolved to True")
            pass
        elif result is None:
            #print("No reduction")
            pass
        else:
            if result not in kb:
                kb.setdefault(result, (i + 1, j + 1))
                n += 1
            '''
            unique = True
            for clause in kb.keys():
                isSame = True
                for lit in clause.split():
                    if lit not in result.split():
                        isSame = False
                        break
                if len(clause.split()) != len(result.split()):
                    isSame = False
                if isSame:
                    print(result,"is same as",clause)
                    break
            if result not in kb.keys() and not isSame:
                kb.setdefault(result, (i+1, j+1))
                n += 1
            else:
                print("Same so not added to KB")
            '''
    i += 1
for line, item in enumerate(kb.items(),1):
    clause, parents = item
    toPrint = ""
    toPrint += str(line) + ". " + clause + " {"
    if parents is None:
        toPrint += "}"
    else:
        toPrint += str(parents[0]) + ", " + str(parents[1]) + "}"
    print(toPrint)
if list(kb.keys())[-1] == "Contradiction":
    print("Valid")
else:
    print("Fail")

#print("--- %s seconds ---" % (time.time() - start_time))