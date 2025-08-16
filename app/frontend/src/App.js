import React, { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
  fetch('/api/message')
      .then(res => res.json())
      .then(data => setMessage(data.message));
  }, []);

  return (
    <div>
      <h1>Full Stack Boilerplate</h1>
      <p>Backend says: {message}</p>
    </div>
  );
}

export default App;
