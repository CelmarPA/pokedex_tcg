console.log("DECK JS CARREGADO");

document.addEventListener("DOMContentLoaded", () => {

    document.addEventListener("submit", async event => {

        const form = event.target.closest(".deck-action-form");

        if (!form) {
            return;
        }

        // Confirma remoção da última cópia
        if (form.dataset.action === "remove") {

            const card = form.closest(".deck-card");

            const quantityElement =
                card.querySelector(".deck-quantity");

            const quantity =
                parseInt(quantityElement.textContent);

            if (quantity === 1) {

                const confirmed = confirm(
                    "This is the last copy of this card. Remove it from the deck?"
                );

                if (!confirmed) {
                    return;
                }

            }

        }

        event.preventDefault();

        const button = form.querySelector("button");

        const originalHTML = button.innerHTML;

        button.disabled = true;

        button.innerHTML =  `
            <span
                class="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
            ></span>
        `;

        try {

            const response = await fetch(form.action, {

                method: "POST",

                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                },

                body: new FormData(form)

            });

            const data = await response.json();

            if (!response.ok) {

                showToast(
                    data.message,
                    "danger"
                );

                return;

            }

            const card =
                form.closest(".deck-card");

            if (data.removed) {

                const section = card.closest(".deck-section");

                const column = card.closest(".col-md-4");

                if (column) {

                    column.remove();

                }

                if (section) {

                    const remainingCards =
                        section.querySelectorAll(".deck-card");


                    if (remainingCards.length === 0) {

                        section.remove();

                    }

                    else {

                        const cards =
                            section.querySelectorAll(".deck-card");


                        let total = 0;
                        let unique = cards.length;


                        cards.forEach(card => {

                            const quantity =
                                card.querySelector(".deck-quantity");

                            if(quantity){

                                total += parseInt(quantity.textContent);

                            }

                        });


                        const totalBadge =
                            section.querySelector(".section-total-cards");


                        const uniqueBadge =
                            section.querySelector(".section-unique-cards");


                        if(totalBadge){

                            totalBadge.textContent =
                                `${total} Cards`;

                        }


                        if(uniqueBadge){

                            uniqueBadge.textContent =
                                `${unique} Unique`;

                        }

                    }

                }

                showToast(
                    "Card removed from deck.",
                    "success"
                );

            }

            else {

                const quantity =
                    card.querySelector(".deck-quantity");

                if (quantity) {

                    quantity.textContent =
                        data.quantity;

                }

                const input =
                    card.querySelector(".deck-quantity-input");

                if (input) {

                    input.value =
                        data.quantity;

                }

                if (form.dataset.action === "add") {

                    showToast(
                        "Card added to deck.",
                        "success"
                    );

                }

                else {

                    showToast(
                        "Quantity updated.",
                        "success"
                    );

                }

            }

            if (data.summary) {

                updateDeckSummary(data.summary);

            }

            if (data.sections) {

                updateDeckSections(data.sections);

            }

        }

        catch (error) {

            console.error(error);

            showToast(
                "Unexpected server error.",
                "danger"
            );

        }

        finally {

            button.disabled = false;

            button.innerHTML = originalHTML;

        }

    });

});

function updateDeckSummary(summary) {

    document.querySelector("#deck-total-cards").textContent =
        summary.total_cards;

    document.querySelector("#deck-total-unique").textContent =
        summary.total_unique_cards;

    document.querySelector("#deck-total-pokemon").textContent =
        summary.pokemon;

    document.querySelector("#deck-total-trainers").textContent =
        summary.trainers;

    document.querySelector("#deck-total-energies").textContent =
        summary.energies;

    document.querySelector("#deck-total-value").textContent =
        `$${summary.total_value.toFixed(2)}`;

    const progressBar =
        document.querySelector("#deck-progress-bar");

    progressBar.style.width =
        `${summary.progress}%`;

    document.querySelector("#deck-progress-text").textContent =
        `${summary.total_cards}/60`;

}


function updateDeckSections(sections) {

    sections.forEach(sectionData => {

        const section =
            document.querySelector(
                `.deck-section[data-title="${sectionData.title}"][data-section="${sectionData.subtitle}"]`
            );


        if (!section) {
            return;
        }


        const totalBadge =
            section.querySelector(".section-total-cards");


        const uniqueBadge =
            section.querySelector(".section-unique-cards");


        if (totalBadge) {

            totalBadge.textContent =
                `${sectionData.total_cards} Cards`;

        }


        if (uniqueBadge) {

            uniqueBadge.textContent =
                `${sectionData.unique_cards} Unique`;

        }

    });

}