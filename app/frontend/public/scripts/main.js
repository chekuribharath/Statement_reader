document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.getElementById('doc-upload');
  const uploadLabel = document.querySelector('.upload-btn');
  const container = document.querySelector('.container');

  // Create output area for extracted text
  let outputDiv = document.getElementById('pdf-output');
  if (!outputDiv) {
    outputDiv = document.createElement('div');
    outputDiv.id = 'pdf-output';
    outputDiv.style.marginTop = '24px';
    container.appendChild(outputDiv);
  }

  uploadLabel.addEventListener('click', () => {
    fileInput.click();
  });

  fileInput.addEventListener('change', async () => {
    if (!fileInput.files.length) {
      outputDiv.textContent = 'No file selected.';
      return;
    }
    const file = fileInput.files[0];
    if (file.type !== 'application/pdf') {
      outputDiv.textContent = 'Please select a PDF file.';
      return;
    }

    outputDiv.textContent = 'Uploading and processing...';

    const formData = new FormData();
    formData.append('file', file);

    try {
  const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });
      const result = await response.json();
      if (response.ok) {
        outputDiv.textContent = result.text || 'No text extracted from PDF.';
      } else {
        outputDiv.textContent = result.error || 'Error processing PDF.';
      }
    } catch (err) {
      outputDiv.textContent = 'Network error or server not reachable.';
    }
  });
});