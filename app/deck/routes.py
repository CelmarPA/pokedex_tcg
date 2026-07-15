from flask import render_template, flash, redirect, url_for, abort, request
from flask_login import login_required, current_user
from . import deck
from .exceptions import DeckValidationError, DeckNotFoundError, DeckError
from .forms import DeckForm
from .service import deck_service
from ..search.filters import SearchFilters
from ..search.service import search_service


@deck.route("/")
@login_required
def index():

    filters = SearchFilters(request.args)

    decks = deck_service.get_user_decks(current_user, filters)

    return render_template(
        "deck/index.html",
        decks=decks.items,
        pagination=decks.pagination,
        filters=filters
    )


@deck.route("/create", methods=["GET", "POST"])
@login_required
def create():

    form = DeckForm()

    if form.validate_on_submit():

        try:

            deck_service.create(
                user=current_user,
                name=form.name.data,
                description=form.description.data
            )

            flash(
                "Deck created successfully.",
                "success"
            )

            return redirect(url_for("deck.index"))

        except DeckValidationError as e:

            flash(str(e), "warning")

    return render_template("deck/create.html", form=form)


@deck.route("/edit/<int:deck_id>", methods=["GET", "POST"])
@login_required
def edit(deck_id: int):

    deck_ = deck_service.get_deck(current_user, deck_id)

    if deck_ is None:
        raise DeckNotFoundError()

    form = DeckForm()

    if form.validate_on_submit():

        try:

            deck_service.update(
                user=current_user,
                deck_id=deck_id,
                name=form.name.data,
                description=form.description.data
            )

            flash("Deck updated successfully.", "success")

            return redirect(url_for("deck.index"))


        except DeckNotFoundError:
            abort(404)

    elif not form.is_submitted():

        form.name.data = deck_.deck.name
        form.description.data = deck_.deck.description

    return render_template("deck/edit.html", form=form, deck=deck_)


@deck.route("/delete/<int:deck_id>", methods=["POST"])
@login_required
def delete(deck_id: int):

    try:

        deck_service.delete(current_user, deck_id)

        flash("Deck deleted successfully.", "success")

    except DeckNotFoundError:

        flash("Deck not found.", "warning")

    return redirect(url_for("deck.index"))


@deck.route("/<int:deck_id>")
@login_required
def detail(deck_id: int):

    page = deck_service.get_deck(current_user, deck_id)

    if page is None:
        abort(404)

    return render_template(
        "deck/detail.html",
        deck=page.deck,
        statistics=page.statistics
    )


@deck.route("/<int:deck_id>/add/<card_id>", methods=["POST"])
@login_required
def add_card(deck_id: int, card_id: str):

    try:

        deck_service.add_card(
            user=current_user,
            deck_id=deck_id,
            card_id=card_id
        )

        flash("Card added to deck.", "success")

    except DeckError as e:

        flash(str(e), "warning")

    return redirect(url_for("deck.detail", deck_id=deck_id))


@deck.route("/<int:deck_id>/remove/<card_id>", methods=["POST"])
@login_required
def remove_card(deck_id: int, card_id: str):

    try:

        deck_service.remove_card(
            user=current_user,
            deck_id=deck_id,
            card_id=card_id
        )

        flash("Card remove from deck.", "success")

    except DeckError as e:

        flash(str(e), "warning")

    return redirect(url_for("deck.detail", deck_id=deck_id))


@deck.route("/<int:deck_id>/quantity/<card_id>", methods=["POST"])
@login_required
def update_quantity(deck_id: int, card_id: str):

    try:

        quantity = int(request.form["quantity"])

        deck_service.update_quantity(
            user=current_user,
            deck_id=deck_id,
            card_id=card_id,
            quantity=quantity
        )

        flash("Quantity updated.", "success")

    except ValueError:

        flash("Invalid quantity.", "warning")

    except DeckError as e:

        flash(str(e), "warning")

    return redirect(url_for("deck.detail", deck_id=deck_id))


@deck.route("/<int:deck_id>/statistics")
@login_required
def statistics(deck_id: int):

    deck_statistics = deck_service.get_statistics(current_user, deck_id)

    return render_template("deck/statistics.html", statistics=deck_statistics)


@deck.route("/<int:deck_id>/add-card")
@login_required
def add_card_page(deck_id):

    filters = SearchFilters(
        request.args
    )

    context = search_service.get_search_context()

    page = deck_service.get_add_cards_page(current_user, deck_id, filters)

    pagination = page.cards.pagination

    return render_template(
        "deck/add_card.html",
        page=page,
        filters=filters,
        pagination=pagination,
        **context
    )
