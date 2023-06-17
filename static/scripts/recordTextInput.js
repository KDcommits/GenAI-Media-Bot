//function to display text message 
function sendMessage() {
    const userInput = document.getElementById('textInput').value.trim();
    if (userInput.trim() !== '') {
        const userMessage = createUserMessage(userInput);
        document.getElementById('chatWindow').appendChild(userMessage);
        document.getElementById('textInput').value = '';

        // Optionally, you can send the user's text message to your chatbot backend for processing
        // In this example, we'll simulate a response from the bot
        simulateBotTextResponse();
    }
}

//Function to create a user message
function createUserMessage(message) {
    const userMessage = document.createElement('div');
    userMessage.className = 'userMessage';
    userMessage.innerHTML ="<p style='text-align:right;'>" + message + "</p>";
    return userMessage;
  }

function simulateBotTextResponse(){
    const botMessage = document.createElement('div');
    botMessage.className = 'botMessage';
    botMessage.innerHTML ="<p>" + "OpenAI Response" + "</p>";
    return document.getElementById('chatWindow').appendChild(botMessage);

    }

function handleKeyPress(event) {
    if (event.keyCode === 13) {
    sendMessage();
    }
}

