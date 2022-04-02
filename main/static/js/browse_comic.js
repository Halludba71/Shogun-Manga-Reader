function SearchChapters(){
    console.log("hello")
    var input = document.getElementById("search_box")
    var filter = input.value.toUpperCase();
    var list = document.getElementById("chapters");
    var li = list.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        row = li[i].getElementsByTagName("p")[0];
        if (row) {
            txtValue = row.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                li[i].style.display = "";
            } else {
                li[i].style.display = "none";
            }
        }
    }
}