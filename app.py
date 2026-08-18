
import io

import streamlit as st
from PIL import Image
from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration,
    BlipForQuestionAnswering,
    MarianMTModel,
    MarianTokenizer,
)
from gtts import gTTS

st.set_page_config(page_title="See it, Say it", page_icon="🗣️")

LANGUAGES = {
    "None (English only)": {"marian": None, "gtts": "en"},
    "Hindi": {"marian": "Helsinki-NLP/opus-mt-en-hi", "gtts": "hi"},
    "French": {"marian": "Helsinki-NLP/opus-mt-en-fr", "gtts": "fr"},
    "Spanish": {"marian": "Helsinki-NLP/opus-mt-en-es", "gtts": "es"},
    "German": {"marian": "Helsinki-NLP/opus-mt-en-de", "gtts": "de"},
}




@st.cache_resource(show_spinner=False)
def load_caption_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )
    return processor, model


@st.cache_resource(show_spinner=False)
def load_vqa_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
    model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
    return processor, model


@st.cache_resource(show_spinner=False)
def load_translation_model(model_name: str):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model



def caption_image(image: Image.Image) -> str:
    processor, model = load_caption_model()
    inputs = processor(image, return_tensors="pt")
    output_ids = model.generate(**inputs, max_new_tokens=60)
    return processor.decode(output_ids[0], skip_special_tokens=True)


def answer_question(image: Image.Image, question: str) -> str:
    processor, model = load_vqa_model()
    inputs = processor(image, question, return_tensors="pt")
    output_ids = model.generate(**inputs, max_new_tokens=40)
    return processor.decode(output_ids[0], skip_special_tokens=True).strip()


def translate_text(text: str, model_name: str) -> str:
    tokenizer, model = load_translation_model(model_name)
    batch = tokenizer([text], return_tensors="pt", padding=True)
    generated = model.generate(**batch)
    return tokenizer.decode(generated[0], skip_special_tokens=True)


def text_to_speech(text: str, lang_code: str) -> io.BytesIO:
    tts = gTTS(text=text, lang=lang_code)
    buffer = io.BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    return buffer



st.title("🗣️ See it, Say it")
st.caption("Upload or take a photo. I'll describe what's in it — out loud, in your language.")

image_source = st.radio("Image source", ["Upload", "Camera"], horizontal=True)
uploaded_file = (
    st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if image_source == "Upload"
    else st.camera_input("Take a photo")
)

question = st.text_input(
    "Optional: ask a specific question about the image",
    placeholder="e.g. What color is the object? How many people are there?",
)
target_lang = st.selectbox("Speak the result in:", list(LANGUAGES.keys()))

if not uploaded_file:
    st.info("Upload or capture an image to get started.")
    st.stop()

try:
    image = Image.open(uploaded_file).convert("RGB")
except Exception:
    st.error("Couldn't read that image. Please try a different file.")
    st.stop()

st.image(image, caption="Your image", use_container_width=True)

try:
    with st.spinner("Looking at the image..."):
        caption = caption_image(image)

    result_text = caption
    if question.strip():
        with st.spinner("Thinking about your question..."):
            answer = answer_question(image, question)
        result_text = f"{caption}. Regarding your question — {question} — the answer is: {answer}."

except Exception as exc:
    st.error(f"Something went wrong while analyzing the image: {exc}")
    st.stop()

st.subheader("Description")
st.write(result_text)

lang_info = LANGUAGES[target_lang]
speech_text = result_text

if lang_info["marian"]:
    try:
        with st.spinner(f"Translating to {target_lang}..."):
            speech_text = translate_text(result_text, lang_info["marian"])
        st.subheader(f"Translation ({target_lang})")
        st.write(speech_text)
    except Exception as exc:
        st.warning(f"Translation failed, playing English audio instead. ({exc})")
        speech_text = result_text
        lang_info = LANGUAGES["None (English only)"]

try:
    with st.spinner("Generating speech..."):
        audio_buffer = text_to_speech(speech_text, lang_info["gtts"])
    st.subheader("Listen")
    st.audio(audio_buffer, format="audio/mp3")
    st.download_button(
        "Download audio", audio_buffer, file_name="description.mp3", mime="audio/mp3"
    )
except Exception as exc:
    st.error(f"Couldn't generate audio: {exc}")