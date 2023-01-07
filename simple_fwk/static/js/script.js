for (let li of tree.querySelectorAll('li')) {
    let span = document.createElement('span')
    span.classList.add('show')
    li.prepend(span)  // вставляем <span></span>xxx
    span.append(span.nextSibling)  // <span>xxx</span>
}

tree.onclick = e => {
    if (e.target.tagName != 'SPAN') return

    let trg = e.target  // выбираем путь категории
    let s = ''
    while (trg != tree) {
        if (trg.tagName == 'LI') {
            s = trg.firstChild.innerText + '-> ' + s
        }
        trg = trg.parentNode
    }
    document.getElementById("selected-ctg").innerText = s
}