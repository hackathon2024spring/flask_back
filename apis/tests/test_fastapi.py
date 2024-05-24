import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient, ASGITransport, Cookies
from ddd.router.hello import view as view0
from ddd.router.signup import view as view1
from ddd.router.login import view as view2
from ddd.router.logout import view as view3
from ddd.router.getuser import view as view4
from ddd.router.addexercises_setting import view as view5
from ddd.router.getexercises_setting import view as view6
from ddd.router.addexercises import view as view7
from ddd.router.getexercises import view as view8
from ddd.router.getcalendars import view as view9


app = FastAPI()
for v in [view1, view2, view3, view4]:
    app.include_router(v.router)

app = FastAPI()
for v in [view0, view1, view2, view3, view4, view5, view6, view7, view8, view9]:
    app.include_router(v.router)


@pytest.mark.asyncio
async def test_hello():
    """
    Test:   ダミーAPI
    Expect: テストやFastAPIにアクセスできるかの確認。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/hello")
        print(response.json())
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_signup_illegal_email():
    """
    Test:   ユーザーの新規登録でemailが無い
    Expect: 不適切なemailで失敗したレスポンスが帰ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/signup",
            json={
                "username": "testuser",
                "email": "",
                "password1": "testpass",
                "password2": "testpass",
            },
        )
        data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "value is not a valid email address" in data["detail"]


@pytest.mark.asyncio
async def test_signup_illegal_username():
    """
    Test:   ユーザーの新規登録でusernameが無い
    Expect: ユーザー登録が失敗したレスポンスが帰ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/signup",
            json={
                "username": "",
                "email": "test@example.com",
                "password1": "testpass",
                "password2": "testpass",
            },
        )
        data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "ユーザー名は半角英数と_.+のみです" in data["detail"]


@pytest.mark.asyncio
async def test_signup_short_password():
    """
    Test:   ユーザーの新規登録でパスワードが短すぎる
    Expect: ユーザー登録が失敗したレスポンスが帰ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/signup",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "test",
                "password2": "test",
            },
        )
        data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "パスワードは8文字以上です" in data["detail"]


@pytest.mark.asyncio
async def test_signup_wrong_password():
    """
    Test:   ユーザーの新規登録でconfrim_passwordが不一致
    Expect: ユーザー登録が失敗したレスポンスが帰ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/signup",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "testpass",
                "password2": "hogehoge",
            },
        )
        data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "パスワードが一致しません" in data["detail"]


@pytest.mark.asyncio
async def test_signup_success():
    """
    Test:   ユーザーの新規登録
    Expect: ユーザー登録が成功したレスポンスが返ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/signup",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "testpass",
                "password2": "testpass",
            },
        )
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data["data"]["username"] == "testuser"


@pytest.mark.asyncio
async def test_signup_again():
    """
    Test:   同じユーザーの登録
    Expect: ユーザー登録が失敗したレスポンスが帰ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/signup",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "testpass",
                "password2": "testpass",
            },
        )
        data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Emailアドレス・パスワードに問題があります。" in str(data["detail"])


@pytest.mark.asyncio
async def test_login_wrong_password():
    """
    Test:   使えないパスワードでログイン
    Expect: ログインが失敗したレスポンスが帰ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "hogehoge",
            },
        )
        data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Emailアドレス・パスワードに問題があります" in str(data["detail"])


@pytest.mark.asyncio
async def test_login_wrong_email():
    """
    Test:   使えないemailアドレスでログイン
    Expect: ログインが失敗したレスポンスが帰ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/login",
            json={
                "email": "hoge@example.com",
                "password": "testpass",
            },
        )
        data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Emailアドレス・パスワードに問題があります" in str(data["detail"])


@pytest.mark.asyncio
async def test_login_success():
    """
    Test:   ログイン
    Expect: ログインが成功したレスポンスが返ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "testpass",
            },
        )
        data = response.json()
        cookies = response.cookies
        assert response.status_code == status.HTTP_200_OK
        assert data["token_type"] == "bearer"
        assert "access_token" in cookies


@pytest.mark.asyncio
async def test_get_user_info():
    """
    Test:   ユーザー情報の取得
    Expect: ユーザー情報が返ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:

        response = await client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "testpass",
            },
        )

        response = await client.get("/user")
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data["data"]["username"] == "testuser"


@pytest.mark.asyncio
async def test_add_exercises_setting():
    """
    Test:   Exercise設定を更新
    Expect: 更新成功のstatusが返ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:

        response = await client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "testpass",
            },
        )

        # 2番目をfalseにして後のテストに反映させる
        response = await client.post(
            "/exercises_setting",
            json={
                "data": [
                    {"exerciseId": 1, "selected": "true"},
                    {"exerciseId": 2, "selected": "false"},
                ]
            },
        )
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data["status"] == 1


@pytest.mark.asyncio
async def test_get_exercises_setting():
    """
    Test:   現在のExercise設定を取得
    Expect: 前のテストで更新されたExercise設定が返ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:

        response = await client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "testpass",
            },
        )
        # 前のテストで書き換えた内容が反映されている。
        response = await client.get("/exercises_setting")
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data["status"] == 1
        assert data["data"][1] == {
            "exerciseId": 2,
            "exerciseName": "散歩する",
            "exerciseSelected": False,
        }


@pytest.mark.asyncio
async def test_add_exercises():
    """
    Test:   Exerciseを更新
    Expect: 更新成功のstatusが返ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:

        response = await client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "testpass",
            },
        )

        # 1番目2番目をtrueにして後のテストに反映させる
        response = await client.post(
            "/exercises/2024-05-24",
            json={
                "data": [
                    {"exerciseId": 1, "done": "true"},
                    {"exerciseId": 2, "done": "true"},
                ]
            },
        )
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data["status"] == 1


@pytest.mark.asyncio
async def test_get_exercises():
    """
    Test:   2024-05-24のExerciseを取得
    Expect: Exerciseが返ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:

        response = await client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "testpass",
            },
        )
        # 前のテストで書き換えた内容が反映されている。
        response = await client.get("/exercises/2024-05-24")
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data["status"] == 1
        assert data["data"][0] == {
            "exerciseId": 1,
            "exerciseName": "階段を使う",
            "exerciseDone": True,
        }


@pytest.mark.asyncio
async def test_get_calendar():
    """
    Test:   2024年05月のcalendarを取得
    Expect: calendarのTrue/Falseが返ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:

        response = await client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "testpass",
            },
        )
        # 前のテストで書き換えた内容が反映されている。
        response = await client.get("/calendars/2024/5")
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert data["status"] == 1
        assert data["data"][23] == {"day": "2024-05-24", "exerciseDone": True}


@pytest.mark.asyncio
async def test_logout_success():
    """
    Test:   ログアウト
    Expect: ログアウトが成功したレスポンスが帰ること。
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # まずログインしてクッキーを取得
        login_response = await client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "testpass",
            },
        )
        cookies = Cookies()
        cookies.update(login_response.cookies)

        # クッキーをクライアントインスタンスに設定
        client.cookies = cookies

        # /logout にアクセス
        logout_response = await client.get("/signout")
        data = logout_response.json()
        assert logout_response.status_code == status.HTTP_200_OK
        assert data["message"] == "Successfully logged out"
        assert logout_response.cookies.get("access_token") is None
