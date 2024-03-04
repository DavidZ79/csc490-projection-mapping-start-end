# import speech_recognition as sr
#
# def detect_speech(audio_file):
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(audio_file) as source:
#         audio_data = recognizer.record(source)  # Read the entire audio file
#
#     try:
#         # Recognize speech using the default API key
#         text = recognizer.recognize_google(audio_data)
#         print("Transcription:")
#         print(text)
#     except sr.UnknownValueError:
#         print("Google Speech Recognition could not understand the audio")
#     except sr.RequestError as e:
#         print(f"Could not request results from Google Speech Recognition service; {e}")
#
# if __name__ == "__main__":
#     audio_file = input("Enter the path to the audio file: ")
#     detect_speech(audio_file)

from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
import io


def detect_voice_segments(audio_file):
    audio = AudioSegment.from_file(audio_file)  # load audio file into AudioSegment obj

    # split audio into segments based on silence
    segments = split_on_silence(audio, min_silence_len=500, silence_thresh=-50)

    voice_segments = []
    start_time = 0
    for segment in segments:
        if len(segment) > 0:  # Only consider segments with non-zero length
            end_time = start_time + len(segment) / 1000  # convert ms to s
            voice_segments.append((start_time, end_time, segment))
            start_time = end_time

    return voice_segments


def transcribe_voice_segments(voice_segments):
    recognizer = sr.Recognizer()
    transcripts = []
    for start_time, end_time, segment in voice_segments:
        with io.BytesIO() as wav_file:
            segment.export(wav_file, format="wav")
            wav_file.seek(0)
            try:
                audio_data = sr.AudioData(wav_file.read(), segment.frame_rate, 2)
                transcript = recognizer.recognize_google(audio_data)
                transcripts.append((start_time, end_time, transcript))
            except sr.UnknownValueError:
                transcripts.append((start_time, end_time, "Unknown"))
            except sr.RequestError as e:
                transcripts.append((start_time, end_time, f"Error: {e}"))

    return transcripts


if __name__ == "__main__":
    audio_file = input("Enter the path to the audio file: ")
    voice_segments = detect_voice_segments(audio_file)
    transcripts = transcribe_voice_segments(voice_segments)

    for i, (start_time, end_time, transcript) in enumerate(transcripts):
        print(f"Voice segment {i + 1}:")
        print(f"Start time: {start_time} seconds")
        print(f"End time: {end_time} seconds")
        print("Transcription:", transcript)
        print()







