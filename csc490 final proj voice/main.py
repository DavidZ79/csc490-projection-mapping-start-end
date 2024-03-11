from pydub import AudioSegment
from pydub.silence import *  # docs: https://github.com/jiaaro/pydub/blob/master/pydub/silence.py
import speech_recognition as sr
import io


def detect_voice_segments(audio_file):
    audio = AudioSegment.from_file(audio_file)  # load audio file into AudioSegment obj

    segments = split_on_silence(audio, min_silence_len=500, silence_thresh=-50)

    # 2d array: inner list is [start, end] in ms
    start_end_times = detect_nonsilent(audio, min_silence_len=500, silence_thresh=-50)

    # return list of tuples, each tuple represents a segment (start, end, segment audio object)
    num_of_segments = len(segments)  # len(segments) = len(start_end_times)
    voice_segments = []
    for i in range(num_of_segments):
        # divide by 1000 for ms -> s
        voice_segments.append((start_end_times[i][0] / 1000, start_end_times[i][1] / 1000, segments[i]))

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







