let counterElement = document.getElementById('counter');
let incrementBtn = document.getElementById('incrementBtn');
let decrementBtn = document.getElementById('decrementBtn');
let ws = new WebSocket("ws://127.0.0.1:8000/ws");
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    counterElement.textContent = data.counterValue;
};
incrementBtn.addEventListener('click', () => ws.send("increment"));
decrementBtn.addEventListener('click', () => ws.send("decrement"));

