let counterElement = document.getElementById('counter');
let incrementBtn = document.getElementById('incrementBtn');
let decrementBtn = document.getElementById('decrementBtn');
let pollingInterval = 5000; // 5 seconds
let pollingTimer = null;

function updateCounter(value) {
    console.log(`New counter to: ${value}`);
    counterElement.textContent = value;
}
async function makeRequest(url, method = 'POST') {
    console.log(`Making ${method} request to: ${url}`);
    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        });
        console.log(`Response status: ${response.status} ${response.statusText}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log(`Received data:`, data);
        updateCounter(data.counterValue);
        return data;
    } catch (error) {
        console.error('Erreur lors de la requête:', error);
    }
}
const API_BASE = 'http://127.0.0.1:8000';
incrementBtn.addEventListener('click', function() {
    console.log('Increment button clicked');
    makeRequest(`${API_BASE}/increment`);
});
decrementBtn.addEventListener('click', function() {
    console.log('Decrement button clicked');
    makeRequest(`${API_BASE}/decrement`);
});
window.addEventListener('DOMContentLoaded', function() {
    console.log('fetching initial counter value');
    makeRequest(`${API_BASE}/counter`, 'GET');
});
function startPolling() {
    console.log('Starting polling every', pollingInterval, 'ms');
    pollingTimer = setInterval(() => {
        makeRequest(`${API_BASE}/counter`, 'GET');
    }, pollingInterval);
}
startPolling();