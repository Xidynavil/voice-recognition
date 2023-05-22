import telebot
import os
import requests as rqt
import speech_recognition as sr
import librosa
import soundfile as sf
import SECRET

#in SECRET your token

recognizer = sr.Recognizer()
bot = telebot.TeleBot(token=SECRET.TOKEN)





def recognition(path):
    global text
    with sr.AudioFile(path) as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language='ru-RU')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, просто отправь мне голосовое сообщение, а я сделаю тебе расшифровку.')


@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        file = rqt.get('https://api.telegram.org/file/bot{0}/{1}'.format(SECRET.TOKEN, file_info.file_path))
        with open('voice.mp3', 'wb') as f:
            f.write(file.content)

        y, sr = librosa.load('voice.mp3', sr=16000)
        file1 = 'voice.wav'
        sf.write(file1, y, sr)
        recognition("voice.wav")
        bot.send_message(message.chat.id, text)
        os.remove("voice.wav")
        os.remove("voice.mp3")
    except:
        bot.reply_to(message, "Ошибка, попробуйте ещё раз")


bot.polling()
