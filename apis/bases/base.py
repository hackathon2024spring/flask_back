from sqlalchemy.ext.declarative import declarative_base
# 循環インポートを避けるため、扇状に広がるイメージでmodelとschemaを作る
Base = declarative_base()
