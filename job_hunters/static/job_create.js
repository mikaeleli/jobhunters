let datePickers = Array.from(document.querySelectorAll('.job_create__form .form__field input[type="date"]'));

// prepare locale aware input value, from: https://stackoverflow.com/a/13052187
const toDateInputValue = (dateObject) => {
    const local = new Date(dateObject);
    local.setMinutes(dateObject.getMinutes() - dateObject.getTimezoneOffset());
    return local.toJSON().slice(0,10);
};

const now = new Date();
const now_date_input = toDateInputValue(now);
const in_one_week = new Date(new Date().setDate(now.getDate() + 7));
const in_one_week_date_input =  toDateInputValue(in_one_week)

let jobDueDateInput = datePickers.find(el => el.id === 'job_due_date')
if (jobDueDateInput.value === "") {
    jobDueDateInput.value = in_one_week_date_input;
}
jobDueDateInput.min = now_date_input;

let jobStartDateInput = datePickers.find(el => el.id === 'job_start_date')
if (jobStartDateInput.value === "") {
    jobStartDateInput.value = in_one_week_date_input;
}
jobStartDateInput.min = now_date_input;

let categorySelectOptions = Array.from(document.querySelectorAll('.job_create__form .form__field select#job_category option'));

const toggleSelected = (option) => {
    option.hasAttribute('selected') ? option.removeAttribute('selected', '') : option.setAttribute('selected', '');
};
categorySelectOptions.forEach((option) => {
   option.addEventListener('mousedown', (el) => {
       el.preventDefault();
       toggleSelected(el.currentTarget);
   });
});

let toggleCheckboxContainers = Array.from(document.querySelectorAll('.form__toggle__container'));

const toggleChecked = (el) => {
    if (el.hasAttribute('data-toggle-target')) {
        console.log(el.parent);
        checkbox = el.parent.children.getElementById(el.dataset.toggleTarget)
        checkbox.hasAttribute('checked') ? option.removeAttribute('checked', '') : option.setAttribute('checked', '');
    }
};
toggleCheckboxContainers.forEach((option) => {
   option.addEventListener('mousedown', (el) => {
       el.preventDefault();
       toggleChecked(el.currentTarget);
   });
});