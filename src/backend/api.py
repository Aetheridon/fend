from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm import check_hardware_type

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

current_model = None
current_tokenizer = None
current_device = None
current_model_name = None

class InferRequest(BaseModel):
    model_name: str
    prompt: str
    max_length: int = 100
    temperature: float = 0.1

@app.post("/infer")
async def infer(request: InferRequest):
    """Load model if needed and generate response"""
    global current_model, current_tokenizer, current_device, current_model_name

    # load model if not loaded or if model_name changed
    if current_model is None or current_model_name != request.model_name:
        try:
            current_tokenizer, current_model, current_device = check_hardware_type(request.model_name)
            current_model_name = request.model_name
            print(f"Model {current_model_name} loaded on {current_device}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")

    # generate response
    try:
        inputs = current_tokenizer(request.prompt, return_tensors="pt").to(current_device)
        is_seq2seq = "flan-t5" in current_model_name.lower()
        outputs = current_model.generate(
            inputs["input_ids"],
            max_length=request.max_length,
            temperature=request.temperature,
            num_beams=4 if is_seq2seq else 1,
            do_sample=True if request.temperature > 0.1 else False
        )
        response = current_tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during inference: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)