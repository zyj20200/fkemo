import random
import requests

base_url = 'http://127.0.0.1:8000'


# 生成随机用户
def random_username(n=10):
    # 生成随机n个用户
    # {
    #     "phone_number": "15811110001",
    #     "password": "123456",
    #     "nickname": "测试1"
    # }
    user_info = []
    for i in range(n):
        phone_number = '158' + ''.join(random.sample('0123456789', 8))
        password = '123456'
        nickname = '测试' + phone_number[-4:]
        data = {
            'phone_number': phone_number,
            'password': password,
            'nickname': nickname
        }
        user_info.append(data)
    return user_info


# 生成随机帖子
def random_post(n=10):
    # 生成随机n个帖子
    # {
    #     "content": "这是一条测试帖子",
    # }
    post_info = []
    for i in range(n):
        content = '这是一条测试帖子' + str(i)
        data = {
            'content': content,
        }
        post_info.append(data)
    return post_info


# 生成随机评论
def random_comment(n=10):
    # 生成随机n个评论
    # {
    #     "content": "这是一条测试评论",
    #     "nickname": "测试1"
    # }
    comment_info = []
    for i in range(n):
        data = {
            'content': '这是一条测试评论' + str(i),
            'nickname': '匿名用户' + str(i)
        }
        comment_info.append(data)
    return comment_info


def register(data):
    url = base_url + '/register'
    print(data)
    response = requests.post(url, json=data)
    print(response.json())


def login(data):
    url = base_url + '/login'
    username = data['phone_number']
    password = data['password']
    # body form-data
    response = requests.post(url, data={'username': username, 'password': password})
    print(response.json())
    return response.json()['access_token']


def create_post(data, token):
    url = base_url + '/post'
    headers = {
        'Authorization': 'Bearer ' + token
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())


def create_comment(data, post_id):
    url = base_url + '/comment'
    params = {"post_id": post_id}
    response = requests.post(url, json=data, params=params)
    print(response.json())


if __name__ == '__main__':
    # 注册用户
    user_info = random_username(2)
    for user in user_info:
        register(user)

    # 登录
    for user in user_info:
        access_token = login(user)
        # 发帖
        post_info = random_post(3)
        for post in post_info:
            create_post(post, access_token)

    # 评论
    comment_info = random_comment(5)
    for comment in comment_info:
        create_comment(comment, 1)
