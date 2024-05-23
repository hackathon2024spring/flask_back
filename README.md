## 最小限フォルダ構成 ($ tree -a -I '.git')

.
├── .devcontainer
│ └── devcontainer.json …dev container の設定
├── apis
│ ├── Dockerfile
│ ├── main.py
│ ├── requirements.txt ...NodeJS と異なり、自作の requirements.txt に基づいて FastAPI の環境が作られる
│ ├── bases ...このフォルダのファイル群が DB と FastAPI の間に挟まる
│ │ ├── \_\_init\_\_.py
│ │ ├── base.py
│ │ ├── channel.py
│ │ ├── message.py
│ │ └── user.py
│ ├── routers ...このフォルダのファイル構成で 1 つの API を作る
│ │ ├── login
│ │ │ ├── model.py
│ │ │ ├── schema.py
│ │ │ └── view.py
│ │ ├── signout
│ │ │ ├── model.py
│ │ │ ├── schema.py
│ │ │ └── view.py
│ │ └── signup
│ │ ├── model.py
│ │ ├── schema.py
│ │ └── view.py
│ └── services ...routers で共通して使う ファイル群
│ 　 ├── \_\_init\_\_.py
│ 　 ├── authfunctions.py ...HttpOnly の認証関連
│ 　 └── oauth2.py ...HttpOnly の cookie を発行するように OAuth2 を派生
├── mysql
│ ├── Dockerfile …sed -i でデフォルトの port や user を変える
│ ├── data
│ │ └── db …MySQL が生成する模様
│ ├── init.sql …placeholder が Dockerfile で書き換えられる
│ └── my.cnf …placeholder が Dockerfile で書き換えられる
├── phpmyadmin
│ ├── Dockerfile ...sed -i でデフォルトの port を変える
│ └── sessions …phpMyAdmin が生成する模様
├── .env ...MY_UID・MY_GID から HOST_OS に変更
├── .gitignore
├── docker-compose.yml ...MY_UID・MY_GID を動的に作るようにしたので、GUI で動作しなくなった。
├── alembic.ini ...build.sh において MySQL の接続文字列を.env の定数から作る
├── env.py ...alembic が参照する環境ファイル。「env.py」のファイル名は alembic 指定。
├── create_db.py ...alembic に基づいてデータベースを作る
├── build.sh ...docker-compose.yml の commands で実行されるシェルスクリプト
├── docker_compose.sh ...MY_UID・MY_GID を動的に作って docker-compose.yml に渡す
├── docker_softclear.sh ...docker コンテナを image を除き、削除
├── dumpDB.sh ...MySQL のエンティティをテキスト形式(backup.sql)でダウンロード
├── restoreDB.sh ...backup.sql で MySQL を再構築するので、エンティティを変えた場合、backup.sql も手動更新する必要がある。
└── README.md

## 環境変数を収めた.env について

- GitHub にパスワードや ID を公開することはできないので、.env というファイルに環境変数として保存する。
- GitHub をクローンしても.env ファイルが無ければ動作しない。
- .env は拡張子ではなく、Linux では先頭に.を置くと隠しファイルになる。

## alembic

- alembic は declarative_base を継承するクラスをマイグレーションして env.py で指定したデータベースにテーブルを自動生成する。マイグレーションとは Python ファイルを設計図とし、データベースのテーブルを作成することを言う。データベースをゼロから作るのであれば、build.sh に一連の手続きを記載しているので、コンテナ消去・再生成で自動的にマイグレーションされる。
- 手動でテーブルを再構成する場合、以下の手順で進める。
  1.FastAPI のある devcontainer に入り、alembic.ini を右クリック →Open in Integrated Terminal

  2.apis/bases/\_\_init\_\_.py に MySQL のテーブルを作りたい class を import で記載することを忘れにない。ファイルを apis/bases フォルダにファイルを置くだけではマイグレーションに関与せず、テーブルが作られない。

  3.以下コマンドを実行しマイグレーションファイルを生成。messege に何をするのかを記入。"Add column hoge"など。
  ~/devcon$ alembic revision --autogenerate -m "message"

  4./alembic/versions にマイグレーションファイルが自動生成され、upgrade と downgrade の一対でデータベースを操作するコードが含まれる。upgrade を message に見合う内容で自作する。既に何らかのデータがテーブルに保存されていて、それを残しながらテーブル構造を変更するには、カラムの nullable=True を設定して値を追加更新するなど、Python でのテーブル操作を熟知しておく必要がある。downgrade は upgrade をキャンセルする内容で自作する。

  5.以下コマンドを実行しマイグレーションファイルを適用する。
  ~/devcon$ alembic upgrade head

  6.面倒なら devcontainer から抜け、./docker_softclear.sh を実行してコンテナを完全削除し、apis/bases にテーブルの仕様を示した py を追加。\_\_init\_\_.py を更新して改めて docker-compose.yml を右クリック → compose up で再構築する。最初のマイグレーションファイルはゼロからデータベースにテーブルを作るので、そのまま使えるから。

- dumpDB.sh で MySQL をバックアップし、restoreDB.sh で元に戻す。ただしテーブル構成が変わっていない事が条件。backup.sql を手動で修正すれば、不可能ではない。
- dumpDB.sh の上にマウスカーソルを置き右クリック →Open in Integrated Terminal を選択 →CLI で./dumpDB.sh を実行するとデータベースが backup.sql にバックアップされる。
- restoreDB.sh の上にマウスカーソルを置き右クリック →Open in Integrated Terminal を選択 →CLI で./restoreDB.sh を実行するとデータベースが backup.sql に基づいてレストアされる。

## docker コンテナ

- CLI で./docker_compose.sh を実行する
  - fastapi コンテナ：api を提供する本体
  - mysql_fast コンテナ：データベース
  - pma_fast コンテナ:データベースを閲覧するツール
- http://localhost:8080/docs にブラウザでアクセスすると FastAPI を動作させる GUI (Swagger UI)が起動する。
- http://localhost:4081 にブラウザでアクセスするとデータベースの中を閲覧できる。

## dev container

- クジラのアイコンから 動作中の docker コンテナ(緑の三角マーク)を右クリック →Attach Shell を実行すると、CLI でコンテナ内に入ることができる。dev container は CLI ではなく VSCode の GUI でコンテナ内に入るツール。
- python コンテナであれば requirements.txt、nodejs コンテナ(React、NextJS など)であれば package.json に導入するライブラリとバージョンが明記されるので、均質な開発環境を共有できる。
- 入れるコンテナは.devcontainer フォルダの devcontainer.json の service で決定され、この service は docker-compose.yml の service が選択される。このプロジェクトの場合、fastapi コンテナに入れる。
- OS によって MY_UID・MY_GID が変わってしまうので、動的に変化させることにした。その余波で dev container を直接起動できなくなった。まず./docker_compose.sh で OS に応じた MY_UID・MY_GID でコンテナを立ち上げ、それから左下の><を左クリック →Reopen in Container で dev container に入れる。
- 左下>< Dev Container を左クリック → Reopen Folder Locally で dev container から出られる。

## FastAPI @app や@route と SwaggerUI の関係

- responses パラメータを指定しない場合、FastAPI はデフォルトのレスポンススキーマを SwaggerUI に表示しますが、実際にどのようなレスポンスが返されるかは実装によります。
- responses を指定すると、SwaggerUI では指定したステータスコードと説明が表示され、実際にそれらのレスポンスを返すようにエンドポイントを実装することが期待されます。
- response_model は確かにステータスコード 200 の場合のレスポンスモデルを指定しますが、これはサーバーが成功した応答としてどのモデルを返すかを示します。
- ステータスコード 422 は、デフォルトでリクエストのバリデーションエラーに対するレスポンスコードとして FastAPI によって使われます。カスタムレスポンスを提供するためには、@app.exception_handler（または@app.exception_handler(RequestValidationError)）を使ってアプリケーションレベルでカスタムハンドラを設定する必要があります。
- ただし、@app.exception_handler(RequestValidationError) でカスタムレスポンスを提供する場合、リクエストクラスを完全に互換性を持たせる必要はありません。カスタム例外ハンドラ内でリクエストの内容を調査し、必要に応じて異なるレスポンスを返すことができます。ただし、これは通常のエラーハンドリングの実践よりも複雑であり、通常は避けられます。
- これらの例外ハンドラは、API のユーザーに一貫性のあるエラーメッセージを提供するためのものです。API の使用者が異なるエンドポイントで同じ種類のエラー（例えばバリデーションエラー）に遭遇した場合に、一貫したレスポンスを受け取ることができるように設計されています。

## Pytest
- testsフォルダにtest_hoge.pyのファイル名で保存するとテスト対象になる。
- conftest.pyがテスト環境の初期設定と終端処理を司る。だからテストファイルで使わないget_dbで繋がれている。
- devcontainerに入った後、./run_test.shを実行するとtestsフォルダの全テストファイルがテストされる。
- test_hoge.pyを1発で仕上げることは難しい。assert Trueで終わらせ、テスト中にどんなレスポンスが得られるのかを確認しながらassert の条件式を作る。
- sqlite3のテスト用のデータベースが作られ、pytestを動作させるシェルスクリプトにテストだけ有効となる環境変数 IS_TEST=Trueを追加し、データベースを切り替える。
- pytestが作ったテスト用データベースがmain.pyのルーティングを介してアクセスできるよう、singletonパターンを採用している。
- テスト用データベースsqliteは1つのテストが終わるとテーブルの中身を消去するらしい。テーブル自体はテスト全体が終わるまで維持されている。だから1つのテストの中でデータ登録と呼び出しなどを組み合わせる必要がある。
- テストファイルはAPIの出力が予想と一致するかしか判断しない。アルゴリズムの成否は判断しないので注意。「作った様に動いているか」を確認するためのもの。
- 自分で作ったアルゴリズムを自分でテストするマッチポンプなのだが、testsフォルダに他者が作ったテストも置かれる。他者のテストと一緒にテストされることで、自分が想定しない参照先の更新を把握することができる。例えば大元のライブラリの仕様変更でアクセス方法が変わった等
- dddにおいてinfa層・presentation層・presentation層に分かれる。sessionの管理とエラー処理は密接に関わるため、infra層で発生する様々なエラーを全てHttpExceptionに変換して呼び出し元に投げ、presentationでHttpExceptとExceptionのみ受け取る構成にすると分かりやすい。
- UseServiceImplでのエラー処理がほとんど無くなり、UseRepositoryImplを使わないvalidationなどを担う。