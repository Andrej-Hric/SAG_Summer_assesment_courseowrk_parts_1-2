import time
from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO

# Function to perform BLAST search and retrieve the best UniProt ID match
def blast_sequence(sequence, retries=3):
    """BLAST the sequence against UniProt to get the best match."""
    for attempt in range(retries):
        try:
            # Perform BLAST search against the 'swissprot' (UniProtKB) database
            result_handle = NCBIWWW.qblast("blastp", "swissprot", sequence)
            blast_record = NCBIXML.read(result_handle)

            if blast_record.alignments:
                # Get the best hit's accession (UniProt ID) from the first alignment
                best_alignment = blast_record.alignments[0]
                uniprot_id = best_alignment.accession
                return uniprot_id
            else:
                return None
        except Exception as e:
            print(f"BLAST search failed for sequence: {sequence[:30]}... Error: {e}")
            time.sleep(1)  # Wait for a second before retrying
    return None

# Function to process the FASTA file and map sequences to UniProt IDs via BLAST
def map_fasta_to_uniprot_blast(fasta_file: str, output_file: str, log_file: str):
    """Map sequences in FASTA to their UniProt IDs using BLAST."""
    with open(fasta_file, 'r') as fasta, open(output_file, 'w') as output, open(log_file, 'w') as log:
        sequence = ""
        header = ""

        for line in fasta:
            if line.startswith(">"):  # Header line
                if sequence:
                    # Perform BLAST search for the previous sequence
                    uniprot_id = blast_sequence(sequence)

                    if not uniprot_id:
                        log.write(f"Failed to BLAST UniProt ID for sequence: {header}\n")
                        print(f"Failed to fetch UniProt ID for: {header}")
                    else:
                        output.write(f">{uniprot_id}|\n")
                        output.write(f"{sequence}\n")
                        print(f"Success: {header} mapped to UniProt ID: {uniprot_id}")

                    sequence = ""  # Reset sequence for the next entry
                
                header = line.strip()  # Set the new header
            else:
                sequence += line.strip()

        # Process the last sequence in the file
        if sequence:
            uniprot_id = blast_sequence(sequence)
            if not uniprot_id:
                log.write(f"Failed to BLAST UniProt ID for sequence: {header}\n")
                print(f"Failed to fetch UniProt ID for: {header}")
            else:
                output.write(f">{uniprot_id}|\n")
                output.write(f"{sequence}\n")
                print(f"Success: {header} mapped to UniProt ID: {uniprot_id}")

# Paths to input/output files
fasta_file = 'COG5002_eggnog_sequences.fasta'  # Input FASTA file
output_file = 'COG5002_with_uniprot_ids_blast.fasta'  # Output FASTA with UniProt IDs (from BLAST)
log_file = 'uniprot_blast_errors.log'  # Log file for failed BLAST searches

# Run the BLAST-based mapping function
map_fasta_to_uniprot_blast(fasta_file, output_file, log_file)

print("BLAST processing complete. Check output and log files.")