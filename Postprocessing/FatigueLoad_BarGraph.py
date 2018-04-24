# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 17:17:55 2018

@author: J
"""
import numpy as np
import matplotlib.pyplot as plt
from JaimesThesisModule import PostProc

def ReqVsWsp(dlc, dlc_noipc, )
if __name__ is '__main__':
   if ('dlc_noipc' not in locals()) or ('dlc' not in locals()):
        mode = 'fullload'
        dlc_noipc = PostProc.DLC('dlc11_0')
        dlc_noipc.analysis(mode=mode)

        dlc = PostProc.DLC('dlc11_1')
        dlc.analysis(mode=mode)

   save = False
   c = 'ipc04'
   key = 'RBM1'; title = ''#Main Bearing (torsion)'
   WSP = np.array([4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26])
   Req_ol, Req_cl = [0]*12, [0]*12

   for i, wsp in enumerate(WSP):
       sim = dlc(wsp=wsp, yaw=0, controller=c)[0]
       Req_cl[i] = float(sim.Req[key])

       sim_ref = dlc_noipc(wsp=wsp, yaw=0)[0]
       Req_ol[i] = float(sim_ref.Req[key])

       # bargraph
       width = 0.7

   fig, ax = plt.subplots()
   ax.set_ylabel('$R_{eq}$ [kNm]')
   ax.set_xlabel('Wind Speed [m/s]')
   ax.set_xticks(np.arange(4, 27, 2))
   ax.bar(WSP, Req_ol, width, label = '$RBM_f$ (No control)')
   ax.bar(WSP + width, Req_cl, width, label = '$RBM_f$ (With control)')
   ax.set_title(title)
   ax.legend()
   if save:
        plt.savefig('../Figures/FatigueLoads/FatigueLoads_{}_{}.png'.format(c, key), dpi=200)
