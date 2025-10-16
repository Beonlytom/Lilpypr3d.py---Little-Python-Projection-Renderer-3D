




![alt text](https://github.com/Beonlytom/Lilpypr3d.py---Little-Python-Projection-Renderer-3D/blob/main/Image1.png)
# 🧵 2D OBJ Renderer

A lightweight Python renderer that projects 3D `.obj` models onto a 2D pixel canvas using custom math and basic geometry.

## 🧠 About This Project

This was built in about **8 hours** as a personal learning experiment.  
No libraries for 3D rendering — just raw Python, PIL, and a lot of trial and error.  
The math behind the projection and shading was **invented on the spot**, so it's probably not the most optimized or accurate. But it works!

## 🎨 Features

- Wireframe and filled triangle rendering
- Depth-based grayscale shading
- Random color generation
- Simple geometry tools (lines, triangles, midpoints)
- OBJ file parsing for vertices and faces
- NEW: Progressive Build Animation and Video Creation!

The renderer can iterate over each face and save it as a progressive frame, simulating the model being "built."

Automatic compilation of these frames into a final video file (Output_video.mp4) using OpenCV (cv2).

- ![alt text](https://github.com/Beonlytom/Lilpypr3d.py---Little-Python-Projection-Renderer-3D/blob/main/Image2.png)

## 📦 Dependencies

- `PIL` (Pillow)
- `tqdm`
- Python 3.x

## 🛠️ How It Works

1. Loads a `.obj` file and parses vertices and faces.
2. Projects 3D coordinates onto a 2D canvas.
3. Renders each face as a triangle using custom math.
4. Applies shading based on average depth (Z-axis).
5. Saves the final image as `Render_output.png`.

- ![alt text](https://github.com/Beonlytom/Lilpypr3d.py---Little-Python-Projection-Renderer-3D/blob/main/gif.gif)
## ⚠️ Disclaimer

This is **not** a production-grade renderer.  
It’s a fun, messy, and educational project — perfect for learning how graphics work at a low level.

## 📸 Output Example

The final image is flipped vertically to match screen coordinates and saved locally.

---

Feel free to fork, break, or improve it.  
If you spot bugs or weird behavior… yeah, same 😅
