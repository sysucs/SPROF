import scipy as sp
import numpy as np

##############################################################################
# Calculate torsion angle

def protein_torsion_angle(positions):

    # Bond vectors
    b1 = positions[1,] - positions[0,]
    b2 = positions[2,] - positions[1,]
    b3 = positions[3,] - positions[2,]

    # Normal vectors to bond pairs
    n1 = np.cross(b1,b2)
    n2 = np.cross(b2,b3)
    n1 = n1/np.linalg.norm(n1)
    n2 = n2/np.linalg.norm(n2)

    # Normal vector to plane defined by b2 and n1
    m1 = np.cross(b2/np.linalg.norm(b2),n1)

    return np.arctan2(np.dot(m1,n2),np.dot(n1,n2))


##############################################################################
# 

def protein_bond_angle(positions):

    # Bond vectors
    b1 = positions[0,] - positions[1,]
    b2 = positions[2,] - positions[1,]
    b1 = b1/np.linalg.norm(b1)
    b2 = b2/np.linalg.norm(b2)

    # The dot product represents the cosine of the angle
    return np.arccos(np.dot(b1,b2))


##############################################################################
# 
def gen_features_angles(raw_positions):
    
    # Remove extraneous info
    clean_positions = raw_positions[:,2:]

    # Initialise output feature array
    features_angles = np.zeros((raw_positions.shape[0]/4, 10))

    # Phi
    for residue in range(1,features_angles.shape[0]):
        features_angles[residue,0] = protein_torsion_angle(np.concatenate((np.expand_dims(clean_positions[4*(residue-1)+2,],0),clean_positions[(4*residue):(4*residue+3),]), axis=0))
    features_angles[0,0] = features_angles[1,0]

    # Psi
    for residue in range(features_angles.shape[0]-1):
        features_angles[residue,2] = protein_torsion_angle(np.concatenate((clean_positions[(4*residue):(4*residue+3),],np.expand_dims(clean_positions[4*(residue+1),],0)), axis=0))
    features_angles[-1,2] = features_angles[-2,2]

    # Tau(N[i],Ca[i],C[i])
    for residue in range(1,features_angles.shape[0]-1):
        features_angles[residue,4] = protein_bond_angle(clean_positions[(4*residue):(4*residue+3),])
    features_angles[0,4] = features_angles[1,4]
    features_angles[-1,4] = features_angles[-2,4]

    # Tau(Ca[i-1],Ca[i],Ca[i+1])
    for residue in range(1,features_angles.shape[0]-1):
        features_angles[residue,6] = protein_bond_angle(clean_positions[(4*(residue-1)+1):(4*(residue+2)+1):4,])
    features_angles[0,6] = features_angles[1,6]
    features_angles[-1,6] = features_angles[-2,6]

    # Theta(Ca[i],Ca[i+1])
    for residue in range(1,features_angles.shape[0]-2):
        features_angles[residue,8] = protein_torsion_angle(clean_positions[(4*(residue-1)+1):(4*(residue+3)+1):4,])
    features_angles[0,8] = features_angles[1,8]
    features_angles[-2,8] = features_angles[-3,8]
    features_angles[-1,8] = features_angles[-3,8]

    # Calculate cos and sin
    features_angles[:,1] = np.sin(features_angles[:,0])
    features_angles[:,3] = np.sin(features_angles[:,2])
    features_angles[:,5] = np.sin(features_angles[:,4])
    features_angles[:,7] = np.sin(features_angles[:,6])
    features_angles[:,9] = np.sin(features_angles[:,8])
    features_angles[:,0] = np.cos(features_angles[:,0])
    features_angles[:,2] = np.cos(features_angles[:,2])
    features_angles[:,4] = np.cos(features_angles[:,4])
    features_angles[:,6] = np.cos(features_angles[:,6])
    features_angles[:,8] = np.cos(features_angles[:,8])

    # Return features
    return features_angles


##############################################################################
# COUNT NEARBY CA ATOMS

def gen_features_ca_count(raw_positions):

    # Extract CA atoms
    CA_positions = raw_positions[1::4,2:]

    # Calculate deltas
    CA_xD = np.subtract(CA_positions[:,0],CA_positions[:,0].reshape((-1,1)))
    CA_yD = np.subtract(CA_positions[:,1],CA_positions[:,1].reshape((-1,1)))
    CA_zD = np.subtract(CA_positions[:,2],CA_positions[:,2].reshape((-1,1)))

    # Calculate squared Euclidean distances
    CA_sD = np.square(CA_xD) + np.square(CA_yD) + np.square(CA_zD)

    # Initialise output feature array
    features_ca_num = np.zeros((CA_sD.shape[0], 16))

    # Count nearby CA atoms
    for distance in range(5,21):
        temporary_count = np.less_equal(CA_sD, distance*distance).astype(np.float_)
        features_ca_num[:,distance-5] = np.sum(temporary_count, axis=0) - 1

    # Return features
    return features_ca_num
        


##############################################################################
# CALCULATE ATOM DISTANCES BETWEEN RESIDUES
def gen_features_inter(raw_positions):

    # Initialise output feature array
    features_inter_prev = np.zeros((raw_positions.shape[0]/4 - 1, 16))
    features_inter_next = np.zeros((raw_positions.shape[0]/4 - 1, 16))

    # Previous residues
    for atom_cur in range(4):
        for atom_prev in range(4):
            dist_x = np.subtract(raw_positions[(atom_cur+4)::4,2], raw_positions[atom_prev:(raw_positions.shape[0]-4):4,2])
            dist_y = np.subtract(raw_positions[(atom_cur+4)::4,3], raw_positions[atom_prev:(raw_positions.shape[0]-4):4,3])
            dist_z = np.subtract(raw_positions[(atom_cur+4)::4,4], raw_positions[atom_prev:(raw_positions.shape[0]-4):4,4])
            features_inter_prev[:,4*atom_prev+atom_cur] = np.sqrt(np.square(dist_x) + np.square(dist_y) + np.square(dist_z))
    features_inter_prev = np.concatenate((np.expand_dims(features_inter_prev[0,], 0), features_inter_prev))

    # Next residues
    for atom_cur in range(4):
        for atom_next in range(4):
            dist_x = np.subtract(raw_positions[(atom_next+4)::4,2], raw_positions[atom_cur:(raw_positions.shape[0]-4):4,2])
            dist_y = np.subtract(raw_positions[(atom_next+4)::4,3], raw_positions[atom_cur:(raw_positions.shape[0]-4):4,3])
            dist_z = np.subtract(raw_positions[(atom_next+4)::4,4], raw_positions[atom_cur:(raw_positions.shape[0]-4):4,4])
            features_inter_next[:,4*atom_next+atom_cur] = np.sqrt(np.square(dist_x) + np.square(dist_y) + np.square(dist_z))
    features_inter_next = np.concatenate((features_inter_next, np.expand_dims(features_inter_next[-1,], 0)))

    # Return features
    return np.concatenate((features_inter_prev[:,0:8],features_inter_prev[:,9:],features_inter_next[:,0:2],features_inter_next[:,3:]), axis=1)




##############################################################################
# CALCULATE ATOM DISTANCES WITHIN A RESIDUE
def gen_features_intra(raw_positions):

    # Initialise output feature array
    features_intra = np.zeros((raw_positions.shape[0]/4, 2))

    # Calculate N->O distances
    dist_x = np.subtract(raw_positions[0::4,2], raw_positions[3::4,2])
    dist_y = np.subtract(raw_positions[0::4,3], raw_positions[3::4,3])
    dist_z = np.subtract(raw_positions[0::4,4], raw_positions[3::4,4])
    features_intra[:,0] = np.sqrt(np.square(dist_x) + np.square(dist_y) + np.square(dist_z))

    # Calculate Ca->O distances
    dist_x = np.subtract(raw_positions[1::4,2], raw_positions[3::4,2])
    dist_y = np.subtract(raw_positions[1::4,3], raw_positions[3::4,3])
    dist_z = np.subtract(raw_positions[1::4,4], raw_positions[3::4,4])
    features_intra[:,1] = np.sqrt(np.square(dist_x) + np.square(dist_y) + np.square(dist_z))

    # Return features
    return features_intra


##############################################################################
# 



##############################################################################
# 



##############################################################################
# 



##############################################################################
# 



##############################################################################
# 



##############################################################################
# 





