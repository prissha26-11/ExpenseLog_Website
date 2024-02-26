function deleteEntry(entryId,person) {
    fetch('/delete-entry', {
        method: 'POST',
        body: JSON.stringify({ entryId: entryId , person }),
    }).then((_res) => {
        window.location.href = "/expense_entry/"+person;
    });
}

function deleteCategory(categoryId,person) {
    fetch('/delete-category', {
        method: 'POST',
        body: JSON.stringify({ categoryId: categoryId, person }),
    }).then((_res) => {
        window.location.href = "/expense_entry/"+person;
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
