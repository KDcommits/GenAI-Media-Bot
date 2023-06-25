let isExpanded = false;

function toggleChatbot() {
  const chatbotWindow = document.getElementById('chatbotWindow');
  const chatbotContent = document.getElementById('chatWindow');
  const buttonbotContent = document.getElementById('buttonWindow');

  if (isExpanded) {
    chatbotWindow.classList.remove('expanded');
    // chatbotContent.style.display = 'none';
    // buttonbotContent.style.display = 'none';
  } else {
    chatbotWindow.classList.add('expanded');
    // chatbotContent.style.display = 'block';
    // buttonbotContent.style.display = 'block';
  }

  isExpanded = !isExpanded;
}