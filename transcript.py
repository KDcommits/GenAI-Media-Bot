import whisper
import os, glob

def speech2Text(recorded_audio_path, transcripted_audio_path):
    try:
        # find most recent files in a directory
        print(recorded_audio_path)
        recordings_dir = os.path.join(recorded_audio_path,'*')
        model = whisper.load_model("base")

        # get most recent wav recording in the recordings directory
        files = sorted(glob.iglob(recordings_dir), key=os.path.getctime, reverse=True)
        latest_recording = files[0]
        print("latest_recording : ", latest_recording)
        latest_recording_filename = latest_recording.split('\\')[-1]
        print("latest_recording_filename : ", latest_recording_filename)

        if os.path.exists(latest_recording):
            audio = whisper.load_audio(latest_recording)
            audio = whisper.pad_or_trim(audio)
            mel = whisper.log_mel_spectrogram(audio).to(model.device)
            options = whisper.DecodingOptions(language= 'en', fp16=False)

            result = whisper.decode(model, mel, options)

            if result.no_speech_prob < 0.5:
                print(result.text)
                textfiles = os.listdir(transcripted_audio_path)
                if len(textfiles)!=0:
                    os.remove(os.path.join(transcripted_audio_path,textfiles[0]))

                transcription_filename = os.path.join(transcripted_audio_path,'input_audio_transcription.txt')#'Stored Data/Input/Transcription/input_audio_transcription.txt'
                with open(transcription_filename, 'a') as f:
                    f.write(result.text)

                return result.text
            
            else:
                alternate_text = "The input audio contains no word"
                textfiles = os.listdir(transcripted_audio_path)
                if len(textfiles)!=0:
                    os.remove(os.path.join(transcripted_audio_path,textfiles[0]))

                transcription_filename = os.path.join(transcripted_audio_path,'input_audio_transcription.txt')#'Stored Data/Input/Transcription/input_audio_transcription.txt'
                with open(transcription_filename, 'a') as f:
                    f.write(alternate_text)

                return alternate_text

    except:
        print("Error! Check 'speech2Text' function")

# recorded_audio_path = "C:\\Users\\krish\\OneDrive\\Desktop\\Study\\Gen AI\\Gen AI - PDFBot\\Data\\Input\\Input Audio\\"
# transcripted_audio_path = 'C:\\Users\\krish\\OneDrive\\Desktop\\Study\\Gen AI\\Gen AI - PDFBot\\Data\\Output\\Audio Transcript\\'
# speech2Text(recorded_audio_path,transcripted_audio_path)
