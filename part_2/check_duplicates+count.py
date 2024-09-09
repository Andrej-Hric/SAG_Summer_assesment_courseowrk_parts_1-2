from Bio import SeqIO

# Set the file path
fasta_file = "COG5002_mapped_uniprot.fasta"

# Create a set to store unique sequences
unique_sequences = set()

# Counter for duplicates
duplicates = 0

# Iterate over each sequence in the FASTA file
for seq_record in SeqIO.parse(fasta_file, "fasta"):
    # Convert the sequence to a string to add to the set
    sequence_str = str(seq_record.seq)
    
    if sequence_str in unique_sequences:
        # If sequence already exists in the set, it is a duplicate
        duplicates += 1
        print(f"Duplicate found: {seq_record.id}")
    else:
        # Add the sequence to the set if it's not a duplicate
        unique_sequences.add(sequence_str)

print(f"\nTotal number of duplicate sequences: {duplicates}")


from Bio import SeqIO

# Set the file path
fasta_file = "COG5002_mapped_uniprot.fasta"

# Count the number of sequences
sequence_count = sum(1 for _ in SeqIO.parse(fasta_file, "fasta"))

print(f"Total number of sequences: {sequence_count}")
