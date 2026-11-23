import numpy as np
from scipy.optimize import least_squares
from lls_localization import LLS_localization

class LavenbergMarquadtLocalization:
    def __init__(self, ref_id):
        self.ref_id = ref_id

    def _residuals(self, pos, anchors, distances):
        calculated_distances = np.linalg.norm(anchors - pos, axis=1)
        return calculated_distances - distances

    def get_position(self, anchors: list):
        anchor_poses = []
        distances = []

        for anchor in anchors:
            x, y, z = anchor['x'], anchor['y'], anchor['z']
            dist = anchor['distance']
            anchor_poses.append([x, y, z])
            distances.append(dist)

        anchor_poses = np.array(anchor_poses)
        distances = np.array(distances)

        loc = LLS_localization(self.ref_id)
        initial_guess = loc.get_position(anchors).flatten()

        result = least_squares(
                self._residuals, 
                initial_guess, 
                args=(anchor_poses, distances), 
                method='lm'
            )
        
        return np.round(result.x, 3)