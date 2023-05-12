"""
This script uses the Open Babel tool to format a MOL2 file. Given an input MOL2 file, it generates a formatted MOL2
file by executing the "obabel" command using subprocess.

Usage:
    python format_mol2.py input_file_path [-o output_file_path]

If the optional argument "-o" or "--output_file_path" is not provided, the script will generate a default output
file with the same name as the input file, but with the suffix "_formatted.mol2" added.

Improvements made:
- Used context managers to open and close files.
- Added error handling for file not found and Open Babel command failure.
- Improved variable naming for clarity.
"""

import os
import argparse
import subprocess

# Define the function to format the MOL2 file
def format_mol2(input_file_path, output_file_path=None):
    # If no output file is specified, construct default output file path
    if output_file_path is None:
        # Get the base name of the input file (without extension)
        file_name = os.path.splitext(os.path.basename(input_file_path))[0]
        # Construct the default output file path by adding "_formatted.mol2" to the base name
        output_file_path = f"{file_name}_formatted.mol2"

    # Construct the Open Babel command
    obabel_cmd = ["obabel", "-imol2", input_file_path, "-omol2", "-O", output_file_path]
    # Run the command using subprocess
    try:
        subprocess.run(obabel_cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"Error: Failed to format MOL2 file {input_file_path}.")
        return False
    return True

# Define the main block of the script
if __name__ == "__main__":
    # Define the command-line arguments using argparse
    parser = argparse.ArgumentParser(description="Format a MOL2 file using Open Babel")
    # Define the input file path as a required positional argument
    parser.add_argument("input_file_path", help="Input MOL2 file path")
    # Define the output file path as an optional argument with a default value
    parser.add_argument("-o", "--output_file_path", help="Output file path for formatted MOL2 file")
    # Parse the command-line arguments
    args = parser.parse_args()

    # If no output file is specified, construct default output file path
    if args.output_file_path is None:
        # Get the base name of the input file (without extension)
        file_name = os.path.splitext(os.path.basename(args.input_file_path))[0]
        # Construct the default output file path by adding "_formatted.mol2" to the base name
        args.output_file_path = f"{file_name}_formatted.mol2"

    # Use context managers to open and close files
    try:
        with open(args.input_file_path, "r") as input_file:
            with open(args.output_file_path, "w") as output_file:
                # Format the input MOL2 file using the format_mol2 function
                if not format_mol2(input_file, output_file):
                    raise Exception("Failed to format MOL2 file.")
    except FileNotFoundError:
        print(f"Error: File {args.input_file_path} not found.")
    except Exception as e:
        print(f"Error: {e}")