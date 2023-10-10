import gzip

# read accession to taxonomy into dictionary
acc2tax = {}
with gzip.open('nucl_gb.accession2taxid.gz','rb') as f:
    for line in f:
        line = line.decode().rstrip("\n").split("\t")
        if line[0] != "accession":
            acc = line[1]
            tax = line[2]
            acc2tax[acc] = tax

# open accession_list input and accession2tax output
accession_list = open("accessions.txt", "r")
accession2tax = open("accession2taxid.txt", "w")

# iterate through accession_list
for line in accession_list:
    acc = line.rstrip("\n")
    # if no taxonomy in acc2tax use unidentified
    # https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=32644
    accession2tax.write(f"{acc}\t{acc2tax.get(acc, '32644')}\n")

# close 
accession_list.close()
accession2tax.close()

