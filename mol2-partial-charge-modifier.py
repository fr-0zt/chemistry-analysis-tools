"""
This script modifies charges in a MOL2 file using the Open Babel library. Given an input MOL2 file and a file containing
charge differences, it modifies the charges of specific atoms in the molecule and generates a modified MOL2 file.

Usage:
python modify_charges.py input_file charge_file [-o output_file]

If the optional argument "-o" or "--output_file" is not provided, the script will generate a default output file with
the same name as the input file, but with the suffix "_charge-modified.mol2" added.

Improvements made:

Used context managers to open and close files.
Added error handling for file not found.
Improved variable naming for clarity.
"""

import argparse
from openbabel import openbabel as ob
import os
import sys

# Define command line arguments
parser = argparse.ArgumentParser(description='Modify charges in a mol2 file.')
parser.add_argument('input_file', type=str, help='Path to input mol2 file')
parser.add_argument('output_file', type=str, nargs='?', default=None, help='Path to output modified mol2 file')
parser.add_argument('charge_file', type=str, help='Path to file containing charge differences')

# Parse command line arguments
args = parser.parse_args()

# Load molecule from input file
mol = ob.OBMol()
obConversion = ob.OBConversion()
obConversion.SetInAndOutFormats('mol2', 'mol2')

if not os.path.isfile(args.input_file):
    print(f"Error: File {args.input_file} not found.", file=sys.stderr)
    sys.exit(1)

try:
    obConversion.ReadFile(mol, args.input_file)
except RuntimeError as e:
    print(f"Error: Failed to read file {args.input_file}: {e}", file=sys.stderr)
    sys.exit(1)

# Load charge differences from file
charge_diff = {}
try:
    with open(args.charge_file) as f:
        next(f)  # skip header line
        for line in f:
            atom_name, charge = line.split()
            charge_diff[atom_name] = float(charge)
except FileNotFoundError:
    print(f"Error: File {args.charge_file} not found.", file=sys.stderr)
    sys.exit(1)
except (ValueError, TypeError):
    print(f"Error: Failed to parse charge file {args.charge_file}. Each line should contain an atom name and a charge separated by whitespace.", file=sys.stderr)
    sys.exit(1)

# Modify charges in molecule
for res in ob.OBResidueIter(mol):
    for atom in ob.OBResidueAtomIter(res):
        atom_name = res.GetAtomID(atom)
        if atom_name in charge_diff:
            atom.SetPartialCharge(charge_diff[atom_name])

# Set output file name
if args.output_file is None:
    input_file_name = os.path.splitext(args.input_file)[0]
    output_file_name = f"{input_file_name}_charge-modified.mol2"
else:
    output_file_name = args.output_file

# Write modified molecule to output file
try:
    with open(output_file_name, 'w') as f:
        obConversion.WriteFile(mol, f)
except OSError as e:
    print(f"Error: Failed to write to file {output_file_name}: {e}", file=sys.stderr)
    sys.exit(1)