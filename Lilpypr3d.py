from PIL import Image, ImageDraw  # Python Imaging Library for creating and manipulating images
from tqdm import tqdm # A library for creating smart, fast progress bars
import math      # For mathematical operations like square root and floor
import random    # For generating random numbers



# A palette of common colors defined as RGB tuples for easy access
blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
white = (255,255,255)
black = (0,0,0)
yellow = (255,255,0)
purple = (255,0,255)

# Predefined points for quick testing or use
Point_A = [10,100]
Point_B = [50,100]
Point_C = [150,40]

# Direction vectors, useful for translations or vector operations
Up = [0,1]
Down = [0,-1]
Right = [1,0]
Left = [-1,0]


# Set the dimensions of the output image
Render_Width = 2000
Render_Height = 2000

# Create a new blank image with the specified dimensions and a green background.
# This image object will act as our canvas.
Render_Output = Image.new("RGB", [Render_Width,Render_Height], color = black)

# --- Helper Functions ---

def Generate_Color_Shades(nofshades):
      """Generates a list of random shades of purple/magenta."""
      returnlist = []
      for _ in range(nofshades):
           # Create a color with a random red and blue component, and zero green
           a = (random.randrange(100,255), 0,random.randrange(100,255))
           returnlist.append(a)
      return returnlist
          
def Random_Point():
      """Generates a random point [x, y] within the render canvas."""
      return [random.randrange(0,Render_Width),random.randrange(0,Render_Height)]


def Middlepoint(pointlist):
      """Calculates the midpoint between the first and last points in a list."""
      # Note: This function only considers the first and last elements, not the entire list.
      x_mid = math.floor((pointlist[0][0] + pointlist[-1][0])/2)
      y_mid = math.floor((pointlist[0][1] + pointlist[-1][1])/2)
      return [x_mid, y_mid]

# --- Core Drawing Functions ---

def Draw_Point(coord,color):
    """
    Draws a single pixel at the given coordinate with a specified color.
    This function includes a basic Z-buffer check: it only draws the new pixel
    if its color value is "greater" than the pixel color already on the canvas.
    This is used to ensure objects closer to the camera (brighter color) are drawn over objects farther away.
    """
    try:
        # Z-buffer implementation: check if the new pixel is "brighter" than the existing one.
        if Image.Image.getpixel(self=Render_Output, xy=coord) <= color:
            draw = ImageDraw.Draw(Render_Output)
            # Draw the point on the canvas
            draw.point(xy=(coord[0], coord[1]), fill=color)
    except IndexError:
          pass
    
def Draw_Line(Coord1, Coord2, Color, Color2=white, Highlight_Ends=False):
    """
    Draws a line between two points using linear interpolation.
    It calculates each point on the line segment and draws it pixel by pixel.
    """
    # Calculate the Euclidean distance between the two points
    Distance = math.sqrt((Coord2[1] - Coord1[1])**2 + (Coord2[0] - Coord1[0])**2)
    
    # These variables are weights for the linear interpolation
    Ponder1 = Distance  # Weight for the starting point (Coord1)
    Ponder2 = 0         # Weight for the ending point (Coord2)
    LinePixels = []     # A list to store the coordinates of each pixel in the line

    if Distance != 0:
        # Iterate for each step along the line's length
        for i in range(0, int(Distance) + 1):
            # Linearly interpolate to find the next point on the line
            # Formula: P = (P1*w1 + P2*w2) / (w1+w2)
            Middle_Point = [
                math.floor((Coord1[0] * Ponder1 + Coord2[0] * Ponder2) / Distance),
                math.floor((Coord1[1] * Ponder1 + Coord2[1] * Ponder2) / Distance)
            ]
            Draw_Point(Middle_Point, Color)
            LinePixels.append(Middle_Point)
            
            # Update the weights for the next iteration
            Ponder1 -= 1
            Ponder2 += 1
            
        # Optionally, draw a different colored pixel at the start and end of the line
        if Highlight_Ends:
            Draw_Point(Coord1, Color2)
            Draw_Point(Coord2, Color2)
            
    return LinePixels

def Draw_Triangle(Coord1, Coord2, Coord3, Color):
      """Draws the wireframe outline of a triangle."""
      Draw_Line(Coord1, Coord2, Color)
      Draw_Line(Coord3, Coord2, Color)
      Draw_Line(Coord1, Coord3, Color)

def Draw_Filled_Triangle(Coord1, Coord2, Coord3, Color):
    """
    Fills a triangle by drawing lines between points on its edges.
    NOTE: This is a very inefficient method for triangle rasterization and can be slow.
    It connects every point on Line1 to every point on Line2. A more optimal approach
    would be scanline rendering.
    """
    Line1 = Draw_Line(Coord1, Coord2, Color)
    Line2 = Draw_Line(Coord3, Coord2, Color)
    
    # Iterate through each point on two edges of the triangle
    for point2 in Line2:
        for point1 in Line1:
            # Draw a line between the points, effectively filling the triangle
            Draw_Line(point1, point2, Color)

# --- 3D Model Rendering Functions ---

def Draw_Wireframe_Projection(Obj_Model, color):
    """
    Renders a 3D model in wireframe mode. It reads faces from the model
    and draws the outline of each triangle on the 2D canvas.
    """
    for line in Obj_Model.Faces_List:
        # For each vertex of the face, get its 3D coordinates from the vertex list
        # The indices line[0], line[3], line[6] are used because the face data
        # is stored on the same line in different position
        
        # Vertex 1
        Point1x = (Obj_Model.Vertex_List[line[0] - 1][0] + 1) * (Render_Width / 2)
        Point1y = (Obj_Model.Vertex_List[line[0] - 1][1] + 1) * (Render_Height / 2)

        # Vertex 2
        Point2x = (Obj_Model.Vertex_List[line[3] - 1][0] + 1) * (Render_Width / 2)
        Point2y = (Obj_Model.Vertex_List[line[3] - 1][1] + 1) * (Render_Height / 2)

        # Vertex 3
        Point3x = (Obj_Model.Vertex_List[line[6] - 1][0] + 1) * (Render_Width / 2)
        Point3y = (Obj_Model.Vertex_List[line[6] - 1][1] + 1) * (Render_Height / 2)
        
        # The formulas above convert model coordinates (from -1 to 1) to screen coordinates (from 0 to Render_Width/Height).
        
        # Draw the triangle outline
        Draw_Triangle([Point1x, Point1y], [Point2x, Point2y], [Point3x, Point3y], color)

def Draw_Mesh_Projection(Obj_Model, color):
    """
    Renders a 3D model as a solid mesh with depth-based shading.
    Closer faces are drawn with a brighter color.
    """
    # Create a progress bar for the rendering process
    pbar = tqdm(Obj_Model.Faces_List, desc="Rendering Progress:", unit="Mesh", smoothing=0)
    
    for line in pbar:
        # --- Project 3D vertices to 2D screen coordinates ---
        # This mapping converts model space coordinates (usually -1 to 1) to screen space (0 to 200)
        # Vertex 1
        Point1x = (Obj_Model.Vertex_List[line[0] - 1][0] + 1) * (Render_Width / 2)
        Point1y = (Obj_Model.Vertex_List[line[0] - 1][1] + 1) * (Render_Height / 2)

        # Vertex 2
        Point2x = (Obj_Model.Vertex_List[line[3] - 1][0] + 1) * (Render_Width / 2)
        Point2y = (Obj_Model.Vertex_List[line[3] - 1][1] + 1) * (Render_Height / 2)

        # Vertex 3
        Point3x = (Obj_Model.Vertex_List[line[6] - 1][0] + 1) * (Render_Width / 2)
        Point3y = (Obj_Model.Vertex_List[line[6] - 1][1] + 1) * (Render_Height / 2)

        # --- Calculate depth for Z-buffering and shading ---
        # Average the Z-coordinates of the triangle's three vertices
        avg_z = (Obj_Model.Vertex_List[line[0] - 1][2] + 
                 Obj_Model.Vertex_List[line[3] - 1][2] + 
                 Obj_Model.Vertex_List[line[6] - 1][2])
        # Normalize the depth to a 0-255 grayscale value for coloring
        # We assume Z is in [-1, 1], so (avg_z/3 + 1)/2 maps it to [0,1], then scale by 255.
        depth = ((avg_z / 3 + 1) / 2) * 255
        
        # Note: The following line is inefficient as it's called inside a loop.
        # It was likely part of an earlier experiment with random colors.
        colorlist = Generate_Color_Shades(100)
        # The commented-out line below would draw triangles with random colors.
        # Draw_Filled_Triangle([Point1x,Point1y],[Point2x,Point2y],[Point3x,Point3y], colorlist[random.randrange(0 ,len(colorlist) - 1)])
        
        # Draw the filled triangle using the calculated depth as a grayscale color.
        # The Draw_Point function will handle the Z-buffering to ensure correct ordering.
        Draw_Filled_Triangle([Point1x,Point1y],[Point2x,Point2y],[Point3x,Point3y], (int(depth), int(depth), int(depth)))

# --- Data Structure for 3D Model ---

class Model():
    """A class to load and store 3D model data from an .obj file."""
    def __init__(self, FileName, vertexlist, faceslist):
        self.File_Name = FileName
        self.Vertex_List = vertexlist
        self.Faces_List = faceslist
        
    @staticmethod
    def Model_Vertex_Constructor(filename):
        """Reads an .obj file and extracts all vertex coordinates."""
        Vertex_List = []
        with open(filename, "r") as Obj_File:
            for line in Obj_File:
                # Vertex lines in .obj files start with "v "
                if line.startswith("v "):
                    # Parse the x, y, z coordinates into a tuple of floats
                    vertex = tuple(map(float, line[2:].strip().split()))
                    Vertex_List.append(vertex)
        return Vertex_List
        
    @staticmethod
    def Model_Faces_Constructor(filename):
        """Reads an .obj file and extracts all face definitions."""
        Faces_List = []
        with open(filename, "r") as Obj_File:
            for line in Obj_File:
                # Face lines in .obj files start with "f "
                if line.startswith("f "):
                    linelist = []
                    # A face is defined by 3+ vertices, e.g., "f 1/1/1 2/2/2 3/3/3"
                    # This splits the line into ["1/1/1", "2/2/2", "3/3/3"]
                    TempoFace = tuple(map(str, line[2:].strip().split()))
                    for i in TempoFace:
                        # This splits each vertex definition, e.g., "1/1/1" -> ["1", "1", "1"]
                        face = i.split("/")
                        for a in face:
                            # Convert each index to an integer and add to the list
                            linelist.append(int(a))
                    # The final list for one face will be [v1, vt1, vn1, v2, vt2, vn2, ...]
                    Faces_List.append(linelist)
        return Faces_List

# --- Main Execution Block ---

if __name__ == "__main__":
    # The 'counter' variable is initialized but never used.
    counter = 0 
    
    # Load the 3D model from the "model.obj" file by parsing its vertices and faces.
    Objmodel = Model("OBJ Test Model", 
                     Model.Model_Vertex_Constructor("model.obj"), 
                     Model.Model_Faces_Constructor("model.obj"))
                     
    # Render the loaded model as a solid mesh. The 'red' color argument is not used
    # because the function calculates its own grayscale color based on depth.
    Draw_Wireframe_Projection(Objmodel, red)

    # The Y-axis is often inverted between 3D modeling coordinates and 2D image coordinates.
    # Flip the final image vertically to correct the orientation.
    flip_img = Render_Output.transpose(Image.FLIP_TOP_BOTTOM)
    
    # Save the final rendered image to a PNG file.
    flip_img.save("Render_output.png")
    print("Rendering complete. Image saved as Render_output.png")