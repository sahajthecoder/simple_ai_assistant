import { useState } from 'react'
import './App.css'   // This is a feature of vite, it lets us import any type of file apart from JS files

import { ChatInput } from './components/ChatInput'     // named Export
import ChatMessages from './components/ChatMessages'   // default Export



function App(){

    const [chatMessages, setChatMessages] = useState([{     // this returns an array with 2 variables, currentValue and function to change the currentValue
      message: 'Hello There',
      sender: 'user',
      id: 'id1'
    },{
      message: 'Heyy!! How are you',
      sender: 'robot',
      id: 'id2'
    },{
      message: 'I am fine',
      sender: 'user',
      id: 'id3'
    },{
      message: 'Good to hear that',
      sender: 'robot',
      id: 'id4'
    }]);
    
    // const [chatMessages, setChatMessages] = array;
    // const chatMessages = array[0];
    // const setChatMessages = array[1];

    return (
      <div className="app-container">
        <ChatMessages
          	chatMessages = {chatMessages}
        />

        {/* This calls the component directly (not recommended) */}
        {/*ChatInput()*/}

        {/* This is the proper React component usage */}
        <ChatInput
          chatMessages = {chatMessages}
          setChatMessages = {setChatMessages}
        />
      </div>
    )
}

export default App
