###########################################################
# Author: Senal Liyanage
# Affiliation: Mississippi State University
# Contact: sdd313@msstate.edu
# Date: June 4, 2023
# Description: Lipid Bilayer Structure Identifier
###########################################################

import argparse


def identify_lipid_residues(pdb_file):
    lipid_residues = []
    all_residues = set()  # Using a set to avoid counting the same residue multiple times
    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                residue_name = line[17:20].strip()
                residue_number = int(line[22:28].strip())
                all_residues.add(residue_number)
                if residue_name in ['PA', 'PC', 'OL']:
                    lipid_residues.append(residue_number)

    start_residue = min(lipid_residues) if lipid_residues else None
    end_residue = max(lipid_residues) if lipid_residues else None

    return start_residue, end_residue, len(all_residues)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lipid Bilayer Structure Identifier')
    parser.add_argument('pdb_file', help='Path to the PDB file')
    args = parser.parse_args()

    start, end, total = identify_lipid_residues(args.pdb_file)
    print(f"Total residues: {total}")
    if start is not None and end is not None:
        print(f"Lipid bilayer structure starts at residue {start} and ends at residue {end}")
    else:
        print("No lipid bilayer structure found in the PDB file.")
