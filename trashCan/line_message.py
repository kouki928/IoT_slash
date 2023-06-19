# ------------------------------------------------------------------------------ #
# line_message.py                                                           
# 株式会社Reizoko : 株式会社ハウジング福井様のLINE Bot開発                                                
#
# 本ファイルが行う処理の全体概要の説明：                                            
# LINE Bot からメッセージを送信するための関数をまとめたファイル。
# ------------------------------------------------------------------------------- #
# 番号　更新内容                                                  更新日     更新者   #
# ------------------------------------------------------------------------------- #
# 0000 新規作成                                             2022/07/04    古川幸樹  #
# ------------------------------------------------------------------------------- #
# 0001 クラス解体                                           2022/08/28    古川幸樹  #
# ------------------------------------------------------------------------------- #
#
# ------------------------------------------------------------------------------- #



# ------------------------------------------------------------------------------- #
# import ファイル
# ------------------------------------------------------------------------------- #
import urllib.request
import json
from IoT.settings import STATIC_URL
from linebot import LineBotApi



# ------------------------------------------------------------------------------- #
# 共通変数 
# ------------------------------------------------------------------------------- #
REPLY_ENDPOINT_URL = ""
ACCESSTOKEN = "KtWWC+Kb9/5LUcrLunX8PYcBuQlG3yjWSdDgYREi2vBH02YmrueXeE/LIlfMnt6X9MVYcix5PY6fUdrEhRSE+tHEnMaq8a+OrjjoAc9bVM8QtzMen1dZkQpCcQ669HdwQog7p5Yhql8gjlKF2BQ7CAdB04t89/1O/w1cDnyilFU="
HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + ACCESSTOKEN
}





# -------------------------------------------------------------------------------------------------------------- #
# LINE にメッセージを送るための関数群
# -------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------------------------- #
# 関数名；reply_messages
# 引数：messages, replyToken
# 戻り値：なし
#
# 機能説明：
# replyToken を使って、ユーザーのアクションに対して messages を返信する関数
# ------------------------------------------------------------------------------- #
def reply_messages(messages, replyToken):
    """
    ユーザーの応答をキーに返信する。
    messages   : リスト型。messages.py prepareText関数で作成する。
    replyToken : str型. events[i][replyToken]から取得
    """

    # リクエストの準備 ----------------------------------------------------------------------------------------------- #
    REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/reply"
    body = {
        'replyToken' : replyToken,
        'messages'   : messages
    }

    # リクエスト送信して処理終了 ------------------------------------------------------------------------ #
    req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
    send_request(req)
    return -1






# ------------------------------------------------------------------------------- #
# 関数名 : reply_flex_message
# 引数　 : address, replyToken, lavel, messages
# 戻り値 : なし
#
# 機能説明：
# ユーザーの応答をキーにしてflexMessageを replyToken を使って、address に送る関数
# ------------------------------------------------------------------------------- #
def reply_flex_message(address, replyToken, label, messages):
    """
    ユーザーの応答をキーにflexMessageを送信する。

    address    : str型。userId や groupId
    replyToken : str型. events[i][replyToken]から取得
    label      : str型。メッセージが届いた時の通知の表示
    messages   : List型。messages.py carouselMessage関数で作成
    """

    # リクエストの準備 -------------------------------------------------------------------------------------------- #
    REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/reply"
    body = {
        "to"        : address,
        "replyToken": replyToken,
        "messages"  : [
            {
                "type"     : "flex",
                "altText"  : label,
                "contents" : messages
            }
        ]
    }

    # リクエスト送信して処理終了 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
    req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
    send_request(req)
    return -1





# ------------------------------------------------------------------------------- #
# 関数名 : push_message
# 引数　 : address, messages
# 戻り値 : なし
#
# 機能説明：
# こちらから一方的に address に messages を送る関数
# ------------------------------------------------------------------------------- #
def push_message(address, messages):
    """
    ユーザー関係なしに一方的にメッセージを送る

    address  : str型. events[i][source][~Id]から取得
    messages : List型. messages.py prepareText関数で作成
    """

    # リクエストの準備 --------------------------------------------------------------------------------- #
    REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/push"
    body = {
        "to"       : address,
        "messages" : messages
    }

    # リクエスト送信して処理終了 --------------------------------------------------------------------------------------- #
    req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
    send_request(req)
    return -1





# ------------------------------------------------------------------------------- #
# 関数名 : push_flex_message
# 引数　 : address, label, messages
# 戻り値 : なし
#
# 機能説明：
# こちらから一方的に address に flexMessages を送る関数
# ------------------------------------------------------------------------------- #
def push_flex_message(address, label, messages):
    """
    ユーザー関係なしに一方的にflexMessageを送る

    address  : str型. events[i][source][~Id]から取得
    label    : str型。通知の表示メッセージ
    messages : List型. messages.py carouselMessage関数などで作成
    """

    # リクエストの準備 -------------------------------------------------------------------------------------- #
    REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/push"
    body = {
        "to"       : address,
        "messages" : [
            {
                "type"     : "flex",
                "altText"  : label,
                "contents" : messages
            }
        ]
    }

    # リクエスト送信して処理終了 ---------------------------------------------------------------------------------- #
    req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
    send_request(req)
    return -1





# -------------------------------------------------------------------------------------------------------------- #
# Bot の入退室に関わる処理を行う関数
# -------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------------------------- #
# 関数名；leave_group
# 引数：groupId
# 戻り値：なし
#
# 機能説明：
# 管理グループとgroupIdが異なるグループに参加した場合、Botを退出させる関数
# ------------------------------------------------------------------------------- #
def leave_group(groupId):
    """
    グループから退出する。
    """

    # リクエストの準備 ---------------------------------------------------------------- #
    REPLY_ENDPOINT_URL = f"https://api.line.me/v2/bot/group/{groupId}/leave"
    req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps({}).encode(), HEADER)

    # リクエストして処理終了 ------------------------------------------------------------ #
    send_request(req)
    return -1




# ------------------------------------------------------------------------------- #
# 関数名；leave_room
# 引数：roomId
# 戻り値：なし
#
# 機能説明：
# 複数人トークに参加した場合、Botに退出させる関数
# ------------------------------------------------------------------------------- #
def leave_room(roomId):
    """
    複数人トークから退出する。
    """

    # リクエストの準備 ---------------------------------------------------------------- #
    REPLY_ENDPOINT_URL = f"https://api.line.me/v2/bot/room/{roomId}/leave"
    req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps({}).encode(), HEADER)

    # リクエストして処理終了 ------------------------------------------------------------ #
    send_request(req)
    return -1







# -------------------------------------------------------------------------------------------------------------- #
# LINE にリクエストして情報を得る関数郡
# -------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
# 関数名：send_request
# 引数：req
# 戻り値：なし
#
# 機能説明：
# リクエストするための関数。引数 req をリクエストする
# ------------------------------------------------------------------------------- #
def send_request(req):

    # 失敗したらエラーメッセージを表示する ------------------------------------------------------  #
    try:
        with urllib.request.urlopen(req) as res:
            res.read()
    except urllib.error.HTTPError as err:
        print(err)
    except urllib.error.URLError as err:
        print(err.reason)

    # 処理終了 ---------------------------------------------------------------------------- #
    return -1





# ------------------------------------------------------------------------------- #
# 関数名 : get_image
# 引数　 : messageId
# 戻り値 : image_name
#
# 機能説明：
# 画像メッセージを受け取った時、その画像の情報を得るための関数。
# ------------------------------------------------------------------------------- #
def get_image(messageId) -> None:
    """
    画像をダウンロードして名前付けする関数

    messageId : 画像メッセージのId
    """

    # 画像データを取得 ----------------------------------------------------------- #
    line_bot_api = LineBotApi(ACCESSTOKEN)
    message_content = line_bot_api.get_message_content(messageId)

    image_name = randomStr(30)
    image_path = "HousingFukuiCorporationBot/static/HousingFukuiCorporationBot/image/" + image_name + ".jpg"
    # 画像を保存 ---------------------------------------------------------------- #
    # with open(image_path, "wb") as f:
    #     for chunk in message_content.iter_content():
    #         f.write(chunk)

    # image_nameを返して処理終了 ------------------------------------------------- #
    # return image_name
    binary_base64 = base64.b64encode(message_content.content).decode("utf-8")

    return binary_base64




# ------------------------------------------------------------------------------- #
# クラス名；LINEMessage
# 引数：messages(dict), message_type(str)
#
# 機能説明：
# LINEBotからユーザーにメッセージを送信するための関数をまとめたクラス。
# メッセージのjsonと送信タイプを指定して初期化する。
# ------------------------------------------------------------------------------- #
# class LINEMessage():

#     # 初期化 -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
#     def __init__(self, messages, message_type):
#         """
#         初期化する。
#         messages: dict型. messages.pyで生成したjsonを入れる
#         message_type: str型. push かそれ以外で判断
#         """

#         # 送信に使う素材 -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
#         self.messages = messages
#         self.REPLY_ENDPOINT_URL = ""

#         if message_type == "push":
#             self.REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/push"
#         else:
#             self.REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/reply"

#         self.ACCESSTOKEN = "KtWWC+Kb9/5LUcrLunX8PYcBuQlG3yjWSdDgYREi2vBH02YmrueXeE/LIlfMnt6X9MVYcix5PY6fUdrEhRSE+tHEnMaq8a+OrjjoAc9bVM8QtzMen1dZkQpCcQ669HdwQog7p5Yhql8gjlKF2BQ7CAdB04t89/1O/w1cDnyilFU="
#         self.HEADER = {
#             'Content-Type': 'application/json',
#             'Authorization': 'Bearer ' + self.ACCESSTOKEN
#             }


#     # ユーザーに返信 -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
#     def reply_messages(self, replyToken):
#         """
#         ユーザーの応答をキーに返信する。
#         replyToken: str型. events[i][replyToken]から取得
#         """

#         # 返信用body --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
#         body = {
#             'replyToken': replyToken,
#             'messages': self.messages
#         }

#         # リクエスト送信して処理終了 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
#         req = urllib.request.Request(self.REPLY_ENDPOINT_URL, json.dumps(body).encode(), self.HEADER)
#         self.send_request(req)
#         return


#     # flexMessageをユーザーに返信 ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
#     def reply_flex_message(self, userId, replyToken):
#         """
#         ユーザーの応答をキーにflexMessageを送信する。
#         userId: str型. events[i][source][userId]から取得
#         replyToken: str型. events[i][replyToken]から取得
#         """

#         # 返信用body --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
#         body = {
#             "to":userId,
#             "replyToken":replyToken,
#             "messages": [
#                 {
#                     "type":"flex",
#                     "altText": "This is a Flex Message",
#                     "contents": self.messages
#                 }
#             ]
#         }

#         # リクエスト送信して処理終了 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
#         req = urllib.request.Request(self.REPLY_ENDPOINT_URL, json.dumps(body).encode(), self.HEADER)
#         self.send_request(req)
#         return


#     # pushMessage を送信する ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
#     def push_message(self,address):
#         """
#         ユーザー関係なしに一方的にメッセージを送る
#         address: str型. events[i][source][~Id]から取得
#         """

#         # 返信用body --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
#         body = {
#             "to": address,
#             "messages": self.messages
#         }

#         # リクエスト送信して処理終了 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
#         req = urllib.request.Request(self.REPLY_ENDPOINT_URL, json.dumps(body).encode(), self.HEADER)
#         self.send_request(req)
#         return 


#     # flexMessageをユーザーの応答なしに送信 ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
#     def push_flex_message(self,userId):
#         """
#         ユーザー関係なしに一方的にflexMessageを送る
#         userId: str型. events[i][source][userId]から取得
#         """

#         # 返信用body --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
#         body = {
#             "to": userId,
#             "messages": [
#                 {
#                     "type": "flex",
#                     "altText": "メッセージが届いています!",
#                     "contents": self.messages
#                 }
#             ]
#         }

#         # リクエスト送信して処理終了 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #
#         req = urllib.request.Request(self.REPLY_ENDPOINT_URL, json.dumps(body).encode(), self.HEADER)
#         self.send_request(req)
#         return


#     # リクエスト送信 -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
#     def send_request(self,req):

#         # 失敗したらエラーメッセージを表示する ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
#         try:
#             with urllib.request.urlopen(req) as res:
#                 res.read()
#         except urllib.error.HTTPError as err:
#             print(err)
#         except urllib.error.URLError as err:
#             print(err.reason)


#     # 送られた画像のデータを取得する
#     def get_image(self,messageId):

#         line_bot_api = LineBotApi(self.ACCESSTOKEN)

#         message_content = line_bot_api.get_message_content(messageId)

#         # img = Image.open(BytesIO(message_content.content))
#         # img.show()
#         return message_content.content


#     def push_image(self,userId,image):

#         # 返信用body --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
#         body = {
#             "to": userId,
#             "messages": [
#                 {
#                     "type": "image",
#                     "originalContentUrl": "https://firebasestorage.googleapis.com/v0/b/housingfukuicorporationbot.appspot.com/o/download20220703011142.png?alt=media&token=b2ef0c48-7fee-45d9-8a42-f4f69db514cc",
#                     "previewImageUrl": "https://firebasestorage.googleapis.com/v0/b/housingfukuicorporationbot.appspot.com/o/download20220703011142.png?alt=media&token=b2ef0c48-7fee-45d9-8a42-f4f69db514cc",
#                 }
#             ]
#         }

#         req = urllib.request.Request(self.REPLY_ENDPOINT_URL, json.dumps(body).encode(), self.HEADER)
#         self.send_request(req)
#         return 
