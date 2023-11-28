"""
Recommendation Service

Paths:
------
GET /recommendations - Returns a list all of the Recommendations
GET /recommendations/{id} - Returns the Recommendation with a given id number
POST /recommendations - creates a new Recommendation record in the database
PUT /recommendations - updates a Recommendation record in the database
DELETE /recommendations/{id} - deletes a Recommendation record in the database

"""

from flask import jsonify, request, url_for, abort
from service.models import Recommendation, RecommendationType, RecommendationStatus
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/healthcheck")
def healthcheck():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


######################################################################
# LIST ALL RECOMMENDATIONS
######################################################################
@app.route("/recommendations", methods=["GET"])
def list_recommendations():
    """Returns all of the Recommendations"""
    page_index = request.args.get("page-index", type=int, default=1)
    page_size = request.args.get("page-size", type=int, default=10)
    rec_type = request.args.get("type", default=None)
    rec_status = request.args.get("status", default=None)
    type_value = None
    status_value = None

    if rec_type is not None:
        app.logger.info("Find by recommendation type: %s", rec_type)
        try:
            type_value = getattr(RecommendationType, rec_type.upper())
        except AttributeError:
            abort(
                status.HTTP_400_BAD_REQUEST,
                f"Invalid recommendation type: '{rec_type}'.",
            )
    elif rec_status is not None:
        app.logger.info("Find by recommendation status: %s", rec_status)
        try:
            status_value = getattr(RecommendationStatus, rec_status.upper())
        except AttributeError:
            abort(
                status.HTTP_400_BAD_REQUEST,
                f"Invalid recommendation type: '{rec_status}'.",
            )
    paginated_recommendations = Recommendation.paginate(
        page_index=page_index,
        page_size=page_size,
        rec_type=type_value,
        rec_status=status_value,
    )

    results = {
        "page": paginated_recommendations.page,
        "per_page": paginated_recommendations.per_page,
        "total": paginated_recommendations.total,
        "pages": paginated_recommendations.pages,
        "items": [
            recommendation.serialize()
            for recommendation in paginated_recommendations.items
        ],
    }

    app.logger.info("Returning %d recommendations", len(results["items"]))
    return results, status.HTTP_200_OK


######################################################################
# RETRIEVE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendation_id>", methods=["GET"])
def get_recommendations(recommendation_id):
    """
    Retrieve a single Recommendation

    This endpoint will return a Recommendation based on it's id
    """
    app.logger.info("Request for recommendation with id: %s", recommendation_id)
    recommendation = Recommendation.find(recommendation_id)
    if not recommendation:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Recommendation with id '{recommendation_id}' was not found.",
        )

    app.logger.info("Returning recommendation: %s", recommendation.id)
    # need a more explicit message

    return jsonify(recommendation.serialize()), status.HTTP_200_OK


@app.route("/recommendations/source-product", methods=["GET"])
def read_recommendations_by_source_type():
    """
    Read a list of recommendations based on the source product they select,
    with optional sorting by recommendation weight.
    """
    app.logger.info("Request for recommendations list based on source product")
    source_item_id = request.args.get("source_item_id", type=int)
    sort_order = request.args.get("sort_order", default="desc")  # Added sorting parameter
    product_status = request.args.get("status", default=None)

    if source_item_id is None:
        return jsonify({"error": "Source item ID is required"}), 400

    recommendations = []
    if product_status == "valid":
        # Assuming find_valid_by_source_item_id also needs to be updated for sorting
        recommendations = Recommendation.find_valid_by_source_item_id(source_item_id, sort_order)
    else:
        recommendations = Recommendation.find_by_source_item_id(source_item_id, sort_order)

    results = [recommendation.serialize() for recommendation in recommendations]
    app.logger.info("Returning %d recommendations", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# ADD A NEW RECOMMENDATION
######################################################################
@app.route("/recommendations", methods=["POST"])
def create_recommendations():
    """
    Creates a Recommendation
    This endpoint will create a Recommendation based the data in the body that is posted
    """
    app.logger.info("Request to create a recommendation")
    check_content_type("application/json")
    recommendation = Recommendation()
    recommendation.deserialize(request.get_json())
    recommendation.create()
    message = recommendation.serialize()
    location_url = url_for(
        "get_recommendations",
        recommendation_id=recommendation.id,
        _external=True,
    )
    app.logger.info("Recommendation with ID [%s] created.", recommendation.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# UPDATE AN EXISTING RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendation_id>", methods=["PUT"])
def update_recommendation(recommendation_id):
    """
    Update a recommendation

    This endpoint will update a recommendation based the body that is posted

    payload: {
        (keys to be changed): (fields to be changed)
    }
    """
    check_content_type("application/json")
    app.logger.info("Request to update recommendation with id: %s", recommendation_id)
    recommendation = Recommendation.find(recommendation_id)
    if recommendation:
        recommendation.update(request.get_json())
    app.logger.info("Recommendation with ID %s updated", recommendation.id)

    return jsonify(recommendation.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendation_id>", methods=["DELETE"])
def delete_recommendations(recommendation_id):
    """
    Delete a Recommendation

    This endpoint will delete a Recommendation based the id specified in the path
    """
    app.logger.info("Request to delete recommendation with id: %s", recommendation_id)
    recommendation = Recommendation.find(recommendation_id)
    if recommendation:
        recommendation.delete()

    app.logger.info("Recommendation with ID [%s] delete complete.", recommendation_id)
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# LIKE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendation_id>/like", methods=["PUT"])
def like_recommendation(recommendation_id):
    """
    Like a Recommendation

    This endpoint will like a Recommendation based the id specified in the path
    """
    app.logger.info("Request to like recommendation with id: %s", recommendation_id)
    recommendation = Recommendation.find(recommendation_id)
    if not recommendation:
        abort(status.HTTP_404_NOT_FOUND, "recommendation not found")
    recommendation.like()
    app.logger.info("Recommendation with ID %s like", recommendation.id)

    return jsonify(recommendation.serialize()), status.HTTP_200_OK


######################################################################
# Activate and Deactivate a RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendation_id>/deactivation", methods=["PUT"])
def deactivate_recommendation(recommendation_id):
    """
    Deactivate a Recommendation
    """
    app.logger.info(
        "Request to deactivate recommendation with id: %s", recommendation_id
    )
    recommendation = Recommendation.find(recommendation_id)
    if not recommendation:
        abort(status.HTTP_404_NOT_FOUND, "recommendation not found")
    recommendation.deactivate()

    return jsonify(recommendation.serialize()), status.HTTP_200_OK


@app.route("/recommendations/<int:recommendation_id>/activation", methods=["PUT"])
def activate_recommendation(recommendation_id):
    """
    Activate a Recommendation
    """
    app.logger.info("Request to activate recommendation with id: %s", recommendation_id)
    activated_status = request.args.get("status", default=None)
    valid_status = ["VALID", "OUT_OF_STOCK"]
    recommendation = Recommendation.find(recommendation_id)
    if not recommendation:
        abort(status.HTTP_404_NOT_FOUND, "recommendation not found")
    if activated_status not in valid_status:
        abort(status.HTTP_400_BAD_REQUEST, "status for activation is required")
    recommendation.activate(activated_status)

    return jsonify(recommendation.serialize()), status.HTTP_200_OK


######################################################################
# PURCHASE A PET
######################################################################
# @app.route("/pets/<int:pet_id>/purchase", methods=["PUT"])
# def purchase_pets(pet_id):
#     """Purchasing a Pet makes it unavailable"""
#     pet = Pet.find(pet_id)
#     if not pet:
#         abort(status.HTTP_404_NOT_FOUND, f"Pet with id '{pet_id}' was not found.")
#     if not pet.available:
#         abort(
#             status.HTTP_409_CONFLICT,
#             f"Pet with id '{pet_id}' is not available.",
#         )

#     # At this point you would execute code to purchase the pet
#     # For the moment, we will just set them to unavailable

#     pet.available = False
#     pet.update()

#     return pet.serialize(), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
