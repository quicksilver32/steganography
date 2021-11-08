import random


def encrypt_pixel(char, pixel):
    if char > 1000:
        char -= 890
    (b, g, r) = pixel
    b = (b & 0b11111000) + ((char & 0b11100000) >> 5)
    g = (g & 0b11111100) + ((char & 0b00011000) >> 3)
    r = (r & 0b11111000) + (char & 0b00000111)
    return list((b, g, r))


def decrypt_pixel(pixel):
    (b, g, r) = pixel
    char = ((b & 0b00000111) << 5) + ((g & 0b00000011) << 3) + (r & 0b00000111)
    if char > 130:
        char += 890
    return chr(char)


def encrypt_image(img, text, seed_key):
    random.seed(seed_key)
    used_pixels = []
    for char in text:
        while True:
            index = random.randint(0, img.shape[0] * img.shape[1] - 1)
            if index in used_pixels:
                continue
            else:
                used_pixels.append(index)
                break
        i, j = index // img.shape[1], index % img.shape[0]
        img[i][j] = encrypt_pixel(ord(char), img[i][j])
    return img


def decrypt_image(img, seed_key):
    random.seed(seed_key)
    used_pixels = []
    encrypted_text = ""
    while True:
        while True:
            index = random.randint(0, img.shape[0] * img.shape[1] - 1)
            if index in used_pixels:
                continue
            else:
                used_pixels.append(index)
                break
        i, j = index // img.shape[1], index % img.shape[0]
        enc_char = decrypt_pixel(img[i][j])
        if enc_char != "\0":
            encrypted_text += enc_char
        else:
            break
    return encrypted_text
