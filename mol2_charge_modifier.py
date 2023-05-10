"""
mol2_charge_modifier.py - a Python script for modifying charge values in mol2 files.

This script takes as input a table of charge difference data stored in a .dat file and a directory containing one or more mol2 files.
For each mol2 file, the script modifies the charge values for specific atoms according to the values in the charge difference table.
The modified mol2 files are saved in the same directory as the original files with '_modified' appended to the filename.

Usage: python mol2_charge_modifier.py --dat <charge_diff.dat> --mol2dir <mol2_directory>

Required arguments:
--dat <charge_diff.dat>     : Path to the charge difference data file in .dat format.
--mol2dir <mol2_directory> : Path to the directory containing the mol2 files to modify.

Example usage:
python mol2_charge_modifier.py --dat charge_diff.dat --mol2dir mol2_files/
"""

import argparse
import os

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--dat', help='Path to charge difference data file (.dat format)', required=True)
parser.add_argument('--mol2dir', help='Path to directory containing mol2 files to modify', required=True)
args = parser.parse_args()

# Read charge difference data from dat file into a dictionary
with open(args.dat, 'r') as f:
    lines = f.readlines()

charge_diff = {}
for line in lines[1:]:
    fields = line.split()
    charge_diff[fields[0]] = float(fields[1])

# Process each mol2 file in the directory
for filename in os.listdir(args.mol2dir):
    if not filename.endswith('.mol2'):
        continue

    mol2path = os.path.join(args.mol2dir, filename)

    # Modify charge values in the mol2 file based on the charge difference dictionary
    with open(mol2path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if 'File Created by:' in line:
            lines[i] = f'# Created by mol2_charge_modifier.py, a Python script for modifying charge values in mol2 files.\n'

        if '@<TRIPOS>ATOM' in line:
            for j in range(i + 1, len(lines)):
                fields = lines[j].split()
                if len(fields) < 9:
                    break
                atom_id = fields[0]
                charge = float(fields[8])
                charge_diff_value = charge_diff.get(atom_id, 0.0)
                fields[8] = str(charge_diff_value + charge)
                lines[j] = '\t'.join(fields) + '\n'

    # Write the modified mol2 file to a new file
    output_filename = os.path.splitext(filename)[0] + '_modified.mol2'
    output_path = os.path.join(args.mol2dir, output_filename)
    with open(output_path, 'w') as f:
        f.writelines(lines)

    print(f'Modified {filename}. Output written to {output_path}.')