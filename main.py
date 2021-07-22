#!/usr/bin/env python
# encoding: utf-8

from fastapi import FastAPI, File, UploadFile
from typing import Optional
import numpy as np
from PIL import Image
from io import BytesIO
import time
import requests
from pydantic import BaseModel
from configparser import ConfigParser
from fastapi.middleware.cors import CORSMiddleware
cfg = ConfigParser()
cfg.read('config.ini')
local_path = cfg.get('common','local_path')
url_path = cfg.get('common','url_path')

app = FastAPI()

#@app.get("/test/")
#def read_root():
#    return {"message": "Hello World"}

app.add_middleware(
    CORSMiddleware,
    # 设置允许的url， * 表示全部
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_image_into_numpy_array(data):
    return np.array(Image.open(BytesIO(data)))

def stack_image(src_im, width, height, stack_times):
    src_im = Image.fromarray(src_im)
    size = src_im.size
    dst_im = Image.new("RGBA", (width ,height), "white" )
    im = src_im.convert('RGBA')
    # 添加阴影
    img_new = Image.new('RGBA', (size[0]+2, size[1]+2), (80, 80, 80))
    img_new.paste(im, (1, 1, size[0]+1, size[1]+1))
    i1 = 0
    i2 = 0
    # 铺底
    while i1 < width:
        while i2 < height:
            dst_im.paste(im, (i1 , i2), im)
            i2 += size[1]
        i1 += size[0]
        i2 = 0
    # 随机角度，随机位置
    for i in range(stack_times):
        ra=np.random.randint(0,360)
        rot = img_new.rotate( ra, expand=1 )
        h = np.random.randint(-1/2 * height, height + height * 1/2)
        w = np.random.randint(-1/2 * width, width + width * 1/2)
        dst_im.paste( rot, ( h , w), rot )
    file_name = 'stack'+str(int(time.time())) + '.png'
    output = local_path + file_name
    dst_im.save( output )
    target_url = url_path + file_name
    return target_url

class Item(BaseModel):
    image_url: str
    width: Optional[int] = 2000
    height: Optional[int] = 1000
    stack_times: Optional[int] = 200

@app.post("/stack_url/")
async def dollar_stack_url(item: Item):
    if not item.image_url:
        return {"status": "Error", 'target_url': None, 'message': 'url is None!'}
    res = requests.get(item.image_url)
    if res.status_code == 200:
        try:
            src_im = np.array(Image.open(BytesIO(res.content)))
            target_url = stack_image(src_im, item.width, item.height, item.stack_times)
            return {"status": "Success", 'target_url': target_url}
        except:
            return {"status": "Error", 'target_url': None, 'message': 'can not get image file from url'}
    else:
        return {"status": "Error", 'target_url': None, 'message': 'image response code:' +str(res)}



@app.post("/stack/")
async def dollar_stack(my_file: UploadFile = File(...), width: Optional[int] = 2000, height: Optional[int] = 1000, stack_times: Optional[int] = 200):
    src_im = load_image_into_numpy_array(await my_file.read())
    #src_im = Image.open(my_file)
    target_url = stack_image(src_im, width, height, stack_times)
    return {"status": "Success", 'target_url': target_url}


