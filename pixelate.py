from PIL import Image
import matplotlib.pyplot as plt

# Load image
img = Image.open('C:/Users/mroiz/Documents/Warcraft III/illidan.png')

# Pixelate to X by X
pixelate = img.resize((20,20), Image.NEAREST)

# Display enlarged for clarity
plt.figure(figsize=(3, 3))
plt.imshow(pixelate)
plt.axis('off')
plt.show()

pixelate