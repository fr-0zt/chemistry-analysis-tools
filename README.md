**Chemistry Analysis Tools**

A collection of Python scripts for analyzing chemistry data.

**Scripts:**

The following scripts are currently available in this repository:

mol2_formatter.py: Python script that can be used to format a MOL2 file. A MOL2 file is a common file format for describing molecules and their properties. This script reads in a MOL2 file, removes any comments, and formats the molecule information in a consistent manner. The formatted MNOL2 file is then output to a new file.

mol2_charge_diff.py: Python script that can be used to calculate the difference between two sets of charges for a molecule. The script reads in two MOL2 files that contain the same molecule, but with different sets of charges. The charges for each molecule are extracted, and the difference between the charges for each atom is calculated. The results are output to a file.

mol2_partial_charge_modifer.py: Python script that can be used to modify the partial charges for a molecule. The script reads in a MOL2 file and a text file that contains the desired modifications to the charges. The modifications are specified as a list of atom indices and the corresponding partial charges. The script updates the charges in the MOL2 file according to the modifications, and outputs a new MOL2 file.


**Installation:**

To use these scripts, you will need to have Python installed on your computer. You can download Python from the official website: https://www.python.org/downloads/

After installing Python, you can clone this repository to your local machine using the following command:

git clone https://github.com/username/chemistry-analysis-tools.git

**Usage:**

To run any of the scripts, simply navigate to the directory where the script is located and run it using the python command. For example:

cd /path/to/chemistry-analysis-tools

_python mol2_formatter.py_


**License:**

This project is licensed under the MIT License - see the LICENSE file for details.
