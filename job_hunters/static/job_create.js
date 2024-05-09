let datePickers = Array.from(document.querySelectorAll('.job_create__form .form__field input[type="date"]'));

// prepare locale aware input value, from: https://stackoverflow.com/a/13052187
function toDateInputValue(dateObject){
    const local = new Date(dateObject);
    local.setMinutes(dateObject.getMinutes() - dateObject.getTimezoneOffset());
    return local.toJSON().slice(0,10);
};

const now = new Date();
const now_date_input = toDateInputValue(now);
const in_one_week = new Date(new Date().setDate(now.getDate() + 7));
const in_one_week_date_input =  toDateInputValue(in_one_week)
datePickers.find(el => el.id === 'job_due_date').value = in_one_week_date_input;
datePickers.find(el => el.id === 'job_due_date').value = in_one_week_date_input;

datePickers.find(el => el.id === 'job_starting_date').value = in_one_week_date_input;


// const selectAccountType = (event, el) => {
//     el.parentNode.childNodes.forEach((child) => {
//         if (child.tagName && child.tagName === 'SELECT') {
//             child.value = el.dataset.userType;
//             registerForm.dataset.userType = el.dataset.userType;
//         }
//         if (child.classList && child.classList.contains('form__select_selected')) {
//             child.classList.remove('form__select_selected');
//         }
//     })
//     el.classList.add('form__select_selected');
//
// }
// selectsOnPage.forEach(el => {
//     el.addEventListener('click', event => selectAccountType(event, el));
// });

