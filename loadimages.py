import sqlite3 as sql
import vk_api
import requests

token = 'b370bdfb6bbda4c683c6cee8996e4dd20f8db524eb68cf782867698a1d3125ab490138448e27d3e3798c6'

vk_session = vk_api.VkApi(token = token)

connection = sql.connect('./base.sqlite', check_same_thread=False)
bd = connection.cursor()

bd.execute('CREATE TABLE IF NOT EXISTS cards (key, tags)')

file = open('./words.txt', 'r')
values = file.read().split('\n')

for n in range(1, 99):
    server = vk_session.method('photos.getMessagesUploadServer')
    upload = requests.post(server['upload_url'], files={'photo':open(f'./images/{n}.jpg', 'rb')}).json()
    image = vk_session.method('photos.saveMessagesPhoto', dict(
        photo=upload['photo'],
        hash=upload['hash'],
        server=upload['server']
    ))
    key = f'photo{str(image[0]["owner_id"])}_{str(image[0]["id"])}'
    tags = values[n-1].split('	')[1]
    print(key, tags)
    bd.execute('INSERT INTO cards (key, tags) VALUES (?, ?)', (key, tags))
    connection.commit()

req = bd.execute('SELECT * FROM cards')
res = req.fetchall()
print(res)

connection.commit()
connection.close()