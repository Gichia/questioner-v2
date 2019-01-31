from app.api import ver2

@ver2.route("/", methods=["GET"])
def home():
    """Register new user endpoint"""
    return 'Home'