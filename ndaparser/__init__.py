import ndaparser

if __name__ == "__main__" : 
    trns = ndaparser.parseLine("T10188000060SCTSZFW3GT3WU1B   1501131501131501121710Viitemaksu                         +000000000000002800  HAKKERI HEIKKI HOKSAAVA            A               00000000000000111012         ")
    print(trns)
