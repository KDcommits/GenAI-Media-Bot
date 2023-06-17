import os
import re
import openai
import shutil
import datetime
# from dotenv import load_dotenv
# from transcript import speech2Text
# from counter import generateResponse
# from text2speech import synthesize_speech
from flask import Flask,request, jsonify, render_template

# load_dotenv()

# openai.api_key = os.getenv('OPENAI_KEY')

def filename():
    now = str(datetime.datetime.now())
    return re.sub('[^0-9]','',now)


app= Flask(__name__)
app.config["UPLOAD_FOLDER"] ="./Data/"
# app.config["INPUT_AUDIO"] = ".\\recordings\\Input\\Input Audio\\"
# app.config['INPUT_AUDIO_TRANSCRIPTION'] = ".\\recordings\\Input\\Transcription\\"
# app.config["GPT_RESPONSE"] ='.\\recordings\\Output\\GPT Response\\'
# app.config["OUTPUT_AUDIO"] = '.\\recordings\\Output\\Output Audio\\'
# app.config['STATIC_PATH']= '.\\static\\'

@app.route('/', methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def audioTranscripter():
    return render_template('index.html')

@app.route('/result', methods=['GET','POST'])
def result():
    if request.method == "POST":
        if 'data' in request.files:
            # input_audio_file = 'recorded_audio.wav'
            # os.remove(os.path.join(os.path.join(app.config['INPUT_AUDIO'],input_audio_file)))
            file = request.files['data']
            filepath = os.path.join(app.config["UPLOAD_FOLDER"] , 'recorded_audio.wav')
            file.save(filepath)
            return jsonify("Input Audio is stored")

        if 'pdfFile' in request.files:
            file = request.files['pdfFile']
            filepath = os.path.join(app.config["UPLOAD_FOLDER"] , 'downloaded_pdf.pdf')
            file.save(filepath)
            return jsonify("File uploaded successfully!")

            # transcripted_text = 'input_audio_transcription.txt'
            # # os.remove(os.path.join(app.config['INPUT_AUDIO_TRANSCRIPTION'],transcripted_text))
            # response_text = generateResponse(app.config['INPUT_AUDIO_TRANSCRIPTION'], app.config["GPT_RESPONSE"] )

            # return jsonify(response_text)
            
        

# @app.route('/display', methods=['GET','POST'])
# def displayText():
#     if request.method == "POST":
#         gpt_response_text = 'response.txt'
#         print(app.config["INPUT_AUDIO"])
#         # os.remove(os.path.join(os.path.join(app.config["GPT_RESPONSE"] ,gpt_response_text)))
#         transcript = speech2Text(app.config["INPUT_AUDIO"], app.config['INPUT_AUDIO_TRANSCRIPTION'])
#         return jsonify(transcript)

# @app.route('/audate',methods=['GET','POST'])
# def audateResponse():
#     if request.method == "POST":
#         response_text = generateResponse(app.config['INPUT_AUDIO_TRANSCRIPTION'], app.config["GPT_RESPONSE"] )
#         synthesize_speech(app.config["GPT_RESPONSE"],app.config["OUTPUT_AUDIO"])
#         return jsonify(response_text)

# if __name__ == "__main__":
#     app.run(debug=False)