import numpy as np
import open3d as o3d

pcd = o3d.io.read_point_cloud("sync.ply")
pcd = pcd.voxel_down_sample(voxel_size=10)

distances = pcd.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 3 * avg_dist

print(avg_dist)
print(np.max(distances))
print(np.min(distances))

pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=100, max_nn=30))

#mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius, radius * 2]))
#mesh.compute_vertex_normals()
#o3d.visualization.draw_geometries([pcd, mesh])

o3d.visualization.draw_geometries([pcd])