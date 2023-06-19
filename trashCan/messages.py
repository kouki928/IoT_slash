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
MANEGEMENT_BUTTON_MESSAGE = {

    "type" : "bubble",

    "body" : {
        "type"     : "box",
        "layout"   : "vertical",
        "contents" : [
        {
            "type": "text",
            "text": "管理画面へは以下のボタンから進みます。",
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
                "type"  : "uri",
                "label" : "来店予約を確認",
                "uri"   : "https://liff.line.me/1657271805-VXAlbd43"
            }
        },
        {
            "type"   : "button",
            "action" : {
                "type"  : "uri",
                "uri"   : "https://liff.line.me/1657271805-RgDW6Z38",
                "label" : "写真を送って相談を確認"
            }
        }
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






# ---------------------------------------------------------------------------------------- #
# データを紐付けする変数
# 商品検索後の動きを具体化する。
# 
# やることメモ；
# ・前の質問に戻る、という質問を付け加える
# 
# ---------------------------------------------------------------------------------------- #
PRODUCT_KEYS = {

    # リッチメニューのボタン --------------------------------------------------------------------------------------- #
    "product_search":[
        {
            "name": "「商品を探して相談」",
            "text":"商品を探して相談",
            "image":"https://housing-fukui.herokuapp.com/static/HousingFukuiCorporationBot/image/Product.jpg",
            "data":"address_product",
            "reservation": False,
        },
        # {
        #     "name": "「お悩みから探す」",
        #     "text":"お悩みから探す",
        #     "image":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data":"problem",
        #     "reservation": False,
        # },
        {
            "name": "「写真を送って相談」",
            "text":"写真を送って相談",
            "image":"https://housing-fukui.herokuapp.com/static/HousingFukuiCorporationBot/image/Picure.jpg",
            "data":"picture",
            "reservation": False,
        }
    ],


    # 商品を探す --------------------------------------------------------------------------------------- #
    "product":[
        {
            "name": "カーポート",
            "text":"カーポート",
            "image":"https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&lpageid=10295830000&lx=39&ly=147&lw=324&lh=179",
            "data":"カーポート",
            "reservation": False,
        },
        {
            "name" : "物置",
            "text" : "物置",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_01.jpg",
            "data" : "物置",
            "reservation": False,
        },
        {
            "name": "フェンス",
            "text":"フェンス",
            "image":"https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/3534/x032_index_image_lineup_013.jpg",
            "data":"フェンス",
            "reservation": False,
        },
        {
            "name": "リウッドデッキ",
            "text":"リウッドデッキ",
            "image":"https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/9809/x097_index_image_lineup_01-001.jpg",
            "data":"基本セット",
            "reservation": False,
        },
        {
            "name" : "その他",
            "text" : "その他",
            "image":"https://housing-fukui.herokuapp.com/static/HousingFukuiCorporationBot/image/other.png",
            "data" : "その他",
            "reservation": False,
        },
    ],

    












    # カーポート ----------------------------------------------------------------------------------------- #
    "カーポート" : [
        {
            "name" : "折板屋根",
            "text" : "耐荷重性能を重視した「折板屋根」",
            "image": "https://www.ykkap.co.jp/consumer/satellite/products/articles/carport_textbook/02/image/img_06.png",
            "data" : "折板屋根",
            "reservation": False,
        },
        {
            "name" : "ポリカ屋根",
            "text" : "明るさを確保できる「ポリカ屋根」",
            "image": "https://www.ykkap.co.jp/consumer/satellite/products/articles/carport_textbook/02/image/img_05.png",
            "data" : "ポリカ屋根",
            "reservation": False,
        }
    ],


    # 折板屋根 ------------------------------------------------------------------------------------------- #
    "折板屋根" : [
        {
            "name" : "1台用",
            "text" : "1台用",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10595640000&designID=pro&lpageid=10596500000&lx=75&ly=137&lw=251&lh=170",
            "data" : "折板屋根1台用",
            "reservation": False,
        },
        {
            "name" : "2台用",
            "text" : "2台用",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/10996/lineup_02_XCH21678.jpg",
            "data" : "折板屋根2台用",
            "reservation": False,
        },
        {
            "name" : "3台用",
            "text" : "3台用",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10595640000&designID=pro&lpageid=10596580000&lx=32&ly=287&lw=337&lh=130",
            "data" : "折板屋根3台用",
            "reservation": False,
        },
    ],


    # 折板屋根1台用 ----------------------------------------------------------------------------------------------- #
    "折板屋根1台用" : [
        {
            "name" : "ジーポートPro 1台用",
            "text" : "折半屋根、1台用のカーポートです。",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10595640000&designID=pro&lpageid=10596500000&lx=75&ly=137&lw=251&lh=170",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/gport_pro",
            "data" : "reservation",
            "reservation": True,
        },
    ],


    # 折板屋根2台用 ----------------------------------------------------------------------------------------------- #
    "折板屋根2台用" : [
        {
            "name" : "ジーポートPro 2台用",
            "text" : "折半屋根、2台用のカーポートです。",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/10996/lineup_02_XCH21678.jpg",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/gport_pro",
            "data" : "reservation",
            "reservation": True,
        },
    ],


    # 折板屋根3台用 ----------------------------------------------------------------------------------------------- #
    "折板屋根3台用" : [
        {
            "name" : "ジーポートPro 3台用",
            "text" : "折半屋根、3台用のカーポートです。",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10595640000&designID=pro&lpageid=10596580000&lx=32&ly=287&lw=337&lh=130",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/gport_pro",
            "data" : "reservation",
            "reservation": True,
        }
    ],


    # ポリカ屋根 ------------------------------------------------------------------------------------------- #
    "ポリカ屋根" : [
        {
            "name" : "1台用",
            "text" : "1台用",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&lpageid=10295830000&lx=39&ly=147&lw=324&lh=179",
            "data" : "ポリカ屋根1台用",
            "reservation": False,
        },
        {
            "name" : "2台用",
            "text" : "2台用",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&lpageid=10295850000&lx=31&ly=145&lw=333&lh=189",
            "data" : "ポリカ屋根2台用",
            "reservation": False,
        },
        {
            "name" : "3台用",
            "text" : "3台用",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&lpageid=10295870000&lx=30&ly=145&lw=335&lh=187",
            "data" : "ポリカ屋根3台用",
            "reservation": False,
        },
    ],


    # ポリカ屋根1台用 ----------------------------------------------------------------------------------------------- #
    "ポリカ屋根1台用" : [
        {
            "name" : "エフルージュ ワン",
            "text" : "ポリカ屋根、1台用のカーポートです。",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&lpageid=10295830000&lx=39&ly=147&lw=324&lh=179",
            "url"  : "https://www.ykkap.co.jp/business/products/exterior/frouge",
            "data" : "reservation",
            "reservation": True,
        },
    ],


    # ポリカ屋根2台用 ----------------------------------------------------------------------------------------------- #
    "ポリカ屋根2台用" : [
        {
            "name" : "エフルージュ ツイン",
            "text" : "ポリカ屋根、2台用のカーポートです",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&lpageid=10295850000&lx=31&ly=145&lw=333&lh=189",
            "url"  : "https://www.ykkap.co.jp/business/products/exterior/frouge",
            "data" : "reservation",
            "reservation": True,
        },
    ],


    # ポリカ屋根3台用 ----------------------------------------------------------------------------------------------- #
    "ポリカ屋根3台用" : [
        {
            "name" : "エフルージュ トリプル",
            "text" : "ポリカ屋根、3台用のカーポートです。",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&lpageid=10295870000&lx=30&ly=145&lw=335&lh=187",
            "url"  : "https://www.ykkap.co.jp/business/products/exterior/frouge",
            "data" : "reservation",
            "reservation": True,
        }
    ],















    # フェンス -------------------------------------------------------------------------------------------------------- #
    "フェンス" : [
        {
            "name" : "アルミ",
            "text" : "住宅に合わせやすいシンプルデザインの「アルミ製」",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/3534/x032_index_image_lineup_013.jpg",
            "data" : "アルミ",
            "reservation": False,
        },
        {
            "name" : "樹脂",
            "text" : "木目仕様が特徴的な「樹脂製」",
            "image": "https://www.extile.co.jp/themes/extile/img/urbanfence_uv/img-main.jpg",
            "data" : "樹脂",
            "reservation": False,
        },
        {
            "name" : "スチール",
            "text" : "日当たりや通風を妨げず、開放感のある「スチール製」",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/8671/x081_index_image_lineup_01-001.jpg",
            "data" : "スチール",
            "reservation": False,
        },
        
    ],


    # アルミ ----------------------------------------------------------------------------------------------------------- #
    "アルミ" : [
        {
            "name" : "目隠しフェンス",
            "text" : "外からの視線をカットする「目隠しフェンス」",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/3534/x032_index_image_lineup_013.jpg",
            "data" : "目隠しフェンス",
            "reservation": False,
        },
        {
            "name" : "縦格子フェンス",
            "text" : "縦格子フェンス H600~H1000",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&rpageid=10293620000&rx=36&ry=109&rw=203&rh=115",
            "data" : "縦格子フェンスH600~H1000",
            "reservation": False,
        },
    ],


    # 目隠しフェンス　----------------------------------------------------------------------------------------------------------- #
    "目隠しフェンス" : [
        {
            "name" : "H600~H1600",
            "text" : "H600~H1600",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/3534/x032_index_image_lineup_013.jpg",
            "data" : "目隠しフェンスH600~H1600",
            "reservation": False,
        },
        {
            "name" : "H1700~H2300",
            "text" : "H1700~H2300",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&rpageid=10293740000&rx=54&ry=139&rw=181&rh=118",
            "data" : "目隠しフェンスH1700~H2300",
            "reservation": False,
        },
    ],


    # 目隠しフェンス H600~H1600 ---------------------------------------------------------------------------- #
    "目隠しフェンスH600~H1600" : [
        # {
        #     "name" : "YKKガーデンエクステリア",
        #     "text" : "YKKガーデンエクステリア\n2022①",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
        {
            "name" : "シンプレオ フェンスSY1F型",
            "text" : "アルミ製、目隠しフェンスです。",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/3534/x032_index_image_lineup_013.jpg",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/simpleo-fence",
            "data" : "reservation",
            "reservation": True,
        },
        {
            "name" : "シンプレオ フェンス13F型",
            "text" : "アルミ製、目隠しフェンスです。",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/3532/x032_index_image_lineup_011.jpg",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/simpleo-fence",
            "data" : "reservation",
            "reservation": True,
        },
        {
            "name" : "シンプレオ フェンス5F型",
            "text" : "アルミ製、目隠しフェンスです。",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/3541/x032_index_image_lineup_005.jpg",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/simpleo-fence",
            "data" : "reservation",
            "reservation": True,
        },
        # {
        #     "name" : "2段支柱",
        #     "text" : "WEBカタログ P.1138",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/simpleo-fence",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
    ],

    # 目隠しフェンス H1700~H2300 ---------------------------------------------------------------------------- #
    "目隠しフェンスH1700~H2300" : [
        {
            "name" : "シンプレオ フェンスSY1F型",
            "text" : "アルミ製、目隠しフェンスです。",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/3534/x032_index_image_lineup_013.jpg",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/simpleo-fence",
            "data" : "reservation",
            "reservation": True,
        },
        {
            "name" : "シンプレオ フェンス13F型",
            "text" : "アルミ製、目隠しフェンスです。",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/3532/x032_index_image_lineup_011.jpg",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/simpleo-fence",
            "data" : "reservation",
            "reservation": True,
        },
        {
            "name" : "シンプレオ フェンス5F型",
            "text" : "アルミ製、目隠しフェンスです。",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/3541/x032_index_image_lineup_005.jpg",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/simpleo-fence",
            "data" : "reservation",
            "reservation": True,
        },
    ],


    # 縦格子フェンス --------------------------------------------------------------------------------------- #
    "縦格子フェンス" : [
        {
            "name" : "H600~H1000",
            "text" : "H600~H1000",
            "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
            "data" : "縦格子フェンスH600~H1000",
            "reservation": False,
        },
    ],


    # 縦格子フェンスH600~H1000 --------------------------------------------------------------------------------------- #
    "縦格子フェンスH600~H1000" : [
        # {
        #     "name" : "YKKガーデンエクステリア\n2022①",
        #     "text" : "YKKガーデンエクステリア\n2022①",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
        {
            "name" : "シンプレオ フェンスT1型",
            "text" : "アルミ製、縦格子フェンスです。",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&rpageid=10293620000&rx=36&ry=109&rw=203&rh=115",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/simpleo-fence",
            "data" : "reservation",
            "reservation": True,
        },
        {
            "name" : "シンプレオ フェンスT2型",
            "text" : "アルミ製、縦格子フェンスです。",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&lpageid=10293630000&lx=30&ly=102&lw=202&lh=113",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/simpleo-fence",
            "data" : "reservation",
            "reservation": True,
        },
        {
            "name" : "シンプレオ フェンスT3型",
            "text" : "アルミ製、縦格子フェンスです。",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&rpageid=10293640000&rx=36&ry=110&rw=204&rh=112",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/simpleo-fence",
            "data" : "reservation",
            "reservation": True,
        },
    ],


    # 樹脂フェンス -------------------------------------------------------------------------------------------- #
    "樹脂" : [
        {
            "name" : "目隠し",
            "text" : "外からの視線をカットする「目隠しフェンス H800〜H2000」",
            "image": "https://www.extile.co.jp/themes/extile/img/urbanfence_uv/img-main.jpg",
            "data" : "樹脂目隠しH800~H2000",
            "reservation": False,
        },
    ],


    # 目隠し ------------------------------------------------------------------------------------------------- #
    "目隠し" : [
        {
            "name" : "H800~H2000",
            "text" : "H800~H2000",
            "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
            "data" : "樹脂目隠しH800~H2000",
            "reservation": False,
        },
    ],


    # 樹脂目隠しH800~H2000 ---------------------------------------------------------------------- #
    "樹脂目隠しH800~H2000" : [
        {
            "name" : "アーバンフェンスUV",
            "text" : "樹脂製の目隠しフェンスH800〜H2000です。",
            "image": "https://www.extile.co.jp/themes/extile/img/urbanfence_uv/img-main.jpg",
            "url"  : "https://www.extile.co.jp/lineup/urbanfence_uv/",
            "data" : "reservation",
            "reservation": True,
        },
    ],


    # スチールフェンス -------------------------------------------------------------------------------------------- #
    "スチール" : [
        {
            "name" : "メッシュ",
            "text" : "メッシュタイプ H600~H2000",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/8671/x081_index_image_lineup_01-001.jpg",
            "data" : "メッシュH600~H2000",
            "reservation": False,
        },
    ],


    # メッシュ ------------------------------------------------------------------------------------------------- #
    "メッシュ" : [
        {
            "name" : "H600~H2000",
            "text" : "H600~H2000",
            "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
            "data" : "メッシュH600~H2000",
            "reservation": False,
        },
    ],


    # メッシュH600~H2000 ---------------------------------------------------------------------- #
    "メッシュH600~H2000" : [
        {
            "name" : "イーネット フェンスA1F型",
            "text" : "スチール製、メッシュタイプのフェンスです。",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/8671/x081_index_image_lineup_01-001.jpg",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/enet",
            "data" : "reservation",
            "reservation": True,
        },
        {
            "name" : "イーネット フェンスA2F型",
            "text" : "スチール製、メッシュタイプのフェンスです。",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/8673/x081_index_image_lineup_01-003.jpg",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/enet",
            "data" : "reservation",
            "reservation": True,
        }
    ],
























    # 物置 ----------------------------------------------------------------------------------- #
    "物置" : [
        {
            "name" : "小型物置",
            "text" : "小型物置",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_01.jpg",
            "data" : "小型物置",
            "reservation": False,
        },
        {
            "name" : "中型物置",
            "text" : "中型物置",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_07.jpg",
            "data" : "中型物置",
            "reservation": False,
        },
        {
            "name" : "大型物置",
            "text" : "大型物置",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_09.jpg",
            "data" : "大型物置",
            "reservation": False,
        },

    ],


    # 小型物置 ----------------------------------------------------------------------------------- #
    "小型物置" : [
        {
            "name" : "ドア型収納庫",
            "text" : "出し入れラクラクな「ドア型収納庫」",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_01.jpg",
            "data" : "ドア型収納庫",
            "reservation": False,
        },
        {
            "name" : "タイヤ収納庫",
            "text" : "全面開口を生かしたタイヤ専用の「タイヤ収納庫」",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_02.jpg",
            "data" : "タイヤ収納庫",
            "reservation": False,
        },
        {
            "name" : "引戸収納庫",
            "text" : "シンプルだから調和する庭先のクローゼット「引戸収納庫」",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_03.jpg",
            "data" : "引戸収納庫",
            "reservation": False,
        },
    ],



    # ドア型収納庫 ----------------------------------------------------------------------------------- #
    "ドア型収納庫" : [
        {
            "name" : "アイビーストッカー",
            "text" : "ドア型収納庫の小型物置です。",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_01.jpg",
            "url"  : "https://www.inaba-ss.co.jp/monooki/lineup/D_BJ/index.html",
            "data" : "reservation",
            "reservation": True,
        },
        # {
        #     "name" : "イナバ物置総合カタログVol.62\nP10,P11",
        #     "text" : "イナバ物置総合カタログVol.62\nP10,P11",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
        # {
        #     "name" : "イナバ物置総合カタログVol.62\nP15",
        #     "text" : "イナバ物置総合カタログVol.62\nP15",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
    ],


    # タイヤ収納庫 --------------------------------------------------------------------------------------- #
    "タイヤ収納庫" : [
        {
            "name" : "タイヤストッカー",
            "text" : "タイヤ収納庫の小型物置です。",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_02.jpg",
            "url"  : "https://www.inaba-ss.co.jp/monooki/lineup/D_BJX-T/index.html",
            "data" : "reservation",
            "reservation": True,
        },
        # {
        #     "name" : "イナバ物置総合カタログVol.62\nP17",
        #     "text" : "イナバ物置総合カタログVol.62\nP17",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
    ],


    # 引戸収納庫　--------------------------------------------------------------------------------------- #
    "引戸収納庫" : [
        {
            "name" : "シンプリー",
            "text" : "引戸収納庫の小型物置です。",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_03.jpg",
            "url"  : "https://www.inaba-ss.co.jp/monooki/lineup/D_MJ/index.html",
            "data" : "reservation",
            "reservation": True,
        },
        # {
        #     "name" : "イナバ物置総合カタログVol.62\nP36",
        #     "text" : "イナバ物置総合カタログVol.62\nP36",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
    ],



    # 中型物置 ------------------------------------------------------------------------------------ #
    "中型物置" : [
        {
            "name" : "2枚引込戸",
            "text" : "片側から約2/3が開く「引き込み式2枚戸」",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_07.jpg",
            "data" : "中型2枚引込戸",
            "reservation": False,
        },
        {
            "name" : "引分け戸",
            "text" : "片側から約1/2が開く「引分け戸」",
            "image": "https://housing-fukui.herokuapp.com/static/HousingFukuiCorporationBot/image/%E3%83%95%E3%82%A9%E3%83%AB%E3%82%BF%E5%BC%95%E3%81%8D%E5%88%86%E3%81%91%E6%88%B8%E3%82%BF%E3%82%A4%E3%83%97.png",
            "data" : "引分け戸",
            "reservation": False,
        },
    ],


    # 中型2枚引込戸 ------------------------------------------------------------------------------------ #
    "中型2枚引込戸" : [
        {
            "name" : "屋根傾斜 後面流れ",
            "text" : "通常タイプの「屋根傾斜 後面流れ」",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_07.jpg",
            "data" : "屋根傾斜後面流れ",
            "reservation": False,
        },
        {
            "name" : "屋根傾斜 側面流れ",
            "text" : "お隣に雪や雨水を落とさない「屋根傾斜 側面流れ」",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_08.jpg",
            "data" : "屋根傾斜側面流れ",
            "reservation": False,
        },
    ],


    # 屋根傾斜 後面流れ ----------------------------------------------------------------------------------- #
    "屋根傾斜後面流れ" : [
        {
            "name" : "フォルタ",
            "text" : "引き込み式2枚戸、屋根傾斜 後面流れの中型物置です。",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_07.jpg",
            "url"  : "https://www.inaba-ss.co.jp/monooki/lineup/D_FS/index.html",
            "data" : "reservation",
            "reservation": True,
        },
        # {
        #     "name" : "イナバ物置総合カタログVol.62\nP85",
        #     "text" : "イナバ物置総合カタログVol.62\nP85",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
    ],


    # 屋根傾斜 側面流れ ----------------------------------------------------------------------------------- #
    "屋根傾斜側面流れ" : [
        {
            "name" : "フォルタ 屋根傾斜変更タイプ",
            "text" : "引き込み式2枚戸、屋根傾斜 側面流れの中型物置です。",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_08.jpg",
            "url"  : "https://www.inaba-ss.co.jp/monooki/lineup/D_FK/index.html",
            "data" : "reservation",
            "reservation": True,
        },
        # {
        #     "name" : "イナバ物置総合カタログVol.62\nP85",
        #     "text" : "イナバ物置総合カタログVol.62\nP85",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
    ],


    # 引分け戸 --------------------------------------------------------------------------------------- #
    "引分け戸" : [
        {
            "name" : "フォルタ 引き分け戸タイプ",
            "text" : "引分け戸の中型物置です。",
            "image": "https://housing-fukui.herokuapp.com/static/HousingFukuiCorporationBot/image/%E3%83%95%E3%82%A9%E3%83%AB%E3%82%BF%E5%BC%95%E3%81%8D%E5%88%86%E3%81%91%E6%88%B8%E3%82%BF%E3%82%A4%E3%83%97.png",
            "url"  : "https://www.inaba-ss.co.jp/monooki/lineup/D_FS/index.html",
            "data" : "reservation",
            "reservation": True,
        },
        # {
        #     "name" : "イナバ物置総合カタログVol.62\nP92",
        #     "text" : "イナバ物置総合カタログVol.62\nP92",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
    ],


    # 大型物置 --------------------------------------------------------------------------------------- #
    "大型物置" : [
        {
            "name" : "2枚引込み戸",
            "text" : "片側から約2/3が開く「引き込み式2枚戸」",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_09.jpg",
            "data" : "大型2枚引込み戸",
            "reservation": False,
        },
        {
            "name" : "物置+解放スペース",
            "text" : "使い勝手・収納力抜群な「物置＋解放スペース」",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_10.jpg",
            "data" : "物置+解放スペース",
            "reservation": False,
        },

    ],


    # 大型2枚引込み戸 --------------------------------------------------------------------------------------- #
    "大型2枚引込み戸" : [
        {
            "name" : "フォルタ大型",
            "text" : "引き込み式2枚戸の大型物置です。",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_09.jpg",
            "url"  : "https://www.inaba-ss.co.jp/monooki/lineup/D_FB/index.html",
            "data" : "reservation",
            "reservation": True,
        },
    ],


    # 物置+解放スペース
    "物置+解放スペース" : [
        {
            "name" : "フォルタ ウィズ",
            "text" : "物置＋解放スペースの大型物置です。",
            "image": "https://www.inaba-ss.co.jp/monooki/lineup/images/listImg_10.jpg",
            "url"  : "https://www.inaba-ss.co.jp/monooki/lineup/D_FW/index.html",
            "data" : "reservation",
            "reservation": True,
        },
    ],

































    # リウッドデッキ -------------------------------------------------------------------------------------- #
    "リウッドデッキ" : [
        {
            "name" : "基本セット",
            "text" : "基本セット",
            "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
            "data" : "基本セット",
            "reservation": False,
        },
    ],


    # 基本セット　-------------------------------------------------------------------------------------- #
    "基本セット" : [
        {
            "name" : "オプションなし",
            "text" : "オプションなし ※写真右端にあるステップは付いておりません",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/9809/x097_index_image_lineup_01-001.jpg",
            "data" : "オプションなし",
            "reservation": False,
        },
        {
            "name" : "ステップ付き",
            "text" : "ステップ付き",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/9813/x097_index_image_lineup_03-001.jpg",
            "data" : "ステップ付き",
            "reservation": False,
        },
        {
            "name" : "フェンス付き",
            "text" : "フェンス付き ※写真右端にあるステップは付いておりません",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/9832/x066_index_image_lineup_1-002.jpg",
            "data" : "フェンス付き",
            "reservation": False,
        },
        {
            "name" : "手摺付き",
            "text" : "手すり付き ※写真右端にあるステップは付いておりません",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/3190/x029_index_image_lineup_1-004.jpg",
            "data" : "手摺付き",
            "reservation": False,
        },

    ],


    # オプションなし -------------------------------------------------------------------------------------- #
    "オプションなし" : [
        {
            "name" : "リウッドデッキ 200",
            "text" : "リウッドデッキです。",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/9809/x097_index_image_lineup_01-001.jpg",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/rewood200",
            "data" : "reservation",
            "reservation": True,
        },
    ],


    # ステップ付き -------------------------------------------------------------------------------------- #
    "ステップ付き" : [
        {
            "name" : "リウッドデッキ 200 ステップ付き",
            "text" : "ステップ付きのリウッドデッキです。",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/9809/x097_index_image_lineup_01-001.jpg",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/rewood200",
            "data" : "reservation",
            "reservation": True,
        },
    ],


    # フェンス付き -------------------------------------------------------------------------------------- #
    "フェンス付き" : [
        {
            "name" : "リウッドデッキ 200 リウッドデッキフェンス付き",
            "text" : "フェンス付きのリウッドデッキです。",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/9832/x066_index_image_lineup_1-002.jpg",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/gardenclub-deck",
            "data" : "reservation",
            "reservation": True,
        },
        # {
        #     "name" : "YKKガーデンエクステリア\n2022①P1933",
        #     "text" : "YKKガーデンエクステリア\n2022①P1933",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
    ],


    # 手摺付き -------------------------------------------------------------------------------------- #
    "手摺付き" : [
        {
            "name" : "リウッドデッキ 200 ルシアスデッキフェンス付き",
            "text" : "手すり付きのリウッドデッキです。",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/3190/x029_index_image_lineup_1-004.jpg",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/lucias-deck",
            "data" : "reservation",
            "reservation": True,
        },
        # {
        #     "name" : "YKKガーデンエクステリア\n2022①P1941",
        #     "text" : "YKKガーデンエクステリア\n2022①P1941",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
    ],


















    # その他 --------------------------------------------------------------------------------------- #
    "その他" : [
        {
            "name" : "テラス屋根",
            "text" : "テラス屋根",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/3657/x093_index_image_lineup_1-001.jpg",
            "data" : "テラス屋根",
            "reservation": False,
        },
        {
            "name" : "テラス囲い",
            "text" : "テラス囲い",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10818920000&designID=pro&rpageid=10820680000&rx=31&ry=83&rw=157&rh=98",
            "data" : "テラス囲い",
            "reservation": False,
        },
        {
            "name" : "ブロック",
            "text" : "ブロック",
            "image": "https://toyo-kogyo.icata.net/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=TYK10002&catalogid=19715990000&designID=TOYOD01&lpageid=19728890000&lx=269&ly=310&lw=91&lh=73",
            "data" : "ブロック",
            "reservation": False,
        },
    ],


    # テラス屋根 --------------------------------------------------------------------------------------- #
    "テラス屋根" : [
        {
            "name" : "アール屋根",
            "text" : "アール型",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&rpageid=10302820000&rx=34&ry=97&rw=143&rh=165",
            "data" : "アール屋根柱標準タイプ",
            "reservation": False,
        },
        {
            "name" : "フラット屋根",
            "text" : "フラット型",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&rpageid=10302820000&rx=195&ry=96&rw=149&rh=168",
            "data" : "フラット屋根柱標準タイプ",
            "reservation": False,
        },
    ],


    # アール屋根 --------------------------------------------------------------------------------------- #
    # "アール屋根" : [
    #     {
    #         "name" : "柱標準タイプ",
    #         "text" : "柱標準タイプ",
    #         "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&lpageid=10302590000&lx=156&ly=143&lw=105&lh=95",
    #         "data" : "アール屋根柱標準タイプ",
    #         "reservation": False,
    #     },
    #     {
    #         "name" : "柱奥行移動タイプ",
    #         "text" : "柱奥行移動タイプ",
    #         "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&lpageid=10302590000&lx=269&ly=141&lw=93&lh=87",
    #         "data" : "アール屋根柱奥行移動タイプ",
    #         "reservation": False,
    #     },
    # ],


    # アール屋根柱標準タイプ --------------------------------------------------------------------------------------- #
    "アール屋根柱標準タイプ" : [
        {
            "name" : "ソラリア アール型",
            "text" : "アール型のテラス屋根です。",
            "image": "https://housing-fukui.herokuapp.com/static/HousingFukuiCorporationBot/image/%E3%82%BD%E3%83%A9%E3%83%AA%E3%82%A2%E3%82%A2%E3%83%BC%E3%83%AB%E5%9E%8B.png",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/solarea",
            "data" : "reservation",
            "reservation": True,
        },
    ],


    # 柱奥行移動タイプ --------------------------------------------------------------------------------------- #
    # "アール屋根柱奥行移動タイプ" : [
    #     {
    #         "name" : "ソラリア",
    #         "text" : "WEBカタログ P.2012",
    #         "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&lpageid=10302590000&lx=156&ly=143&lw=105&lh=95",
    #         "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/solarea",
    #         "data" : "reservation",
    #         "reservation": True,
    #     },
    # ],


    # フラット屋根 --------------------------------------------------------------------------------------- #
    # "フラット屋根" : [
    #     {
    #         "name" : "柱標準タイプ",
    #         "text" : "柱標準タイプ",
    #         "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&lpageid=10302590000&lx=156&ly=143&lw=105&lh=95",
    #         "data" : "フラット屋根柱標準タイプ",
    #         "reservation": False,
    #     },
    #     {
    #         "name" : "柱奥行移動タイプ",
    #         "text" : "柱奥行移動タイプ",
    #         "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&lpageid=10302590000&lx=269&ly=141&lw=93&lh=87",
    #         "data" : "フラット屋根柱奥行移動タイプ",
    #         "reservation": False,
    #     },
    # ],


    # フラット屋根柱標準タイプ --------------------------------------------------------------------------------------- #
    "フラット屋根柱標準タイプ" : [
        {
            "name" : "ソラリア フラット型",
            "text" : "フラット型のテラス屋根です。",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&lpageid=10302590000&lx=31&ly=142&lw=102&lh=95",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/solarea",
            "data" : "reservation",
            "reservation": True,
        },
    ],


    # 柱奥行移動タイプ --------------------------------------------------------------------------------------- #
    # "フラット屋根柱奥行移動タイプ" : [
    #     {
    #         "name" : "ソラリア",
    #         "text" : "WEBカタログ P.2011",
    #         "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10282370000&designID=pro&lpageid=10302590000&lx=156&ly=143&lw=105&lh=95",
    #         "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/solarea",
    #         "data" : "reservation",
    #         "reservation": True,
    #     },
    # ],


    # テラス囲い --------------------------------------------------------------------------------------- #
    "テラス囲い" : [
        {
            "name" : "スタンダードタイプ",
            "text" : "スタンダードタイプ",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/3653/x093_index_image_lineup_2-001.jpg",
            "data" : "スタンダードタイプ",
            "reservation": False,
        },
        {
            "name" : "木調ガーデンルームタイプ",
            "text" : "木調ガーデニングタイプ",
            "image": "https://assets.ykkap.co.jp/uploads/tmg_block_page_image/file/3654/x093_index_image_lineup_2-002.jpg",
            "data" : "木調ガーデンルームタイプ",
            "reservation": False,
        },
    ],


    # スタンダードタイプ --------------------------------------------------------------------------------------- #
    "スタンダードタイプ" : [
        {
            "name" : "床納まり",
            "text" : "床納まり",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10818920000&designID=pro&rpageid=10820680000&rx=31&ry=83&rw=157&rh=98",
            "data" : "スタンダードタイプ床納まり",
            "reservation": False,
        },
        {
            "name" : "デッキ納まり",
            "text" : "デッキ納まり",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10818920000&designID=pro&rpageid=10820680000&rx=204&ry=83&rw=157&rh=98",
            "data" : "スタンダードタイプデッキ納まり",
            "reservation": False,
        },
        {
            "name" : "土間納まり",
            "text" : "土間納まり",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10818920000&designID=pro&rpageid=10820680000&rx=31&ry=267&rw=157&rh=98",
            "data" : "スタンダードタイプ土間納まり",
            "reservation": False,
        },
    ],


    # スタンダードタイプ床納まり --------------------------------------------------------------------------------------- #
    "スタンダードタイプ床納まり" : [
        {
            "name" : "ソラリア テラス囲い 床納まり",
            "text" : "スタンダードタイプ、床納まりのテラス囲いです。",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10818920000&designID=pro&rpageid=10820680000&rx=31&ry=83&rw=157&rh=98",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/solarea",
            "data" : "reservation",
            "reservation": True,
        },
        # {
        #     "name" : "YKKウォールエクステリア\n2022①P166",
        #     "text" : "YKKウォールエクステリア\n2022①P166",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
    ],


    # スタンダードタイプデッキ納まり --------------------------------------------------------------------------------------- #
    "スタンダードタイプデッキ納まり" : [
        {
            "name" : "ソラリア テラス囲い デッキ納まり",
            "text" : "スタンダードタイプ、デッキ納まりのテラス囲いです。",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10818920000&designID=pro&rpageid=10820680000&rx=204&ry=83&rw=157&rh=98",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/solarea",
            "data" : "reservation",
            "reservation": True,
        },
    ],


    # スタンダードタイプ土間納まり --------------------------------------------------------------------------------------- #
    "スタンダードタイプ土間納まり" : [
        {
            "name" : "ソラリア テラス囲い 土間納まり",
            "text" : "スタンダードタイプ、土間納まりのテラス囲いです。",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10818920000&designID=pro&rpageid=10820680000&rx=31&ry=267&rw=157&rh=98",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/solarea",
            "data" : "reservation",
            "reservation": True,
        },
    ],


    # 木調ガーデンルームタイプ --------------------------------------------------------------------------------------- #
    "木調ガーデンルームタイプ" : [
        {
            "name" : "床納まり",
            "text" : "床納まり",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10818920000&designID=pro&rpageid=10820700000&rx=31&ry=83&rw=157&rh=97",
            "data" : "木調ガーデンルームタイプ床納まり",
            "reservation": False,
        },
        {
            "name" : "デッキ納まり",
            "text" : "デッキ納まり",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10818920000&designID=pro&rpageid=10820700000&rx=204&ry=83&rw=157&rh=97",
            "data" : "木調ガーデンルームタイプデッキ納まり",
            "reservation": False,
        },
        {
            "name" : "土間納まり",
            "text" : "土間納まり",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10818920000&designID=pro&rpageid=10820700000&rx=31&ry=256&rw=157&rh=97",
            "data" : "木調ガーデンルームタイプ土間納まり",
            "reservation": False,
        },
    ],


    # 木調ガーデンルームタイプ床納まり --------------------------------------------------------------------------------------- #
    "木調ガーデンルームタイプ床納まり" : [
        {
            "name" : "ソラリア テラス囲い 木調ガーデニングタイプ 床納まり",
            "text" : "木調ガーデニングタイプ、床納まりのテラス囲いです。",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10818920000&designID=pro&rpageid=10820700000&rx=31&ry=83&rw=157&rh=97",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/solarea",
            "data" : "reservation",
            "reservation": True,
        },
        # {
        #     "name" : "YKKウォールエクステリア\n2022①P173",
        #     "text" : "YKKウォールエクステリア\n2022①P173",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
    ],


    # 木調ガーデンルームタイプデッキ納まり --------------------------------------------------------------------------------------- #
    "木調ガーデンルームタイプデッキ納まり" : [
        {
            "name" : "ソラリア テラス囲い 木調ガーデニングタイプ デッキ納まり",
            "text" : "木調ガーデニングタイプ、デッキ納まりのテラス囲いです。",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10818920000&designID=pro&rpageid=10820700000&rx=204&ry=83&rw=157&rh=97",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/solarea",
            "data" : "reservation",
            "reservation": True,
        },
        # {
        #     "name" : "YKKウォールエクステリア\n2022①P173",
        #     "text" : "YKKウォールエクステリア\n2022①P173",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
    ],


    # 木調ガーデンルームタイプ土間納まり --------------------------------------------------------------------------------------- #
    "木調ガーデンルームタイプ土間納まり" : [
        {
            "name" : "ソラリア テラス囲い 木調ガーデニングタイプ 土間納まり",
            "text" : "木調ガーデニングタイプ、土間納まりのテラス囲いです。",
            "image": "https://webcatalog.ykkap.co.jp/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=YKKAPDC1&catalogid=10818920000&designID=pro&rpageid=10820700000&rx=31&ry=256&rw=157&rh=97",
            "url"  : "https://www.ykkap.co.jp/consumer/products/exterior/solarea",
            "data" : "reservation",
            "reservation": True,
        },
        # {
        #     "name" : "YKKウォールエクステリア\n2022①P173",
        #     "text" : "YKKウォールエクステリア\n2022①P173",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "reservation",
        #     "reservation": True,
        # },
    ],


    # ブロック --------------------------------------------------------------------------------------- #
    "ブロック" : [
        # {
        #     "name" : "コンクリートブロック塀",
        #     "text" : "コンクリートブロック塀",
        #     "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        #     "data" : "コンクリートブロック塀",
        #     "reservation": False,
        # },
        {
            "name" : "化粧ブロック塀",
            "text" : "化粧ブロック塀",
            "image": "https://toyo-kogyo.icata.net/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=TYK10002&catalogid=19715990000&designID=TOYOD01&lpageid=19728830000&lx=36&ly=296&lw=323&lh=233",
            "data" : "化粧ブロック塀",
            "reservation": False,
        },
    ],

    
    # コンクリートブロック塀 --------------------------------------------------------------------------------------- #
    # "コンクリートブロック塀" : [
    #     {
    #         "name" : "コンクリートブロック塀",
    #         "text" : "コンクリートブロックの塀です。",
    #         "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
    #         "url"  : "https://team-reizoko.studio.site/",
    #         "data" : "reservation",
    #         "reservation": True,
    #     },
    # ],


    # 化粧ブロック塀 --------------------------------------------------------------------------------------- #
    "化粧ブロック塀" : [
        {
            "name" : "ライク",
            "text" : "化粧ブロック塀です。",
            "image": "https://toyo-kogyo.icata.net/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=TYK10002&catalogid=19715990000&designID=TOYOD01&rpageid=19728900000&rx=4&ry=32&rw=359&rh=230",
            "url"  : "http://www.toyo-kogyo.co.jp/exterior/products/katawaku/",
            "data" : "reservation",
            "reservation": True,
        },
        {
            "name" : "イースワン",
            "text" : "化粧ブロック塀です。",
            "image": "https://toyo-kogyo.icata.net/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=TYK10002&catalogid=19715990000&designID=TOYOD01&lpageid=19728830000&lx=36&ly=296&lw=323&lh=233",
            "url"  : "http://www.toyo-kogyo.co.jp/exterior/products/katawaku/",
            "data" : "reservation",
            "reservation": True,
        },
        {
            "name" : "リベルタストーン",
            "text" : "化粧ブロック塀です。",
            "image": "https://toyo-kogyo.icata.net/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=TYK10002&catalogid=19715990000&designID=TOYOD01&lpageid=19728730000&lx=98&ly=146&lw=151&lh=95",
            "url"  : "http://www.toyo-kogyo.co.jp/exterior/products/katawaku/",
            "data" : "reservation",
            "reservation": True,
        },
        {
            "name" : "ソリッドストーンエッジ",
            "text" : "化粧ブロック塀です。",
            "image": "https://toyo-kogyo.icata.net/iportal/webapi.do?api=getCatalogviewClippedpage&volumeid=TYK10002&catalogid=19715990000&designID=TOYOD01&lpageid=19728750000&lx=112&ly=32&lw=185&lh=129",
            "url"  : "http://www.toyo-kogyo.co.jp/exterior/products/katawaku/",
            "data" : "reservation",
            "reservation": True,
        },
    ],












    # カーポートを探す --------------------------------------------------------------------------------------- #
    # "カーポート(sample)":[
    #     {
    #         "name" : "",
    #         "text" : "",
    #         "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
    #         "data" : "",
    #         "reservation": False,
    #     },
    #     {
    #         "name" : "",
    #         "text" : "",
    #         "image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
    #         "data" : "reservation",
    #         "reservation": True,
    #     },
    # ]

}