# chemistry-analysis-tools

**Charge Difference Calculator**

This script reads the partial charges from two mol2 files representing bound and unbound structures, respectively. It then calculates the charge differences between the two structures and saves the results in a tab-delimited file. The output file contains the atom indices and their corresponding charge differences.

**Usage:**

python charge_difference_calculator.py bound.mol2 unbound.mol2 -o output.txt

bound_mol2: The filename of the mol2 file for the bound structure
unbound_mol2: The filename of the mol2 file for the unbound structure
output (optional): The name of the output file (default: output.dat)

**Dependencies**
The script requires the following packages:

_argparse_

--------------------------------------------------------------------------------------------------------------------------------

**Mol2 Charge Modifier**

This Python script modifies charge values in Mol2 files based on a charge difference data table stored in a .dat file. The modified Mol2 files are saved in the same directory as the original files with "_modified" appended to the filename.

**Usage:**

python mol2_charge_modifier.py --dat <charge_diff.dat> --mol2dir <mol2_directory>

--dat <charge_diff.dat>: Path to the charge difference data file in .dat format.
--mol2dir <mol2_directory>: Path to the directory containing the Mol2 files to modify.

**Example usage:**
python mol2_charge_modifier.py --dat charge_diff.dat --mol2dir Mol2_files/

**Dependencies:**

This script requires the following packages:

_argparse_
_os_
