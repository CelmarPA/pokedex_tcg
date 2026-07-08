from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import deck
from .exceptions import (
    DeckValidationError,
    DeckRuleError
)
from .service import deck_service


@deck.route("/")
@login_required
def index():
    return render_template("deck/index.html")


@deck.route("/create", methods=["POST"])
@login_required
def create():

    try:

        deck_service.create(
            current_user,
            request.form["name"],
            request.form["description"]
        )

        flash(
            "Deck created successfully.",
            "success"
        )

    except DeckValidationError as e:

        flash(str(e), "warning")

    return redirect(url_for("deck.index"))




from . import deck
from .exceptions import DeckError
from .service import deck_service

@deck.route("/test-create")
@login_required
def test_create():

    try:

        deck_ = deck_service.create(
            user=current_user,
            name="Test Deck",
            description="Temporary deck"
        )

        flash(
            f'Deck "{deck_.name}" created successfully.',
            "success"
        )

    except DeckError as e:

        flash(str(e), "warning")

    return redirect(url_for("main.dashboard"))