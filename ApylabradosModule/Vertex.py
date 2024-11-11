import numpy as np

class Vertex():
    def transformation(self, x) -> int:
        """
        Convert interval (-1,16) to interval (0,1)

        Args:
            x (int): interval for transformation

        Returns:
            int: the transformation interval
        """
        
        return (x + 1) / 17
    
    def transformationX(self, x) -> float:
        """

        Args:
            x (int): x axis for transformation

        Returns:
            float: transformation x axis
        """
        
        return x / 16
    
    def transformationY(self, y) -> float:
        """

        Args:
            y (int): y axis for transformation

        Returns:
            float: transformation y axis
        """
        
        return (y + 1) / 3
    
    def generateVertex(self, center_x, center_y) -> np.ndarray:
        """
        Generate the vertices of a square centered at (center_x, center_y).
        
        Args:
            center_x (int): x-coordinate of the center
            center_y (int): y-coordinate of the center

        Returns:
            np.ndarray: 2D array of vertices representing the square
        """
        
        return np.array([
            [center_x - 0.5, center_y - 0.5], [center_x - 0.5, center_y + 0.5],
            [center_x + 0.5, center_y + 0.5], [center_x + 0.5, center_y - 0.5]
        ])