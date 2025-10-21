// Basic frontend script to call the FastAPI backend and render itinerary
const form = document.getElementById('itinerary-form');
const outputSection = document.getElementById('output-section');
const itineraryDiv = document.getElementById('itinerary');
const statusDiv = document.getElementById('status');
const downloadPdfBtn = document.getElementById('download-pdf-btn');

// If backend served under a different host/port adjust here or read from query param
const API_URL = 'https://smartitinerary-2.onrender.com/plan-itinerary';

// const API_URL = 'http://localhost:8000/plan-itinerary';
const PDF_URL = 'https://smartitinerary-2.onrender.com/generate-pdf';

// Store the current itinerary text for PDF generation
let currentItinerary = '';

function setStatus(msg, type = 'info') {
  statusDiv.textContent = msg;
  statusDiv.className =
    'status ' +
    (type === 'error' ? 'error' : type === 'success' ? 'success' : '');
}

function buildPayload(fd) {
  // Dates: ensure hotel dates align with flights if user left blank (we mark required in UI though)
  return {
    flight_request: {
      departure_airport_code: fd.get('departure_airport_code').toUpperCase(),
      arrival_airport_code: fd.get('arrival_airport_code').toUpperCase(),
      outbound_date: fd.get('outbound_date'),
      return_date: fd.get('return_date'),
    },
    hotel_request: {
      city: fd.get('city'),
      check_in_date: fd.get('check_in_date'),
      check_out_date: fd.get('check_out_date'),
      hotel_class: fd.get('hotel_class') || '4,5',
    },
    sights_request: {
      query: fd.get('sights_query'),
    },
  };
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  outputSection.classList.remove('hidden');
  itineraryDiv.textContent = '';
  downloadPdfBtn.classList.add('hidden'); // Hide download button while loading

  // Disable form during submission
  const submitBtn = form.querySelector('button[type="submit"]');
  const originalBtnText = submitBtn.innerHTML;
  submitBtn.disabled = true;
  submitBtn.innerHTML = '<span class="btn-icon">⏳</span> Generating...';

  setStatus('🚀 Creating your personalized itinerary...');
  const fd = new FormData(form);
  const payload = buildPayload(fd);

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'Server error');
    }
    const data = await res.json();
    setStatus('✅ Itinerary generated successfully!', 'success');
    // Backend returns markdown-like text. We can do a very small conversion for headers + bold
    currentItinerary = data.itinerary || 'No itinerary returned.';
    itineraryDiv.innerHTML = renderMarkdownLite(currentItinerary);

    // Show download button after successful generation
    downloadPdfBtn.classList.remove('hidden');

    // Scroll to results
    outputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (err) {
    console.error(err);
    setStatus('❌ Error: ' + err.message, 'error');
    itineraryDiv.textContent = '';
    currentItinerary = '';
  } finally {
    // Re-enable form
    submitBtn.disabled = false;
    submitBtn.innerHTML = originalBtnText;
  }
});

function renderMarkdownLite(markdown) {
  // Extremely tiny markdown renderer (safe subset) - replace headings & bold
  let html = markdown
    .replace(/^### (.*$)/gim, '<h4>$1</h4>')
    .replace(/^## (.*$)/gim, '<h3>$1</h3>')
    .replace(/^# (.*$)/gim, '<h2>$1</h2>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n\n/g, '<br/><br/>');
  return html;
}

// Prefill dates with sensible defaults (today + 7 days, today + 12 days)
(function autoDates() {
  const today = new Date();
  const plus7 = new Date(today.getTime() + 7 * 86400000);
  const plus12 = new Date(today.getTime() + 12 * 86400000);
  const fmt = (d) => d.toISOString().split('T')[0];
  form.outbound_date.value = fmt(plus7);
  form.return_date.value = fmt(plus12);
  form.check_in_date.value = fmt(plus7);
  form.check_out_date.value = fmt(plus12);
})();

// Download PDF button handler
downloadPdfBtn.addEventListener('click', async () => {
  if (!currentItinerary) {
    alert('No itinerary available to download');
    return;
  }

  const originalBtnText = downloadPdfBtn.innerHTML;
  downloadPdfBtn.disabled = true;
  downloadPdfBtn.innerHTML =
    '<span class="btn-icon">⏳</span> Generating PDF...';

  try {
    setStatus('📄 Generating your PDF...');
    const res = await fetch(PDF_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ itinerary_text: currentItinerary }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'Server error');
    }

    // Convert response to blob and trigger download
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'Itinerary.pdf';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);

    setStatus('✅ PDF downloaded successfully!', 'success');
  } catch (err) {
    console.error(err);
    setStatus('❌ Error generating PDF: ' + err.message, 'error');
  } finally {
    downloadPdfBtn.disabled = false;
    downloadPdfBtn.innerHTML = originalBtnText;
  }
});
