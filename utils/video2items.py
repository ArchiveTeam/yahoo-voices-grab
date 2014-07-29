'''Batch article video URLs to tracker items.'''
import argparse


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('file')
    args = arg_parser.parse_args()

    with open(args.file) as f:
        for line in f:
            name = line.strip().replace('http://voices.yahoo.com/', '').replace('.html', '')
            assert ',' not in name

            if 'video/' in name:
                print('video:' + name.replace('video/', ''))

if __name__ == '__main__':
    main()
