// Function to handle file selection
function uploadFile() {
    document.getElementById('audioInput').click();
  }


// function downloadPDF(event) {
//     const pdf_file = event.target.files[0];
//     if (pdf_file && pdf_file.type === 'application/pdf') {
//         const pdfreader = new FileReader();
//         pdfreader.onload = function () {
//         const arrayBuffer = pdfreader.result;
//         const blob = new Blob([arrayBuffer], { type: 'application/pdf' });
//         const audioUrl = URL.createObjectURL(audioBlob);
//         let formData = new FormData();
//         formData.append('pdfFile', blob, "data.pdf");
//         $.ajax({
//             type: 'POST',
//             url: '/result',
//             data: formData,
//             contentType: false,
//             processData: false
//         });
//     }
//     pdfreader.readAsArrayBuffer(pdf_file);}
// }

// Function to handle file upload
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
        const reader = new FileReader();
        reader.onload = function () {
        const pdfUrl = reader.result;
        const linkElement = document.createElement('a');
        linkElement.href = pdfUrl;
        linkElement.textContent = 'Uploaded PDF';
        linkElement.innerHTML = "<p style='text-align:right;'>" + "PDF"+ "</p>";
        linkElement.target = '_blank';
        document.getElementById('chatWindow').appendChild(linkElement);
        document.getElementById('audioMessage').innerHTML = '';
        stimulateBotPDFResponse();
        };

        const pdfreader = new FileReader();
        pdfreader.onload = function () {
        const arrayBuffer = pdfreader.result;
        const blob = new Blob([arrayBuffer], { type: 'application/pdf' });
        let formData = new FormData();
        formData.append('pdfFile', blob, "data.pdf");
        $.ajax({
            type: 'POST',
            url: '/result',
            data: formData,
            contentType: false,
            processData: false
        });
        };
        pdfreader.readAsArrayBuffer(file);
        reader.readAsDataURL(file);
        //pdfreader.readAsArrayBuffer(file);
        // downloadPDF(event)
        // reader.readAsArrayBuffer(pdf_file);
        
    }
    }

function stimulateBotPDFResponse(){
    const botMessage = document.createElement('div');
    botMessage.className = 'botMessage';
    botMessage.innerText ="OpenAI Response";
    return document.getElementById('chatWindow').appendChild(botMessage);

}