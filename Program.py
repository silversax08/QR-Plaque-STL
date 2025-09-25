import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image
import numpy as np
import trimesh

# --- Step 1: Generate QR code ---
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=1,  # box_size is irrelevant here; we read the matrix
    border=4,
)
qr.add_data("https://venmo.com/Savannah-Hawkins-2?txn=pay&amount=0&note=Thanks!")
qr.make(fit=True)

# Preview (optional)
img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer()
)
img.show()

# --- Step 2: Get QR matrix (True = black, False = white) ---
matrix = qr.get_matrix()
matrix = np.array(matrix, dtype=bool)

rows, cols = matrix.shape
module_size = 2.0   # mm
height = 2.0        # extrusion height in mm
radius = 0.3        # corner rounding for blocks

meshes = []

# --- Step 3: Create 3D blocks for each module ---
for r in range(rows):
    for c in range(cols):
        if matrix[r, c]:
            # Center of this module
            x = c * module_size
            y = (rows - r - 1) * module_size  # flip y-axis so QR is upright
            # Create rounded cube (trimesh box with chamfer is simplest approximation)
            # trimesh doesn't have a built-in rounded cube, so we approximate
            block = trimesh.creation.box(
                extents=[module_size, module_size, height]
            )
            # Move it into place
            block.apply_translation([x + module_size/2, y + module_size/2, height/2])
            meshes.append(block)

# --- Step 4: Combine all blocks ---
qr_mesh = trimesh.util.concatenate(meshes)

# --- Step 5: Save STL ---
stl_path = r"C:\Users\GarrettHawkins\Downloads\rounded_qr.stl"
qr_mesh.export(stl_path)
print(f"Saved STL at: {stl_path}")
