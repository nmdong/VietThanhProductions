from flask import Flask
from config import Config
from flasgger import Swagger
import yaml
from routes.user_routes import user_bp

app = Flask(__name__)
app.config.from_object(Config)

# Load swagger template
with open("swagger/swagger_generated.yaml", "r", encoding="utf-8") as f:
    swagger_template = yaml.safe_load(f)

swagger = Swagger(app, template=swagger_template)

# register blueprints
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True, port=Config.PORT)
