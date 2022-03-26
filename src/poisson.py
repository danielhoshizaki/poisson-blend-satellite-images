"""
Author: Daniel Hoshizaki
"""

import numpy as np
from scipy import sparse


def rook_neighbor(location: tuple, shape: tuple) -> list:
    """Given a location, return the coordinates of locations above, below, left, and right"""
    (height, width) = shape
    i, j = location
    valid_neighbors = []
    
    if i+1 < height: valid_neighbors.append((i+1, j));
    if i-1 >= 0: valid_neighbors.append((i-1, j));
    if j+1 < width: valid_neighbors.append((i, j+1));
    if j-1 >= 0: valid_neighbors.append((i, j-1));

    return valid_neighbors


def valid_neighbor(location: tuple, points_in_mask: dict):
    """Return the index of a neighbor if the neighbor is within the mask"""
    i, j = location
    valid_locations = [neighbor for neighbor in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)] if neighbor in points_in_mask]
    return valid_locations


def laplacian_kernel(location: tuple, img: np.ndarray) -> int:
    """Apply a Laplacian kernel to the target location"""
    i, j = location
    neighbors = rook_neighbor(location, img.shape)
    
    val = (4 * img[i, j])
    for neighbor in neighbors:
        val -= img[neighbor]
    
    return val


def laplacian_operator(points: dict) -> sparse.lil_matrix:
    """Fill a sparce matrix and create a Laplacian operator"""
    
    # Create an empty sparse matrix
    n = len(points)
    operator = sparse.lil_matrix((n, n))

    # Fill the sparse matrix with the Laplacian operator
    for index, i in points.items():
        operator[i,i] = 4
        
        # Get all surrounding points
        for neighbor in valid_neighbor(index, points):
            j = points[neighbor]
            operator[i,j] = -1
    
    return sparse.csr_matrix(operator)


def boundary_locations(location: tuple, all_points: dict, shape: tuple) -> list:
    """Check if a target location is at the edge of the mask. If it is
    return the rook neighbor(s) that are outside of the mask"""
    edge_of_mask = []

    for neighbor in rook_neighbor(location, shape):
        # Check if the neighbor is outside the mask
        if neighbor not in all_points:
            # One neighbor is not in the mask
            edge_of_mask.append(neighbor)
    
    return edge_of_mask


def compute_gradient(points: dict, source: np.ndarray, target: np.ndarray) ->  np.ndarray:
    """Calculate the gradient values for vector b in Ax = b. The gradient is a combination
    of the Laplacian of the source and target intensities at the mask edges"""
    
    # Create an empty gradient vector b
    b = np.zeros(len(points))

    # Fill b
    for index, i in points.items():

        # Compute the gradient at the target location
        b[i] = laplacian_kernel(index, source)
        
        # Collect locations that are on the mask boundary
        boundary_neighbors = boundary_locations(index, points, source.shape)

        # If boundary neighbors are detected, add the target intensities to the gradient
        if len(boundary_neighbors) > 0:
            for boundary_neighbor in boundary_neighbors:
                b[i] += target[boundary_neighbor]
    
    return b


def insert_values(new_values: np.ndarray, target: np.ndarray, target_points: dict) -> np.ndarray:
    """Insert new values into a target image according to a set of coordinates and corresponding values"""
    new_img = target.copy()
    
    for index, i in target_points.items():
        new_target_value = int(new_values[i])

        # Pin the values between 1-255
        if new_target_value > 255:
            new_target_value = 255
        elif new_target_value <= 0:
            new_target_value = 1
        
        new_img[index] = new_target_value
    
    return new_img
