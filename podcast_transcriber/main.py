import os
import json
from pathlib import Path

from pydub import AudioSegment

from faster_whisper import WhisperModel

from pyannote.audio import Pipeline

import config



# ------------------------------------
# Ordner vorbereiten
# ------------------------------------

os.makedirs(
    config.OUTPUT_FOLDER,
    exist_ok=True
)


# ------------------------------------
# Modelle laden
# ------------------------------------

print("Lade Whisper Modell...")

whisper = WhisperModel(
    config.WHISPER_MODEL,
    device="cuda",
    compute_type="float16"
)


print("Lade Sprechererkennung...")


diarization_pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=config.HF_TOKEN
)



# ------------------------------------
# Sprecher erkennen
# ------------------------------------

def detect_speakers(wav_file):

    print("Sprecheranalyse...")

    result = diarization_pipeline(wav_file)

    speakers = []


    for turn, _, speaker in result.itertracks(
        yield_label=True
    ):

        speakers.append(
            {
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker
            }
        )


    return speakers



# ------------------------------------
# Audio transkribieren
# ------------------------------------

def transcribe_audio(wav_file):

    print("Transkription...")


    segments, info = whisper.transcribe(
        wav_file,
        language=config.LANGUAGE,
        beam_size=5
    )


    result = []


    for segment in segments:

        result.append(
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            }
        )


    return result




# ------------------------------------
# Sprecher zu Text zuordnen
# ------------------------------------

def assign_speakers(
        transcription,
        speakers
):

    final = []


    for text_segment in transcription:


        speaker_name = "UNKNOWN"


        midpoint = (
            text_segment["start"]
            +
            text_segment["end"]
        ) / 2



        for speaker in speakers:

            if (
                speaker["start"]
                <= midpoint
                <= speaker["end"]
            ):

                speaker_name = speaker["speaker"]
                break



        final.append(
            {
                "start":
                    text_segment["start"],

                "end":
                    text_segment["end"],

                "speaker":
                    speaker_name,

                "text":
                    text_segment["text"]
            }
        )


    return final



# ------------------------------------
# Markdown Ausgabe
# ------------------------------------

def save_markdown(data, filename):

    path = Path(
        config.OUTPUT_FOLDER
    ) / filename


    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:


        for line in data:


            minutes = int(
                line["start"] // 60
            )

            seconds = int(
                line["start"] % 60
            )


            timestamp = (
                f"{minutes:02d}:"
                f"{seconds:02d}"
            )


            f.write(
                f"\n## [{timestamp}] "
                f"{line['speaker']}\n\n"
            )

            f.write(
                line["text"]
            )

            f.write("\n")



# ------------------------------------
# JSON Ausgabe
# ------------------------------------

def save_json(data, filename):

    path = Path(
        config.OUTPUT_FOLDER
    ) / filename


    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )



# ------------------------------------
# Hauptprogramm
# ------------------------------------

def process_file(mp3):


    name = mp3.stem


    print("\n===================")
    print(name)
    print("===================")


    wav = (
        Path("input")
        /
        f"{name}.wav"
    )


    if not wav.exists():

        print("Konvertiere MP3...")

        audio = AudioSegment.from_mp3(
            mp3
        )

        audio.export(
            wav,
            format="wav"
        )



    speakers = detect_speakers(
        wav
    )


    transcription = transcribe_audio(
        wav
    )


    combined = assign_speakers(
        transcription,
        speakers
    )


    save_json(
        combined,
        f"{name}.json"
    )


    save_markdown(
        combined,
        f"{name}.md"
    )


    print(
        "Fertig:",
        name
    )





# ------------------------------------
# Alle Podcasts verarbeiten
# ------------------------------------

files = list(
    Path(config.INPUT_FOLDER)
    .glob("*.mp3")
)


if not files:

    print(
        "Keine MP3 Dateien gefunden"
    )

else:

    for file in files:

        process_file(file)


print("\nALLE PODCASTS FERTIG")