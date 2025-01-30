function playBase64Audio(baseString) {
    try{
        const base64Data = baseString.replace(/^data:audio\/\w+;base64,/, ''); // Remove the data URL prefix
        const binaryData = atob(base64Data);                        // Decode the base64 string
        const arrayBuffer = new ArrayBuffer(binaryData.length);     // Create a buffer
        const byteArray = new Uint8Array(arrayBuffer);        // Convert bytes to a typed array

        for (let i = 0; i < binaryData.length; i++) {  // Fill array with the binary data
            byteArray[i] = binaryData.charCodeAt(i);
        }


        const blob = new Blob([byteArray], { type: 'audio/wav' }); // Create a blob from the typed array
        const audioUrl = URL.createObjectURL(blob); // Create a URL for the blob    
        const audio = new Audio(audioUrl);

        audio.addEventListener('ended', () => {
            URL.revokeObjectURL(audioUrl); // Clean up
        });

        audio.addEventListener('error', (error) => {
            console.error('Error playing audio:', error);
            URL.revokeObjectURL(audioUrl);
        });


        audio.play().catch((error) => {
            console.error('Error playing audio:', error);
            URL.revokeObjectURL(audioUrl);
        });
        return audio
    }catch (e) {
        console.log(e); 
    }
}


