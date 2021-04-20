if (CSS.supports("display", "grid")!=true) {
    document.getElementById('main').style.display = 'none';
    document.getElementById('browser_error').style.display = 'block';
    console.log('bad browser');
}
else {
    console.log('good browser');
}

/* document.getElementsByName('call_form')[0].addEventListener('keydown', function(event) {
    if(event.keyCode == 13) {
    event.preventDefault();
    return false;
    }
}); */

document.getElementsByClassName("search")[0].value = ''

//убираем GET параметры из адресной строки
if(typeof window.history.pushState == 'function') {
    window.history.pushState({}, "Hide", "http://127.0.0.1:8080/ezcall/");
}

var len = document.getElementsByClassName('contact_name').length
for(i=0;i<len;i++) {
    let content = document.getElementsByClassName("contact_name")[i].innerHTML;
    if (content.indexOf('ектор') > -1 || content.indexOf('Центр') > -1 || content.indexOf('201') > -1 || content.indexOf('о.п.') > -1) {
        document.getElementsByClassName("contact_name")[i].classList.add("bold")
    }
}

function searchFunc(ulClass,sClass) {    
    var input, filter, ul, li, i, summary;
    input = document.getElementsByClassName("search")[sClass];
    if (input.value === "") {
        ul = document.getElementsByClassName(ulClass);
        for (j = 0; j < 3; j++) {
            document.getElementsByTagName('details')[j].open = false;
            li = ul[j].getElementsByTagName("li");
            for (i = 0; i < li.length; i++) {
                li[i].style.display = "";  
            }
        }
    }
    else {
        filter = input.value.toUpperCase();    
        ul = document.getElementsByClassName(ulClass);
        for (j = 0; j < 3; j++) {
            li = ul[j].getElementsByTagName("li");
            for (i = 0; i < li.length; i++) {
                summary = li[i].getElementsByClassName("summary")[0];
                if (summary.innerHTML.toUpperCase().indexOf(filter) > -1) {
                    li[i].style.display = "";
                } else {
                    li[i].style.display = "none";
        
                }
            }
            document.getElementsByTagName('details')[j].open = true;
        }
    }
}

/*     var elements = document.querySelectorAll(".callee");
    for (var i = 0; i < elements.length; i++) {
      elements[i].onclick = function(){
        document.getElementsByClassName('outer')[i].appeng('loading..') 
        //= '<div id="circleG"><div id="circleG_1" class="circleG"></div><div id="circleG_2" class="circleG"></div><div id="circleG_3" class="circleG"></div></div>'
      };
    } */
