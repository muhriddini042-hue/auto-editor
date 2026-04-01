from .ai_scorer import score_image

def select_best(images):
    return sorted(images, key=score_image, reverse=True)
