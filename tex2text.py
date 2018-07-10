import argparse


def _parse_args():
    """
    Parses input and output file parameters from command line arguments, provides help documentation and error handling
    for missing arguments.

    Returns
    -------
    input : str
        Path to input file
    output : str
        Path to output file
    """
    parser = argparse.ArgumentParser(description='Specify input and output file.')
    parser.add_argument('input', help='Input file')
    parser.add_argument('output', help='Output file')

    args = parser.parse_args()

    return args.input, args.output


if __name__ == '__main__':
    infile, outfile = _parse_args()
