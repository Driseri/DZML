import sys
import json
import wave
from vosk import Model, KaldiRecognizer, SpkModel
from sklearn.cluster import KMeans
from pprint import pprint
import tkinter as tk
from tkinter import filedialog


def transcribe_and_split_speakers(audio_file, model_path, spk_model_path):
    # Загрузка модели
    model = Model(model_path)
    spk_model = SpkModel(spk_model_path)

    data_speaker = []

    # Открытие аудиофайла
    with wave.open(audio_file, "rb") as wf:
        if wf.getnchannels() != 1:
            print("Audio file must be mono.")
            exit(1)
        if wf.getsampwidth() != 2:
            print("Audio file must be WAV format PCM. sampwidth=", wf.getsampwidth())
            exit(1)

        if wf.getcomptype() != "NONE":
            print("Audio file must be WAV format PCM. comptype=", wf.getcomptype())
            exit(1)

        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print("Audio file must be WAV format mono PCM.")
            sys.exit(1)

        # Создание распознавателя
        rec = KaldiRecognizer(model, wf.getframerate(), spk_model)

        # Распознавание и диаризация
        speakers = {}
        texts = []
        while True:
            data = wf.readframes(3000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                try:
                    speaker = res['spk']
                    data_speaker.append(speaker)
                    texts.append(res['text'])
                    # if speaker not in speakers:
                    #     speakers[speaker] = []
                    # speakers[speaker].append(res['text'])
                except:
                    print('неОТрбаотатаы')

        # # Вывод результатов
        # for speaker, text in speakers.items():
        #     print(f"Speaker {speaker}: {' '.join(text)}")
        #
    kmeans = KMeans(n_clusters=2)
    kmeans.fit(data_speaker)
    labels = kmeans.labels_


    spek = []
    current_s = labels[0]
    text_spk = ''
    for i in range(len(labels)):
        if labels[i] != current_s:
            spek.append([current_s, text_spk])
            current_s = labels[i]
            text_spk = ''
            text_spk = text_spk + ' ' + texts[i]
        else:
            text_spk = text_spk + ' ' + texts[i]

    import os
    import yaml
    import torch
    from torch import package

    with open('models.yml', 'r', encoding='utf-8') as yaml_file:
        models = yaml.load(yaml_file, Loader=yaml.SafeLoader)
    model_conf = models.get('te_models').get('latest')

    model_url = model_conf.get('package')

    model_dir = "downloaded_model"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, os.path.basename(model_url))

    if not os.path.isfile(model_path):
        torch.hub.download_url_to_file(model_url,
                                       model_path,
                                       progress=True)

    imp = package.PackageImporter(model_path)
    model = imp.load_pickle("te_model", "model")
    example_texts = model.examples

    def apply_te(text, lan='en'):
        return model.enhance_text(text, lan)


    spek_final = [[i[0], apply_te(i[1])] for i in spek]

    for spkss in spek_final:
        print('Спикер {}: '.format(spkss[0]) + spkss[1])

    return spek_final

# transcribe_and_split_speakers('nextFinal.wav', 'vosk-model-small-ru-0.22', 'vosk-model-spk-0.4')


def start_processing():
    filepath = filedialog.askopenfilename()
    print(filepath)
    speak_mass = transcribe_and_split_speakers(filepath, 'vosk-model-small-ru-0.22', 'vosk-model-spk-0.4')
    print(speak_mass)
    text_output.delete('1.0', tk.END)  # Очищаем текстовый блок
    for spkss in speak_mass:
        text_output.insert(tk.END ,'\nСпикер {}: '.format(spkss[0]) + spkss[1])


root = tk.Tk()

# Создаем поле выбора файла
file_button = tk.Button(root, text="Выбрать файл", command=start_processing)
file_button.pack(fill=tk.X, padx=10, pady=10)

# Создаем текстовый блок
text_output = tk.Text(root)
text_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()

