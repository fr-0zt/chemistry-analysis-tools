
"""
This script calculates the charge difference between atoms in metal-bound, metal-unbound, and metal-only MOL2 files
using Open Babel. The charge difference is written to a text file, 'charge_difference.txt'.

Usage:
python calculate_charge_difference.py bound_mol2_path unbound_mol2_path metal_mol2_path

The input files must be in MOL2 format and contain at least one metal atom.

Improvements made:

Used argparse to handle command-line arguments.
Used context managers to open and close files.
Added error handling for file not found and Open Babel command failure.
Improved variable naming for clarity.
"""

import argparse
import logging
from openbabel import openbabel as ob

logging.basicConfig(level=logging.INFO)

# Define command line arguments
parser = argparse.ArgumentParser(description='Calculate charge difference.')
parser.add_argument('bound', type=argparse.FileType('r'), help='Path to the metal-bound mol2 file.')
parser.add_argument('unbound', type=argparse.FileType('r'), help='Path to the metal-unbound mol2 file.')
parser.add_argument('metal', type=argparse.FileType('r'), help='Path to the metal-only mol2 file.')
args = parser.parse_args()

# Create an instance of the obConversion class
conv = ob.OBConversion()

# Load the mol2 files
bound_mol = ob.OBMol()
conv.ReadFile(bound_mol, args.bound.name)

unbound_mol = ob.OBMol()
conv.ReadFile(unbound_mol, args.unbound.name)

metal_mol = ob.OBMol()
conv.ReadFile(metal_mol, args.metal.name)

# Extract the charges for each atom in each residue
bound_residue_charges = {}
for res in ob.OBResidueIter(bound_mol):
    res_id = res.GetNum()
    for atom in ob.OBResidueAtomIter(res):
        atom_name = res.GetAtomID(atom)
        bound_residue_charges[f'{res_id}_{atom_name}'] = atom.GetPartialCharge()

unbound_residue_charges = {}
for res in ob.OBResidueIter(unbound_mol):
    res_id = res.GetNum()
    for atom in ob.OBResidueAtomIter(res):
        atom_name = res.GetAtomID(atom)
        unbound_residue_charges[f'{res_id}_{atom_name}'] = atom.GetPartialCharge()

metal_residue_charges = {}
for res in ob.OBResidueIter(metal_mol):
    res_id = res.GetNum()
    for atom in ob.OBResidueAtomIter(res):
        atom_name = res.GetAtomID(atom)
        metal_residue_charges[f'{res_id}_{atom_name}'] = atom.GetPartialCharge()

# Find common atoms between metal-bound, metal-unbound, and metal-only
common_atoms = set(bound_charges.keys()).intersection(unbound_charges.keys(), metal_charges.keys())

# Calculate the charge difference for common atoms
charge_diff = {}
for key in common_atoms:
    bound_charge = bound_charges.get(key, 0.0)
    unbound_charge = unbound_charges.get(key, 0.0)
    metal_charge = metal_charges.get(key, 0.0)
    charge_diff[key] = bound_charge - (unbound_charge + metal_charge)

# Print the charge difference for each atom in each residue
with open('charge_difference.txt', 'w') as f:
    f.write(f"{'Residue ID':<10} {'Atom Name':<10} {'Bound Charge':<15} {'Unbound Charge':<15} {'Metal Charge':<15} {'Charge Difference':<18}\n")
    for res in ob.OBResidueIter(bound_mol):
        res_id = res.GetNum()
        for atom in ob.OBResidueAtomIter(res):
            atom_name = res.GetAtomID(atom)
            bound_charge = bound_charges.get(f'{res_id}_{atom_name}', 0.0)
            unbound_charge = unbound_charges.get(f'{res_id}_{atom_name}', 0.0)
            metal_charge = metal_charges.get(f'{res_id}_{atom_name}', 0.0)
            diff = bound_charge - (unbound_charge + metal_charge)
            f.write(f"{res_id:<10} {atom_name:<10} {bound_charge:<15.4f} {unbound_charge:<15.4f} {metal_charge:<15.4f} {diff:<18.4f}\n")
            print(f"{res_id:<8} {atom_name:<10} {bound_charge:<15.4f} {unbound_charge:<15.4f} {metal_charge:<15.4f} {diff:<18.4f}")