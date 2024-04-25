import os
import sys
from pstats import Stats

if __name__ == '__main__':
    filenames = [f for f in os.listdir('./prof') if f.endswith('.prof')]

    for filename in filenames:
        my_stat = Stats(f'./prof/{filename}', stream=sys.stdout)
        my_stat.print_stats()
