var i = 0;

function getElements(){
    const coll = document.getElementsByClassName('dropdown');
    for(i = 0; i<2; i++){
        coll[i].addEventListener("click", function(){
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.maxHeight){
                content.style.maxHeight = null;
                content.style.overflow = hidden;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
                content.style.overflow = scroll;
            }
        });
    }
}

window.onload =()=> getElements();