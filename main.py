from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
#from pdf_utils import extract_text_from_pdf
from qa_engine import answer_question, summarize_history
from chat_history import ChatManager
from models import AskRequest
from fastapi import WebSocket, WebSocketDisconnect
#from fastapi.responses import HTMLResponse
from typing import List
import fitz

from utils import split_text_to_chunks

app = FastAPI()
chat_manager = ChatManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pdf_text_chunks: List[str] = []

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hi! I'm ready to answer your questions based on the uploaded document(s). Ask me anything!")  # welcome

    chat_history = []

    try:
        while True:
            data = await websocket.receive_text()
            question = data.strip()

            answer = answer_question(question, pdf_text_chunks, chat_manager.get_history(), chat_manager.get_summary())
            chat_manager.add_to_history("user", question)
            chat_manager.add_to_history("assistant", answer)

            await websocket.send_text(answer)

    except WebSocketDisconnect:
        print("Client disconnected")

@app.post("/upload")
async def upload_pdf(files: List[UploadFile] = File(...)):
    global pdf_text_chunks
    all_text = ""

    valid_files = []
    for file in files:
        if file.content_type == "application/pdf":
            valid_files.append(file)
        else:
            return {"error": f"{file.filename} is not a valid PDF."}

    for file in valid_files:
        content = await file.read()
        doc = fitz.open(stream=content, filetype="pdf")
        for page in doc:
            all_text += page.get_text()
        doc.close()

    if not all_text.strip():
        return {"error": "Uploaded PDFs had no readable content."}

    new_chunks = split_text_to_chunks(all_text)
    pdf_text_chunks += new_chunks
    print(f"[UPLOAD] Added {len(new_chunks)} new chunks. Total: {len(pdf_text_chunks)}")

    chat_manager.set_summary("")

    notice = "📄 New document uploaded. I'm updated and ready for your next question!"
    chat_manager.add_to_history("assistant", notice)

    return {
        "message": "Files uploaded and processed successfully.",
        "notice": notice,
        "chunks": len(pdf_text_chunks)
    }
@app.post("/ask")
async def ask_question(request: AskRequest):
    global pdf_text_chunks

    if not pdf_text_chunks:
        return {"error": "No PDF uploaded yet."}

    history = chat_manager.get_history()
    summary = chat_manager.get_summary()

    #print("Chunks at ask time:", len(pdf_text_chunks))
    answer = answer_question(
        question=request.question,
        chunks=pdf_text_chunks,
        history=history,
        summary=summary
    )

    chat_manager.add_to_history("user", request.question)
    chat_manager.add_to_history("assistant", answer)

    updated_history = chat_manager.get_history()

    if len(updated_history) % 10 == 0:
        new_summary = summarize_history(updated_history)
        chat_manager.set_summary(new_summary)

    return {
        "answer": answer,
        "history": updated_history,
        "summary": chat_manager.get_summary()
    }
