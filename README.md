# Claude3 Video Analyzer

Claude3 Video Analyzerは、Anthropic社のClaude-3モデルのマルチモーダル機能を利用して、MP4形式の動画をプロンプトに基づいて解析するPythonプロジェクトです。

## 主な機能

- MP4動画からフレームを抽出し、base64エンコードされた画像データに変換
- プロンプトとエンコードされた画像データをClaude-3モデルに送信し、動画の内容を解析
- 解析結果をテキストとして出力

## 必要条件

- Python 3.10.13以上
- AnthropicのAPIキー

## インストール

1. リポジトリをクローンします:
```
git clone https://github.com/Olemi-llm-apprentice/claude3-video-analyzer.git
```
2. プロジェクトディレクトリに移動します:
```
cd claude3-video-analyzer
```

3. 必要なPythonパッケージをインストールします:
```
pip install -r requirements.txt
```

4. AnthropicのAPIキーを設定します:
- 環境変数 `ANTHROPIC_API_KEY` にAPIキーを設定するか、
- プロジェクトのルートディレクトリに `.env` ファイルを作成し、`ANTHROPIC_API_KEY=your_api_key_here` のように記述します。

## 使用方法

1. `resources` ディレクトリに解析したいMP4動画ファイルを配置します。

2. `main.py` の以下の部分を編集します:

```python
if __name__ == "__main__":
    video_file_path = os.path.join("resources", "video_name.mp4")  # ビデオファイルのパスを指定
    prompt = "これは動画のフレーム画像です。動画の最初から最後の流れ、動作を微分して日本語で解説してください。"  # プロンプトを指定
    model = "claude-3-sonnet-20240229"  # モデルを指定 "claude-3-opus-20240229" or "claude-3-sonnet-20240229"

    get_text_from_video(video_file_path, prompt, model)
```

- `video_file_path` に解析したい動画ファイルのパスを指定します。
- `prompt` に動画解析のためのプロンプトを指定します。
- `model` に使用するClaude-3モデルを指定します。

3. スクリプトを実行します:

```
python main.py
```

解析結果がコンソールに出力されます。


## ライセンス
このプロジェクトはMITライセンスの下で公開されています。詳細については、LICENSEファイルを参照してください。

