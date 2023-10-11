function sendMessage() {
    var userInput = document.getElementById("user-input").value;
  
    // Send user input to the Python backend using an HTTP request
    fetch("/text-question", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(responseData => {
      // Handle the response from the backend
      console.log("Response from backend:", responseData);
  
      // Display the user input and backend response in the chat log
      var chatLog = document.getElementById("chat-log");
      var userMessage = document.createElement("div");
      userMessage.textContent = "User: " + userInput;
      var botMessage = document.createElement("div");
      botMessage.textContent = "Bot: " + responseData.message;
  
      chatLog.appendChild(userMessage);
      chatLog.appendChild(botMessage);
  
      // Clear the user input field
      document.getElementById("user-input").value = "";
    })
    .catch(error => {
      console.error("Error:", error);
      // Handle any errors that occur during the request
    });
  }
  