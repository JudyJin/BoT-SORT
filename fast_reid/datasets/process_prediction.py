import pandas as pd
import argparse
parser = argparse.ArgumentParser("BoT-SORT Demo!")
parser.add_argument("dir", default="reid_test-99", help="test dir")
    
args = parser.parse_args()
dir = args.dir

gt_path = '/home/zhaojin/TrackEval/data/gt/mot_challenge/REID-test/'+dir+'/gt/gt.txt'
ouput_path = '/home/zhaojin/TrackEval/data/trackers/mot_challenge/REID-test/data/data/'+dir+'.txt'

gt = pd.read_csv(gt_path, header=None)
frames = gt[0].unique()
output = pd.read_csv(ouput_path, header=None)
output = output[output[0].isin(frames)]
output.to_csv(ouput_path, header=None, index=False)