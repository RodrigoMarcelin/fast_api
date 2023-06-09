from typing import Optional, Any 
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi import Path
from fastapi import Query
from fastapi import Header
from fastapi import Depends
from time import sleep
# from fastapi.responses import JSONResponse 
from fastapi import Response
from models import Curso
import uvicorn

def fake_db():
    try:
        print('Abrindo conexão com banco de dados...')
        sleep(1)

    finally:
        print('Fechando conexão com banco de dados')


app = FastAPI(
    title='API de Cursos da Geek University',
    version='0.0.1',
    description='Uma API para estudar fastapi'
    )

cursos = {
    1: {
        "titulo": "Programação para Leigos",
        "aulas": 112,
        "horas": 58
    },
    2: {
        "titulo": "Algoritimo e Lógica de Programação",
        "aulas": 87,
        "horas": 67
    }
}

@app.get('/cursos', descripition='Retorna todos os cursos ou uma lista vazia', summary='Retorna ')
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos

@app.get('/cursos/{curso_id}')
async def get_cursos(curso_id : int = Path(title='ID do curso', description='Deve ser entre 1 e 2', gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        return curso
    
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')

@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    next_id: int = len(cursos) + 1
    cursos[next_id] = curso
    del curso.id
    return curso
    
@app.put('/cursos/{curso_id}')
async def put_curso(curso_id : int, curso  : Curso, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id
        return curso
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe um curso com id {curso_id}')

@app.get('/calculadora')
async def calcular(a : int = Query(default=None, gt=5), b : int = Query(default=None, gt=10), c : int = Query(default=None, gt=6), xgeek : str = Header(default=None)):
    soma = a + b + c
    print(f'X-GEEK: {xgeek}')
    return {"resultado":soma}


@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe um curso com id {curso_id}')

if __name__ == '__main__':

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)