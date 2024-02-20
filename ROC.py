import subprocess

#run the awk commands -> 

#java -jar negsel2 .jar -self english.train -n 10 -r 4 -c -l < english.test | awk ’{n+= $1}END{print n/NR}’
#
#java -jar negsel2 .jar -self english.train -n 10 -r 4 -c -l < tagalog.test | awk
#’{n+= $1}END{print n/NR}’

#result =subprocess.run(["java", "-jar", "negative-selection/negsel2.jar", "-self","english.train","-n","10","-r","4","-c","-l","<","english.test","|","awk", "’{n+= $1}END{print n/NR}’"], shell=True, capture_output=True)



p = subprocess.Popen("java -jar negative-selection/negsel2.jar -self negative-selection/english.train -n 10 -r 4 -c -l".split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)


testfile = open("negative-selection/english.test").readlines()
print(len(testfile))

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
    



print(entropies)
print(len(entropies))