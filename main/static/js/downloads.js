function cancelDownload(downloadId){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", document.URL, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
    xhr.send(JSON.stringify({
        "value": "cancelDownload",
        "downloadId": downloadId
    }));
}

const refreshInterval = setInterval(refreshTable, 1000);

function refreshTable(){
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
        if (this.readyState == 4 && this.status == 200) {
            var currentDownloads = JSON.parse(this.responseText)["downloads"];
            var table = document.getElementById('download_list');
            table.innerHTML = "";
            if (currentDownloads.length == 0){
                var row = table.insertRow(0);
                var noDownloads = row.insertCell(0);
                noDownloads.innerHTML = "<p>No downloads are taking place!</p>";
                clearInterval(refreshInterval);
            } else{
                currentDownloads.forEach(download =>{
                    var row = table.insertRow(0);
                    var mangaName = row.insertCell(0);
                    mangaName.innerHTML = `<h4>${download.mangaName}:</h4>`;
                    var chapterName = row.insertCell(1);
                chapterName.innerHTML = `<p>${download.name}</p>`;
                var downloadProgress = row.insertCell(2);
                downloadProgress.innerHTML = `<p>${download.downloaded}/${download.totalPages}</p>`;
                var cancelButton = row.insertCell(3);
                cancelButton.innerHTML = 
                `<div class="tooltip">
                    <span class="tooltipText">Cancel Download</span>
                    <button onclick="cancelDownload(${download.id})" class="tool">
                        Cancel Download
                    </button>
                </div>`;
                })
            }
        }
    };
    xhr.open("GET", "progress/", true);
    xhr.send();
}