from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any
import re
import numpy as np

app = FastAPI(title="AI Text Detector API")

# CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

class DetectionResponse(BaseModel):
    is_ai_generated: bool
    confidence: float
    human_probability: float
    ai_probability: float
    explanation: str
    features: Dict[str, Any]

def analyze_text_features(text: str) -> Dict:
    """Analyze text features that might indicate AI generation"""
    features = {}
    
    # Basic text statistics
    words = text.split()
    features['word_count'] = len(words)
    features['char_count'] = len(text)
    features['avg_word_length'] = sum(len(word) for word in words) / max(len(words), 1)
    
    # Sentence analysis
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    features['sentence_count'] = len(sentences)
    features['avg_sentence_length'] = features['word_count'] / max(len(sentences), 1)
    
    # Calculate sentence length variance (AI tends to have more uniform sentences)
    if len(sentences) > 1:
        sentence_lengths = [len(s.split()) for s in sentences]
        features['sentence_length_variance'] = np.var(sentence_lengths)
    else:
        features['sentence_length_variance'] = 0
    
    # Repetition detection
    words_lower = [w.lower() for w in words]
    unique_words = len(set(words_lower))
    features['lexical_diversity'] = unique_words / max(len(words), 1)
    
    # Common AI patterns and phrases
    ai_phrases = [
        'as an ai', 'language model', 'i don\'t have', 'i cannot', 'i can\'t',
        'it\'s important to note', 'it is important to note',
        'in conclusion', 'furthermore', 'moreover', 'however',
        'it\'s worth noting', 'it is worth noting',
        'i apologize', 'i\'m sorry', 'my apologies',
        'delve into', 'navigating', 'landscape of',
        'realm of', 'it\'s crucial', 'underscores the importance'
    ]
    
    text_lower = text.lower()
    features['ai_phrase_count'] = sum(1 for phrase in ai_phrases if phrase in text_lower)
    
    # Punctuation patterns
    features['exclamation_count'] = text.count('!')
    features['question_count'] = text.count('?')
    features['ellipsis_count'] = text.count('...')
    features['comma_count'] = text.count(',')
    
    # Capitalization patterns (humans more varied)
    uppercase_words = sum(1 for word in words if word.isupper() and len(word) > 1)
    features['uppercase_word_ratio'] = uppercase_words / max(len(words), 1)
    
    # Contractions (humans use more)
    contractions = ["n't", "'m", "'re", "'ve", "'ll", "'d", "'s"]
    features['contraction_count'] = sum(text.count(c) for c in contractions)
    
    # Slang and informal words (more human)
    slang_words = ['lol', 'omg', 'btw', 'idk', 'tbh', 'ngl', 'fr', 'rn', 'gonna', 'wanna', 'gotta']
    features['slang_count'] = sum(1 for word in words_lower if word in slang_words)
    
    # Typos and repetitions (more human) - basic detection
    features['repeated_chars'] = len(re.findall(r'(.)\1{2,}', text))  # like "soooo", "noooo"
    
    # Perfect grammar indicators (more AI)
    # Count transitions and formal connectors
    formal_transitions = ['furthermore', 'moreover', 'additionally', 'consequently', 
                         'therefore', 'thus', 'hence', 'accordingly', 'nevertheless']
    features['formal_transition_count'] = sum(1 for word in formal_transitions if word in text_lower)
    
    return features

def calculate_ai_score(text: str, features: Dict) -> tuple:
    """
    Enhanced AI detection algorithm with weighted features
    Returns: (ai_probability, human_probability)
    """
    
    # Start with neutral score
    score = 0.5
    confidence_factors = []
    
    # Feature 1: AI phrases (very strong indicator)
    if features['ai_phrase_count'] > 0:
        ai_phrase_boost = min(0.25, features['ai_phrase_count'] * 0.15)
        score += ai_phrase_boost
        confidence_factors.append(f"AI phrases: +{ai_phrase_boost:.2f}")
    
    # Feature 2: Lexical diversity (AI tends to have higher diversity)
    if features['lexical_diversity'] > 0.80:
        score += 0.15
        confidence_factors.append("High lexical diversity: +0.15")
    elif features['lexical_diversity'] < 0.60:
        score -= 0.12
        confidence_factors.append("Low lexical diversity: -0.12")
    
    # Feature 3: Sentence length uniformity (AI more uniform)
    if features['sentence_length_variance'] < 10 and features['sentence_count'] > 2:
        score += 0.12
        confidence_factors.append("Uniform sentences: +0.12")
    elif features['sentence_length_variance'] > 30:
        score -= 0.10
        confidence_factors.append("Varied sentences: -0.10")
    
    # Feature 4: Long average sentence length (AI tends to write longer)
    if features['avg_sentence_length'] > 25:
        score += 0.10
        confidence_factors.append("Long sentences: +0.10")
    elif features['avg_sentence_length'] < 15:
        score -= 0.08
        confidence_factors.append("Short sentences: -0.08")
    
    # Feature 5: Formal transitions (AI uses more)
    if features['formal_transition_count'] > 2:
        score += 0.12
        confidence_factors.append("Formal transitions: +0.12")
    
    # Feature 6: Punctuation variety (humans more varied)
    if features['exclamation_count'] > 0 or features['question_count'] > 1:
        score -= 0.10
        confidence_factors.append("Varied punctuation: -0.10")
    
    if features['ellipsis_count'] > 0:
        score -= 0.08
        confidence_factors.append("Ellipsis usage: -0.08")
    
    # Feature 7: Contractions (humans use more)
    contraction_ratio = features['contraction_count'] / max(features['word_count'], 1)
    if contraction_ratio > 0.03:
        score -= 0.12
        confidence_factors.append("High contractions: -0.12")
    elif contraction_ratio == 0 and features['word_count'] > 50:
        score += 0.08
        confidence_factors.append("No contractions: +0.08")
    
    # Feature 8: Slang and informal language (very human)
    if features['slang_count'] > 0:
        slang_boost = min(0.20, features['slang_count'] * 0.10)
        score -= slang_boost
        confidence_factors.append(f"Slang words: -{slang_boost:.2f}")
    
    # Feature 9: Repeated characters (human emotional expression)
    if features['repeated_chars'] > 0:
        score -= 0.10
        confidence_factors.append("Repeated chars: -0.10")
    
    # Feature 10: Uppercase emphasis (humans do this more)
    if features['uppercase_word_ratio'] > 0.05:
        score -= 0.08
        confidence_factors.append("Uppercase emphasis: -0.08")
    
    # Feature 11: Very short text is harder to classify
    if features['word_count'] < 30:
        # Pull toward neutral for very short texts
        score = 0.5 + (score - 0.5) * 0.6
        confidence_factors.append("Short text: reduced confidence")
    
    # Feature 12: Perfect grammar and structure (AI indicator)
    # No informal punctuation, no slang, high diversity, formal
    if (features['exclamation_count'] == 0 and 
        features['slang_count'] == 0 and 
        features['repeated_chars'] == 0 and
        features['lexical_diversity'] > 0.75 and
        features['word_count'] > 40):
        score += 0.10
        confidence_factors.append("Perfect structure: +0.10")
    
    # Clamp score between 0.05 and 0.95
    score = max(0.05, min(0.95, score))
    
    ai_probability = score
    human_probability = 1 - score
    
    return ai_probability, human_probability, confidence_factors

def get_explanation(is_ai: bool, confidence: float, features: Dict, factors: List[str]) -> str:
    """Generate detailed explanation for the detection"""
    explanations = []
    
    if is_ai:
        if features['ai_phrase_count'] > 0:
            explanations.append("Contains typical AI assistant phrases")
        if features['formal_transition_count'] > 2:
            explanations.append("Uses formal transitions like 'furthermore' and 'moreover'")
        if features['lexical_diversity'] > 0.75:
            explanations.append("High vocabulary diversity typical of AI")
        if features['avg_sentence_length'] > 25:
            explanations.append("Consistently long, complex sentences")
        if features['sentence_length_variance'] < 10 and features['sentence_count'] > 2:
            explanations.append("Very uniform sentence structure")
        if features['contraction_count'] == 0 and features['word_count'] > 50:
            explanations.append("Formal tone with no contractions")
        
        if not explanations:
            explanations.append("Text structure and patterns suggest AI generation")
    else:
        if features['slang_count'] > 0:
            explanations.append("Uses informal language and slang")
        if features['repeated_chars'] > 0:
            explanations.append("Contains emotional expressions with repeated characters")
        if features['exclamation_count'] > 0 or features['question_count'] > 1:
            explanations.append("Varied punctuation suggests human writing")
        if features['contraction_count'] > 0:
            explanations.append("Natural use of contractions")
        if features['sentence_length_variance'] > 30:
            explanations.append("Sentence lengths vary naturally")
        if features['lexical_diversity'] < 0.65:
            explanations.append("Natural word repetition patterns")
        
        if not explanations:
            explanations.append("Writing style and patterns suggest human authorship")
    
    confidence_text = f"Confidence: {confidence*100:.1f}%"
    return f"{'. '.join(explanations)}. {confidence_text}"

@app.post("/detect", response_model=DetectionResponse)
async def detect_text(input_data: TextInput):
    text = input_data.text.strip()
    
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(text) < 10:
        raise HTTPException(status_code=400, detail="Text too short for analysis (minimum 10 characters)")
    
    # Warning for short texts
    word_count = len(text.split())
    if word_count < 20:
        raise HTTPException(
            status_code=400, 
            detail="Text is too short for reliable detection. Please provide at least 20 words (50+ words recommended for best accuracy)"
        )
    
    # Analyze text features
    features = analyze_text_features(text)
    
    # Calculate AI probability using enhanced algorithm
    ai_prob, human_prob, factors = calculate_ai_score(text, features)
    
    is_ai_generated = ai_prob > 0.5
    confidence = max(ai_prob, human_prob)
    
    explanation = get_explanation(is_ai_generated, confidence, features, factors)
    
    return DetectionResponse(
        is_ai_generated=is_ai_generated,
        confidence=confidence,
        human_probability=human_prob,
        ai_probability=ai_prob,
        explanation=explanation,
        features=features
    )

@app.get("/")
async def root():
    return {
        "message": "AI Text Detection API",
        "version": "2.0.0",
        "endpoints": {
            "/detect": "POST - Detect if text is AI-generated",
            "/health": "GET - Check API health"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "algorithm": "rule-based-enhanced"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)