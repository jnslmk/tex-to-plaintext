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


class LineCeaner:
    """Line cleaning class"""

    def __init__(self):
        self.f_newline = False

    def clean_line(self, line):
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
        # Insert empty newlines add end of paragraphs
        if line == '\n':
            # Prevent insertion of duplicate newlines
            if self.f_newline:
                return ''
            else:
                self.f_newline = True
                return '\n\n'
        # Remove comments
        elif line.startswith('%'):
            return ''
        else:
            self.f_newline = False

        # Remove linebreaks within paragraphs
        if line.endswith('\n'):
            line = line[:-1]

        # Remove whitespace from begin of line
        if line.startswith(' '):
            line = line[1:]

        # Add whitespace at end of line for lines within paragraphs
        if not line.endswith(' '):
            line += ' '

        # Remove header commands and insert newline after header
        rgx_header = r'(?:(?:chapter)|(?:section)|(?:subsection)){((?:\w| )+)}'
        match = re.search(rgx_header, line)
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
    lc = LineCeaner()
    with open(path_in, 'r') as f:
        for line in f:
            line = lc.clean_line(line)
            out += line
    with open(path_out, 'w') as f:
        f.write(out)


if __name__ == '__main__':
    infile, outfile = _parse_args()
    _convert_to_text(infile, outfile)
