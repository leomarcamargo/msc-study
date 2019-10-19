from math import pow
import csv

features = {}
modules = {} 
dedi = {}
conc = {}

dos = {}
dot = {}

def updateTabularData(row) :
    # read data from the row columns,

    delta = row[2]
    feature = row[3]
    loc = float(row[4])

    # assign zero to the lines of code of the
    # current delta and feature, if they do not
    # exist. 
    deltaLoc = modules.get(delta, 0.0)
    featureLoc = features.get(feature, 0.0)
        
    modules[delta] = deltaLoc + loc
    features[feature] = featureLoc + loc

    deltaLoc = dedi.get((delta, feature), 0.0)
    featureLoc = conc.get((feature, delta), 0.0)

    dedi[(delta, feature)] = deltaLoc + loc 
    conc[(feature, delta)] = featureLoc + loc    
  

def computeMetrics():
    for (f, d) in conc:
        c = conc[(f, d)]
        conc[(f, d)] = c / features[f]

    for (d, f) in dedi:
        c = dedi[(d, f)]
        dedi[(d, f)] = c / modules[d]

    #print conc
    #print dedi
    
    for f in features:
        sm = len(modules)
        summ = 0.0
        for m in modules:
            summ = summ + pow((conc.get((f,m),0.0) - (1.0/sm)),2)
        dos[f] = round(1 - round(((sm * summ) / (sm - 1.0)), 5), 5)    

    for m in modules:
        sf = len(features)
        summ = 0.0
        for f in features:
            summ = summ + pow((dedi.get((m,f), 0.0)) - (1.0/sf),2)
        dot[m] = round(1 - round(((sf * summ) / (sf - 1.0)), 5), 5)

       
pathMetrics = 'D:/Mestrado/msc-study/metrics/'
technique = input('Technique (like delta or cc): ')
technique = technique.lower()
if technique == "delta":
    fileName = pathMetrics + 'reminder/delta-oriented-programming-version/delta-values/loc/'
else:
    fileName = pathMetrics + 'reminder/conditional-compilation-version/classes-values/loc/'
release   = input('Release (like v1, v2, v3, or v4): ')
release = release.lower()
fileName += release + '.csv'


with open(fileName) as f:
    data = [d.strip() for d in f.readlines()]
    for d in data:
        r = d.split(",")
        updateTabularData(r)

    computeMetrics()

    with open('dos-' + release + '-' + technique +'.csv', 'w', newline='') as csvDoS:
        writerDoS = csv.writer(csvDoS)
        for feature in dos:
            resultDoS = [technique, release, feature, str(dos[feature])]
            writerDoS.writerow(resultDoS)
    csvDoS.close()
        
    with open('dot-' + release + '-' + technique +'.csv', 'w', newline='') as csvDoT:
        writerDoT = csv.writer(csvDoT)  
        for delta in dot:
            resultDoT = [technique, release, delta, str(dot[delta])]
            writerDoT.writerow(resultDoT)
    csvDoT.close()
    
    f.close()
    
print ('Process completed successfully. CSV files were generated!')
