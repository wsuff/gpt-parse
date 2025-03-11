# Utilities to allow easier parsing of exports from LLM services such as ChatGPT

Contribs from:
* DarkFlib
* Wsuff
* your name could be here... contribute some code

## Gemini.js
**Key Adaptations**

1.  **Selectors:**
    * `'chat-window-content .conversation-container'` to get each turn.
    * `'user-query-content .query-text'` to get user input.
    * `'response-container .response-content'` to get model output.
2.  **`extractTextContent` and `extractHTMLContent`:**
    * `extractTextContent` now uses `innerText` to get plain text from user queries.
    * `extractHTMLContent` uses `innerHTML` to preserve formatting in model responses.
3.  **Role Assignment:**
    * User queries are assigned the `role: 'user'`.
    * Model responses are assigned the `role: 'assistant'`.
4.  **Position Sorting:**
    * The `getNodePosition` function and sorting logic are retained to ensure the correct conversation order.
5.  **JSON Structure:**
    * The output JSON includes `title`, `timestamp`, and `conversation` (an array of messages).
      

**How to Use**

1.  Open the Gemini chat you want to extract.
2.  Open the browser console.
3.  Paste the script.
4.  Press Enter.

This script should now provide you with a JSON file in the desired format, consistent with the ChatArchiver's expectations.

### Bugs
- Gemini doesn't appear to keep Conversation Title anywhere but the nav bar, so this doesn't populate that correctly yet.
- Output is still HTML as displayed. Post process likely needed but rather not write my own.
