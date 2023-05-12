import argparse
from openbabel import openbabel as ob

# Define command line arguments
parser = argparse.ArgumentParser(description='Calculate charge difference.')
parser.add_argument('bound', help='Path to the metal-bound mol2 file.')
parser.add_argument('unbound', help='Path to the metal-unbound mol2 file.')
parser.add_argument('metal', help='Path to the metal-only mol2 file.')
args = parser.parse_args()

# Create an instance of the obConversion class
conv = ob.OBConversion()

# Load the mol2 files
bound_mol = ob.OBMol()
conv.ReadFile(bound_mol, args.bound)

unbound_mol = ob.OBMol()
conv.ReadFile(unbound_mol, args.unbound)

metal_mol = ob.OBMol()
conv.ReadFile(metal_mol, args.metal)

# Extract the charges for each atom in each residue
bound_charges = {}
for res in ob.OBResidueIter(bound_mol):
    res_id = res.GetNum()
    for atom in ob.OBResidueAtomIter(res):
        atom_name = res.GetAtomID(atom)
        bound_charges[f'{res_id}_{atom_name}'] = atom.GetPartialCharge()

unbound_charges = {}
for res in ob.OBResidueIter(unbound_mol):
    res_id = res.GetNum()
    for atom in ob.OBResidueAtomIter(res):
        atom_name = res.GetAtomID(atom)
        unbound_charges[f'{res_id}_{atom_name}'] = atom.GetPartialCharge()

metal_charges = {}
for res in ob.OBResidueIter(metal_mol):
    res_id = res.GetNum()
    for atom in ob.OBResidueAtomIter(res):
        atom_name = res.GetAtomID(atom)
        metal_charges[f'{res_id}_{atom_name}'] = atom.GetPartialCharge()

# Find common atoms between metal-bound, metal-unbound, and metal-only
common_atoms = set(bound_charges.keys()) & set(unbound_charges.keys()) | set(bound_charges.keys()) & set(metal_charges.keys()) | set(unbound_charges.keys()) & set(metal_charges.keys())

# Calculate the charge difference for common atoms
charge_diff = {}
for key in common_atoms:
    bound_charge = bound_charges.get(key, 0.0)
    unbound_charge = unbound_charges.get(key, 0.0)
    metal_charge = metal_charges.get(key, 0.0)
    charge_diff[key] = bound_charge - (unbound_charge + metal_charge)

# Print the charge difference for each atom in each residue
with open('charge_difference.txt', 'w') as f:
    f.write(f"{'Atom Name':<10} {'Charge Difference':<18}\n")
    for res in ob.OBResidueIter(bound_mol):
        res_id = res.GetNum()
        for atom in ob.OBResidueAtomIter(res):
            atom_name = res.GetAtomID(atom)
            bound_charge = bound_charges.get(f'{res_id}_{atom_name}', 0.0)
            unbound_charge = unbound_charges.get(f'{res_id}_{atom_name}', 0.0)
            metal_charge = metal_charges.get(f'{res_id}_{atom_name}', 0.0)
            diff = bound_charge - (unbound_charge + metal_charge)
            f.write(f"{atom_name:<10} {diff:<18.4f}\n")
            print(f"{res_id:<8} {atom_name:<10} {bound_charge:<15.4f} {unbound_charge:<15.4f} {metal_charge:<15.4f} {diff:<18.4f}")


# Print the charge difference for each common atom
#with open('charge_difference.txt', 'w') as f:
#    f.write(f"{'Atom Name':<10} {'Charge Difference':<18}\n")
#    for key in sorted(common_atoms, key=lambda x: x.split('_')[0]):
#        residue_num, atom_name = key.split('_')
#        diff = charge_diff.get(key, 0.0)
#        f.write(f"{atom_name:<10} {diff:<18.4f}\n")
#        print(f"{residue_num:<8} {atom_name:<10} {bound_charge:<15.4f} {unbound_charge:<15.4f} {metal_charge:<15.4f} {diff:<18.4f}")