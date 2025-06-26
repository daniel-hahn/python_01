import tkinter as tk
from collections import OrderedDict
import re
import colorsys

# SETTINGS
filename = "/Users/dan/Desktop/LAMP proj. studie/bieber/msa/bieber.aln-fasta"
reference_keyword = "fiber"
start_pos = 0
max_bases = 3000
match_color = "#1f77b4"

# LOAD FASTA
sequences = OrderedDict()
with open(filename, "r") as f:
    current_id = None
    for line in f:
        if line.startswith(">"):
            current_id = line.strip()[1:]
            sequences[current_id] = ""
        else:
            sequences[current_id] += line.strip()

# CHOOSE REFERENCE
ref_id = next(i for i in sequences if reference_keyword in i.lower())
ref_seq = sequences[ref_id][start_pos:start_pos + max_bases]

# TRIM ALL SEQUENCES
for sid in sequences:
    sequences[sid] = sequences[sid][start_pos:start_pos + max_bases]

# HELPER: extract species name
def extract_species(name):
    return re.sub(r'[_\d]+$', '', name)

# Assign species to each ID
species_map = {sid: extract_species(sid) for sid in sequences}
species_list = sorted(set(species_map.values()))

# Assign unique colors per species
def assign_species_colors(species_list):
    colors = {}
    num_species = len(species_list)
    for i, species in enumerate(sorted(species_list)):
        hue = i / num_species
        r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(hue, 0.6, 0.9)]
        colors[species] = f"rgb({r},{g},{b})"
    return colors

species_colors = assign_species_colors(species_list)

# Define Eisvogel species by prefix
eisvogel_prefixes = ["Alcedo", "Halcyon", "Ceyx"]

def is_eisvogel(species):
    return any(species.startswith(prefix) for prefix in eisvogel_prefixes)

# Sort IDs: Eisvogel first, then others
eisvogel_ids = [sid for sid in sequences if is_eisvogel(species_map[sid])]
other_ids = [sid for sid in sequences if not is_eisvogel(species_map[sid])]
eisvogel_ids.sort(key=lambda x: species_map[x])
other_ids.sort(key=lambda x: species_map[x])
sorted_ids = eisvogel_ids + other_ids

# EXPORT TO HTML
def export_to_html():
    html_content = """
    <html>
    <head><title>Sequence Alignment</title><style>
    body { font-family: Courier, monospace; margin: 0; padding: 1em; }
    .match { color: #1f77b4; font-size: 8px; }
    .mismatch { color: #ff0000; font-size: 8px; }
    .label-column {
        position: sticky;
        left: 0;
        background: #fff;
        font-size: 9px;
        text-align: left;
        white-space: nowrap;
        padding-right: 10px;
        border-right: 1px solid #ccc;
    }
    table {
        border-collapse: collapse;
        width: max-content;
    }
    td, th {
        padding: 2px 4px;
        white-space: nowrap;
        font-size: 8px;
    }
    th {
        text-align: left;
        font-size: 9px;
        background: #f0f0f0;
        position: sticky;
        top: 0;
        z-index: 2;
    }
    .wrapper {
        overflow: auto;
        border: 1px solid #ddd;
        max-height: 90vh;
    }
    </style></head>
    <body><h1>Sequence Alignment Viewer</h1>
    <div class="wrapper">
    <table>
    <tr><th class="label-column">Label</th><th>Sequence</th></tr>
    """

    def html_row(label, seq, ref):
        is_ref = label == "REFERENCE"
        species = species_map.get(label, "")
        color = "#555" if is_ref else species_colors[species]
        is_atthis = species == "Alcedo_atthis"
        is_eisvogel_species = is_eisvogel(species)

        row = f"<tr><td class='label-column' style='color: {color}'>{label}</td><td>"

        # Detect long match runs for non-eisvogels
        match_run = [base == ref[i] for i, base in enumerate(seq)]
        highlight_match = [False] * len(seq)
        if not is_eisvogel_species and not is_ref:
            i = 0
            while i < len(seq):
                if match_run[i]:
                    start = i
                    while i < len(seq) and match_run[i]:
                        i += 1
                    if (i - start) >= 10:  # Change this threshold to 10
                        for j in range(start, i):
                            highlight_match[j] = True
                else:
                    i += 1

        for i, base in enumerate(seq):
            match = base == ref[i]
            tag = "match" if match else "mismatch"

            # Background color logic
            bg = ""
            if is_ref:
                bg = ""
            elif is_atthis and match:
                bg = "background-color: #fff3b0;"  # yellow for Alcedo_atthis
            elif is_eisvogel_species and match:
                bg = "background-color: #e6f7ff;"  # light blue for Eisvogel
            elif highlight_match[i]:
                bg = "background-color: #fff3b0;"  # yellow for 10+ match streak

            row += f'<span class="{tag}" style="{bg}">{base}</span>'
        row += "</td></tr>"
        return row



    # Add reference row
    html_content += html_row("REFERENCE", ref_seq, ref_seq)

    # Add all other sequences
    for sid in sorted_ids:
        if sid != ref_id:
            html_content += html_row(sid, sequences[sid], ref_seq)

    html_content += "</table></div></body></html>"

    with open("alignment_viewer.html", "w") as f:
        f.write(html_content)

# Run export
export_to_html()
print("HTML export complete: alignment_viewer.html")
