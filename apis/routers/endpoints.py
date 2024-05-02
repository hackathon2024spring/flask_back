# 運動アプリ用コード

class GetExercise:
    endpoint = "/exercise/{date}"
    summary = "実施できる運動の取得"
    description = """実施できる運動の取得"""

class GetExercise_setting:
    endpoint = "/exercise_setting"
    summary = "登録されている運動の取得"
    description = """登録されている運動の取得"""

class AddExercise:
    endpoint = "/exercise"
    summary = "実施した運動の変更"
    description = """実施した運動の変更"""

class AddExercise_setting:
    endpoint = "/exercise_setting"
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
