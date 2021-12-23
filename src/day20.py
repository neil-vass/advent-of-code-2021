# Was a bit confused with this one, took some marvellous inspiration from 
# https://github.com/James-Ansley/adventofcode/blob/main/2021/day20.py

def fetch_data(path):
    with open(path, 'r') as f:
        algorithm = [1 if c == '#' else 0 for c in f.readline().rstrip()]
        f.readline()
        image = [[1 if c == '#' else 0 for c in ln.rstrip()] for ln in f]
        return algorithm, image

def add_padding(image, pad_value):
    pad_width = len(image[0]) + 6
    padded_image = [[pad_value] * pad_width] * 3

    for rw in image:
        padded_image.append([pad_value]*3 + rw + [pad_value]*3)
    
    padded_image += [[pad_value] * pad_width] * 3
    return padded_image


def apply_algorithm(algorithm, image, pad_value=0):
    padded_image = add_padding(image, pad_value)
    height, width = len(padded_image), len(padded_image[0])   
    enhanced_image = [[0] * width for _ in range(height)]
    for x in range(height-2):
        for y in range(width-2):
            binary_str = ''
            for xn in range(x, x+3):
                for yn in range(y, y+3):
                    binary_str += str(padded_image[xn][yn])   
            val = int(binary_str, base=2)
            enhanced_image[x+1][y+1] = algorithm[val]
    
    # Remove padding 
    enhanced_image = [ln[2:-2] for ln in enhanced_image[2:-2]]
    return enhanced_image

def count_lights(image):
    return sum(sum(row) for row in image)

def apply_repeatedly(filename, repeats):
    algorithm, image = fetch_data(filename)
    twinkle = algorithm[0] and not algorithm[-1]
    pad_value = 0
    for _ in range(repeats):
        image = apply_algorithm(algorithm, image, pad_value)
        if twinkle:
            pad_value = 0 if pad_value else 1
    
    return count_lights(image)

#--------------------- tests -------------------------#

def test_fetch_data():
    algorithm, image = fetch_data('sample_data/day20.txt')
    assert len(algorithm) == 512
    assert not algorithm[0]
    assert algorithm[34]
    assert len(image) == 5

def test_add_padding():
    algorithm, image = fetch_data('sample_data/day20.txt')
    padded_image = add_padding(image, 0)
    assert len(padded_image) == len(image) + 6
    assert len(padded_image[0]) == len(image[0]) + 6

def test_apply_algorithm():
    algorithm, image = fetch_data('sample_data/day20.txt')
    enhanced_image = apply_algorithm(algorithm, image)
    assert count_lights(enhanced_image) == 24
    enhanced_image = apply_algorithm(algorithm, enhanced_image)
    assert count_lights(enhanced_image) == 35

def test_apply_repeatedly():
    assert apply_repeatedly('sample_data/day20.txt', 50) == 3351

#-----------------------------------------------------#

if __name__ == "__main__":
    print(apply_repeatedly('data/day20.txt', 50))
