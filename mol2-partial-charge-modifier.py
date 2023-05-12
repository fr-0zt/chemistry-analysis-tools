import argparse
from openbabel import openbabel as ob
import os

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
obConversion.ReadFile(mol, args.input_file)

# Load charge differences from file
charge_diff = {}
with open(args.charge_file) as f:
    next(f)  # skip header line
    for line in f:
        atom_name, charge = line.split()
        charge_diff[atom_name] = float(charge)

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
obConversion.WriteFile(mol, output_file_name)
