from cv2 import cv2
import random


def encrypt_pixel(char, pixel):
    if char > 1000:
        char -= 890
    (b, g, r) = pixel
    b = (b & 0b11111000) + ((char & 0b11100000) >> 5)
    g = (g & 0b11111100) + ((char & 0b00011000) >> 3)
    r = (r & 0b11111000) + (char & 0b00000111)
    # print(bin(b), bin(g), bin(r))
    return list((b, g, r))


def decrypt_pixel(pixel):
    (b, g, r) = pixel
    char = ((b & 0b00000111) << 5) + ((g & 0b00000011) << 3) + (r & 0b00000111)
    # print(bin(b), bin(g), bin(r))
    if char > 130:
        char += 890
    return chr(char)


def encrypt_image(img):
    random.seed(seed_key)
    used_pixels = []
    for char in text:
        while True:
            index = random.randint(0, height * width - 1)
            if index in used_pixels:
                continue
            else:
                used_pixels.append(index)
                break
        i, j = index // width, index % height
        print(index, i,j)
        img[i][j] = encrypt_pixel(ord(char), img[i][j])
        # print(i, j, char, bin(ord(char)))
    cv2.imwrite(input("enc ing: ") + ".bmp", img)
    return


def decrypt_image(img):
    random.seed(seed_key)
    used_pixels = []
    encrypted_text = ""
    while True:
        while True:
            index = random.randint(0, height * width - 1)
            if index in used_pixels:
                continue
            else:
                used_pixels.append(index)
                break
        i, j = index // width, index % height
        enc_char = decrypt_pixel(img[i][j])
        if enc_char != "\0":
            encrypted_text += enc_char
        else:
            break
    return encrypted_text


seed_key = "123kl21"

if input("encrypt?\n") == "+":
    start_img = cv2.imread(input("start img: "))
    text = "НЮХАЙ БЕБРУ!!!! >:}"
    text += "\0"
    height, width = start_img.shape[0], start_img.shape[1]
    print(height, width)
    encrypt_image(start_img)

if input("decrypt?\n") == "+":
    enc_img = cv2.imread(input("enc img: "))
    height, width = enc_img.shape[0], enc_img.shape[1]
    print(decrypt_image(enc_img))
