import numpy as np
import matplotlib.pyplot as plt
from PIL import Image 

class Photo:
    def __init__(self, path: str, convert=True):
        self.path = path 
        self.convert = convert

        if self.convert:
            self.image = np.array(Image.open(path).convert('RGB'))
            self.type = "RGB"
        else:
            self.image = np.array(Image.open(path))
            self.type = "Grayscales"

    def __str__(self):
        return f"Photo(type={self.type}, shape={self.image.shape})"

    def __repr__(self) -> str:
        return f"Photo({self.path}, type={self.type}, shape={self.image.shape})"

    def _find_contours(self, offset, average_color):
        
        fish_pixels_mask = np.all(self.image <= np.array(average_color) + offset, axis=-1) & np.all(self.image >= np.array(average_color) - offset, axis=-1)
        return fish_pixels_mask

    def crop_background(self, average_color=[134.97261671, 112.81255394,  71.81577089], offset=25, set_bg_to=(0, 0, 0)):
        assert 0 <= offset <= 255, "The offset has to be between 0 and the 255"

        fish_pixels = self._find_contours(offset, average_color)
        new_mask = fish_pixels.copy()

        for i in range(fish_pixels.shape[1]):
            col = fish_pixels[:, i]
            true_index = np.argwhere(col == True)  # All the indexes where the mask is True

            if len(true_index) >= 2:
                new_mask[true_index.min(): true_index.max(), i] = True
            else:
                new_mask[:, i] = False


        no_fish_here = ~new_mask
        self.image[no_fish_here] = set_bg_to


    def no_black(self):
        """ Get rid of the black pixels"""

        assert self.type == "RGB", "This method only works with RGB pictures"
        non_black_pixels_mask = np.any(self.image != [0, 0, 0], axis=-1) 
        self.image = self.image[non_black_pixels_mask]
    
    def no_white(self):
        """ Get rid of the black pixels"""

        assert self.type == "RGB", "This method only works with RGB pictures"
        non_white_pixels_mask = np.any(self.image != [255, 255, 255], axis=-1) 
        self.image = self.image[non_white_pixels_mask]

    def no_black_and_white(self):
        """ Get rid of the black and white pixels"""

        assert self.type == "RGB", "This method only works with RGB pictures"
        non_black_pixels_mask = np.any(self.image != [0, 0, 0], axis=-1) 
        non_white_pixels_mask = np.any(self.image != [255, 255, 255], axis=-1) 
        non_white_nor_black_pixels = non_black_pixels_mask & non_white_pixels_mask

        self.image = self.image[non_white_nor_black_pixels]

    def inverse_colors(self, inplace=True):
        if inplace:
            self.image = 255 - self.image
        else:
            return 255 - self.image 


    def to_numpy(self):
        return self.image

    
    @property
    def average_color(self):
        if self.convert:
            return np.mean(self.image, axis=0)
        else:
            return np.mean(self.image)


    @property
    def brightness(self):
        assert self.convert 
        array = self.average_color
        r, g, b = array

        return np.sqrt(0.241 * r**2 + 0.691 * g**2 + 0.68 * b**2)


    def plot(self, title=str(), axis=None):
        plt.figure()
        plt.title(title)
        plt.imshow(self.image)
        if not axis:
            plt.axis("off")

        plt.show()

    
    def save(self, path):
        plt.imshow(self.image)
        plt.axis('off')
        plt.savefig(path)




# The class below is more a draft for grayscales

# class PhotoDraft:
#     def __init__(self, path: str, convert=True):
#         self.path = path 
#         self.convert = convert

#         if self.convert:
#             self.image = np.array(Image.open(path).convert('RGB'))
#         else:
#             self.image = np.array(Image.open(path))

#     def __str__(self):
#         return f"{self.image}"

#     def __repr__(self) -> str:
#         return f"Photo({self.path})"


#     def inverse_colors(self, inplace=True):
#         if inplace:
#             self.image = 255 - self.image
#         else:
#             return 255 - self.image 


#     def to_numpy(self):
#         return self.image


#     def auto_seuil(self):
#         """Find the optimum threshold based on the histogram giving
#             the number of pixel for each color (grey levels)

#             Returns an int
#          """
#         # create histogramm
#         hauteurs, bins = np.histogram(self.image.flatten(), bins=256, range=(0, 256))
#         hauteurs = hauteurs.astype(int)

#         seuil = 0
#         while seuil < 256:
#             occurences_gauche = hauteurs[:seuil].sum()
#             moy_gauche = (hauteurs[:seuil] * range(0, seuil)).sum()

#             occurences_droite = hauteurs[seuil:].sum()
#             moy_droite = (hauteurs[seuil:] * range(seuil, 256)).sum()

#             if occurences_gauche > 0 and occurences_droite > 0:
#                 moy_gauche /= occurences_gauche
#                 moy_droite /= occurences_droite

#             if seuil >= (moy_gauche+ moy_droite)/2:
#                 return seuil 
            
#             seuil += 1

#         print("No threshold found")
#         return None 


#     def replace_pixels(self, seuil: int, value: int = 255):
#         """ Replace the pixels with color under the threshold 
#             with the value chosen.
#         """
#         self.image[self.image >= seuil] = value


#     @property
#     def average_color(self):
#         if self.convert:
#             return np.mean(self.image, axis=0)
#         else:
#             return np.mean(self.image)


#     @property
#     def brightness(self):
#         assert self.convert 
#         array = self.average_color
#         r, g, b = array

#         return np.sqrt(0.241 * r**2 + 0.691 * g**2 + 0.68 * b**2)


#     def plot(self, title=str(), axis=None):
#         plt.figure()
#         plt.title(title)
#         plt.imshow(self.image)
#         if not axis:
#             plt.axis("off")

#         plt.show()

    
#     def save(self, path):
#         plt.imshow(self.image)
#         plt.axis('off')
#         plt.savefig(path)


# def average_color(array):
#     return np.mean(array, axis=0)


# def brightness(array):
#     r, g, b = array
#     return np.sqrt(0.241 * r**2 + 0.691 * g**2 + 0.68 * b**2)