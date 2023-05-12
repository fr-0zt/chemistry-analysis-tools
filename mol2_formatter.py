import os
import argparse
import subprocess

def format_mol2(input_file, output_file=None):
    # If no output file is specified, construct default output file path
    if output_file is None:
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{file_name}_formatted.mol2"

    # Construct Open Babel command
    cmd = ["obabel", "-imol2", input_file, "-omol2", "-O", output_file]
    subprocess.run(cmd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format a MOL2 file using Open Babel")
    parser.add_argument("input_file", help="Input MOL2 file path")
    parser.add_argument("-o", "--output_file", help="Output file path for formatted MOL2 file")
    args = parser.parse_args()

    # If no output file is specified, construct default output file path
    if args.output_file is None:
        file_name = os.path.splitext(os.path.basename(args.input_file))[0]
        args.output_file = f"{file_name}_formatted.mol2"

    # Format the input MOL2 file
    format_mol2(args.input_file, args.output_file)
