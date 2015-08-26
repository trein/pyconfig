import logging
import argparse
import loader


def main():
    parser = argparse.ArgumentParser(description='Python project workflow management')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='verbose output (default false)')
    parser.add_argument('mode', default='release', help='lifecycle step (default release)')
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=log_level, format=log_format)
    loader.setup_project(args)


if __name__ == '__main__':
    main()