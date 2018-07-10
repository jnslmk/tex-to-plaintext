import argparse
import re

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


def _clean_line(line):
    """
    Fixes linebreaks between lines and removes TeX commands from text.

    Parameters
    ----------
    line : str
        Line of TeX file

    Returns
    -------
    line : str
        Processed line
    """
    if line == '\n':
        return '\n\n'
    if line.startswith('%'):
        return ''

    if line.endswith('\n'):
        line = line[:-1]

    if line.startswith(' '):
        line = line[1:]

    if not line.endswith(' '):
        line += ' '

    rgx_header = r'(?:(?:chapter)|(?:section)|(?:subsection)){(?:\w| )+}'
    match = re.match(rgx_header, line)
    if match is not None:
        line = match.group(1) + '\n'

    return line


def _convert_to_text(path_in, path_out):
    """
    Reads contents of infile, scraps TeX-specific linebreaks and functions and stores the result in outfile.

    Parameters
    ----------
    path_in : str
        Path to input file
    path_out : str
        Path to output file
    """
    out = ''
    with open(path_in, 'r') as f:
        for line in f:
            line = _clean_line(line)
            out += line
    with open(path_out, 'w') as f:
        f.write(out)


if __name__ == '__main__':
    infile, outfile = _parse_args()
    _convert_to_text(infile, outfile)
