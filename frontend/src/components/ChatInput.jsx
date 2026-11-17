import { useState } from 'react'
// --- [PREVIOUS: supersimpledev mock package] ---
// import { Chatbot } from 'supersimpledev'  // manual package by supersimple deb, for the Chatbot API

import './ChatInput.css'

export function ChatInput({ chatMessages, setChatMessages }){
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    
    // function saveInputText(event){
    // 	setInputText(event.target.value)
    // }

    // Stream response from FastAPI backend in real-time token-by-token
    async function sendMessage(){
      if (!inputText.trim() || isLoading) return;

      const userText = inputText;
      setInputText('');  // after entering replace it with an empty string immediately

      /*
      // --- [PREVIOUS: Static Non-Streaming User Message Rendering] ---
      // const newMessages = [
      //   ...chatMessages,
      //   {
      //     message : userText,
      //     sender : 'user',
      //     id: crypto.randomUUID()
      //   }
      // ]
      // setChatMessages(newMessages);
      */

      /*
      // --- [PREVIOUS: Synchronous SuperSimpleDev Mock Response] ---
      // const response = Chatbot.getResponse(inputText);
      // setChatMessages([
      //   ...newMessages,
      //   {
      //     message : response,
      //     sender : 'robot',
      //     id: crypto.randomUUID()
      //   }
      // ])
      */

      /*
      // --- [PREVIOUS: Static JSON Fetch (Why commented out: waited for full response before displaying all at once)] ---
      // try {
      //   const res = await fetch('http://localhost:8000/api/chat', {
      //     method: 'POST',
      //     headers: {
      //       'Content-Type': 'application/json'
      //     },
      //     body: JSON.stringify({ message: userText })
      //   });
      //   const data = await res.json();
      //   setChatMessages(prev => [
      //       ...prev,
      //       { message: data.reply, sender: 'robot', id: crypto.randomUUID() }
      //   ]);
      // } catch (error) {
      //   console.error("Error connecting to AI backend:", error);
      // }
      */

      // --- [NEW: Real-Time Token Streaming with ReadableStream] ---
      const botMessageId = crypto.randomUUID();

      // 1. Render the user's message AND an empty robot message placeholder immediately
      setChatMessages(prev => [
        ...prev,
        {
          message: userText,
          sender: 'user',
          id: crypto.randomUUID()
        },
        {
          message: '',
          sender: 'robot',
          id: botMessageId
        }
      ]);

      setIsLoading(true);

      // 2. Stream tokens from FastAPI backend as they are generated
      try {
        const res = await fetch('http://localhost:8000/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message: userText })
        });

        if (!res.ok) {
          throw new Error(`Server returned HTTP ${res.status}`);
        }

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let accumulatedBotText = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          accumulatedBotText += chunk;

          // Update the robot message bubble live with each streamed chunk
          setChatMessages(prev =>
            prev.map(msg =>
              msg.id === botMessageId
                ? { ...msg, message: accumulatedBotText }
                : msg
            )
          );
        }
      } catch (error) {
        console.error("Error connecting to AI backend:", error);
        setChatMessages(prev =>
          prev.map(msg =>
            msg.id === botMessageId
              ? { ...msg, message: "Error: Unable to connect to AI backend. Make sure FastAPI server is running on port 8000." }
              : msg
          )
        );
      } finally {
        setIsLoading(false);
      }
    }


    return (
        <div className="chat-input-container"> {/* Used div instead of fragment because of CSS container to use flexbox */}
        <input
            placeholder={isLoading ? "AI is thinking..." : "Send a message to the Chatbot"}
            size="30"
            disabled={isLoading}
            onChange={e => setInputText(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter') sendMessage(); }}
            value={inputText}
            className="chat-input"
            // Each time the input changes, React calls the inline arrow function.
            // That arrow function takes the event e and immediately extracts e.target.value and passes it to setInputText.
            // No separate named function is created — it’s all inlined.
        />
        
        <button onClick={sendMessage} disabled={isLoading} className="send-btn">
          {isLoading ? "..." : "Send"}
        </button>
        </div>
    );
}
