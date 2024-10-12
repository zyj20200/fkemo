# 创建兴趣类别 & 粉丝类型
import random
import requests


base_url = 'http://127.0.0.1:8000'

interests = ['科技', '文化', '生活', '娱乐', '体育', '教育', '财经', '汽车', '旅游', '美食']
fans_type = ['教师', '键盘侠', '码农', '机车', '喷子', '二次元', '道友', '赛博朋克', '搞笑', '感性']


def create_interest_category():
    for interest in interests:
        data = {
            'name': interest
        }
        response = requests.post(base_url + '/interest_categories', json=data)
        print(response.json())


def create_fan_type():
    for fan_type in fans_type:
        data = {
            'name': fan_type
        }
        response = requests.post(base_url + '/fan_types', json=data)
        print(response.json())


if __name__ == '__main__':
    create_interest_category()
    create_fan_type()