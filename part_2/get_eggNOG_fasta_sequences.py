#note need to first install pip install requests

import csv
import requests

def fetch_sequence_from_eggnog(member_id):
    """Fetch the sequence from the eggNOG API."""
    url = f"http://eggnogapi6.embl.de/get_sequence/{member_id}"
    response = requests.get(url)
    if response.status_code == 200:
        # need to skip first line and replace header to get to sequences
        return '\n'.join(response.text.splitlines()[1:])
    else:
        print(f"Error fetching sequence for {member_id}")
        return None

def tsv_to_fasta_eggnog(tsv_file: str, fasta_file: str):
    """Convert the TSV to FASTA using the eggNOG API."""
    with open(tsv_file, 'r') as infile, open(fasta_file, 'w') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        next(reader)  # skip header
        
        for row in reader:
            species = row[0].replace(" ", "_")  
            taxid = row[1]
            member_id = row[2]
            
            # fetching the sequence from the eggnog as in manual for eggnog API
            sequence = fetch_sequence_from_eggnog(member_id)
            
            if sequence:
                # write header and sequence to the FASTA file
                header = f">{member_id}|taxid:{taxid}|{species}\n"
                outfile.write(header)
                outfile.write(sequence + "\n")
            else:
                print(f"Error: No sequence found for {member_id}")


tsv_file = 'COG5002_members_1762.tsv'  # path to the members tsv file 
fasta_file = 'COG5002_eggnog_sequences.fasta'  # output in fasta format

#TSV to FASTA format
tsv_to_fasta_eggnog(tsv_file, fasta_file)