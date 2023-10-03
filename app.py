import os
import re
import json 
import glob
import time
import openai
import shutil
import datetime
import pandas as pd
from dotenv import load_dotenv
from transcript import speech2Text
from data_final import Data
from model_final import Model
from excelAI import ExcelQuery
from flask import Flask,request, jsonify, render_template

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_KEY')
OPENAI_KEY = os.getenv("OPENAI_KEY")


def filename():
    now = str(datetime.datetime.now())
    return re.sub('[^0-9]','',now)


app= Flask(__name__)
app.config["UPLOAD_AUDIO_FOLDER"] = os.getenv('UPLOAD_AUDIO_FOLDER')
app.config["UPLOAD_PDF_FOLDER"] = os.getenv('UPLOAD_PDF_FOLDER')
app.config["UPLOAD_EXCEL_FOLDER"] = os.getenv('UPLOAD_EXCEL_FOLDER')
app.config["INPUT_AUDIO_FOLDER"] = os.path.join(os.getcwd(),'Data','Input','Input Audio')
app.config["INPUT_PDF_FOLDER"] = os.path.join(os.getcwd(),'Data','Input','Input File')
app.config["VECTOR_DB_FOLDER"] = os.path.join(os.getcwd(),'Data','Input','VectorDB')
app.config["INPUT_CHUNKS_FOLDER"] = os.path.join(os.getcwd(),'Data','Input','Input Chunks')
app.config['TRANSCRIPTED_AUDIO_FOLDER'] = os.path.join(os.getcwd(),'Data','Output','Audio Transcript')

data_obj = Data(app.config["INPUT_PDF_FOLDER"], app.config["VECTOR_DB_FOLDER"])
model_obj = Model()

@app.route('/', methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def audioTranscripter():
    # for pdf_filename in os.listdir(app.config["UPLOAD_PDF_FOLDER"]):
    #     pdf_path = os.path.join(app.config["UPLOAD_PDF_FOLDER"],pdf_filename)
    #     os.remove(pdf_path)

    if len(os.listdir(app.config["VECTOR_DB_FOLDER"]))>0:
        for vector_filename in os.listdir(app.config["VECTOR_DB_FOLDER"]):
            vector_file = os.path.join(app.config["VECTOR_DB_FOLDER"],vector_filename)
            os.remove(vector_file)

    if len(os.listdir(app.config['TRANSCRIPTED_AUDIO_FOLDER']))>0:
        for transcript_filename in os.listdir(app.config['TRANSCRIPTED_AUDIO_FOLDER']):
            transcription = os.path.join(app.config['TRANSCRIPTED_AUDIO_FOLDER'],transcript_filename)
            os.remove(transcription)
                

    return render_template('index.html')

@app.route('/result', methods=['GET','POST'])
def result():
    if request.method == "POST":
        if 'data' in request.files:
            # input_audio_file = 'recorded_audio.wav'
            # os.remove(os.path.join(os.path.join(app.config['INPUT_AUDIO'],input_audio_file)))
            file = request.files['data']
            filepath = os.path.join(app.config["UPLOAD_AUDIO_FOLDER"] , 'recorded_audio.wav')
            file.save(filepath)
            speech2Text(app.config["INPUT_AUDIO_FOLDER"] , app.config['TRANSCRIPTED_AUDIO_FOLDER'])
            if len(os.listdir(app.config['TRANSCRIPTED_AUDIO_FOLDER']))>0:
                return jsonify("Input Audio is stored")
        

        if 'pdfFile' in request.files:
            pdf_filename = 'downloaded_pdf.pdf'
            file = request.files['pdfFile']
            filepath = os.path.join(app.config["UPLOAD_PDF_FOLDER"], pdf_filename)
            file.save(filepath)
            data_obj.createPDFVectorDBwithFAISS(chunk_size=2000, chunk_overlap=500)
            if len(os.listdir(app.config["VECTOR_DB_FOLDER"]))>0:
                return jsonify("Input PDF is stored")
        
        if 'excelFile' in request.files:
            excel_filename = 'downloaded_excel.xlsx'
            file = request.files['excelFile']
            filepath = os.path.join(app.config["UPLOAD_EXCEL_FOLDER"], excel_filename)
            file.save(filepath)

            return jsonify("Input Excel is stored")
        else:
            error = 'Some Error Occured!'
            return jsonify({'error': error})
        
@app.route('/text-question', methods=['GET','POST'])
def fetchTextQuestion():
    input_question = request.json['text'].strip()
    input_file_path = app.config["INPUT_PDF_FOLDER"]
    files_dir = os.path.join(input_file_path,'*')
    latest_file = sorted(glob.iglob(files_dir), key=os.path.getmtime, reverse=True)[0]
    print(latest_file)

    if latest_file.count('.pdf') ==1:
        top_k_chunks = data_obj.create_top_k_chunk_from_FAISS(input_question, top_k =3)

        prompt = model_obj.createQuestionPrompt(top_k_chunks)
        prompt_template = model_obj.createQuestionPromptTemplate(prompt)
        response = model_obj.generateAnswerwithMemory(input_question, prompt_template,chat_history=[])
        return jsonify(response),200

    if latest_file.count('.xlsx') == 1:
        # stored_excel_filename = 'downloaded_excel.xlsx'
        # excel_filepath = os.path.join(input_file_path, stored_excel_filename)
        # query_result = ExcelQuery(OPENAI_KEY).excelQuery(latest_file,input_text)
        # return jsonify(query_result)

        time.sleep(5)
        return jsonify("HI from KD, Excel " + latest_file)




@app.route('/audio-question', methods=['GET','POST'])
def fetchAudioQuestion():
    transcripted_audio_file = 'input_audio_transcription.txt'
    with open(os.path.join(app.config['TRANSCRIPTED_AUDIO_FOLDER'], transcripted_audio_file)) as f_audio:
        input_question = "".join(f_audio)
    f_audio.close()
    top_k_chunks = data_obj.create_top_k_chunk_from_FAISS(input_question, top_k =3)
    prompt = model_obj.createQuestionPrompt(top_k_chunks)
    prompt_template = model_obj.createQuestionPromptTemplate(prompt)
    response = model_obj.generateAnswerwithMemory(input_question, prompt_template,chat_history=[])
    print(response)
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=False)