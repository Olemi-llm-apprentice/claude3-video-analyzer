import anthropic
import base64
import cv2
from dotenv import load_dotenv
import os

# APIキーの取得
api_key = os.getenv("ANTHROPIC_API_KEY")

if api_key is None:
    # 環境変数にAPIキーがない場合は、.envファイルから読み取る
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

if api_key is None:
    # 環境変数にも.envファイルにもAPIキーがない場合は、エラーメッセージを表示して終了する
    print("Error: ANTHROPIC_API_KEY not found in environment variables or .env file.")
    exit(1)

# Anthropicクライアントの初期化
client = anthropic.Anthropic(api_key=api_key)

def get_frames_from_video(file_path, max_images=20):
    video = cv2.VideoCapture(file_path)
    base64_frames = []
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64_frame = base64.b64encode(buffer).decode("utf-8")
        base64_frames.append(base64_frame)
    video.release()

    # 選択する画像の数を制限する
    selected_frames = base64_frames[0::len(base64_frames)//max_images][:max_images]

    return selected_frames, buffer

def get_text_from_video(file_path, prompt, model, max_images=20):
    # ビデオからフレームを取得し、それらをbase64にエンコードする
    print(f"{file_path}:\nフレーム取得開始")
    base64_frames, buffer = get_frames_from_video(file_path, max_images)
    print("フレーム取得完了")
    # Claude APIにリクエストを送信
    with client.messages.stream(
        model=model,  # モデル指定
        max_tokens=1024,  # 最大トークン数
        messages=[
            {
                "role": "user",
                "content": [
                    *map(lambda x: {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": x}}, base64_frames),
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    ) as stream:
        for text in stream.text_stream: 
            print(text, end="", flush=True)

if __name__ == "__main__":
    video_file_path = os.path.join("resources", "video_name.mp4")  # ビデオファイルのパスを指定
    prompt = "これは動画のフレーム画像です。動画の最初から最後の流れ、動作を微分して日本語で解説してください。"  # プロンプトを指定
    model = "claude-3-sonnet-20240229"  # モデルを指定 "claude-3-opus-20240229" or "claude-3-sonnet-20240229"

    get_text_from_video(video_file_path, prompt, model)
