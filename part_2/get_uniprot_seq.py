import requests
import csv
import sys
import os

# Base UniProt API URL
UNIPROT_SEARCH_URL = "https://rest.uniprot.org/uniprotkb/search?query="

def search_uniprot_by_name(name):
    """
    Function to search UniProt for a specific protein by name.
    """
    # Prepare the query
    query = f"{name}"
    
    # Format the query URL to return results in FASTA format
    url = f"{UNIPROT_SEARCH_URL}{query}&format=fasta"
    
    # Send the request to UniProt
    response = requests.get(url)
    
    # Return the response content if a hit is found
    if response.status_code == 200 and len(response.text) > 0:
        return response.text
    else:
        return None

def process_tsv_file(tsv_file, output_fasta_file):
    """
    Process the TSV file containing protein names and fetch FASTA sequences from UniProt.
    """
    # List to store FASTA sequences found
    fasta_sequences = []
    
    # Open the TSV file and read each line
    with open(tsv_file, mode='r') as file:
        tsv_reader = csv.DictReader(file, delimiter='\t')
        for row in tsv_reader:
            species_name = row['Species']
            taxid = row['Taxid']
            member_id = row['Member']
            
            # Create a full name to search in UniProt
            full_name = f"{species_name} {taxid} {member_id}"
            print(f"Searching for: {full_name}")
            
            # Search UniProt for the protein by full name
            fasta_sequence = search_uniprot_by_name(full_name)
            
            # If a sequence is found, append it to the list
            if fasta_sequence:
                print(f"FASTA sequence found for {full_name}")
                fasta_sequences.append(fasta_sequence)
            else:
                print(f"No sequence found for {full_name}")

    # Write the collected FASTA sequences to an output file
    with open(output_fasta_file, 'w') as output_file:
        for sequence in fasta_sequences:
            output_file.write(sequence)

    print(f"FASTA sequences saved to {output_fasta_file}")

if __name__ == "__main__":
    # Path to your TSV file
    tsv_file = 'COG5002_members_1762.tsv'
    
    # Path for the output FASTA file
    output_fasta_file = 'COG5002_mapped_uniprot.fasta'
    
    # Check if the input file exists
    if not os.path.exists(tsv_file):
        print(f"Error: The file {tsv_file} was not found.")
        sys.exit(1)
    
    # Process the TSV file and fetch FASTA sequences
    process_tsv_file(tsv_file, output_fasta_file)