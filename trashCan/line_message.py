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
# from linebot import LineBotApi



# ------------------------------------------------------------------------------- #
# 共通変数 
# ------------------------------------------------------------------------------- #
REPLY_ENDPOINT_URL = ""
ACCESSTOKEN = "3bPtYS6igNdrunIz2LiCf+BypRt32b3Rk+705kTCYBdROU5A1sx+r8eMtBZuLiKZFuoWv58ckBGhmUG74f+Wy0olUArUFD2DIO1ejO18brEfWKyMJSX2Z5QPcVVV7T/IrdXCF2NNWW2nA/Ia/JnZ8QdB04t89/1O/w1cDnyilFU="
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
