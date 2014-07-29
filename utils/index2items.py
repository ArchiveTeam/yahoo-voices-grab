'''Batch index URLs to tracker items.'''
import argparse


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('file')
    args = arg_parser.parse_args()

    batch = set()

    category = True

    with open(args.file) as f:
        for line in f:
            name = line.strip().replace('http://voices.yahoo.com/', '').replace('.html', '')

            if not name:
                continue

            assert ',' not in name
            batch.add(name)

            if len(batch) >= 10 or ('?cat' not in name and category):
                if category:
                    print('cat:' + ','.join(sorted(batch)))
                else:
                    print('index:' + ','.join(sorted(batch)))

                batch.clear()

                if '?cat' not in name and category:
                    category = False

    if batch:
        print('index:' + ','.join(sorted(batch)))


if __name__ == '__main__':
    main()
