from PIL import Image

def load_icon(path, size):
        image = Image.open(path)
        original_width, original_height = image.size
        
        if original_width > original_height:
            new_width = size
            new_height = int((original_height * size) / original_width)
        else:
            new_height = size
            new_width = int((original_width * size) / original_height)
        
        return image.resize((new_width, new_height), Image.LANCZOS)