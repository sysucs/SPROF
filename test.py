from dataloader import *
from model import *
import argparse
import os

BATCHSIZE = 1
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# device = torch.device('cpu')
parser = argparse.ArgumentParser()
parser.add_argument('--sequential_features', type=str, default='input/casp_test/sequential_features', help='The full path of sequential features of test data.')
parser.add_argument('--pairwise_features', type=str, default='input/casp_test/pairwise_features', help='The full path of pairwise features of test data.')
parser.add_argument('--target_output', type=str, default='target/casp_test', help='The full path of the target outputs.')
parser.add_argument('--feature_list', type=str, default='casp_test_list', help='The full path of the test list.')
parser.add_argument('--models_path', type=str, default='models', help='path list of models.')
config = parser.parse_args()

if __name__ == '__main__':
    myname = config.models_path
    nameList=os.listdir(myname)#models' names

    for modelname in nameList:
        net = SPROF(ResidualBlock).eval()
        net = net.to(device)
        net.load_state_dict(torch.load(f'{config.models_path}/{modelname}'))
        data_loader = get_loader(config.sequential_features, config.pairwise_features, config.target_output,
                                 config.feature_list, batch_size=1, shuffle=False, num_workers=0)
        lll = []#result record
        f = open('sprofpred', 'w')#result record
        with torch.no_grad():
            for i, (test1d, test2d, targetdata, name) in enumerate(data_loader):
                test1d = test1d.to(device)
                test2d = test2d.to(device)
                targetdata = targetdata.to(device)
                output = net(test1d, test2d)  # model output
                output = output.to(device)
                softm = torch.nn.Softmax(dim=0)
                score = softm(output[0])
                scoreMax = torch.max(score, 0)[1]
                # print(name)
                # print(targetdata[0])
                # print(scoreMax)
                ac = float(torch.sum(scoreMax == targetdata[0])) / float(len(targetdata[0]))#accuracy calc
                print(ac)
                lll.append(ac)
                f.write(name[0] + ' ' + '%.3f' % ac + '\n')#result record
            lll = np.array(lll)
            np.save('sprof.npy', lll)#result record
    f.close()