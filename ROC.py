import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import auc, roc_curve, roc_auc_score
import pandas as pd
import subprocess

#run the awk commands -> 

#java -jar negsel2 .jar -self english.train -n 10 -r 4 -c -l < english.test | awk ’{n+= $1}END{print n/NR}’
#
#java -jar negsel2 .jar -self english.train -n 10 -r 4 -c -l < tagalog.test | awk
#’{n+= $1}END{print n/NR}’

for i in range(1,10):
    #Run the java for english test
    command = "java -jar negative-selection/negsel2.jar -self negative-selection/english.train -n 10 -r "+str(i)+" -c -l"
    p = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)


    testfile = open("negative-selection/english.test").readlines()

    entropies = []

    for line in testfile:
        #print(line)
        p.stdin.write(line)
        p.stdin.flush()
        output = p.stdout.readline().strip()
        entropies.append(output)

    p.stdin.close()
    return_code = p.wait()
    print("Return code: ", return_code)

    error_output = p.stderr.read()
    if error_output:
        print("Error output:", error_output)


    scores_english = [float(item.strip()) for item in entropies]

    file = open(f"scores{i}.txt", 'w')
    for a  in entropies:

        file.write(str(a) + "\n")

    #run it for tagalog test
    command = "java -jar negative-selection/negsel2.jar -self negative-selection/english.train -n 10 -r "+str(i)+" -c -l"
    p = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)


    testfile = open("negative-selection/tagalog.test").readlines()

    entropies = []

    for line in testfile:
        #print(line)
        p.stdin.write(line)
        p.stdin.flush()
        output = p.stdout.readline().strip()
        entropies.append(output)

    p.stdin.close()
    return_code = p.wait()
    print("Return code: ", return_code)

    error_output = p.stderr.read()
    if error_output:
        print("Error output:", error_output)

    scores_tagalog = [float(item.strip()) for item in entropies]

    scores = np.concatenate([scores_tagalog, scores_english])
    labels = np.zeros(len(scores))
    labels[:len(scores_tagalog)] = 1
    labels[len(scores_tagalog):] = -1
    fpr, tpr, thresholds = roc_curve(labels, scores)

    plt.figure()
    plt.plot(fpr, tpr, color='orange', lw=2, label='ROC curve (AUC %0.3f)' % auc(fpr, tpr))
    plt.plot([0,1],[0,1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.05])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc="lower right")
    plt.grid()
    print(f"Finished r={i}")

plt.show()
