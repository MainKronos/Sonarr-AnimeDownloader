// M.AutoInit();

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems, {
    	accordion: true
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.tabs');
    var instances = M.Tabs.init(elems, {
    	swipeable: false
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems, {
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.tap-target');
    var instances = M.TapTarget.init(elems, {

    });


    var lista = document.querySelectorAll('.blocco_anime');
    if (lista.length == 0){
        var elem = document.querySelector('.tap-target');
        var instance = M.TapTarget.getInstance(elem);
        instance.open()
        setTimeout(function(){ instance.close();  instance.destroy();}, 3000);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, {});
});


function get_anime(){
    var elems = document.querySelectorAll('.collapsible-header');
    var data = {};


    for (var i = 0; i < elems.length; i++) {
        data[elems[i].textContent.trim().replace('movie', '')] = null;
    }
    return data;
}


document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.autocomplete');
    var instances = M.Autocomplete.init(elems, {
        data: get_anime()
    });
});


document.getElementById("add_link").addEventListener("click", function (){
    var parent = this.parentNode;
    var input_links = document.querySelectorAll("#input_link");

    var number_input = input_links.length;
    var input_link = input_links[number_input - 1]

    var clon = input_link.cloneNode(true);
    // clon.getElementsByTagName("input")[0].name = "link[" + number_input + "]";
    parent.insertBefore(clon, this);
})

document.getElementById("absolute").addEventListener("click", function () {
    var elem = document.getElementById("season");

    if (this.checked == true) {
        elem.disabled = true;
    } else {
        elem.disabled = false;
    }
})

