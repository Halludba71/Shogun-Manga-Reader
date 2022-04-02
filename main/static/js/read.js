var images = Array.from(document.getElementsByClassName("image"));
var length = images.length;
var orientation = "left-to-right";
var layout = null;

const observer = new IntersectionObserver(entries => {
    entries.forEach(entry =>{
        if((orientation == "continuous-vertical") || (orientation == "vertical")){
            if( (entry.isIntersecting) && (images.indexOf(entry.target) > currentImage) ){
                currentImage = images.indexOf(entry.target);
                console.log(currentImage)
                updateLastRead();
                observer.unobserve(entry.target);
            }
            
        }
    })
},
{
    rootMargin: "-200px",
});

function trackImages(){
    console.log(currentImage);
    if( (orientation == "vertical") || (orientation == "continuous-vertical") ){
        images[currentImage].scrollIntoView(false);
    }
    images.forEach(image =>{
            observer.observe(image);
        });
}

function showSettings() {
    var settings = document.getElementById("settings");
    if (settings.className == "settings"){
        settings.className = "settings show";
    } else if (settings.className == "settings show"){
        settings.className = "settings";
    }
}

document.body.addEventListener('keydown', function(event) {
    const key = event.key;
    switch (key) {
        case "ArrowLeft":
            if (orientation != "vertical"){
                console.log('Left');
                if (currentImage != 0){
                    if(layout == "double-page-odd"){
                        console.log("test")
                        images[currentImage].className = "image hide";
                        if(currentImage > 0){
                            images[currentImage - 1].className = "image hide"
                        }
                        currentImage -= 2;
                        if(images[currentImage].firstElementChild.naturalWidth <= 1000){
                            if(currentImage == 0){
                                images[currentImage].className = "image";
                            } else{
                                images[currentImage].className = "image right";
                                images[currentImage -1].className = "image left";
                                // currentImage -= 1;
                            }
                        } else{
                            images[currentImage].className = "image";
                        }
                    } else{
                        images[currentImage].className = "image hide";
                        currentImage -= 1;
                        images[currentImage].className = "image";
                        updateLastRead();
                    }
                    
                }
            }
            break;
        case "ArrowRight":
            if (orientation != "vertical"){
                console.log('Right');
                if (currentImage != length-1){
                    if(layout == "double-page-odd"){
                        images[currentImage].className = "image hide";
                        if(currentImage > 0){
                            images[currentImage - 1].className = "image hide"
                        }
                        currentImage += 1;
                        if(images[currentImage].firstElementChild.naturalWidth <= 1000){
                            if(currentImage == length -1){
                                images[currentImage].className = "image";
                            } else{
                            images[currentImage].className = "image left";
                            currentImage += 1;
                            images[currentImage].className = "image right"
                            }
                        } else{
                            images[currentImage].className = "image";
                        }
                    } else{
                        images[currentImage].className = "image hide";
                        currentImage += 1;
                        images[currentImage].className = "image";
                        updateLastRead();
                    }
                    

                }
            }
            break;
    }
});
