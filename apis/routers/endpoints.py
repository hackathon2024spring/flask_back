# 運動アプリ用コード

class GetExcercise:
    endpoint = "/excercise"
    summary = "実施できる運動の取得"
    description = """実施できる運動の取得"""

class GetExcercise_setting:
    endpoint = "/excercise_setting"
    summary = "登録されている運動の取得"
    description = """登録されている運動の取得"""

class AddExcercise:
    endpoint = "/excercise"
    summary = "実施した運動の変更"
    description = """実施した運動の変更"""

class AddExcercise_setting:
    endpoint = "/excercise_setting"
    summary = "登録されている運動の変更"
    description = """登録されている運動の登録変更"""

# ログイン機能用コード

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


# 以下はTODOアプリ用コード

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
