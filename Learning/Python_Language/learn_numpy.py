import numpy as np
from PIL import Image

original = Image.open('imagem.png')
cinza = np.array(original)
cinza = np.dot(cinza[..., :3], [0.299, 0.587, 0.114])
cinza = Image.fromarray(cinza.astype('uint8'))
cinza.save('imagem_cinza.png')
