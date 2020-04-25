import os


def cleanLinksInLinksDirectories():
    sum=0
    for file in os.listdir("./links/"):
        if(file==".txt"):
            os.remove(f)
        elif(file[0]!='.'):
            lst = list()
            with open("./links/"+file, "r") as f:
                for line in f:
                    if(line not in lst):
                        lst.append(line)
            sum+=len(lst)
            with open("./links/"+file, "w") as f:
                for line in lst:
                    f.write(line)

    print(str(sum)+" links total.")

def cleanInputFile():
    lst = list()
    with open("input.txt", 'r') as f:
        for line in f:
            if(line not in lst):
                lst.append(line)
    lst.sort()
    with open("input.txt", 'w') as f:
        for line in lst:
            f.write(line)


def cleanLinks():
    cleanLinksInLinksDirectories()
    cleanInputFile()


if __name__ == "__main__":
    cleanLinks()

