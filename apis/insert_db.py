from sqlalchemy import create_engine, text
import os

# 接続情報
host = os.getenv("MYSQL_HOST_FAST")
port = int(os.getenv("PORT_MYSQL_FAST"))
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
db = os.getenv("MYSQL_DB_FAST")

# SQLAlchemyエンジンを作成
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")
print(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")

# INSERTクエリを実行
with engine.connect() as con:
    sql_query = """
        INSERT INTO `exercises`(`id`, `exercise_name`) 
        VALUES ('1','階段を使う'),('2','散歩する'),('3','ストレッチをする'),('4','足踏み運動をする'),('5','一駅分歩く'),('6','ラジオ体操をする'),('7','スクワットをする'),('8','雑巾がけをする'),('9','つま先立ちで皿を洗う'),('10','Nintendo Switch Sportsをする');
    """
    print(sql_query)
    con.execute(text(sql_query))
    con.commit()
    print("終わった")
