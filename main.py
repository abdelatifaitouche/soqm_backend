from fastapi import FastAPI


def create_app() -> FastAPI:

    app = FastAPI(title="SOQM", version="v1")

    return app


app: FastAPI = create_app()


@app.get("/health")
def home():
    return "soqm here"
