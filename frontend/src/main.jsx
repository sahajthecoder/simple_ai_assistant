import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode> {/* Strict mode just gives us some additional checks and warnings when developing our apps `*/}
    <App />
  </StrictMode>,
)

/* 
its like :- 
const container = document.querySelector('.js-container');
ReactDOM.createRoot(container).render(div);

createRoot setsup react, the container element inside createRoot acts as a container, everything we create with react
is gonna displayed inside the container element

render :- it is a feature of react, render means to display something
*/