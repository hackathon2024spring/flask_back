class Signup:
    endpoint = "/signup"
    summary = "ユーザー登録"
    description = """ユーザーを登録します。"""


class Login:
    endpoint = "/login"
    summary = "ログイン"
    description = """ログイン"""


class Signout:
    endpoint = "/signout"
    summary = "サインアウト"
    description = """サインアウト"""


class AddChannel:
    endpoint = "/channel"
    summary = "掲示板の追加"
    description = """掲示板の追加"""


class AddMessage:
    endpoint = "/message"
    summary = "メッセージの追加"
    description = """メッセージの追加"""


class DelMessage:
    endpoint = "/message"
    summary = "メッセージの削除"
    description = """メッセージの削除"""


class DelChannel:
    endpoint = "/channel"
    summary = "掲示板の削除"
    description = """掲示板の削除"""


class GetChannels:
    endpoint = "/channels"
    summary = "掲示板の取得"
    description = """掲示板の取得"""


class GetMessages:
    endpoint = "/messages"
    summary = "メッセージの取得"
    description = """メッセージの取得"""
