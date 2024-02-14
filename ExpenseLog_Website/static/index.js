function deleteEntry(entryId) {
    fetch('/delete-entry', {
        method: 'POST',
        body: JSON.stringify({ entryId: entryId }),
    }).then((_res) => {
        window.location.href = "/expense_entry";
    });
}

function deleteCategory(categoryId) {
    fetch('/delete-category', {
        method: 'POST',
        body: JSON.stringify({ categoryId: categoryId }),
    }).then((_res) => {
        window.location.href = "/expense_entry";
    });
}

/* const checkExpenseEntryDescription = (event) => {
    const descriptionFormElement = event.target
    const description = event.target.value
    const amount = event.target.value
    axios.post('validate-expense-entry-description',{
        description: description
    })
    .then((response) => {
        if(response.data.valid_description == "true"){
            descriptionFormElement.setCustomValidity("Description is either too short or empty.")
            descriptionFormElement.reportValidity()
            console.log("hello")
        }
    }, (error)=>{
        console.log(error)
    })
} */
