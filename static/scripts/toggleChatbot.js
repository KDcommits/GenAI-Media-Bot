let isExpanded = false;

function toggleChatbot() {
  const chatbotWindow = document.getElementById('chatbotWindow');

  if (isExpanded) {
    chatbotWindow.classList.remove('expanded');
  } else {
    chatbotWindow.classList.add('expanded');
  }

  isExpanded = !isExpanded;
}