function SearchChapters(){     
    var input = document.getElementById("search_box")
    var filter = input.value.toUpperCase();
    var books = document.getElementsByClassName("book");
    for (i = 0; i < books.length; i++) {
        bookName = books[i].getElementsByClassName("book-name")[0];
        txtValue = bookName.textContent || bookName.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            books[i].style.display = "";
        } else {
            books[i].style.display = "none";
        }
    }
  }