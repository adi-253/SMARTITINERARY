// Basic frontend script to call the FastAPI backend and render itinerary
const form = document.getElementById('itinerary-form');
const outputSection = document.getElementById('output-section');
const itineraryDiv = document.getElementById('itinerary');
const statusDiv = document.getElementById('status');

// If backend served under a different host/port adjust here or read from query param
const API_URL = 'http://localhost:8000/plan-itinerary';

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
  setStatus('Requesting itinerary...');
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
    setStatus('Itinerary generated successfully!', 'success');
    // Backend returns markdown-like text. We can do a very small conversion for headers + bold
    itineraryDiv.innerHTML = renderMarkdownLite(
      data.itinerary || 'No itinerary returned.',
    );
  } catch (err) {
    console.error(err);
    setStatus('Error: ' + err.message, 'error');
    itineraryDiv.textContent = '';
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
