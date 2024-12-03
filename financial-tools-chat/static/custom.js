const chat = document.getElementsByClassName("chat")

export function enableDisableTextarea(disable){
    const isDisabled = (disable === 'true')

    chat["0"].getElementsByTagName("textarea")["0"].disabled = isDisabled
    chat["0"].getElementsByTagName("button")["0"].disabled = isDisabled
}



export function focusOnTab(tabId){
    const tabDivs = document.querySelectorAll('[data-writer-id]');
    for (const tabDivElement of tabDivs)
        if(tabDivElement.getAttribute("data-writer-id") === tabId) {
            const button = tabDivElement.getElementsByTagName("button")[0];
            console.log(button)
            button.click();
            break;
        }
}
