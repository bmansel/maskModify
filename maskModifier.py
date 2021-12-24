# Copyright 2021 TPS 13A team
########################################################################
# This file is part of maskModifyer                                    #
#                                                                      #
# maskModifyer is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# maskModifyer is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with maskModifyer.  If not, see <https://www.gnu.org/licenses/>.#
########################################################################

import os
import numpy as np
import argparse

def saveMask(maskPixelsX, maskPixelsY, maskValue, experimentDirectory, saveName, overwrite):
    if overwrite is True:
        f=open(experimentDirectory + "/" + saveName, 'w')
        np.savetxt(f, np.transpose([maskPixelsX, maskPixelsY, maskValue]),fmt='%11u%11u%11.6f')
        f.close()
        return
    elif overwrite is False:
        f=open(experimentDirectory + "/" + saveName, 'a')
        np.savetxt(f, np.transpose([maskPixelsX, maskPixelsY, maskValue]),fmt='%11u%11u%11.6f')
        f.close()
        return


def makeMaskFile(experimentDirectory, maskName, saveName, overwrite):
    mask2d = np.load(experimentDirectory+ "/" + maskName)
    mask_sum = np.sum(mask2d)
    maskPixels = np.squeeze(np.where(1 == mask2d))
    if mask_sum <= 1:
        print()
        print("Only 1 or less pixels found. no mask created, please assign more than one pixel.")
        return

    maskValue = np.array([1.000000]*len(maskPixels[0]))
    saveMask(maskPixels[1], maskPixels[0], maskValue, experimentDirectory, saveName, overwrite)
    

def main():
    parser = argparse.ArgumentParser(description='Change mask from 2d pyFAI image mask to 1d reject file.')
    parser.add_argument('--directory', action='store', help='directory where the experiment is, if none default is cwd [default= None]', type=str, default= None)
    parser.add_argument('--pyFAI_mask', action='store', help='name of 2d mask file .npy from pyFAI [default=mask.npy]',type=str, default='mask.npy')
    parser.add_argument('--save_name', action='store', help='name of column .dat file to save [default=reject.dat].',type=str, default='REJECT.dat')
    parser.add_argument('--overwrite', action='store_true', help='If --overwrite reject.dat will be overwritten. otherwise data is appended to old file')
    args = parser.parse_args()
    if args.directory is None:
        experimentDirectory = os.getcwd()
    else:    
        experimentDirectory = args.directory
    maskName = args.pyFAI_mask
    saveName = args.save_name
    overwrite = args.overwrite

    makeMaskFile(experimentDirectory, maskName, saveName, overwrite)

    

if __name__ == "__main__":
    main()
