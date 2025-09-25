import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=20,
    border=4,
)

qr.add_data("https://www.optisys.com")
qr.make(fit=True)

img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer()
)

img.show()
img.save(r"C:\Users\GarrettHawkins\Downloads\rounded_qr.png")
