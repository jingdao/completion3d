import h5py
import sys
import numpy as np
import os

def savePLY(filename, points, faces=None):
	f = open(filename,'w')
	f.write("""ply
format ascii 1.0
element vertex %d
property float x
property float y
property float z
property uchar r
property uchar g
property uchar b
""" % len(points))
	if faces is None:
		f.write("end_header\n")
	else:
		f.write("""
element face %d
property list uchar int vertex_index
end_header
""" % (len(faces)))
	for p in points:
		f.write("%f %f %f %d %d %d\n"%(p[0],p[1],p[2],p[3],p[4],p[5]))
	if not faces is None:
		for p in faces:
			f.write("3 %d %d %d\n"%(p[0],p[1],p[2]))
	f.close()
	print('Saved to %s: (%d points)'%(filename, len(points)))

val_scale_offset = np.loadtxt('data/facade/val_scale_offset.txt')
TEST_SET=["01_mason_east","02_pettit","03_seb_north","04_seb_south","05_seb_west","06_seb_east","07_mason_north","08_vl_south","09_vl_circle","10_vl_east","11_cod"]

for M in ['PCN', 'Folding', 'TopNet']:
    for T in TEST_SET:
        sceneID = int(T[:2])
        f = h5py.File('results/facade/%s/%02d/predictions_val.h5' % (M, sceneID), 'r')
        for i in f:
            for j in f[i]:
                pc = f[i][j][:][0]
                scale = val_scale_offset[sceneID-1, 0]
                offset = val_scale_offset[sceneID-1, 1:4]
                output = scale * pc + offset
                output = np.hstack((output, np.zeros((len(output), 3))))
                ply_gray = 'results/facade/%s/%s.ply'%(M, T)
                savePLY(ply_gray, output)
        f.close()

        cmd = "/usr/bin/python fix_color.py /home/jd/Desktop/point_cloud_scene_completion/input/%s_input.ply %s /home/jd/Desktop/point_cloud_scene_completion/baselines/%s/%s.ply" % (T, ply_gray, M, T)
        os.system(cmd)
