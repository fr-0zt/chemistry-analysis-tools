"""
This script reads the partial charges from two mol2 files representing bound and unbound structures, respectively. It then calculates the charge differences between the two structures and saves the results in a tab-delimited file. The output file contains the atom indices and their corresponding charge differences.
The charge differences are calculated by subtracting the charges of atoms that are common to both bound and unbound structures. For the atoms that are not common, the charges of the bound and unbound structures are simply added and subtracted, respectively.
The script takes three command-line arguments: the filenames of the mol2 files for the bound and unbound structures, and the name of the output file. The output filename is optional and defaults to "output.dat".

The script uses argparse to parse the command-line arguments, and defines three functions:
- read_mol2_charges: Reads the partial charges from a mol2 file and returns them as a dictionary with the atom indices as keys and the charges as values.
- subtract_charges: Subtracts the charges of atoms that are common to both the bound and unbound structures and returns the result as a dictionary with the atom indices as keys and the charge differences as values.
- main: Orchestrates the overall execution of the script by reading the mol2 files, calculating the charge differences, and writing the results to an output file.

To run the script, call it from the command line with the following arguments:
- bound_mol2: The filename of the mol2 file for the bound structure
- unbound_mol2: The filename of the mol2 file for the unbound structure
- output (optional): The name of the output file (default: output.dat)

For example: python script.py bound.mol2 unbound.mol2 -o output.txt
"""


import argparse
from typing import Dict


def read_mol2_charges(filename: str) -> Dict[int, float]:
    """
    Reads the partial charges from a mol2 file and returns them as a dictionary
    with the atom indices as keys and the charges as values.

    Args:
        filename (str): The name of the mol2 file to read charges from.

    Returns:
        charges (dict): A dictionary with the atom indices as keys and the charges as
            values.
    """
    charges = {}
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith('@<TRIPOS>ATOM'):
                for j in range(i+1, len(lines)):
                    fields = lines[j].split()
                    if len(fields) < 9:
                        break
                    index = int(fields[0])
                    charge = float(fields[8])
                    charges[index] = charge
                break
    return charges


def subtract_charges(bound_charges: Dict[int, float], unbound_charges: Dict[int, float]) -> Dict[int, float]:
    """
    Subtracts the charges of atoms that are common to both the bound and unbound
    structures and returns the result as a dictionary with the atom indices as keys
    and the charge differences as values.

    Args:
        bound_charges (dict): A dictionary of the partial charges of the bound structure
        unbound_charges (dict): A dictionary of the partial charges of the unbound structure

    Returns:
        charge_diffs (dict): A dictionary with the atom indices as keys and the charge
            differences as values, sorted by atom index.
    """
    # Get the set of common atom indices
    common_atoms = set(bound_charges.keys()) & set(unbound_charges.keys())

    # Calculate the charge differences for common atoms
    charge_diffs = {index: bound_charges[index] - unbound_charges[index] for index in common_atoms}

    # Add the remaining atoms
    charge_diffs.update({index: bound_charges[index] for index in bound_charges if index not in common_atoms})
    charge_diffs.update({index: -unbound_charges[index] for index in unbound_charges if index not in common_atoms})

    # Sort the result by atom index
    charge_diffs = dict(sorted(charge_diffs.items()))

    return charge_diffs


def main():
    parser = argparse.ArgumentParser(description='Calculate charge differences between bound and unbound structures.')
    parser.add_argument('bound_mol2', help='The filename of the mol2 file for the bound structure')
    parser.add_argument('unbound_mol2', help='The filename of the mol2 file for the unbound structure')
    parser.add_argument('-o', '--output', help='The name of the output file (default: output.dat)', default='output.dat')
    args = parser.parse_args()

    bound_charges = read_mol2_charges(args.bound_mol2)
    unbound_charges = read_mol2_charges(args.unbound_mol2)

    charge_diffs = subtract_charges(bound_charges, unbound_charges)

    with open(args.output, 'w') as f:
        f.write('atom_index\tcharge_diff\n')
        for index, diff in charge_diffs.items():
            f.write(f'{index}\t{diff}\n')

if __name__ == '__main__':
    main()