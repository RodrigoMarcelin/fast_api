from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
async def raiz():
    return {"msg": "FastAPI na Geek University"}

if __name__ == '__main__':

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                    log_level="info", reload=True)