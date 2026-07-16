console.log("DECK JS CARREGADO");

document.addEventListener("DOMContentLoaded", () => {

    document.addEventListener("submit", async event => {


        const form = event.target.closest(".deck-action-form");


        if (!form) {

            return;

        }


        /*
            Confirma remoção somente quando
            a carta possui quantidade 1
        */

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

                alert(data.message);
                return;

            }


            const card =
                form.closest(".deck-card");


            if (data.removed) {

                card.remove();

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

            }


            if (data.summary) {


                const totalCards =
                    document.querySelector("#deck-total-cards");


                if (totalCards) {

                    totalCards.textContent =
                        data.summary.total_cards;

                }


                const totalUnique =
                    document.querySelector("#deck-total-unique");


                if (totalUnique) {

                    totalUnique.textContent =
                        data.summary.total_unique_cards;

                }

            }


        }


        catch(error) {

            console.error(error);

            alert(
                "Unexpected server error."
            );

        }


    });


});