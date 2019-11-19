import torch
import torch.nn as nn

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
FEATURE = 1


def conv3x3(in_channels, out_channels, stride=1):
    return nn.Conv2d(in_channels, out_channels, kernel_size=3,
                     stride=stride, padding=1, bias=False)


def conv5x5(in_channels, out_channels, stride=1):
    return nn.Conv2d(in_channels, out_channels, kernel_size=5,
                     stride=stride, padding=2, bias=False)


def conv1x1(in_channels, out_channels, stride=1):
    return nn.Conv2d(in_channels, out_channels, kernel_size=1,
                     stride=stride, padding=0, bias=False)


# Residual block
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super(ResidualBlock, self).__init__()
        self.conv1 = conv5x5(in_channels, out_channels, stride)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.elu = nn.ELU(inplace=True)
        self.conv2 = conv3x3(out_channels, out_channels)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.downsample = downsample

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.elu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        if self.downsample:
            residual = self.downsample(x)
        out += residual
        out = self.elu(out)
        return out

class SPROF(nn.Module):
    def __init__(self, block):
        super(SPROF, self).__init__()
        self.in_channels = 8
        self.conv = conv3x3(FEATURE, 8)
        self.bn = nn.BatchNorm2d(8)
        self.bn2 = nn.BatchNorm1d(32)
        self.bn3 = nn.BatchNorm1d(64)
        self.bn4 = nn.BatchNorm1d(128)
        self.elu = nn.ELU(inplace=False)
        self.layer1 = self.make_layer(block, 16, 10)
        self.layer2 = self.make_layer(block, 32, 10)
        self.layer3 = self.make_layer(block, 64, 10)
        self.lstm = nn.LSTM(214, 64, 3, batch_first=True, bidirectional=True)
        self.fc1 = nn.Linear(64, 50)
        self.fc11 = nn.Linear(50, 40)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 20)
        self.fc4 = nn.Linear(64, 1)
        self.dropout1d = torch.nn.Dropout(p=0.5, inplace=False)
        self.dropout2d = torch.nn.Dropout2d(p=0.5, inplace=False)

    def make_layer(self, block, out_channels, blocks, stride=1):
        downsample = None
        if (stride != 1) or (self.in_channels != out_channels):
            downsample = nn.Sequential(
                conv3x3(self.in_channels, out_channels, stride=stride),
                nn.BatchNorm2d(out_channels))
        layers = []
        layers.append(block(self.in_channels, out_channels, stride, downsample))
        self.in_channels = out_channels
        for i in range(1, blocks):
            layers.append(block(out_channels, out_channels))
        return nn.Sequential(*layers)

    def forward(self, x1, x2):
        out = self.conv(x2)
        out1 = self.bn(out)
        out2 = self.elu(out1)
        out3 = self.layer1(out2)
        out3 = self.layer2(out3)
        out3 = self.layer3(out3)
        # out4 = self.layer4(out3)

        out4 = self.fc1(out3.permute(0, 2, 3, 1)).permute(0, 3, 1, 2)
        out5 = self.elu(out4)
        out7 = self.fc11(out5.permute(0, 2, 3, 1)).permute(0, 3, 1, 2)
        soft = torch.nn.Softmax(dim=2)
        out8 = soft(out7)
        out9 = out8.permute(0, 3, 1, 2)
        out33 = out3.permute(0, 3, 2, 1)
        out10 = out9 @ out33
        out11 = out10.permute(0, 3, 2, 1)

        o1 = torch.sum(out11, 2) / 40
        x = torch.cat([o1, x1], 1)

        h0 = torch.zeros(6, x.permute(0, 2, 1).size(0), 64).to(device)  # 2 for bidirection
        c0 = torch.zeros(6, x.permute(0, 2, 1).size(0), 64).to(device)
        put, _ = self.lstm(x.permute(0, 2, 1), (h0, c0))

        put4 = put.permute(0, 2, 1)

        put4 = self.fc2(put4.permute(0, 2, 1)).permute(0, 2, 1)
        put4 = self.elu(put4)
        put5 = self.dropout1d(put4)
        o = self.fc3(put5.permute(0, 2, 1)).permute(0, 2, 1)

        return o