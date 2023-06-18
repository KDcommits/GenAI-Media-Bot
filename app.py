import os
import re
import json 
import openai
import shutil
import datetime
from dotenv import load_dotenv
from transcript import speech2Text
from data import Data
from model import Model
from flask import Flask,request, jsonify, render_template

load_dotenv()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def filename():
    now = str(datetime.datetime.now())
    return re.sub('[^0-9]','',now)


app= Flask(__name__)
app.config["UPLOAD_AUDIO_FOLDER"] ="./Data/Input/Input Audio/"
app.config["UPLOAD_PDF_FOLDER"] ="./Data/Input/Input Pdf/"
app.config["INPUT_AUDIO_FOLDER"] = ".\\Data\\Input\\Input Audio\\"
app.config["INPUT_PDF_FOLDER"] = ".\\Data\\Input\\Input Pdf\\"
app.config['TRANSCRIPTED_AUDIO_FOLDER'] = ".\\Data\\Output\\Audio Transcript\\"
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
        print(request.files)
        if 'data' in request.files:
            # input_audio_file = 'recorded_audio.wav'
            # os.remove(os.path.join(os.path.join(app.config['INPUT_AUDIO'],input_audio_file)))
            file = request.files['data']
            filepath = os.path.join(app.config["UPLOAD_AUDIO_FOLDER"] , 'recorded_audio.wav')
            file.save(filepath)
            speech2Text(app.config["INPUT_AUDIO_FOLDER"] , app.config['TRANSCRIPTED_AUDIO_FOLDER'])

            return jsonify("Input Audio is stored")
        

        if 'pdfFile' in request.files:
            pdf_filename = 'downloaded_pdf.pdf'
            file = request.files['pdfFile']
            filepath = os.path.join(app.config["UPLOAD_PDF_FOLDER"], pdf_filename)
            file.save(filepath)
            _chunkifyPdfFile(app.config["INPUT_PDF_FOLDER"], pdf_filename)

            return jsonify("Input PDF is stored")

            # transcripted_text = 'input_audio_transcription.txt'
            # # os.remove(os.path.join(app.config['INPUT_AUDIO_TRANSCRIPTION'],transcripted_text))
            # response_text = generateResponse(app.config['INPUT_AUDIO_TRANSCRIPTION'], app.config["GPT_RESPONSE"] )

            # return jsonify(response_text)
        else:
            error = 'Some Error Occured!'
            return jsonify({'error': error})
        
@app.route('/text-question', methods=['GET','POST'])
def fetchTextQuestion():
    input_text = request.json['text']
    print(input_text)
    with open(os.path.join(app.config["INPUT_PDF_FOLDER"], 'chunks.json'), 'r') as f_read:
        chunk_data = json.load(f_read)
    f_read.close()
    # print(chunk_data[0])
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    print("OpenAI is Generating Response!")
    pdf_bot = Model(OPENAI_KEY, 
                      chunk_data, 
                      input_text) 
    print("\n OpenAI Generating results ... \n")
    response = pdf_bot.generateAnswer() 
    print("\n results generated \n")
    return jsonify(response)
    # return jsonify({'response': response})
    # return jsonify(f"Chunk data Length : {len(chunk_data)}")
    # return jsonify({"status": 200, 'message':'success'})



# @app.route('/audio-question', methods=['GET','POST'])
# def fetchAudioQuestion():


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


def _chunkifyPdfFile(filepath, filename):
    pdf_path = os.path.join(filepath,filename)
    chunks = Data(pdf_path).text_to_chunk()
    with open(os.path.join(filepath,'chunks.json'),'w') as f:
        json.dump(chunks, f)
    f.close()

if __name__ == "__main__":
    app.run(debug=False)