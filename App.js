import React, {useState} from 'react';
import axios from 'axios';

function App() {
  const [text, setText] = useState('');
  const [reply, setReply] = useState('');
  const [uploadFile, setUploadFile] = useState(null);
  const [status, setStatus] = useState('');

  const backendBase = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

  const sendChat = async () => {
    setStatus('Thinking...');
    try {
      const res = await axios.post(`${backendBase}/api/chat`, { text, lang: 'en' });
      setReply(res.data.reply);
      setStatus('');
    } catch (e) {
      setStatus('Error: ' + (e.response?.data?.detail || e.message));
    }
  };

  const uploadReport = async () => {
    if (!uploadFile) { alert('Select a file'); return; }
    const form = new FormData();
    form.append('file', uploadFile);
    form.append('user_id', 'demo_user');
    setStatus('Uploading...');
    try {
      const res = await axios.post(`${backendBase}/api/upload_report`, form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setStatus('Uploaded: ' + res.data.filename);
    } catch (e) {
      setStatus('Upload error: ' + e.message);
    }
  };

  return (
    <div className="app">
      <div className="header"><h2>Gramin GPT (Prototype)</h2></div>

      <div className="card">
        <h3>Ask anything (e.g., "What did my last medical report say?")</h3>
        <textarea rows="3" value={text} onChange={e=>setText(e.target.value)} placeholder="Type your question..." />
        <div style={{marginTop:8}}>
          <button onClick={sendChat}>Ask</button>
        </div>
        {status && <p>{status}</p>}
        {reply && <div style={{marginTop:8, padding:8, background:'#fff', borderRadius:4}}><strong>Reply:</strong><p>{reply}</p></div>}
      </div>

      <div className="card">
        <h3>Upload medical report (PDF / Image)</h3>
        <input type="file" onChange={e=>setUploadFile(e.target.files[0])} />
        <div style={{marginTop:8}}>
          <button onClick={uploadReport}>Upload</button>
        </div>
      </div>

      <div style={{fontSize:12, color:'#666', marginTop:12}}>
        <p>Frontend env: REACT_APP_BACKEND_URL to point to backend.</p>
      </div>
    </div>
  );
}

export default App;
