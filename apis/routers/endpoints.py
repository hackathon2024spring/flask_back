# 運動アプリ用コード

class GetExercises:
    endpoint = "/exercises/{date}"
    summary = "実施できる運動の取得"
    description = """実施できる運動の取得"""

class GetExercises_setting:
    endpoint = "/exercises_setting"
    summary = "登録されている運動の取得"
    description = """登録されている運動の取得"""

class AddExercises:
    endpoint = "/exercises"
    summary = "実施した運動の変更"
    description = """実施した運動の変更"""

class AddExercises_setting:
    endpoint = "/exercises_setting"
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