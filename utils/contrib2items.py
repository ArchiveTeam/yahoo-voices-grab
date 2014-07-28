'''Batch contributor URLs to tracker items.'''
import argparse

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('file')
    args = arg_parser.parse_args()

    batch = set()

    with open(args.file) as f:
        for line in f:
            name = line.strip().replace('http://contributor.yahoo.com/user/', '').replace('.html', '')
            assert ',' not in name
            batch.add(name)

            if len(batch) >= 10:
                print('contrib:' + ','.join(sorted(batch)))
                batch.clear()
    
    if batch:
        print('contrib:' + ','.join(sorted(batch)))


if __name__ == '__main__':
    main()
