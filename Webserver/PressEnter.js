function pressed(e) {
    // Has the enter key been pressed?
    if ( (window.event ? event.keyCode : e.which) == 13) { 
        // If it has been so, manually submit the <form>
        document.forms[1].submit();
    }
}