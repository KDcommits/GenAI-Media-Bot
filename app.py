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
from data import Data
from model import Model
from excelAI import ExcelQuery
from sql import SQLQuerywithFunctionCalling
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
sql_query_obj = SQLQuerywithFunctionCalling()

@app.route('/', methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def clearTempFiles():
    '''
        With each refresh of the webpage it will delete the previously created vectot database
        and audio transcript.
    '''
    ## Deletion of downloaded pdf
    if len(os.listdir(app.config["INPUT_PDF_FOLDER"] ))>0:
        for uploaded_filename in os.listdir(app.config["INPUT_PDF_FOLDER"]):
            uploaded_file = os.path.join(app.config["INPUT_PDF_FOLDER"],uploaded_filename)
            os.remove(uploaded_file)
            
    ## Deletion of vector db storage
    if len(os.listdir(app.config["VECTOR_DB_FOLDER"]))>0:
        for vector_filename in os.listdir(app.config["VECTOR_DB_FOLDER"]):
            vector_file = os.path.join(app.config["VECTOR_DB_FOLDER"],vector_filename)
            os.remove(vector_file)

    ## Deletion of audio transcript
    if len(os.listdir(app.config['TRANSCRIPTED_AUDIO_FOLDER']))>0:
        for transcript_filename in os.listdir(app.config['TRANSCRIPTED_AUDIO_FOLDER']):
            transcription = os.path.join(app.config['TRANSCRIPTED_AUDIO_FOLDER'],transcript_filename)
            os.remove(transcription)
                
    return render_template('index.html')

@app.route('/result', methods=['GET','POST'])
def result():
    if request.method == "POST":
        if 'audioData' in request.files:
            file = request.files['audioData']
            filepath = os.path.join(app.config["UPLOAD_AUDIO_FOLDER"] , 'recorded_audio.wav')
            file.save(filepath)
            speech2Text(app.config["INPUT_AUDIO_FOLDER"] , app.config['TRANSCRIPTED_AUDIO_FOLDER'])
            if len(os.listdir(app.config['TRANSCRIPTED_AUDIO_FOLDER']))>0:
                return jsonify("Input Audio is stored")
        
        if 'pdfFile' in request.files:
            file = request.files['pdfFile']
            print("files:", request.files)
            filepath = os.path.join(app.config["UPLOAD_PDF_FOLDER"], file.filename)
            file.save(filepath)
            data_obj.createPDFVectorDBwithFAISS(chunk_size=2000, chunk_overlap=500)
            ## To counterbalance the time taken for the vector db creation
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
    # input_file_path = app.config["INPUT_PDF_FOLDER"]
    # files_dir = os.path.join(input_file_path,'*')
    # latest_file = sorted(glob.iglob(files_dir), key=os.path.getmtime, reverse=True)[0]
    # print(latest_file)

    if len(os.listdir(app.config["VECTOR_DB_FOLDER"]))!=0:

        # if latest_file.count('.pdf') ==1:
        top_k_chunks = data_obj.create_top_k_chunk_from_FAISS(input_question, top_k =3)

        prompt = model_obj.createQuestionPrompt(top_k_chunks)
        prompt_template = model_obj.createQuestionPromptTemplate(prompt)
        response = model_obj.generateAnswerwithMemory(input_question, prompt_template,chat_history=[])
        return jsonify(response),200

        # if latest_file.count('.xlsx') == 1:
        #     # stored_excel_filename = 'downloaded_excel.xlsx'
        #     # excel_filepath = os.path.join(input_file_path, stored_excel_filename)
        #     # query_result = ExcelQuery(OPENAI_KEY).excelQuery(latest_file,input_text)
        #     # return jsonify(query_result)

        #     time.sleep(5)
        #     return jsonify("HI from KD, Excel " + latest_file)
        
    else:
        # top_k_chunks = data_obj.create_top_k_chunk_from_Pinecone(input_question,top_k=3)
        # prompt = model_obj.createQuestionPrompt(top_k_chunks)
        # prompt_template = model_obj.createQuestionPromptTemplate(prompt=prompt)
        # response_pdf = model_obj.generateAnswerwithMemory(input_question, prompt_template,chat_history=[])
        response_sql = sql_query_obj.openai_functions_chain(input_question)
        # pdf_valid_response = response_pdf.lower().__contains__("found nothing") | response_pdf.lower().__contains__("sorry") 
        # sql_valid_response = response_sql.lower().__contains__("found nothing") | response_sql.lower().__contains__("sorry") 
        return jsonify(response_sql),200
        

@app.route('/audio-question', methods=['GET','POST'])
def fetchAudioQuestion():
    if len(os.listdir(app.config['TRANSCRIPTED_AUDIO_FOLDER']))>0:

        transcripted_audio_file = 'input_audio_transcription.txt'
        with open(os.path.join(app.config['TRANSCRIPTED_AUDIO_FOLDER'], transcripted_audio_file)) as f_audio:
            input_question = "".join(f_audio)
            print(input_question)
        f_audio.close()

        if len(os.listdir(app.config["VECTOR_DB_FOLDER"]))!=0:
            top_k_chunks = data_obj.create_top_k_chunk_from_FAISS(input_question, top_k =3)
            prompt = model_obj.createQuestionPrompt(top_k_chunks)
            prompt_template = model_obj.createQuestionPromptTemplate(prompt)
            response = model_obj.generateAnswerwithMemory(input_question, prompt_template,chat_history=[])
            print(response)
            os.remove(os.path.join(app.config['TRANSCRIPTED_AUDIO_FOLDER'], transcripted_audio_file))
            return jsonify(response),200
        else:
            # top_k_chunks = data_obj.create_top_k_chunk_from_Pinecone(input_question,top_k=3)
            # prompt = model_obj.createQuestionPrompt(top_k_chunks)
            # prompt_template = model_obj.createQuestionPromptTemplate(prompt=prompt)
            # response_pdf = model_obj.generateAnswerwithMemory(input_question, prompt_template,chat_history=[])
            response_sql = sql_query_obj.openai_functions_chain(input_question)
            os.remove(os.path.join(app.config['TRANSCRIPTED_AUDIO_FOLDER'], transcripted_audio_file))
            # pdf_valid_response = response_pdf.lower().__contains__("found nothing") | response_pdf.lower().__contains__("sorry") 
            # sql_valid_response = response_sql.lower().__contains__("found nothing") | response_sql.lower().__contains__("sorry") 
            return jsonify({'audio_transcript':input_question,'response_sql':response_sql}),200

    else:
        time.sleep(0.5)
        return fetchAudioQuestion()


if __name__ == "__main__":
    app.run(debug=False)