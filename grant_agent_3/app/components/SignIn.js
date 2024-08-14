import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './SignIn.css';

const SignIn = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Add any side effects here
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/token', { username: email, password });
      setMessage('Sign in successful!');
      // Handle token storage
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
    } catch (error) {
      if (error.response && error.response.status === 401) {
        setMessage('Invalid email or password. Please try again.');
      } else {
        setMessage('Sign in failed. Please try again.');
      }
    }
  };

  return (
    <div className="signin-container">
      <h2>Sign In</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Sign In</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default SignIn;
