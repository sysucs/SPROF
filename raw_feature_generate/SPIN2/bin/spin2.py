#!/usr/bin/python2

import sys
import numpy as np
import spin2lib as spin2

# Check input arguments
if len(sys.argv) <> 4:
    print >> sys.stderr, "Usage: spin2.py positions.file fragments.file rotomers.file"
    sys.exit(1)



##############################################################################
# Load data
try:
    raw_positions = np.loadtxt(sys.argv[1])
except IOError:
    print >> sys.stderr, "Unable to load atom position data."
try:
    features_fragments = np.loadtxt(sys.argv[2])
except IOError:
    print >> sys.stderr, "Unable to load fragments data."
try:
    features_rotomers = np.loadtxt(sys.argv[3])
except IOError:
    print >> sys.stderr, "Unable to load rotomers data."
try:
    scale_data = np.loadtxt("/mnt/disk1/yang/sunzhe/spin/SPIN2/data/scale_data")
except IOError:
    print >> sys.stderr, "Unable to load scaling data."
try:
    NN_L1 = np.loadtxt("/mnt/disk1/yang/sunzhe/spin/SPIN2/data/nn_l1")
except IOError:
    print >> sys.stderr, "Unable to load layer 1 configuration."
try:
    NN_L2 = np.loadtxt("/mnt/disk1/yang/sunzhe/spin/SPIN2/data/nn_l2")
except IOError:
    print >> sys.stderr, "Unable to load layer 2 configuration."
try:
    NN_L3 = np.loadtxt("/mnt/disk1/yang/sunzhe/spin/SPIN2/data/nn_l3")
except IOError:
    print >> sys.stderr, "Unable to load layer 3 configuration."
try:
    NN_Lo = np.loadtxt("/mnt/disk1/yang/sunzhe/spin/SPIN2/data/nn_lo")
except IOError:
    print >> sys.stderr, "Unable to load output layer configuration."


# Check data lengths
if (features_fragments.shape[0] <> features_rotomers.shape[0]) or (4*features_fragments.shape[0] <> raw_positions.shape[0]) or (scale_data.shape[1] <> 190):
    print >> sys.stderr, "Number of entries in data files don't match."
    sys.exit(1)

# Sort positions array
raw_positions = raw_positions[np.lexsort((raw_positions[:,0],raw_positions[:,1])),]


##############################################################################
# Generate features
features_angles = spin2.gen_features_angles(raw_positions)
features_ca_num = spin2.gen_features_ca_count(raw_positions)
features_inter  = spin2.gen_features_inter(raw_positions)
features_intra  = spin2.gen_features_intra(raw_positions)


##############################################################################
# Combine and normalise features
input_features = np.concatenate((features_angles,features_ca_num,features_inter,features_intra,features_fragments,features_rotomers), axis=1)
input_features = input_features - np.expand_dims(scale_data[0,],0)
input_features = input_features / np.expand_dims(scale_data[1,],0)


##############################################################################
# Run network

nn_out_l1 = np.dot(np.concatenate((np.expand_dims(np.ones(input_features.shape[0]),1), input_features),axis=1), np.transpose(NN_L1))
nn_out_l1 = 1/(1+np.exp(-nn_out_l1))

nn_out_l2 = np.dot(np.concatenate((np.expand_dims(np.ones(nn_out_l1.shape[0]),1), nn_out_l1),axis=1), np.transpose(NN_L2))
nn_out_l2 = 1/(1+np.exp(-nn_out_l2))

nn_out_l3 = np.dot(np.concatenate((np.expand_dims(np.ones(nn_out_l2.shape[0]),1), nn_out_l2),axis=1), np.transpose(NN_L3))
nn_out_l3 = 1/(1+np.exp(-nn_out_l3))

nn_out = np.dot(np.concatenate((np.expand_dims(np.ones(nn_out_l3.shape[0]),1), nn_out_l3),axis=1), np.transpose(NN_Lo))
nn_out = np.exp(nn_out - np.expand_dims(np.amax(nn_out,axis=1),1))
nn_out = nn_out / np.expand_dims(np.sum(nn_out,axis=1),1)


##############################################################################
# Consensus sequence
aa       = "ACDEFGHIKLMNPQRSTVWY"
cons_idx = np.argmax(nn_out, axis=1)
cons_seq = ''.join([aa[i] for i in cons_idx])


##############################################################################
# Output results

print "Consensus sequence is %s" % cons_seq
print ""
print "Probility (in %) for each amino acid type in each position of given backbone"
print ""

print "          A      C      D      E      F      G      H      I      K      L      M      N      P      Q      R      S      T      V      W      Y"
for r in range(nn_out.shape[0]):
    print "%-4d" % (r+1),
    for c in range(20):
        print "%6.2f" % (100.0*nn_out[r,c]),
    print ""

