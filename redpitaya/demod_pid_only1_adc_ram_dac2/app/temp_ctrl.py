"""
19/09/2019 @ ben

                                       --------
           -----   dt   -----    e1    |      |
   t >---->|+  |------->|+  |--------->| pid1 |--------> out
           | - |        | + |          |      |
           -----        -----          --------
             ^            ^
             |            |            --------
             |            |  delta_t   |      |
             ^            -------------| pid2 |----|
             t0                        |      |    |
                                       --------    |
                                                   ^
                                                  in_

"""


import pid_fixed as pid

class TempCtrl(object):

    def __init__(self, kps=[0,0], kis=[0,0], sps=[0,0], osps=[0,0],
                 imaxs=[10**999,10**999], omaxs=[10**999,10**999],
                 oscales=[10,10]):
        self.pid1 = pid.PIDfixed(kps[0], kis[0], sps[0], osps[0],
                                 imaxs[0], omaxs[0], oscales[0])
        self.pid2 = pid.PIDfixed(kps[1], kis[1], sps[1], osps[1],
                                 imaxs[1], omaxs[1], oscales[1])

    def compute(self, in_, t, t0):
        dt = t - t0
        delta_t = self.pid2.compute(in_)
        e1 = dt + delta_t
        out = self.pid1.compute(e1)
        return [out,delta_t]

    def reset(self):
        self.pid1.reset()
        self.pid2.reset()
