from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def extract_keywords_from_image(image: Image.Image, top_k=3):
    labels = [
        "smartphone", "laptop", "headphones", "sneakers", "handbag", "watch",
        "jacket", "camera", "bottle", "book", "toy", "shirt", "sunglasses",
        "sofa", "chair", "bicycle", "television", "earbuds"
    ]
    inputs = _processor(text=labels, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = _model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
        best = torch.topk(probs, top_k)
        top_labels = [labels[i] for i in best.indices[0]]
        return top_labels
