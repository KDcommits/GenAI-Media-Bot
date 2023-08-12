//function to display text message 
function sendMessage() {
    var startTime = new Date();
    const userInput = document.getElementById('textInput').value.trim();
    const userMessage = createUserMessage(userInput);
    const chatWindow = document.getElementById('chatWindow')
    chatWindow.appendChild(userMessage);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    document.getElementById('textInput').value = '';
    const waitMessage = displayPleaseWaitMessage(startTime);
    chatWindow.appendChild(waitMessage);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    if (userInput !== '') {
      // Show please wait message 
        fetch('/text-question', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: userInput })
          }).then(response => response.json())
          .then(responseData => {
        console.log("Response from backend:", responseData);
        console.log(waitMessage);
        // remove please wait message
        displayPleaseWaitMessage(startTime);
        waitMessage.classList.add('hidden');

        // Optionally, you can send the user's text message to your chatbot backend for processing
        // In this example, we'll simulate a response from the bot
        var botResponse = simulateBotTextResponse(responseData);
        chatWindow.appendChild(botResponse);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    })
    .catch(error => {
        console.error("Error:", error);
        // Handle any errors that occur during the request
      });
}}

//Function to create a user message
function createUserMessage(message) {
    const userMessage = document.createElement('div');
    userMessage.className = 'userMessage';
    var now = new Date();
    var timeString = now.toLocaleTimeString("en-US", 
                                                { timeZone: "Asia/Kolkata", hour12: false, 
                                                  hour: "numeric",  minute: "numeric" });
    userMessage.innerHTML ="<p style='text-align:right;'>" + "<span>"+message+"</span>" + "<span class='footnote';'>"+ " "+timeString+ "</span>"+"</p>";
    // console.log(message);
    // $.ajax({
    //     type: 'POST',
    //     url: '/text-question',
    //     data: JSON.stringify({'input_text':message}),
    //     contentType: false,
    //     processData: false
    // });
    return userMessage;
  }

function simulateBotTextResponse(openai_response){
    console.log(typeof(openai_response))
    const botMessage = document.createElement('div');
    botMessage.className = 'botMessage';
    botMessage.innerHTML ="<p>" + openai_response + "</p>";
    // const chatWindow = document.getElementById('chatWindow');
    // return chatWindow.appendChild(botMessage);
    return botMessage;

    }

function handleKeyPress(event) {
    if (event.keyCode === 13) {
    sendMessage();
    }
}

var isExecutionCompleted = true;
function displayPleaseWaitMessage(startTime) {
  const waitMessage  = document.createElement('div'); 
  waitMessage.className = 'hidden';
  if (isExecutionCompleted){
    var timer = setInterval(function() {
            var elapsedSeconds = Math.floor((new Date() - startTime) / 1000);
            $('#timer').text(elapsedSeconds);
            }, 1000);
    waitMessage.classList.remove('hidden');
    waitMessage.innerHTML = "<p align='center'>" + "Please Wait..."+"<span id='timer'>"+0+"</span>" + "</p>";
  }
  else {
    waitMessage.classList.add('hidden');
    waitMessage.innerHTML="";
  }
  isExecutionCompleted = !isExecutionCompleted;
  return waitMessage;
}