import subprocess
import argparse
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(description="This script will compute ani using sourmash",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("g1", type=str, help="The full path to the first genome")
    parser.add_argument("g2", type=str, help="The full path to the second genome")
    parser.add_argument("ksize", type=int, help="k size", default=21)
    parser.add_argument("scaled", type=int, help="Scaled", default=1000)
    parser.add_argument("--seed", type=int, help="Random seed", default=0)
    args = parser.parse_args()
    return args.g1, args.g2, args.seed, args.ksize, args.scaled

def compute_ani_by_sourmash(genome1, genome2, seed, k, scaled):
    cmd = 'sourmash compute -k ' + str(k) + ' --scaled ' + str(scaled) + ' --seed ' + str(seed) + ' -f -o sketch1 ' + genome1
    args = cmd.split(' ')
    subprocess.call(args, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    cmd = 'sourmash compute -k ' + str(k) + ' --scaled ' + str(scaled) + ' --seed ' + str(seed) + ' -f -o sketch2 ' + genome2
    args = cmd.split(' ')
    subprocess.call(args, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    cmd = 'sourmash compare -k ' + str(k) + ' --containment --estimate-ani sketch1 sketch2 -o matrix.cmp'
    args = cmd.split(' ')
    subprocess.call(args, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    mat = np.load('matrix.cmp')
    return mat[0,1], mat[1,0]

def main():
    g1, g2, seed, k, scaled = parse_args()
    ani = compute_ani_by_sourmash(g1, g2, seed, k, scaled)
    print('ANI is: ' + str(ani))

if __name__ == '__main__':
    main()

# sourmash compute -k 21 --scaled 1000 --seed 0 -f -o sketch_ecoli ecoli.fasta
# sourmash compute -k 21 --scaled 1000 --seed 0 -f -o sketch_ecoli_mutated ecoli_mutated.fasta
# sourmash compare -k 21 --containment --estimate-ani sketch_ecoli sketch_ecoli_mutated -o matrix.cmp
# np.load('matrix.cmp')
