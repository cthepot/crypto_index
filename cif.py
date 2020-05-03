from app import app, db
from app.models import Asset, Quote, User, Index, IndexAsset

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Asset': Asset, 'Quote': Quote, 'User': User, "Index": Index, "IndexAsset":IndexAsset}
