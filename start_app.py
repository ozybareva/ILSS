import uvicorn
from application.application import App
from application.container import Container

app = App(Container)

uvicorn.run(app.start())
