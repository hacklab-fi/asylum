import ndaparser

if __name__ == "__main__" : 
    transactions = [];
    with open("./testdata.nda") as f:
        for line in f:
            transaction = ndaparser.parseLine(line)
            if transaction is not None:
                transactions.append(transaction)
    for transaction in transactions:
        print(transaction)
