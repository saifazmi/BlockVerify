from app import app, blockchain


@app.shell_context_processor
def make_shell_context():
    return {
        'blockchain': blockchain
    }
