function uploadFile() {
    document.getElementById('audioInput').click();
  }

  function stimulateBotPDFResponse(){
    const botMessage = document.createElement('div');
    botMessage.className = 'botMessage';
    botMessage.innerText ="Success!!! \nYour File is uploaded.\nYou can now ask relevant question \
                           associated to the uploaded file.";
    return botMessage;
} 

function downloadPDF(event) {
    const pdf_file = event.target.files[0];
    if (pdf_file && pdf_file.type === 'application/pdf') {
        const pdfreader = new FileReader();
        pdfreader.onload = function () {
        const arrayBuffer = pdfreader.result;
        const blob = new Blob([arrayBuffer], { type: 'application/pdf' });
        let formData = new FormData();
        formData.append('pdfFile', blob, pdf_file['name']);
        $.ajax({
            type: 'POST',
            url: '/result',
            data: formData,
            contentType: false,
            processData: false
        });
    }
    pdfreader.readAsArrayBuffer(pdf_file);}
}

// Function to handle file upload
function handleFileUpload(event) {
    const file = event.target.files[0];
    const chatwindow = document.getElementById('chatWindow');
    if (file && file.type === 'application/pdf') {
        const reader = new FileReader();
        reader.onload = function () {
        const pdfUrl = reader.result;
        const linkElement = document.createElement('a');
        const pdfImage =  document.createElement('img');
        linkElement.target = '_blank';
        pdfImage.src = "./static/pdf_image.png";
        pdfImage.className = 'pdfImage';
        linkElement.href = pdfUrl;
        chatwindow.appendChild(linkElement).appendChild(pdfImage);
        chatwindow.scrollTop =chatwindow.scrollHeight;
        document.getElementById('audioMessage').innerHTML = '';
        chatwindow.scrollTop = chatwindow.scrollHeight;
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
            processData: false,
            success: function(data, textStatus, xhr) {
                if (xhr.status === 200) {
                    var botMessage = stimulateBotPDFResponse();
                    chatwindow.appendChild(botMessage);
                    chatwindow.scrollTop = chatwindow.scrollHeight;
                } else {
                    console.log('Error!!! Some issue occured during PDF Upload:', xhr.status);
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                console.error('Error:', textStatus, errorThrown);
            }
        });
        };
        //pdfreader.readAsArrayBuffer(file);
        reader.readAsDataURL(file);
        pdfreader.readAsArrayBuffer(file);
        downloadPDF(event)
        // reader.readAsArrayBuffer(pdf_file);      
    }

    else if(file && file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'){
        console.log(file.type);
        const reader = new FileReader();
        reader.onload = function (e) {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: 'array' });
            const worksheet = workbook.Sheets[workbook.SheetNames[0]];
            const htmlTable = XLSX.utils.sheet_to_html(worksheet);

        const linkElement = document.createElement('a');
        const excelImage =  document.createElement('img');
        linkElement.innerHTML = htmlTable
        linkElement.href = URL.createObjectURL(file);
        linkElement.target = '_blank';
        excelImage.src = "./static/excel_image.png"
        excelImage.className ='excelImage'
        chatwindow.appendChild(linkElement).appendChild(excelImage);
        chatwindow.scrollTop = chatwindow.scrollHeight;
        document.getElementById('audioMessage').innerHTML = '';
        chatwindow.scrollTop = chatwindow.scrollHeight;
        };

        const excelReader = new FileReader();
        excelReader.onload = function () {
          const arrayBuffer = excelReader.result;
          const blob = new Blob([arrayBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
          let formData = new FormData();
          formData.append('excelFile', blob, "data.xlsx");
          $.ajax({
            type: 'POST',
            url: '/result',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data, textStatus, xhr) {
                if (xhr.status === 200) {
                    var botMessage = stimulateBotPDFResponse();
                    chatwindow.appendChild(botMessage);
                    chatwindow.scrollTop = chatwindow.scrollHeight;
                } else {
                    console.log('Error!!! Some issue occured during PDF Upload:', xhr.status);
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                console.error('Error:', textStatus, errorThrown);
            }
          });
        };
        excelReader.readAsArrayBuffer(file);
        reader.readAsDataURL(file);
    }

}