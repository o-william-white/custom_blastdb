# Custom blast databases

This repo describes code used to generate custom blast databases with ncbi taxonomic identifiers for various projects. This includes:
- refseq mitochondrial sequences (accessed Oct 23)
- SILVA ribosomal databases (accessed Oct 23)

### Mitochondrion blast database

```
# set dir
mkdir -p refseq_mitochondrion && cd refseq_mitochondrion

# wget mitochondrial refseq
wget https://ftp.ncbi.nlm.nih.gov/refseq/release/mitochondrion/mitochondrion.1.1.genomic.fna.gz

# gunzip
gunzip mitochondrion.1.1.genomic.fna.gz

# wget accession2taxid
wget https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz

# get accession ids from fasta file
grep -e "^>" mitochondrion.1.1.genomic.fna | sed 's/>//g' | cut -f 1 -d " " > accessions.txt

# write text file with accession and taxonomy id
python ../additional_scripts/accession2taxid.py

# blastn
source activate blast
makeblastdb -dbtype nucl -in mitochondrion.1.1.genomic.fna -out refseq_mitochondrion -taxid_map accession2taxid.txt -parse_seqids
conda deactivate

# rm tmp
rm mitochondrion.1.1.genomic.fna
rm nucl_gb.accession2taxid.gz
rm accessions.txt
rm accession2taxid.txt

cd ..

```

### Silva 138 blast database

```
# silva data accessed using ftp:
# https://ftp.arb-silva.de/release_138_1/Exports/

# set dir
mkdir -p silva_138 && cd silva_138

# wget fasta
# lsu large subunit
# ssu small subunit
# nr99 non redundant 99% similar
wget https://ftp.arb-silva.de/release_138_1/Exports/SILVA_138.1_LSURef_NR99_tax_silva.fasta.gz
wget https://ftp.arb-silva.de/release_138_1/Exports/SILVA_138.1_SSURef_NR99_tax_silva.fasta.gz

# wget taxmap
wget https://ftp.arb-silva.de/release_138_1/Exports/taxonomy/ncbi/taxmap_embl-ebi_ena_lsu_ref_nr99_138.1.txt.gz
wget https://ftp.arb-silva.de/release_138_1/Exports/taxonomy/ncbi/taxmap_embl-ebi_ena_ssu_ref_nr99_138.1.txt.gz

# accession2taxid
zcat taxmap_embl-ebi_ena_lsu_ref_nr99_138.1.txt.gz | tail -n +2  | awk -F "\t" ' { print $1 "." $2 "." $3 "\t" $6 } ' > accession2taxid_lsu.txt
zcat taxmap_embl-ebi_ena_ssu_ref_nr99_138.1.txt.gz | tail -n +2  | awk -F "\t" ' { print $1 "." $2 "." $3 "\t" $6 } ' > accession2taxid_ssu.txt

# cat accession2taxid
cat accession2taxid_[l,s]su.txt > accession2taxid.txt

# cat fasta
zcat SILVA_138.1_[L,S]SURef_NR99_tax_silva.fasta.gz > silva_138.1_lsu_ssu.fasta

# found duplicate sequences after combining lsu and ssu
cat accession2taxid.txt | sort | uniq -d | cut -f 1 > accessions_duplicate.txt

# get unique accesions
grep -f accessions_duplicate.txt -v accession2taxid.txt | cut -f 1 > accessions_unique.txt

# accession2taxid with unique records only
grep -f accessions_duplicate.txt -v accession2taxid.txt > accession2taxid_unique.txt

# subseq fasta for unique sequences
source activate seqtk
seqtk subseq silva_138.1_lsu_ssu.fasta accessions_unique.txt > silva_138.fasta
conda deactivate

# makeblastdb
source activate blast
makeblastdb -dbtype nucl -in silva_138.fasta -out silva_138 -taxid_map accession2taxid_unique.txt -parse_seqids
conda deactivate

# rm intermediate
rm SILVA_138.1_LSURef_NR99_tax_silva.fasta.gz
rm SILVA_138.1_SSURef_NR99_tax_silva.fasta.gz
rm taxmap_embl-ebi_ena_lsu_ref_nr99_138.1.txt.gz
rm taxmap_embl-ebi_ena_ssu_ref_nr99_138.1.txt.gz
rm accession2taxid_lsu.txt
rm accession2taxid_ssu.txt
rm accession2taxid.txt
rm accession2taxid_unique.txt
rm silva_138.1_lsu_ssu.fasta
rm silva_138.fasta
rm accessions_duplicate.txt
rm accessions_unique.txt

# cd ..
```

### blast db tests

```
source activate blast

blastn \
   -query example_data/example_mitochondrial_genomes.fasta \
   -db refseq_mitochondrion/refseq_mitochondrion \
   -out example_data/example_mitochondrial_genomes.txt \
   -outfmt '6 qseqid staxids bitscore std' \
   -max_target_seqs 5

blastn \
   -query example_data/example_ribosomal.fasta \
   -db silva_138/silva_138 \
   -out example_data/example_ribosomal.txt \
   -outfmt '6 qseqid staxids bitscore std' \
   -max_target_seqs 5

conda deactivate
```

