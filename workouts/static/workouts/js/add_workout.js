document.addEventListener('DOMContentLoaded', function() {
    const addSetBtn = document.getElementById('add-set-btn');
    // Find Django's hidden input that tracks the total number of forms
    const totalFormsInput = document.querySelector('input[name$="-TOTAL_FORMS"]');

    if (addSetBtn && totalFormsInput) {
        addSetBtn.addEventListener('click', function() {
            // 1. Find the last set form on the page
            const setForms = document.querySelectorAll('.set-form');
            const lastForm = setForms[setForms.length - 1];

            // 2. Clone it deeply
            const newForm = lastForm.cloneNode(true);

            // 3. Figure out the new index numbers
            const newIndex = parseInt(totalFormsInput.value);
            const oldIndex = newIndex - 1;

            // 4. Update the Bootstrap Collapse Target & ID
            const header = newForm.querySelector('.card-header');
            const collapseDiv = newForm.querySelector('.collapse');

            if (header && collapseDiv) {
                header.setAttribute('data-bs-target', `#collapseSet${newIndex}`);
                collapseDiv.setAttribute('id', `collapseSet${newIndex}`);

                // Update the title text (e.g., "Set 1" -> "Set 2")
                const titleText = header.querySelector('h6');
                if (titleText) {
                    titleText.innerText = `Set ${newIndex + 1}`;
                }

                // Make sure the new one is automatically expanded
                collapseDiv.classList.add('show');
            }

            // 5. UX UPGRADE: Collapse the previous form so the screen stays clean
            const oldCollapse = lastForm.querySelector('.collapse');
            if (oldCollapse) {
                oldCollapse.classList.remove('show');
            }

            // 6. Update all Django form attributes (name, id, for)
            const nameRegex = new RegExp(`-${oldIndex}-`, 'g');
            const idRegex = new RegExp(`_${oldIndex}_`, 'g');

            newForm.querySelectorAll('input, select, textarea, label').forEach(elem => {
                // Update 'name'
                if (elem.hasAttribute('name')) {
                    elem.setAttribute('name', elem.getAttribute('name').replace(nameRegex, `-${newIndex}-`));
                }
                // Update 'id'
                if (elem.hasAttribute('id')) {
                    elem.setAttribute('id', elem.getAttribute('id').replace(idRegex, `_${newIndex}_`));
                }
                // Update 'for' (on labels)
                if (elem.hasAttribute('for')) {
                    elem.setAttribute('for', elem.getAttribute('for').replace(idRegex, `_${newIndex}_`));
                }

                // 7. Clear the values so it is a fresh set
                if (elem.tagName === 'INPUT' || elem.tagName === 'TEXTAREA') {
                    if (elem.type === 'checkbox' || elem.type === 'radio') {
                        elem.checked = false; // Uncheck the "Delete" box
                    } else if (elem.type !== 'hidden') {
                        elem.value = ''; // Clear numbers/text
                    } else if (elem.type === 'hidden' && elem.name.endsWith('-id')) {
                        // CRITICAL: Clear the Django database ID so it knows this is a NEW row, not an edit!
                        elem.value = '';
                    }
                }
                // Notice we do NOT clear `<select>` tags here. This is a massive UX win!
                // If they did a Barbell Bench Press on Set 1, Set 2 will default to Barbell Bench Press too.
            });

            // 8. Insert the new form into the page
            lastForm.parentNode.insertBefore(newForm, lastForm.nextSibling);

            // 9. Tell Django there is one more form to process
            totalFormsInput.value = newIndex + 1;
        });
    }
});