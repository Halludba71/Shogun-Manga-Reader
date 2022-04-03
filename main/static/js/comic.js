var editing = false;
chapterEditor = document.getElementById('chapterEditor');
checkboxes = Array.from(document.getElementsByName('checkbox'));

function markUnread(){
    var chapterids = [];
    checkboxes.forEach(checkbox =>{
        if(checkbox.checked == true){
            checkbox.parentElement.parentElement.lastElementChild.firstElementChild.firstElementChild.firstElementChild.className = "unread";
            chapterids.push(checkbox.value);
        }
    });
    var xhr = new XMLHttpRequest();
    xhr.open("POST", document.URL, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
    xhr.send(JSON.stringify({
        "value": "unread",
        "chapterids": chapterids
    }));
    editing = false;
    chapterEditor.className = "chapterEditor hidden";
    unselectAll();
}
function CancelSelection(){
    checkboxes.forEach(checkbox =>{
        checkbox.checked = false;
    });
    editing = false;
    chapterEditor.className = "chapterEditor hidden"
}

function selectUnselected(){
    checkboxes.forEach(checkbox =>{
        if(checkbox.parentElement.parentElement.style.display != "none"){
            if(checkbox.checked == true){
                checkbox.checked = false;
            } else{
                checkbox.checked = true;
            }
        }
    })
}

function markRead(){
    var chapterids = [];
    checkboxes.forEach(checkbox =>{
        if(checkbox.checked == true){
            chapterids.push(checkbox.value)
            checkbox.parentElement.parentElement.lastElementChild.firstElementChild.firstElementChild.firstElementChild.className = "read";
        }
    });
            
    var xhr = new XMLHttpRequest();
    xhr.open("POST", document.URL, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
    xhr.send(JSON.stringify({
        "value": "read",
        "chapterids": chapterids
    }));
    editing = false;
    chapterEditor.className = "chapterEditor hidden";
    unselectAll();
}

function unselectAll(){
    checkboxes.forEach(checkbox =>{
        if(checkbox.parentElement.parentElement.style.display != "none"){
            checkbox.checked = false;
        }
    });
}

function selectAll(){
    checkboxes.forEach(checkbox =>{
        if(checkbox.parentElement.parentElement.style.display != "none"){
            checkbox.checked = true;
        }
    });
}

function checkBoxChange(){
    if(editing == false){
        editing = true;
        chapterEditor.className = "chapterEditor";
    }
}

function SearchChapters(){
    if(editing == false){
        var input = document.getElementById("search_box")
        var filter = input.value.toUpperCase();
        var table = document.getElementById("chapters");
        var tr = table.getElementsByTagName("tr");
        for (i = 0; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[1];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
        }
}

function showDropdown(value) {
    if(value == 'filter'){
        document.getElementById("filter-dropdown-content").classList.toggle("show");
    } else{
        document.getElementById("dropdown-content").classList.toggle("show");
    }
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropdown-button')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
        }
        }
    } else if (!event.target.matches('.filter-dropdown-button')){
        var dropdowns = document.getElementsByClassName("filter-dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

function removeFromLibrary(){
    window.confirmationDialog.close();
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 302) {
            var json = JSON.parse(this.responseText); 
            console.log(json.success);
            //following line would actually change the url of your window.  
            window.location.href = json.success; 
        }
    };
        xhr.open("POST", document.URL, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
        xhr.send(JSON.stringify({
            "value": "removeManga",
    }));
}