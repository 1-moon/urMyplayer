import os
from app import create_app, db
from app.models import User, Role

app = create_app(os.getenv('MYCSW_CONFIG') or 'default')

# flask shell 
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)