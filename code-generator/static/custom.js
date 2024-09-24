export function scrollToLastLine(){
    const lines = document.getElementsByClassName("cm-line")
    if(lines.length > 0)
        lines[lines.length - 1].scrollIntoView();
}
