#core/pipeline.py
from diffusers import StableDiffusionXLPipeline  
import torch

def build_pipeline(hf_token: str | None = None):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32

    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=dtype,
        use_safetensors=True,
        variant="fp16" if dtype == torch.float16 else None,
        token=hf_token,
    )

    pipe = pipe.to(device)
    if device == "cuda":
        pipe.enable_attention_slicing()

    return pipe
