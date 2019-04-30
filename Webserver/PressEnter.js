function pressed(e,FormNum) {
    // Has the enter key been pressed?
    if ( (window.event ? event.keyCode : e.which) == 13) { 
        // If it has been so, manually submit the <form>
        document.forms[FormNum].submit();
    }
}