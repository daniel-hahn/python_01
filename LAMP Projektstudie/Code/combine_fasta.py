import glob

# Path to the folder containing the FASTA files
fasta_files = glob.glob("/Users/dan/Desktop/LAMP proj. studie/bieber/bold/cytb/*.txt")

# Output file path
output_file = "/Users/dan/Desktop/LAMP proj. studie/bieber/bold/cytb/combined_output.txt"

with open(output_file, "w") as outfile:
    for fasta in fasta_files:
        with open(fasta, "r") as infile:
            outfile.write(infile.read())
            outfile.write("\n")  # optional: ensures newline between sequences
