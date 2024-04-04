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

- docker-compose.yml の上にマウスカーソルを持っていき、右クリック → Compose Up で全てのコンテナが起動する。
  - fastapi コンテナ：api を提供する本体
  - mysql_fast コンテナ：データベース
  - pma_fast コンテナ:データベースを閲覧するツール
- http://localhost:8080/docs にブラウザでアクセスすると FastAPI を動作させる GUI (Swagger UI)が起動する。
- http://localhost:4081 にブラウザでアクセスするとデータベースの中を閲覧できる。

## dev container

- クジラのアイコンから 動作中の docker コンテナ(緑の三角マーク)を右クリック →Attach Shell を実行すると、CLI でコンテナ内に入ることができる。dev container は CLI ではなく VSCode の GUI でコンテナ内に入るツール。
- python コンテナであれば requirements.txt、nodejs コンテナ(React、NextJS など)であれば package.json に導入するライブラリとバージョンが明記されるので、均質な開発環境を共有できる。
- 入れるコンテナは.devcontainer フォルダの devcontainer.json の service で決定され、この service は docker-compose.yml の service が選択される。このプロジェクトの場合、fastapi コンテナに入れる。
- 左下の><を左クリック →Reopen in Container で dev container に入れる。
- 左下>< Dev Container を左クリック → Reopen Folder Locally で dev container から出られる。
- コンテナの内外でユーザー id とグループ id を一致させておく必要がある。異なっているとローカル環境に編集権限の無いファイルやフォルダが生成され、git の監視が乱れる場合がある。
- ubuntu の場合、CLI で id と入力すると uid=1000(ユーザー名) gid=1000(グループ名)が表示され、.env の MY_UID と MY_GID と一致させている。
- mac の場合、同じ id で確認でき、uid=501(ユーザー名) gid=20(グループ名)になる。.env の MY_UID と MY_GID を一致させるべきだが、docker コンテナは全て linux OS で、gid=20 は dialout に設定されているので、何らかの悪影響がある可能性がある。今の所、聞いたことは無いが・・・
