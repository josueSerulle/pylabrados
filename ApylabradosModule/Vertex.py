import numpy as np

class Vertex:
    @staticmethod
    def transformation(x) -> float:
        """
        Convert interval (-1,16) to interval (0,1)

        Args:
            x (float): interval for transformation

        Returns:
            int: the transformation interval
        """

        return (x + 1) / 17

    @staticmethod
    def transformationX(x) -> float:
        """

        Args:
            x (float): x-axis for transformation

        Returns:
            float: transformation x-axis
        """
        
        return x / 16
    
    @staticmethod
    def transformationY(y) -> float:
        """

        Args:
            y (float): y-axis for transformation

        Returns:
            float: transformation y-axis
        """
        
        return (y + 1) / 3
    
    @staticmethod
    def generateVertex(center_x, center_y) -> np.ndarray:
        """
        Generate the vertices of a square centered at (center_x, center_y).
        
        Args:
            center_x (float): x-coordinate of the center
            center_y (float): y-coordinate of the center

        Returns:
            np.ndArray: 2D array of vertices representing the square
        """
        
        return np.array([
            [center_x - 0.5, center_y - 0.5], [center_x - 0.5, center_y + 0.5],
            [center_x + 0.5, center_y + 0.5], [center_x + 0.5, center_y - 0.5]
        ])