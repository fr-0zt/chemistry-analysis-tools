# chemistry-analysis-tools

**Charge Difference Calculator**

This script reads the partial charges from two mol2 files representing bound and unbound structures, respectively. It then calculates the charge differences between the two structures and saves the results in a tab-delimited file. The output file contains the atom indices and their corresponding charge differences.

**Usage**
To run the script, call it from the command line with the following arguments:

python charge_difference_calculator.py bound.mol2 unbound.mol2 -o output.txt

The script takes three command-line arguments:

bound_mol2: The filename of the mol2 file for the bound structure
unbound_mol2: The filename of the mol2 file for the unbound structure
output (optional): The name of the output file (default: output.dat)

**Dependencies**
The script requires the following packages:

_argparse_
