from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

load_certs = os.environ.get("WEBSITE_LOAD_CERTIFICATES", None)
ssl_args = {}

if load_certs and load_certs != "*":
    # 複数指定されている場合は先頭のサムプリントを使用
    thumbprint = load_certs.split(",")[0].strip()
    # Azure App Service の Linux コンテナ内で証明書は /var/ssl/certs/<サムプリント>.pem として配置される
    cert_file = f"/var/ssl/certs/{thumbprint}.pem"
    ssl_args["ssl"] = {"ca": cert_file}
else:
    # WEBSITE_LOAD_CERTIFICATES が "*" の場合や未設定の場合は、
    # 必要に応じてシステム既定の証明書を利用するか、固定パスを指定する
    # 例: ssl_args["ssl"] = {"ca": "/usr/local/share/ca-certificates/BaltimoreCyberTrustRoot.crt.pem"}
    pass

# データベース接続情報
DB_USER = os.getenv('MYSQL_USER')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_HOST = os.getenv('MYSQL_SERVER')
DB_PORT = os.getenv('MYSQL_DB_PORT')
DB_NAME = os.getenv('MYSQL_DB')

# MySQLのURL構築
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print("nakano DATABASE_URL:",DATABASE_URL)

# エンジンの作成
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args=ssl_args
)
