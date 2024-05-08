let selectsOnPage = document.querySelectorAll('.form__select_item');

let registerForm = document.querySelector('.register__form');

const selectAccountType = (event, el) => {
    el.parentNode.childNodes.forEach((child) => {
        if (child.tagName && child.tagName === 'SELECT') {
            child.value = el.dataset.userType;
        }
        if (child.classList && child.classList.contains('form__select_selected')) {
            child.classList.remove('form__select_selected');
        }
    })
    el.classList.add('form__select_selected');

}
selectsOnPage.forEach(el => {
    el.addEventListener('click', event => selectAccountType(event, el));
});

