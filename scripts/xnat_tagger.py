#!/usr/bin/env python3

import os
import sys
import json
import yaml
import yaxil
import logging
import argparse as ap
import xnattagger.io
from xnattagger import Tagger

logger = logging.getLogger(os.path.basename(__file__))
logging.basicConfig(level=logging.INFO)

def main():
    # Parse command line arguments
    parser = ap.ArgumentParser()
    parser.add_argument('-a', '--alias', default='ssbc',
        help='XNAT alias')  # Set default value and provide help text for alias argument
    parser.add_argument('--project',
        help='XNAT project')  # Provide help text for project argument
    parser.add_argument('-c', '--cache', action='store_true',
        help='Speed up development by caching yaxil.scans output')  # Provide help text for cache argument
    parser.add_argument('-o', '--output-file',
        help='Output summary of updates')  # Provide help text for output-file argument
    parser.add_argument('--dry-run', action='store_true',
        help='Do not execute updates')  # Provide help text for dry-run argument
    parser.add_argument('--confirm', action='store_true',
        help='Prompt user to confirm every update')  # Provide help text for confirm argument
    parser.add_argument('--filters', required=True,
        help='Filters configuration output_file') 
    parser.add_argument('--target', choices=['t1', 't2', 'dwi', 'all'], required=True, type=str.lower) # Require --target argument
    parser.add_argument('session')  # Require session argument
    args = parser.parse_args()

    content = xnattagger.io.get(args.filters)
    filters = yaml.load(content, Loader=yaml.SafeLoader)

    auth = yaxil.auth(args.alias)

    tagger = Tagger(auth, filters, args.target, args.session)
    tagger.generate_updates()

    if args.output_file:
        with open(args.output_file, 'w') as fo:
            js = json.dumps(tagger.updates, indent=2)
            fo.write(js)
    if not args.dry_run:
        tagger.apply_updates()

if __name__ == '__main__':
    main()


