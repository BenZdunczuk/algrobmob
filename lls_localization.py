import numpy as np

class LLS_localization:
    def __init__(self, ref_id):
        self.ref_id = ref_id

    def get_position(self, tags: list): 
        n_tags = []
        for tag in tags:
            if tag['frame_id'] == self.ref_id:
                x_ref, y_ref, z_ref, d_ref = tag['x'], tag['y'], tag['z'], tag['distance']
                k2_ref = x_ref**2 + y_ref**2 + z_ref**2
            else:
                n_tags.append(tag)
        
        A = []
        b = []
        for tag in n_tags:
            x, y, z, d = tag['x'], tag['y'], tag['z'], tag['distance']
            k2 = x**2 + y**2 + z**2
            
            A.append([
                2 * (x - x_ref),
                2 * (y - y_ref),
                2 * (z - z_ref),
            ])

            b.append(
                (k2 - k2_ref) - (d**2 - d_ref**2),
            )

        A = np.array(A)
        b = np.array(b)

        position, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        return position