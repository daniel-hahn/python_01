input_path = "/Users/dan/Desktop/LAMP proj. studie/bieber/bold/cytb/combined_output_clean.txt"
output_path = "/Users/dan/Desktop/LAMP proj. studie/bieber/bold/cytb/combined_output_clean_replaced.txt"

with open(input_path, "r") as infile, open(output_path, "w") as outfile:
    for line in infile:
        if line.startswith(">"):
            # Replace pipe symbols with underscores
            new_line = line.replace("|", "_")
            outfile.write(new_line)
        else:
            outfile.write(line)
