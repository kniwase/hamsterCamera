import argparse


def runserver():
    from app.app import api
    from app.settings import (HAMCAM_PRODUCTION, SRC_DIR)
    import uvicorn
    if HAMCAM_PRODUCTION in ("1", "0"):
        # 本番環境、ステージング環境
        uvicorn.run(app=api, host="0.0.0.0", port=9080)
    else:
        # 開発環境
        certdir = SRC_DIR.parents[1] / "dev-env" / "cert" / "pem"
        uvicorn.run(app=api, host="0.0.0.0", port=9080,
                    ssl_keyfile=certdir / "key.pem",
                    ssl_certfile=certdir / "cert.pem")


# コマンドライン引数パーサー
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# サブコマンド: runserver, WEBアプリケーション起動
parser_runserver = subparsers.add_parser("runserver")
parser_runserver.set_defaults(handler=runserver)


if __name__ == "__main__":
    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler()
    else:
        parser.print_help()
