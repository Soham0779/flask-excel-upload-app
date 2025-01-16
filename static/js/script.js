function displayFileName(input, spanId) {
    const fileName = input.files[0]?.name || 'No file chosen';
    document.getElementById(spanId).textContent = fileName;
}
