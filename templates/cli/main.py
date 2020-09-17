#!/usr/bin/env python
"""
This is the template for a script file.
Please change this docstring to reflect
realities.
"""
import argparse
import logging
import os
import sys
import time

from squirro_client import SquirroClient

# Script version. It's recommended to increment this with every change, to make
# debugging easier.
VERSION = '0.9.0'


# Set up logging.
log = logging.getLogger('{0}[{1}]'.format(os.path.basename(sys.argv[0]),
                                          os.getpid()))


def run():
    """Main entry point run by __main__ below. No need to change this usually.
    """
    args = parse_args()
    setup_logging(args)

    log.info('Starting process (version %s).', VERSION)
    log.debug('Arguments: %r', args)

    squirro_client = get_clients(args)

    # run the application
    try:
        main(args, squirro_client)
    except Exception:
        log.exception('Processing error')


def main(args, squirro_client=None):
    """
    The main method. Any exceptions are caught outside of this method and will
    be handled.

    squirro_client is passed in from the args provided to the script
    """

    log.warn('This method has been intentionally left almost blank.')

    raise Exception('Testing exception handling')


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('--verbose', '-v', action='count',
                        help='Show additional information.')
    parser.add_argument('--cluster', required=False,
                        help='Squirro cluster URL')
    parser.add_argument('--token', required=False,
                        help='Squirro user token')
    parser.add_argument('--project-id', required=False,
                        help='Squirro project ID')
    parser.add_argument('--log-file', dest='log_file',
                        help='Log file on disk.')

    return parser.parse_args()


def setup_logging(args):
    """Set up logging based on the command line options.
    """
    # Set up logging
    fmt = '%(asctime)s %(name)s %(levelname)-8s %(message)s'
    if args.verbose == 1:
        level = logging.INFO
        logging.getLogger(
            'requests.packages.urllib3.connectionpool').setLevel(logging.WARN)
    elif args.verbose >= 2:
        level = logging.DEBUG
    else:
        # default value
        level = logging.WARN
        logging.getLogger(
            'requests.packages.urllib3.connectionpool').setLevel(logging.WARN)

    # configure the logging system
    if args.log_file:
        out_dir = os.path.dirname(args.log_file)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)
        logging.basicConfig(
            filename=args.log_file, filemode='a', level=level, format=fmt)
    else:
        logging.basicConfig(level=level, format=fmt)

    # Log time in UTC
    logging.Formatter.converter = time.gmtime


def get_clients(args, source_name=None):
    """"Return Squirro clients.

    Source name can be provided as a parameter, when one script needs multiple
    different uploaders.
    """

    if not args.cluster or not args.token:
        log.info('Cluster or Token is missing, no '
                 'SquirroClient will be available')
        return None

    client = SquirroClient(None, None, cluster=args.cluster)
    client.authenticate(refresh_token=args.token)

    return client


# This is run if this script is executed, rather than imported.
if __name__ == '__main__':
    run()
