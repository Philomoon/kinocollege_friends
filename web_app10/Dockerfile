# Pythonのイメージから作成
FROM python:3

# python環境変数の１つ。コンソールの標準出力(stdout)と標準エラー出力(stderr)がエラー発生時にすぐに出力されるようにする
ENV PYTHONUNBUFFERED 1

# コンテナで/codeディレクトリ作成
RUN mkdir /code

# ワークディレクトリを設定する(/codeで作業)
WORKDIR /code

# codeディレクトリにrequirements.txtを追加する
ADD requirements.txt /code/

# requirements.txtに記載しているものをinstallする
RUN pip install -r requirements.txt

# プロジェクトを追加する
ADD . /code/