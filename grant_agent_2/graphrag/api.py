from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from global_search import ask_query_global
from local_search import ask_query_local
import uvicorn

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/global_search")
def global_search(request: QueryRequest):
    try:
        res = ask_query_global(request.query)
        return {"response": res['response']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/local_search")
def local_search(request: QueryRequest):
    try:
        res = ask_query_local(request.query)
        return {"response": res['response']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
