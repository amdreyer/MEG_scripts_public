#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def getHeadPosDist(headPosFile, returnDist = True):
    """Get Head Position and sample2sample distance from Maxfilter Pos file.
        Code is based on mne.viz.plot_head_positions (see https://mne.tools/stable/index.html)

    Parameters
    ----------
    headPosFile : str
        Pos filepath
    
    returnDist : bool
        Return sample2sample distance?
    
    Returns
    -------
    positions : array, shape (N, 3)
        head position (x,y,z) in mm 
        
    movDist : array, sahep (N, 1)
        sample2sample Distance
        
    """
    import mne
    import numpy as np
    from mne.chpi import head_pos_to_trans_rot_t
    headPos = mne.chpi.read_head_pos(headPosFile)

    pos = [headPos]
     
    for ii, p in enumerate(pos):
        p = np.array(p, float)
        if p.ndim != 2 or p.shape[1] != 10:
            raise ValueError('pos (or each entry in pos if a list) must be '
                             'dimension (N, 10), got %s' % (p.shape,))
        if ii > 0:
            p[:, 0] += pos[ii - 1][-1, 0] - p[0, 0]
        pos[ii] = p
    pos = np.concatenate(pos, axis=0)    
     
    trans, rot, t = head_pos_to_trans_rot_t(pos)  # also ensures pos is okay

    positions = mne.fixes.einsum('ijk,ik->ij', rot[:, :3, :3].transpose([0, 2, 1]),-trans) * 1000

    if returnDist:
        movDist = []
        from math import sqrt

        for iii in range(1,len(positions)):
            tmp = sqrt((positions[iii,0] - positions[iii-1,0])**2 + (positions[iii,1] - positions[iii-1,1])**2 + (positions[iii,2] - positions[iii-1,2])**2)
            movDist.append(tmp)
        return positions, np.array(movDist)
    else:
        return positions