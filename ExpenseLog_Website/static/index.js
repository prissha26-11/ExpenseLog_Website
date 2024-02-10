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