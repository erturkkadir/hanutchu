const qry = document.getElementById("qry");
const ans = document.getElementById("ans");
const sta = document.getElementById('sta');
const btnStart = document.getElementById("btnStart");
const wsUrl = `wss://syshuman.com:7860`;

const maxReconnectAttempts = 5;
const reconnectDelay = 3000;


let mediaRecorder;
let websocket;
let reconnectAttempts = 0;
let audioQueue = [];
let isPlaying = false;
let permMic = false;
let totalChunksExpected = 0;
let chunksReceived = 0;
let isRecording = false;


function showStatus(message) {
    sta.textContent = message;
    console.log(message);
	sta.style.display = 'block';
	setTimeout(() => {sta.style.display = 'none';}, 5000);
}

function connectWebSocket() {
	if (reconnectAttempts >= maxReconnectAttempts) {
		showStatus('Maximum reconnection attempts reached. Please refresh the page.');
		return;
	}
	showStatus(wsUrl);
	websocket = new WebSocket(wsUrl);
	
	
	websocket.onopen = () => {
		showStatus('WebSocket connected');		
		reconnectAttempts = 0;
	};

	websocket.onclose = (event) => {
		showStatus('WebSocket disconnected:' + JSON.stringify(event));		
		reconnectAttempts++;
		setTimeout(connectWebSocket, reconnectDelay);
	};

	websocket.onerror = (error) => {		
		showStatus('Connection error. Attempting to reconnect...' + JSON.stringify(error));
	};

	websocket.onmessage = (event) => {
		try {
			const data = JSON.parse(event.data);
			if (data.type === 'error') {
				showStatus(data.message);
			}
		} catch (e) {
			showStatus('Error parsing message:', e);
		}
	};
}

function updateRecordingStatus(stat) {
	isRecording=stat; 
	if(stat===true) {
		btnStart.innerText = "Stop";		
	} else {
		btnStart.innerText = "Start";
	}
}

// Start recording
async function startRecording() {
	try {
		if (websocket.readyState !== WebSocket.OPEN) {
			showStatus('WebSocket is not connected. Please wait or refresh the page.');
			isrecording = false;
			return;
		}

		const stream = await navigator.mediaDevices.getUserMedia({ 
			audio: {
				channelCount: 1,
				sampleRate: 44100,
				echoCancellation: true,
				noiseSuppression: true
			} 
		});

		mediaRecorder = new MediaRecorder(stream, {
			mimeType: 'audio/webm;codecs=opus'
		});

		mediaRecorder.ondataavailable = (event) => {
			if (event.data.size > 0 && websocket.readyState === WebSocket.OPEN) {
				websocket.send(event.data);
			}
		};

		mediaRecorder.onstart = () => {
			websocket.send(JSON.stringify({ type: 'start' }));
			updateRecordingStatus(true);
		};

		mediaRecorder.onstop = () => {
			websocket.send(JSON.stringify({ type: 'stop' }));
			showStatus('Disconnected');			
			updateRecordingStatus(0);			
			stream.getTracks().forEach(track => track.stop());
		};

		mediaRecorder.onerror = (error) => {			
			showStatus('Recording error: ' + error.message);
			stopRecording();
			updateRecordingStatus(false);
		};

		mediaRecorder.start(100);		
		

	} catch (err) {		
		showStatus('Error accessing microphone. Please ensure you have granted microphone permissions.');
	}
}

function stopRecording() {
	showStatus("Stopping...");
	if (mediaRecorder && mediaRecorder.state !== 'inactive') {
		mediaRecorder.stop();
		showStatus("Stopped...");
	}
	isRecording = false;
}

function startClick() {
	showStatus('StartClick...' + isRecording);
	if(isRecording===false) {
		showStatus('startRecording...');
		startRecording();
	} else {	
		showStatus('stopRecording...');
		stopRecording();
	}
}

btnStart.addEventListener('click', startClick);

connectWebSocket();