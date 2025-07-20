import os
from dotenv import load_dotenv
from ai.perplexity import call_perplexity_chat
load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")


def summarize_history(history: list[dict]) -> str:
    if not history:
        return ""

    messages = [{"role": "system", "content": "You are a helpful summarizer. Read the following conversation and summarize it briefly."}]

    messages += history

    messages.append({"role": "user", "content": "Summarize the above conversation briefly."})

    return call_perplexity_chat("sonar-pro",messages)

# def answer_question(question: str, chunks: list[str], history: list[dict], summary: str) -> str:
#     context = "\n\n".join(chunks[:3])  # Keep context small
#
#     messages = []
#
#     if summary:
#         messages.append({"role": "system", "content": f"Summary of previous chat: {summary}"})
#     else:
#         messages.append({"role": "system", "content": "You are a helpful assistant."})
#
#     # Last 2 Q&A pairs only
#     for item in history[-2:]:
#         messages.append({"role": "user", "content": item["question"]})
#         messages.append({"role": "assistant", "content": item["answer"]})
#
#     # Current question
#     messages.append({
#         "role": "user",
#         "content": f"Based on this document:\n{context}\n\nQuestion: {question}"
#     })
#
#     response = requests.post(
#         "https://api.perplexity.ai/chat/completions",
#         headers={
#             "Authorization": f"Bearer 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",
#             "Content-Type": "application/json"
#         },
#         json={
#             "model": "sonar-pro",
#             "messages": messages
#         }
#     )
#
#     if response.status_code == 200:
#         return response.json()["choices"][0]["message"]["content"]
#     else:
#         return f"Error from Perplexity API: {response.text}"

def build_system_prompt(summary: str | None = None) -> str:
    base = (
        "You are a helpful AI assistant trained to answer questions based on a document and ongoing conversation.\n"
        "- If the user asks something ambiguous or unclear, ask for clarification.\n"
        "- If no answer can be found in the document, say 'I couldn't find a relevant answer in the document.'\n"
        "- Use recent Q&A context when answering.\n"
        "- Be concise and accurate.\n"
        "- You can use bullet points, Emojis and other essential things to make the response effective. [frontend using react-markdown for responses. respond accordingly]"
    )
    if summary:
        base += f"\nHere is a summary of the conversation so far:\n{summary}\n"
    return base

def get_valid_history_pairs(history: list[dict]) -> list[dict]:
    filtered = [msg for msg in history if msg["role"] in ("user", "assistant")]
    result = []
    expecting = "user"
    for msg in filtered:
        if msg["role"] == expecting:
            result.append(msg)
            expecting = "assistant" if expecting == "user" else "user"
        else:
            break

    if len(result) % 2 != 0:
        result = result[:-1]

    return result[-4:]



def answer_question(question: str, chunks: list[str], history: list[dict], summary: str) -> str:
    messages = []

    system_prompt = build_system_prompt(summary)
    messages.append({"role": "system", "content": system_prompt})

    # for item in history[-2:]:
    #     messages.append({"role": "user", "content": item["question"]})
    #     messages.append({"role": "assistant", "content": item["answer"]})
    messages.extend(get_valid_history_pairs(history))
    document_context = "\n".join(chunks[:3])

    print("3 chunks:", document_context)

    user_prompt = f"Here is the document context:\n{document_context}\n\nNow answer this question:\n{question}"
    messages.append({"role": "user", "content": user_prompt})

    return call_perplexity_chat("sonar-pro",messages)