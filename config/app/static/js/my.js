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
    var elem = document.querySelector('.tap-target');
    var instance = M.TapTarget.getInstance(elem);
    instance.open()
    setTimeout(function(){ instance.close();  instance.destroy();}, 3000);
});