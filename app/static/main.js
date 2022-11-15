function hello() {
    alert('Hello');
}
function reply(e) {
    const parent = e.target.parentElement;
    const input = parent.querySelector('input'); 
    if (input.style.display == 'block') {
        parent.submit();
    }
    else {
        input.style.display = 'block';
        input.focus();
    }
}

function hide(e) {
    const element = e.target;
    element.style.display = 'none';
}