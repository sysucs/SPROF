from dataloader import *
from model import *
import time
import os
from logger import Logger
import argparse

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
parser = argparse.ArgumentParser()
parser.add_argument('--learning_rate', type=float, default=0.0005, help='The learning rate of ADAM optimization.')
parser.add_argument('--maximum_epoch', type=int, default=60, help='The maximum epoch of training')
parser.add_argument('--sequential_features', type=str, default='input/train/sequential_features', help='The full path of sequential features of training data.')
parser.add_argument('--pairwise_features', type=str, default='input/train/pairwise_features', help='The full path of pairwise features of training data.')
parser.add_argument('--target_output', type=str, default='target/train', help='The full path of the target outputs.')
parser.add_argument('--train_list', type=str, default='train_list', help='The full path of the train list.')
parser.add_argument('--models_name', type=str, default='models', help='The name of models.')

config = parser.parse_args()
if  __name__ == '__main__':
    myname = config.models_name
    if (os.path.exists(myname) == False):
        os.makedirs(myname)
    torch.backends.cudnn.benchmark = True
    net = SPROF(ResidualBlock).to(device)
    optimizer = torch.optim.Adam(net.parameters(), lr=config.learning_rate)  # optimize all model's parameters
    loss_func = nn.CrossEntropyLoss().to(device)
    data_loader = get_loader(config.sequential_features, config.pairwise_features, config.target_output,config.train_list, batch_size=1, shuffle=True, num_workers=0)
    logger = Logger(myname) # create a log file to record the training
    s = 0
    for epoch in range(config.maximum_epoch):
        shortMean = []
        mediumMean = []
        longMean = []
        j = 0
        for i, (train1d, train2d, targetdata,name) in enumerate(data_loader):
            if(train2d.size(3)<600 and train2d.size(3)>=100):# only proteins with 100<=length<=600 are used for training
                j = i
                start = time.clock()
                train1d = train1d.to(device)
                train2d = train2d.to(device)
                targetdata = targetdata.to(device)
                output = net(train1d, train2d)  # mdoel output
                output = output.to(device)
                loss = loss_func(output, targetdata)  # cross entropy loss
                optimizer.zero_grad()  # clear gradients for this training step
                loss.backward()  # backpropagation, compute gradients
                optimizer.step()  # apply gradients
                softm = torch.nn.Softmax(dim = 0)
                score = softm(output[0])
                scoreMax = torch.max(score,0)[1]
                acc = float(sum(scoreMax == targetdata[0]))/float(len(targetdata[0]))# accuray calc
                print('acc :%.2f\t' % acc)
                print('Epoch: ', epoch, '| train loss: %.4f' % loss.data, '| time cost:', time.clock()-start)
                info = {'loss': loss.item(), 'acc': acc}
                for tag, value in info.items():
                    logger.scalar_summary(tag, value, s + i + 1)# log file
        torch.save(net.state_dict(), os.path.join(myname, myname+'-{}.ckpt'.format(epoch + 1)))# save model
        s+=j