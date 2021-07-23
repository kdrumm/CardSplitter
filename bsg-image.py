

import argparse
import pathlib
from PIL import Image, ImageOps
import os
import json

def parse_args():
    parser = argparse.ArgumentParser(description='Create images from sprite')
    parser.add_argument(
        'config',
        type=str,
        help='config')
    parser.add_argument(
        '--width',
        type=int,
        default=256,
        help='width of final image')
    parser.add_argument(
        '--height',
        type=str,
        default=None,
        help='height of final image')
    parser.add_argument(
        '--border',
        type=int,
        default=0,
        help='border around image')
    
    return parser.parse_args()

def splitImage(args, file, config, settings):
    rows=config.get('rows',1)
    columns=config.get('columns',1)
    sprite=pathlib.Path(file)
    source=Image.open(sprite)
    dy=source.height/rows
    dx=source.width/columns
    
    
    count=0
    border = config.get('border', args.border)
    width = config.get('width', args.width)
    height = config.get('height')
    dest = "dest/"+settings.get('dest','def')
    num_images = config.get('num', None)
    try :
        os.mkdir(dest)
    except:
        None

    if config.get('cardback', False):
        None
    
    ratio=dy / dx
    w=width
    h=height or int(width * ratio)

    num_def=1

    for y in range(rows):
        for x in range(columns):
            num_to_create=config.get(f"{y}-{x}", num_def)
            print(f"creating {num_to_create} at {y} {x}")
            if (num_to_create > 0):
                px=dx*x
                py=dy*y
                card=source.crop((px,py,dx+px,dy+py))
                card=card.resize((w,h))
                if (border > 0):
                    card = ImageOps.expand(card, border=border, fill='white')
                for n in range(num_to_create):
                    card.putpixel((0,0),(x%256,y%256,n%256))
                    card.save(f"{dest}/{sprite.name}-{y}-{x}-{n}.png", "png")
                count+=1
            
            if num_images is not None and count >= num_images:
                num_def = 0

def main():
    args = parse_args()
    with open("config/"+args.config) as cfg:
        config_data = json.load(cfg)
    settings=config_data.get('settings', {})
    files = config_data.get('files',{})
    for file in files.keys():
        path=pathlib.Path(file)
        c= files.get(file, None)
        splitImage(args,path.as_posix(),c, settings)
    


if __name__ == "__main__":
    main()