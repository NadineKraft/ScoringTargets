# Scoring Targets

Preparation script to get all targets of a reference file with a chosen PAM motif

# Command

    ./preparation.py --motif GG --pam NGG --reference_file /path/to/fasta/file --ref_name GRCh38 --mismatches 4
    
# TODO

    Change code #TODO parts when using a different PAM length (other than 3) 
    or different PAM motif (other than NGG).
    Change chromosome dictionary when using a different reference (other than GRCh38)


Output file example:  chr1.NGG.GRCh38.forward.0.1.txt
    
    /home/pythonProject/GRCh38.fna
    NNNNNNNNNNNNNNNNNNNNNGG
    AACCCTAACCCTAACCCTCGCGG	4
    ACCCTCGCGGTACCCTCAGCCGG	4
    CCTCAGCCGGCCCGCCCGCCCGG	4
    GCCCGCCCGGGTCTGACCTGAGG	4
    TACCACCGAAATCTGTGCAGAGG	4
    ACGCAACTCCGCCGTTGCAAAGG	4
    GCAGACACATGCTAGCGCGTCGG	4
    AGACACATGCTAGCGCGTCGGGG	4
    CACATGCTAGCGCGTCGGGGTGG	4
    ATGCTAGCGCGTCGGGGTGGAGG	4
    AGACACATGCTACCGCGTCCAGG	4
    ACACATGCTACCGCGTCCAGGGG	4
    CATGCTACCGCGTCCAGGGGTGG	4
    GCTACCGCGTCCAGGGGTGGAGG	4
    AGACACATGCTAGCGCGTCCAGG	4
    ACACATGCTAGCGCGTCCAGGGG	4
    CATGCTAGCGCGTCCAGGGGTGG	4

Use Cas-Offinder to get off-targets for the single files

Output file example:  chr1.NGG.GRCh38.forward.offinder.0.1.txt

    AACCCTAACCCTAACCCTCGCGG	NC_000001.11 Homo sapiens chromosome 1, GRCh38.p13 Primary Assembly	10450	AACCCTAACCCTAACCCTCGCGG	+	0
    AACCCTAACCCTAACCCTCGCGG	NC_000001.11 Homo sapiens chromosome 1, GRCh38.p13 Primary Assembly	3155373	AACCCgAACCCaAgtCCTCGCGG	-	4
    AACCCTAACCCTAACCCTCGCGG	NC_000001.11 Homo sapiens chromosome 1, GRCh38.p13 Primary Assembly	6481877	AACCCTAACCtTAACCCTtttGG	-	4
    AACCCTAACCCTAACCCTCGCGG	NC_000001.11 Homo sapiens chromosome 1, GRCh38.p13 Primary Assembly	203120708	AcCCCTAACCCTAgCCCaCGgGG	-	4
    AACCCTAACCCTAACCCTCGCGG	NC_000002.12 Homo sapiens chromosome 2, GRCh38.p13 Primary Assembly	29376369	cACCCTAACCCTAACCCTaagGG	-	4
    AACCCTAACCCTAACCCTCGCGG	NC_000003.12 Homo sapiens chromosome 3, GRCh38.p13 Primary Assembly	58527094	AAtCCTAgCCCTAACCCTtGaGG	-	4
    ACCCTCGCGGTACCCTCAGCCGG	NC_000001.11 Homo sapiens chromosome 1, GRCh38.p13 Primary Assembly	180993	ACCCTCGCGGTACCCTCAGCCGG	+	0
    ACCCTCGCGGTACCCTCAGCCGG	NC_000001.11 Homo sapiens chromosome 1, GRCh38.p13 Primary Assembly	10463	ACCCTCGCGGTACCCTCAGCCGG	+	0
    ACCCTCGCGGTACCCTCAGCCGG	NC_000001.11 Homo sapiens chromosome 1, GRCh38.p13 Primary Assembly	42463356	ACgCTCGCGGcACCCTCcGCaGG	+	4
    ACCCTCGCGGTACCCTCAGCCGG	NC_000002.12 Homo sapiens chromosome 2, GRCh38.p13 Primary Assembly	9660564	ACCCTCGCGcTACCtgCAGgCGG	-	4
    ACCCTCGCGGTACCCTCAGCCGG	NC_000003.12 Homo sapiens chromosome 3, GRCh38.p13 Primary Assembly	14267417	ACCCTCGCGacACCCTCAaCaGG	+	4
    CCTCAGCCGGCCCGCCCGCCCGG	NC_000001.11 Homo sapiens chromosome 1, GRCh38.p13 Primary Assembly	10476	CCTCAGCCGGCCCGCCCGCCCGG	+	0
    CCTCAGCCGGCCCGCCCGCCCGG	NC_000001.11 Homo sapiens chromosome 1, GRCh38.p13 Primary Assembly	181006	CCTCAGCCGGCCCGCCCGCCCGG	+	0
    CCTCAGCCGGCCCGCCCGCCCGG	NC_000001.11 Homo sapiens chromosome 1, GRCh38.p13 Primary Assembly	1435910	tCcCAGCCcGCCCGCCCGtCCGG	-	4
    CCTCAGCCGGCCCGCCCGCCCGG	NC_000001.11 Homo sapiens chromosome 1, GRCh38.p13 Primary Assembly	9588654	CCgCcGCCGcCCCGCCCaCCCGG	+	4
    CCTCAGCCGGCCCGCCCGCCCGG	NC_000001.11 Homo sapiens chromosome 1, GRCh38.p13 Primary Assembly	13808345	CCTCAGCCcGCCacCaCGCCCGG	-	4
    CCTCAGCCGGCCCGCCCGCCCGG	NC_000001.11 Homo sapiens chromosome 1, GRCh38.p13 Primary Assembly	17438098	CCTgcGCCGGCCCGgCCGCCgGG	+	4
    CCTCAGCCGGCCCGCCCGCCCGG	NC_000001.11 Homo sapiens chromosome 1, GRCh38.p13 Primary Assembly	22143175	CCgCccCCGGCCCGCCCcCCCGG	-	4

Run scoring script score_offinder_files.py on the offinder files. Use cluster to run files parallel.
# Command

    ./score_offinder_files.py --off /path/to/the/offinder/file --output /path/to/the/output/file

Output file example:  chr1.NGG.GRCh38.forward.offinder.0.1.txt
Entry explanation: Location, sequence, score

    10450,aaccctaaccctaaccctcgCGG,16.949292280664785
    10463,accctcgCGGTACCCTCAGCCGG,11.922733401572579
    10476,CCTCAGCCGGCCCGCCCGCCCGG,36.5618310066556
    10489,GCCCGCCCGGGTCTGACCTGAGG,34.07755611680795
    10535,TACCACCGAAATCTGTGCAGAGG,64.52284816211095
    10607,acgCAACTCCGCCGTTGCAAAGG,22.118711300772745
    10795,gcagacaCATGCTAGCGCGTCGG,1.282692307651923
    10797,agacaCATGCTAGCGCGTCGGGG,9.414938236335079
    10800,caCATGCTAGCGCGTCGGGGTGG,1.6056885612069074
    10803,ATGCTAGCGCGTCGGGGTGGAGG,2.8199815909986112
    10871,agacaCATGCTACCGCGTCCAGG,17.428502588911705
    10873,acaCATGCTACCGCGTCCAGGGG,8.754232175011419
    10876,CATGCTACCGCGTCCAGGGGTGG,12.498570629040834
    10879,GCTACCGCGTCCAGGGGTGGAGG,12.411413793685846
    10947,agacaCATGCTAGCGCGTCCAGG,56.62084022280849
    10949,acaCATGCTAGCGCGTCCAGGGG,48.262614937928255
    10952,CATGCTAGCGCGTCCAGGGGTGG,18.01997768335565

Run merge_all.py script to merge scored cas-offinder-files
# Command

    ./merge_all.py --input /path/to/scored/input/files/directory --output /path/to/output/files/directory

Results in two files (forward and reverse direction) for each chromosome.
Put the csv files in folder TheCrisprApp/backend/targets/crispr_search.
