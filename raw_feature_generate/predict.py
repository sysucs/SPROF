import torch
import numpy as np
import sys
from model import *

def main(name):
    device = torch.device('cpu')
    feature1D = np.load('/home/cs/SPROF/run/numpydata/feature1D/' + name+'.npy')
    featurePair = np.load('/home/cs/SPROF/run/numpydata/feature2D/' + name+'.npy')
    label2D = np.load('/home/cs/SPROF/run/numpydata/target/' + name+'.npy')
    feature1d = torch.FloatTensor(np.expand_dims(feature1D, axis=0)).to(device)
    feature2D = np.expand_dims(featurePair, axis=0)
    feature2d = torch.FloatTensor(np.expand_dims(feature2D, axis=0)).to(device)
    targetdata = torch.LongTensor(np.expand_dims(label2D, axis=0)).to(device)

    model = SPROF(ResidualBlock).eval()
    model = model.to(device)
    model.load_state_dict(torch.load('/home/cs/SPROF/run/models/models_25.ckpt',map_location=torch.device('cpu')))

    output=model(feature1d,feature2d)
    softm = torch.nn.Softmax(dim=0)
    score = softm(output[0])
    f=open('outputs/'+name+'.pred','w')

    maplist2=['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V']
    f.write('Consensus sequence is\n')
    for i in range(len(targetdata[0])):
        f.write(maplist2[int(targetdata[0,i])])
    f.write('\n')
    f.write('Probility (in %) for each amino acid type in each position of given backbone\n')
    f.write('\t')
    f.write('A\t')
    f.write('C\t')
    f.write('D\t')
    f.write('E\t')
    f.write('F\t')
    f.write('G\t')
    f.write('H\t')
    f.write('I\t')
    f.write('K\t')
    f.write('L\t')
    f.write('M\t')
    f.write('N\t')
    f.write('P\t')
    f.write('Q\t')
    f.write('R\t')
    f.write('S\t')
    f.write('T\t')
    f.write('V\t')
    f.write('W\t')
    f.write('Y\t')
    f.write('\n')
    maplist=[0,4,3,6,13,7,8,9,11,10,12,2,14,5,1,15,16,19,17,18]

    for i in range(len(score[0])):
        f.write(f'{i+1}\t')
        for j in range(20):
            f.write('%.1f\t'%(100*score[maplist[j],i]))
        if i !=len(score[0])-1:
            f.write('\n')


    f.close()



if __name__ == '__main__':
    name=sys.argv[1]
    main(name)
