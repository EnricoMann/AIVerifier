from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="AI Verifier API")

# ✅ Middleware de CORS — permite que o frontend (porta 3000) acesse o backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # ou ["*"] se quiser liberar geral
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Inclui as rotas da API (verify, analyze, etc.)
app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
