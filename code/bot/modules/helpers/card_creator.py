from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import textwrap
import random

CARD_WIDTH = 300
CARD_HEIGHT = 480

IMG_OFFSET_Y = 70
IMG_SIZE = 230

BIG_FONT = ImageFont.truetype(font='calibril.ttf', size=30)
SMALL_FONT = ImageFont.truetype(font='calibril.ttf', size=16)


def centre_text_X(text: str, y: int, img_width: int, img_draw: ImageDraw.ImageDraw, font: ImageFont.ImageFont) -> "tuple[int, int]":
    text_length = img_draw.textlength(text, font)
    return ((img_width - text_length) // 2, y)


def create_card_image(card_name, card_type, card_color, image_url, desc1, desc2 = None, atk = 0, hp = 0) -> str:
    print("create_card function called")
    card = Image.new('RGB', (300, 480), (255, 255, 255))
    draw = ImageDraw.Draw(card)

    # print("drawing text")
    draw.text(centre_text_X(card_name, 10, CARD_WIDTH, draw, BIG_FONT), text=card_name, fill=(0,0,0), font=BIG_FONT)
    draw.text(centre_text_X(card_color + " " + card_type, 45, CARD_WIDTH, draw, SMALL_FONT), text=card_color + " " + card_type, fill=(0,0,0), font=SMALL_FONT)

    # print("getting image from url")
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    print("Image format is", img.format)
    img = img.resize((IMG_SIZE, IMG_SIZE))
    # print("got image from url")

    card.paste(im=img, box=(35, IMG_OFFSET_Y, 35 + IMG_SIZE, IMG_OFFSET_Y + IMG_SIZE), mask=img)

    desc1_wrapped = textwrap.wrap(desc1, width=40)
    draw.text((10, 310), "\n".join(desc1_wrapped), fill=(0,0,0), font=SMALL_FONT)
    if desc2:
        desc2_wrapped = textwrap.wrap(desc2, width=40)
        draw.text((10, 360), "\n".join(desc2_wrapped), fill=(0,0,0), font=SMALL_FONT)

    if hp:
        draw.text((10, 450), f"ATK: {atk}", fill=(0,0,0), font=BIG_FONT)
        draw.text((180, 450), f"HP: {atk}", fill=(0,0,0), font=BIG_FONT)

    filename = ''.join([str(random.randint(0, 9)) for i in range(10)])
    
    print(f"card saved to {filename}.png")
    card.save(filename + ".png", "PNG")
    return filename + ".png"
    

if __name__ == "__main__":
    create_card_image(
        card_name = "Bobby",
        card_type = "Flairwarrior",
        card_color = "Green",
        image_url="https://media.discordapp.net/attachments/740797559433330708/1097921520917037226/d30pjoz-fc7284c5-06f0-4e78-bfd6-38756021f5f7.png",
        desc1 = "Steamroll: Whenever you initiate combat, deal 3 damage to a flairwarrior in this lane.",
        atk=3,
        hp=2
        )