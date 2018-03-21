from app import app, chain


@app.shell_context_processor
def make_shell_context():
    return {
        'chain': chain
    }
