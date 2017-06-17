from app import app
import os

# if os.environ.get('ENVIRONMENT', 'local') == 'local':
#     app.run(debug=True, port=5454)
# else:
#     app.run()

app.run(debug=True, port=5454)
