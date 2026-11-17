import robot_Pic from '../assets/robot.png'
import user_Pic from '../assets/user.png'

import './ChatMessage.css'

export function ChatMessage (props){  	// this props is an object and it contains all the attribute that you give to the
  // console.log(props)		// ChatMessage HTML component, props make the component reuseable
  
  // const message = props.message;
  // const sender = props.sender;
  const {message, sender} = props;   //----> Destructuring :- same as above, takes properties from props and assigns to variables
  // You can also destructure ot directly at the top of the function call, (In later example)
  

  /*if(sender === 'user'){
    return(					   
      <div>
        {message}
        <img src="user.png" alt="user Image" width="40"/>
      </div>
    );
  }else{
    return(					   
      <div>
        <img src="robot.png" alt="robo Image" width="40"/>
        {message}
      </div>
    );
  }

  You can directly use the if and else like statement inside the JSX by using the Guard operator
  like this :- 
  */
  return(
    <div className = {
        sender === 'user'
        ? 'chat-message-user'
        : 'chat-message-robot'} >

      {sender === 'robot' && (
        <img className = "chat-message-profile" src={robot_Pic} alt="robo Image"/>
      )}
      
      <div className="chat-message-text">
        {message}
      </div>

      {sender === 'user' && (
        <img className = "chat-message-profile" src={user_Pic} alt="user Image"/>
      )}
    </div>
  );

  
}
