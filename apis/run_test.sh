#!/bin/bash

# 必要なパッケージをインストール（最初の一回だけまたは環境によっては必要）
pip install -r ~/devcon/apis/requirements.txt

export IS_TEST="True"
export PYTHONPATH="/home/appuser/devcon/apis"

# pytestを実行し、テストを走らせる
pytest -s --cov=ddd/ tests/ --asyncio-mode=auto --cov-report html

