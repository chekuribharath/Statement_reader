const express = require('express');
const cors = require('cors');
const multer = require('multer');
const pdfParse = require('pdf-parse');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 5000;
const upload = multer({ dest: 'statements/' });

app.use(cors());
app.use(express.json());

app.get('/api/message', (req, res) => {
  res.json({ message: 'Hello from backend!' });
});

app.post('/api/upload', upload.single('file'), async (req, res) => {
  try {
    const filePath = path.join(__dirname, '..', 'statements', req.file.filename);
    const dataBuffer = fs.readFileSync(filePath);
    const pdfData = await pdfParse(dataBuffer);

    // Example: send extracted text back to frontend
    res.json({ text: pdfData.text });
  } catch (err) {
    res.status(500).json({ error: 'Failed to process PDF.' });
  }
});

app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});
