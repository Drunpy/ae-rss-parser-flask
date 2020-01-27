from flask import jsonify, Blueprint
from flask_jwt import jwt_required
from parser.xml_to_json_parser import XmlToJsonParser
bp = Blueprint("main", __name__, url_prefix="/")

@bp.route("/", methods=("GET",))
@jwt_required()
def index():
    return jsonify(
        XmlToJsonParser(
            url="http://revistaautoesporte.globo.com/rss/ultimas/feed.xml"
        ).as_dict()
    )
