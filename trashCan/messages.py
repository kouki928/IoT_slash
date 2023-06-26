# ------------------------------------------------------------------------------ #
# create_message.py                                                           
# 株式会社Reizoko : HousingFukuiCorporationBot作成                                                
#
# 本ファイルが行う処理の全体概要の説明：                                            
# LINE Botに反映するメッセージを作成する。LINE側が読み込めるJSON形式に変換するのがメイン  
#  
# ------------------------------------------------------------------------------- #
# 番号　更新内容                                                  更新日     更新者   #
# ------------------------------------------------------------------------------- #
# 0000 新規作成                                             2022/07/04    古川幸樹  #
# ------------------------------------------------------------------------------- #
# 0001 カルーセルメッセージ編集                                2022/07/05    古川幸樹  #
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
# import ファイル
# ------------------------------------------------------------------------------- #
from IoT.settings import STATIC_ROOT



# ------------------------------------------------------------------------------- #
# 変数名 : MANAGEMENT_BUTTON_MESSAGE
#
# 機能説明：
# 通知と共に表示されるボタンメッセージ。
# ボタンは2つ設置し、それぞれ来店予約と写真で相談を管理する画面へと飛ぶようにする。
# ------------------------------------------------------------------------------- #
MANAGEMENT_BUTTON_MESSAGE = {

    "type" : "bubble",

    "body" : {
        "type"     : "box",
        "layout"   : "vertical",
        "contents" : [
        {
            "type": "text",
            "text": "ゴミ袋を変えたらボタンを押してください",
            "wrap": True,
            "style": "normal",
            "weight": "bold",
            "align": "start"
        }
        ]
    },

    "footer" : {
        "type"     : "box",
        "layout"   : "vertical",
        "contents" : [
        {
            "type"   : "button",
            "action" : {
                "type"  : "postback",
                "label" : "Yes",
                "data"  : "changed",
                "displayText"  : "お疲れさまでした！"
            }
        },
        ]
    }
}







# ---------------------------------------------------------------------------------------- #
# 変数名 : CHECK_ADDRESS_MESSAGE
#
# 設置理由 :
# 施工地以外から来店予約されるのを防ぐため。
# ---------------------------------------------------------------------------------------- #
CHECK_ADDRESS_MESSAGE = {

    "type" : "bubble",

    "body" : {
        "type"     : "box",
        "layout"   : "vertical",
        "contents" : [
            {
                "type": "text",
                "text": "お住まいはどこにゃ？",
                "wrap": True,
                "style": "normal",
                "weight": "bold",
                "align": "start"
            }
        ]
    },

    "footer" : {
        "type"     : "box",
        "layout"   : "vertical",
        "contents" : [
            {
                "type"   : "button",
                "action" : {
                    "type"  : "postback",
                    "data"  : "fukui",
                    "label" : "福井県"
                }
            },
            {
                "type"   : "button",
                "action" : {
                    "type"  : "postback",
                    "data"  : "shiga",
                    "label" : "滋賀県北部"
                }
            },
            {
                "type"   : "button",
                "action" : {
                    "type"  : "postback",
                    "data"  : "other",
                    "inputOption": "openRichMenu",
                    "label" : "その他の地域"
                }
            }
        ]
    }


}




# ---------------------------------------------------------------------------------------- #
# 変数名 : AGREEMENT_MESSAGE
#
# 設置理由 :
# 最終確認とメッセージが流れないようにするため。
# ---------------------------------------------------------------------------------------- #
AGREEMENT_MESSAGE = {
    "type" : "bubble",

    "body" : {
        "type"     : "box",
        "layout"   : "vertical",
        "contents" : [
            {
                "type": "text",
                "text": "※施工エリア外の可能性もございます。施工エリア外だった場合は、来店予約後にこちらからご連絡いたしますのでご了承ください。",
                "wrap": True,
                "style": "normal",
                "size" : "sm",
                "align": "start"
            }
        ]
    },

    "footer" : {
        "type"     : "box",
        "layout"   : "vertical",
        "contents" : [
            {
                "type"   : "button",
                "action" : {
                    "type"  : "postback",
                    "data"  : "fukui",
                    "label" : "確認"
                }
            }
        ]
    }
}





# ---------------------------------------------------------------------------------------- #
# 関数名: carouselMessage
# 引数: Dict
# 戻り値: JSON
# 
# 機能説明: 
# 引数に応じてカルーセルメッセージのJSONを返す
# ---------------------------------------------------------------------------------------- #
def carouselMessage(messageSource):
    """
    カルーセルメッセージ用のJSONを出力する関数。

    messageSource -> List型。PRODUCT_KEYS を参照。
    """

    # メッセージの土台 ---------------------------------------------------------------------------------------- #
    message = {
        "type": "carousel",
        "contents": []
    }

    if messageSource[0]["reservation"]:
        message["contents"].append({
            "type" : "bubble",
            "size" : "kilo",
            "hero" : {
                "type" : "image",
                "url"  : "https://housing-fukui.herokuapp.com/static/HousingFukuiCorporationBot/image/" + str(len(messageSource)) + ".png",
                "size" : "full",
                "aspectRatio": "20:30",
            }
        })

    if messageSource[0]["name"] == "「商品を探して相談」":

        for idx,source in enumerate(messageSource):

            message["contents"].append(
                {
                    "type" : "bubble",
                    "size" : "kilo",

                    "hero" : {
                        "type" : "image",
                        "url"  : source["image"],
                        "size" : "full",
                        "aspectMode": "cover",
                        "aspectRatio": "20:11",
                        "position": "relative"
                    },

                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "postback",
                                "label": "すすむ",
                                "data": source["data"],
                                "displayText": "{}を選択".format(source["name"])
                            }
                        }
                        ]
                    }
                }
            )

    else:

        # 引数を元にして作成 ---------------------------------------------------------------------------------------- #
        for idx,source in enumerate(messageSource):
            

            # 一番最後か --------------------------------------------------------------------------------------- #
            if source["reservation"]:
                message["contents"].append(
                    {
                        "type": "bubble",
                        "size": "kilo",

                        
                        # ヘッダー ------------------------------------------------------------------ #
                        "hero": {
                            "type": "image",
                            "url": source["image"],
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "fit",
                            "action": {
                                "type": "uri",
                                "uri": source["url"]
                            }
                        },
                        

                        # ボディ ----------------------------------------------------------------------- #
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "weight": "bold",
                                "size": "xl",
                                "text": source["name"],
                                "wrap": True,
                            },
                            {
                                "type": "text",
                                "weight": "regular",
                                "style": "normal",
                                "text": source["text"],
                                "wrap" : True
                            }
                            ]
                        },

                        # フッター -------------------------------------------------------------- #
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {
                                "type": "uri",
                                "label": "商品詳細はこちら",
                                "uri": source["url"],
                                }
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {
                                "type": "uri",
                                "uri": "https://liff.line.me/1657271805-l52r7ay9",
                                "label": "LINEで来店予約"
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "margin": "sm"
                            }
                            ],
                            "flex": 0
                        }
                    }
                )


            # 一番最後以外の選択肢 ----------------------------------------------------------------------------------------- #
            else:

                message["contents"].append({
                    "type": "bubble",
                    "size": "kilo",
                    "hero": {
                        "type": "image",
                        "url": source["image"],
                        "position": "relative",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "align": "center",
                        "aspectMode": "cover" if source["name"] not in ["アール屋根","フラット屋根"] else "fit"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": source["text"],
                            "weight": "regular",
                            "size": "md",
                            "style": "normal",
                            "align": "start",
                            "wrap": True
                        },
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "height": "sm",
                            "action": {
                                "type": "postback",
                                "label": "すすむ",
                                "data": source["data"],
                                "displayText": "{}を選択".format(source["name"])
                            }
                        }
                        ]
                    }
                })


    return message




# ---------------------------------------------------------------------------------------- #
# 関数名: prepareText
# 引数: messages(list)
# 戻り値: List
# 
# 機能説明: 
# 送信したいメッセージを適した形に変形する。
# ---------------------------------------------------------------------------------------- #
def prepareText(messages):
    """
    messages(list型) をLINEに送信できる形に整える。
    """

    # messages を順番に整える -------------------------------------------------------------- #
    result = [] # JSONを入れる

    for message in messages:

        result.append({
            "type" : "text",
            "text" : message
        })

    # 処理終了 ---------------------------------------------------------------------------- #
    return result




