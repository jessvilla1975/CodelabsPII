import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import tempfile, os

SRATE = 16000     # tasa de muestreo
DUR = 5           # segundos

print("Grabando... habla ahora!")
audio = sd.rec(int(DUR*SRATE), samplerate=SRATE, channels=1, dtype='int16')
sd.wait()
print("Listo, procesando...")

# guarda a WAV temporal
fd, tmp_wav = tempfile.mkstemp(suffix=".wav")
os.close(fd)
write(tmp_wav, SRATE, audio)

# reconoce con SpeechRecognition
r = sr.Recognizer()
with sr.AudioFile(tmp_wav) as source:
    data = r.record(source)

try:
    texto = r.recognize_google(data, language="es-ES")
    print("Dijiste:", texto)

    cmd = texto.lower()

    if "hola" in cmd:
        print("¡Hola, bienvenido al curso!")
    elif "abrir google" in cmd:
        import webbrowser
        webbrowser.open("https://www.google.com")
    elif "hora" in cmd:
        from datetime import datetime
        print("Hora actual:", datetime.now().strftime("%H:%M"))
    elif "reproduce" in cmd:
        import requests, re, webbrowser
        cancion = cmd.replace("reproduce", "").strip()
        if cancion:
            search_url = "https://www.youtube.com/results?search_query=" + '+'.join(cancion.split())
            html = requests.get(search_url).text

            match = re.search(r"watch\?v=[\w-]+", html)
            if match:
                link = "https://www.youtube.com/" + match.group(0)
                print(f"Abriendo el video: {link}")
                webbrowser.open(link)
            else:
                print("No se encontró ningún video.")
    elif "brillo" in cmd:
        import re, subprocess
        controlador = "amdgpu_bl0"   #ls /sys/class/backlight/
        path_brightness = f"/sys/class/backlight/{controlador}/brightness"
        path_max = f"/sys/class/backlight/{controlador}/max_brightness"

        match = re.search(r"\d+", cmd)
        if match:
            valor = int(match.group())
            if 0 <= valor <= 100:
                with open(path_max, "r") as f:
                    max_brightness = int(f.read().strip())

                new_value = int(max_brightness * valor / 100)

                subprocess.run(   # sudoers (sudo visudo)
                    ["sudo", "tee", path_brightness],
                    input=str(new_value).encode(),
                    stdout=subprocess.DEVNULL,  
                    stderr=subprocess.DEVNULL
                )
                print(f"Brillo ajustado a {valor}%")
            else:
                print("Por favor, di un valor entre 0 y 100")
    elif "captura" in cmd:
        import re, pyautogui, time, datetime

        match = re.search(r"\d+", cmd)
        delay = int(match.group()) if match else 3 

        print(f"Tomando captura en {delay} segundos...")
        time.sleep(delay)

        filename = datetime.datetime.now().strftime("captura_%Y%m%d_%H%M%S.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)

        print(f"Captura guardada: {filename}")
    else:
        print("Comando no reconocido.")

except sr.UnknownValueError:
    print("No se entendió el audio.")
except sr.RequestError as e:
    print("Error:", e)
finally:
    if os.path.exists(tmp_wav):
        os.remove(tmp_wav)
