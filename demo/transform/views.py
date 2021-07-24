import base64
import json
import cv2
import numpy as np
from datetime import datetime, date
from django.views import View
from django.http import JsonResponse, HttpResponseForbidden
import os
import random
import shutil


# 输入：sketch图像 (h*w*3 的numpy数组)， dilation value l (l属于[0,1])，3个属性 (格式为 [0, 0, 0]，即一个列表，每一位代表一个属性)；
# 性别：男性为1，女性为0；
# 发色：黑发为1，非黑发为0；
# 皮肤：白皙为1，非白皙为0；

# 输出：RGB图像 (h*w*3的numpy数组)；

def generate(sketch, dilation=0.0, sex=1, hair_color=1, skin=1):
    return sketch


class Transform(View):
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'input_image', 'dilation', 'sex', 'hair_color', 'skin'}:
            return JsonResponse({'status': 1, 'output_image': ''})
        input_image = str(kwargs['input_image'])

        dilation = float(kwargs['dilation'])
        sex = int(kwargs['sex'])
        hair_color = int(kwargs['hair_color'])
        skin = int(kwargs['skin'])

        # 图片 base64 编码转 nd_array
        img_data = base64.b64decode(input_image.split(',')[-1])
        np_arr = np.fromstring(img_data, np.uint8)
        img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # 生成转化后的图片
        generated_img = generate(img_np, dilation, sex, hair_color, skin)

        # 图片转 base64 编码
        ret_val, buffer = cv2.imencode('.jpg', generated_img)
        pic_str = base64.b64encode(buffer)

        # pic_str = pic_str.decode()
        return JsonResponse({'status': 200, 'output_image': str(pic_str)})
