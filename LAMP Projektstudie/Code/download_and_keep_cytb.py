# download: 
# https://www.boldsystems.org/index.php/API_Public/sequence?taxon=Ondatra+zibethicus
# https://www.boldsystems.org/index.php/API_Public/sequence?taxon=Castor+canadensis
# https://www.boldsystems.org/index.php/API_Public/sequence?taxon=Cyprinus+carpio
# https://www.boldsystems.org/index.php/API_Public/sequence?taxon=Lutra+lutra
# https://www.boldsystems.org/index.php/API_Public/sequence?taxon=Anas+platyrhynchos
# https://www.boldsystems.org/index.php/API_Public/sequence?taxon=Castor+fiber


input_file = "/Users/dan/Desktop/LAMP proj. studie/bieber/bold/anas_platyrhynchos.txt"
output_file = "/Users/dan/Desktop/LAMP proj. studie/bieber/bold/anas_platyrhynchos_cytb_only.txt"

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    write = False
    for line in infile:
        if line.startswith(">"):
            if "CYTB" in line.upper():
                write = True
                outfile.write(line)
            else:
                write = False
        elif write:
            outfile.write(line)
