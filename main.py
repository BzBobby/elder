# main.py

import re
import requests
import time
import platform
from config import API_URL, API_KEY, MODEL, MAX_HISTORY, MAX_TOKENS
from roles import character_prompts
from asr.record_and_transcribe import record_audio_with_vad, transcribe_audio
from tts.speak_streaming import stream_speak
from history.keywords import save_keywords, get_top_keywords
from history.conversation import save_conversation
from history.summary import summarize_keywords_with_ai
from utils.farewell import generate_farewell

def clean_reply(text: str) -> str:
    text = re.sub(r"[\(（][^）\)]*[\)）]", "", text)
    return re.sub(r"\s+", " ", text).strip()

def extract_keywords(text: str):
    words = re.findall(r"[\u4e00-\u9fff]{2,}", text)
    return list(set(words))

def choose_character():
    print("请选择角色：")
    for i, key in enumerate(character_prompts, 1):
        print(f"{i}. {key}")
    while True:
        idx = input("输入编号 (1-{}): ".format(len(character_prompts))).strip()
        if idx.isdigit() and 1 <= int(idx) <= len(character_prompts):
            name = list(character_prompts.keys())[int(idx)-1]
            return name, character_prompts[name]
        print("无效输入，请重试")

def main():
    role_key, base_prompt = choose_character()

    # 加入关键词记忆
    keywords = get_top_keywords()
    if keywords:
        base_prompt += f"\n你记得用户曾经提到过这些话题：{', '.join(keywords)}。请基于这些信息更亲切地回应。"

    history = [{"role": "system", "content": base_prompt}]
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    print("\n🎤 语音对话已启动，说“退出”结束。\n")

    while True:
        audio_path = record_audio_with_vad()
        user_text = transcribe_audio(audio_path).strip()
        if not user_text:
            print("（未检测到语音）")
            continue
        print("👵 你说：", user_text)

        if any(w in user_text for w in ["退出", "再见", "拜拜"]):
            farewell = generate_farewell(history)
            print("👋", farewell)
            stream_speak(farewell)  # 朗读这句话
            save_conversation(history, role_key)
            summarize_keywords_with_ai()  # 退出前进行一次AI关键词总结
            break

        # 存储关键词
        keywords = extract_keywords(user_text)
        save_keywords(keywords)

        history.append({"role": "user", "content": user_text})
        payload = {
            "model": MODEL,
            "messages": history[-(MAX_HISTORY*2+1):],
            "temperature": 0.7,
            "max_tokens": MAX_TOKENS
        }

        try:
            r = requests.post(API_URL, headers=headers, json=payload, timeout=15)
            r.raise_for_status()
            raw_reply = r.json()["choices"][0]["message"]["content"].strip()
            reply = clean_reply(raw_reply)

            print("🧑 回复中：")
            stream_speak(reply)
            history.append({"role": "assistant", "content": reply})

        except Exception as e:
            print("[错误] 请求失败：", e)

if __name__ == "__main__":
    main()