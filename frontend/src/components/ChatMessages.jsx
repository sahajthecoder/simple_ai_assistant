import { useRef, useEffect } from 'react'
import {ChatMessage} from './ChatMessage'

import './ChatMessages.css'

function ChatMessages({chatMessages}){
  const chatMessagesRef = useRef(null)

  useEffect(() => {
    const containerElement = chatMessagesRef.current   /*conatians the chat-messages-container isnide the ref*/
    if(containerElement){ /* Its a good practice to check of the element is there or not before accessing it */
      
      // Auto scroll to bottom after adding message
      containerElement.scrollTop = containerElement.scrollHeight  
      /* scrollTop = How far form the top we need to scroll ? :- scrollHeight = to the total height 
         this will keep the bar scrolling automatically, instead of doing manually
         This ensures the latest messages are always visible (like in WhatsApp or Slack).
      */
    }
  }, [chatMessages])

  return(
    <div
    className="chat-messages-container"
    ref={chatMessagesRef}>
      {chatMessages.map((chatMessage) => {   // you can direclty insert this result int the curly braces
        return(
          <ChatMessage
            message = {chatMessage.message}
            sender = {chatMessage.sender}
            key = {chatMessage.id}
          />
        );
      })}
    </div>
  )
}

export default ChatMessages;
