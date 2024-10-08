import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (input.trim()) {
      setMessages([...messages, { sender: 'user', text: input }]);
      setInput('');
      try {
        // Send request to local_search endpoint
        const searchResponse = await axios.post('http://localhost:8000/api/local_search', { query: input });
        const aiResponse = searchResponse.data.response;

        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'ai', text: aiResponse },
        ]);
      } catch (error) {
        console.error('Error sending message:', error);
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'ai', text: 'Sorry, something went wrong. Please try again.' },
        ]);
      }
    }
  };

  useEffect(() => {
    // Add any necessary side effects here
  }, []);

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`chat-message ${message.sender === 'user' ? 'user' : 'ai'}`}
          >
            {message.text}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
