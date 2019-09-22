#! /usr/bin/env python

import argparse


def create_argument_parser():
    parser = argparse.ArgumentParser(description='A sudoku generating/solving toolkit.')
    parser.add_argument('--generate', '-g', action='store_true', default=True)
    return parser


if __name__ == '__main__':
    parser = create_argument_parser()
    import IPython
    IPython.embed()
