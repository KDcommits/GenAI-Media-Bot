// Create a new instance of the Media Recorder
let mediaRecorder;
const recordedChunks = [];
let isRecording = false;

// Function to toggle recording audio
function toggleRecording() {
  var recordButton = document.getElementById('audioRecordButton');
  if (isRecording) {
    stopRecording();
    isRecording = false;
    recordButton.style.backgroundColor = '#86ce89'; //green
  } else {
    startRecording();
    isRecording = true;
    recordButton.style.backgroundColor = '#e24d42'; //red
  }
}

// Function to start recording audio
function startRecording() {
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function (stream) {
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.start();

      // Event listener to collect recorded audio data
      mediaRecorder.addEventListener('dataavailable', function (e) {
        recordedChunks.push(e.data);
      });
    })
    .catch(function (err) {
      alert('Error accessing microphone: ' + err)
      //console.log('Error accessing microphone: ' + err);
    });
}

// Function to stop recording audio and send it to the chat window
function stopRecording() {
  mediaRecorder.stop();
  mediaRecorder.addEventListener('stop', function () {
    const audioBlob = new Blob(recordedChunks, { 'type': 'audio/wav; codecs=MS_PCM' });
    const audioUrl = URL.createObjectURL(audioBlob);
    let formData = new FormData();
    formData.append('audioData', audioBlob, "data.wav");
    $.ajax({
        type: 'POST',
        url: '/result',
        data: formData,
        contentType: false,
        processData: false
    });
    // Create an audio element and append it to the chat window
    const audioElement = document.createElement('audio');
    audioElement.className = 'userAudioMessage';
    audioElement.src = audioUrl;
    audioElement.controls = true;
    document.getElementById('chatWindow').appendChild(audioElement);
    document.getElementById('audioMessage').innerHTML = '';
    // Optionally, you can send the audioBlob to your chatbot backend for processing
    // In this example, we'll simulate a response from the bot
    displayResponse();
  });

  recordedChunks.length = 0;
}


function stimulateBotAudioResponse(responseData){
  const botMessage = document.createElement('div');
  botMessage.className = 'botMessage';
  botMessage.innerText = responseData;
  return document.getElementById('chatWindow').appendChild(botMessage);
}

function displayResponse() {
  fetch('/audio-question', {
    method: 'POST',
    body: JSON.stringify(),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(responseData => {
    console.log("Response from backend:", responseData);
    const userMessage = createUserMessage(responseData['audio_transcript']);
    chatWindow.appendChild(userMessage);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    document.getElementById('textInput').value = '';
    stimulateBotAudioResponse(responseData['response_sql']);
  })
  .catch(error => {
    console.error("Error:", error);
  });
}


function createUserMessage(message) {
  const userMessage = document.createElement('div');
  userMessage.className = 'userMessage';
  var now = new Date();
  var timeString = now.toLocaleTimeString("en-US", 
                                              { timeZone: "Asia/Kolkata", hour12: false, 
                                                hour: "numeric",  minute: "numeric" });
  userMessage.innerHTML ="<p style='text-align:right;'>" + "<span>"+message+"</span>" + "<span class='footnote';'>"+ " "+timeString+ "</span>"+"</p>";
  return userMessage;
}