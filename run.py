from app import create_app
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)

app = create_app()

@app.route("/")
def home():
    return "{status: 'ok'}"

if __name__ == '__main__':
    app.run(debug=True)
