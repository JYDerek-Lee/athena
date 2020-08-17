from app.core.quickstart import *
from app import create_app

# main()
app = create_app()
app.run(host="0.0.0.0", port=12012)
