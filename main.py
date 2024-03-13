import anthropic
import base64
import cv2
import tempfile
import time
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

def get_frames_from_video(file_path):
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
   return base64_frames, buffer

def get_text_from_video(file_path):
   # ビデオからフレームを取得し、それらをbase64にエンコードする
   base64_frames, buffer = get_frames_from_video(file_path)

   # Claude APIにリクエストを送信
   prompt = '''
   これは動画のフレーム画像です。動画の最初から最後の流れ、動作を日本語で解説してください。どちらが点をとりましたか？
   '''
   message = client.messages.create(
       model="claude-3-opus-20240229",  # モデル指定
       max_tokens=1024,  # 最大トークン数
       messages=[
           {
               "role": "user",
               "content": [
                   *map(lambda x: {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": x}}, base64_frames[0::90]),
                   {
                       "type": "text",
                       "text": prompt
                   }
               ],
           }
       ],
   )
   time.sleep(0.5)
   return message.content[0].text, buffer

if __name__ == "__main__":
   video_file_path = "path/to/your/video.mp4"
   text, buffer = get_text_from_video(video_file_path)
   print(text)