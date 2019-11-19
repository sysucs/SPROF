import os
import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--preprocess_list', type=str, required=True, help='the path of a preprocess pdb list')
    config = parser.parse_args()

    with open(config.preprocess_list) as f:
        nameList=f.readlines()
    for name in nameList:
        print(name)
        cmd1 = f'./raw_feature_generate/caltheta ./raw_pdbs/{name} > ./raw_features/{name}.t'
        cmd2 = f'./raw_feature_generate/calphipsiomega ./raw_pdbs/{name} > ./raw_features/{name}.om'
        cmd3 = f'./raw_feature_generate/dfire_rotamer ./raw_pdbs/{name} > ./raw_features/{name}.en'
        cmd4 = f'dssp -i ./raw_pdbs/{name} -o ./raw_features/{name}.d'
        cmd5 = f'./raw_feature_generate/getdssp ./raw_features/{name}.d > ./raw_features/{name}.dssp'
        cmd6 = f'./process_pdb.sh {name}'
        cmd = f'{cmd1} && {cmd2} && {cmd3} && {cmd4} && {cmd5} && {cmd6}'
        os.system(cmd)