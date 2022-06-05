import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import sqlite3 as sql
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import baseHandler
import helpers
import json

token = 'b370bdfb6bbda4c683c6cee8996e4dd20f8db524eb68cf782867698a1d3125ab490138448e27d3e3798c6'

vk_session = vk_api.VkApi(token = token)
longpoll = VkBotLongPoll(vk_session, 213729348)
vk = vk_session.get_api()

def handler():
    try:
        for event in longpoll.listen():
            try:
                userid = event.message.peer_id
                if not baseHandler.userIsExist(event.message.peer_id):
                    baseHandler.startUser(event.message.peer_id)

                text = event.message.text
                if baseHandler.getUserAnswer(userid) == 0:
                    if text in ['Старт','Ещё раз']:
                        collection = baseHandler.getRandCollection(5)
                        vk_session.method('messages.send', dict(
                            random_id=0,
                            peer_id=event.message.peer_id,
                            attachment=','.join([i[0] for i in collection])
                        ))
                        card = helpers.choiceCard(collection)
                        baseHandler.setAnswer(event.message.peer_id, card['ans'])
                        vk_session.method('messages.send', dict(
                            random_id=0,
                            peer_id=event.message.peer_id,
                            message=card['tag'],
                            keyboard=json.dumps({
                                'one_time':True,
                                "buttons":[
                                    [
                                        {
                                            "action": {
                                                "type": "text",
                                                "label": "1"
                                            },
                                            "color": "primary"
                                        },
                                        {
                                            "action": {
                                                "type": "text",
                                                "label": "2"
                                            },
                                            "color": "primary"
                                        }
                                    ],
                                    [
                                        {
                                            "action": {
                                                "type": "text",
                                                "label": "3"
                                            },
                                            "color": "primary"
                                        },
                                        {
                                            "action": {
                                                "type": "text",
                                                "label": "4"
                                            },
                                            "color": "primary"
                                        },
                                        {
                                            "action": {
                                                "type": "text",
                                                "label": "5"
                                            },
                                            "color": "primary"
                                        }
                                    ]
                                ]
                            })
                        ))
                else:
                    if text == str(baseHandler.getUserAnswer(userid)):
                        baseHandler.addRating(userid, 3)
                        baseHandler.setAnswer(event.message.peer_id, 0)
                        rating = baseHandler.getRating(userid)
                        vk_session.method('messages.send', dict(
                            random_id=0,
                            peer_id=event.message.peer_id,
                            message=f'Отлично! Ваш рейтинг: {rating}',
                            keyboard=json.dumps({
                                "one_time":True,
                                "buttons":[
                                    [
                                        {
                                            "action": {
                                                "type": "text",
                                                "label": "Ещё раз"
                                            },
                                            "color": "primary"
                                        },
                                    ]
                                ]
                            })
                        ))
                    else:
                        baseHandler.setAnswer(event.message.peer_id, 0)
                        rating = baseHandler.getRating(userid)
                        vk_session.method('messages.send', dict(
                            random_id=0,
                            peer_id=event.message.peer_id,
                            message=f'Мимо! Ответ неверный. Ваш рейтинг: {rating}',
                            keyboard=json.dumps({
                                "one_time": True,
                                "buttons": [
                                    [
                                        {
                                            "action": {
                                                "type": "text",
                                                "label": "Ещё раз"
                                            },
                                            "color": "primary"
                                        },
                                    ]
                                ]
                            })
                        ))
            except Exception as err:
                print(err)
    except Exception as err:
        handler()
        print(err)

if __name__ == '__main__':
    handler()