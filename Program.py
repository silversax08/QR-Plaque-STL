import requests
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image
import numpy as np
import trimesh

# --- Step 0: Shorten the URL using is.gd ---
def shorten_url_isgd(long_url):
    api = "https://is.gd/create.php"
    params = {
        "format": "simple",  # return plain short URL
        "url": long_url
    }
    response = requests.get(api, params=params)
    if response.status_code == 200:
        return response.text.strip()
    else:
        raise Exception(f"URL shortening failed: {response.status_code}")

long_url = "https://venmo.com/Savannah-Hawkins-2?txn=pay&amount=0&note=Thanks!"
short_url = shorten_url_isgd(long_url)
print(f"Short URL: {short_url}")

# --- Step 1: Generate QR code for the shortened URL ---
qr = qrcode.QRCode(
    version=None,  # let qrcode pick the smallest version automatically
    error_correction=qrcode.constants.ERROR_CORRECT_M,  # lower error correction
    box_size=1,
    border=2,  # minimal quiet zone
)
qr.add_data(short_url)
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
module_size = 3.0   # larger module size for easier 3D printing
height = 2.0        # extrusion height in mm
radius = 0.3        # corner rounding for blocks (not applied in mesh, optional)

meshes = []

# --- Step 3: Create 3D blocks for each module ---
for r in range(rows):
    for c in range(cols):
        if matrix[r, c]:
            x = c * module_size
            y = (rows - r - 1) * module_size  # flip y-axis
            block = trimesh.creation.box(extents=[module_size, module_size, height])
            block.apply_translation([x + module_size/2, y + module_size/2, height/2])
            meshes.append(block)

# --- Step 4: Combine all blocks ---
qr_mesh = trimesh.util.concatenate(meshes)

# --- Step 5: Save STL ---
stl_path = r"C:\Users\GarrettHawkins\Downloads\rounded_qr.stl"
qr_mesh.export(stl_path)
print(f"Saved STL at: {stl_path}")
