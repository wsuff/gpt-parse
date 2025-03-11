(function extractGeminiChat() {
  function extractTextContent(element) {
    if (!element) return '';
    return element.innerText.trim(); // Use innerText for consistency
  }

  function extractHTMLContent(element) {
    if (!element) return '';
    return element.innerHTML.trim(); // Use innerHTML for model responses
  }

  function getNodePosition(element) {
    let positions = [];
    while (element) {
      let position = 0;
      let sibling = element;
      while ((sibling = sibling.previousSibling)) {
        position++;
      }
      positions.unshift(position);
      element = element.parentNode;
    }
    return positions.join('.');
  }

  const conversationContainers = document.querySelectorAll(
    'chat-window-content .conversation-container'
  );

  let allMessages = [];

  conversationContainers.forEach((container) => {
    const position = getNodePosition(container);

    const userQueryElement = container.querySelector(
      'user-query-content .query-text'
    );
    const modelResponseElement = container.querySelector(
      'response-container .response-content'
    );

    if (userQueryElement) {
      allMessages.push({
        role: 'user',
        content: extractTextContent(userQueryElement),
        position,
      });
    }

    if (modelResponseElement) {
      allMessages.push({
        role: 'assistant',
        content: extractHTMLContent(modelResponseElement),
        position,
      });
    }
  });

  allMessages.sort((a, b) => {
    const posA = a.position.split('.').map(Number);
    const posB = b.position.split('.').map(Number);

    for (let i = 0; i < Math.min(posA.length, posB.length); i++) {
      if (posA[i] !== posB[i]) {
        return posA[i] - posB[i];
      }
    }
    return posA.length - posB.length;
  });

  allMessages.forEach((msg) => {
    delete msg.position;
  });

  const chatData = {
    title: document.title || 'Gemini Chat',
    timestamp: new Date().toISOString(),
    conversation: allMessages,
  };

  function downloadJSON(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }

  const filename = `gemini-chat-${new Date()
    .toISOString()
    .slice(0, 19)
    .replace(/:/g, '-')}.json`;
  downloadJSON(chatData, filename);

  console.log(
    `Chat extracted with ${allMessages.length} messages. Downloading as ${filename}`
  );

  return `Successfully extracted ${allMessages.length} messages from the Gemini chat.`;
})();
