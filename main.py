import sys

def getName():
    try:
        name_file = sys.argv[1]
        print(name_file)
    except :
        print("Veuillez preciser le PDF")

getName()
