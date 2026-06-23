import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import tempfile
import streamlit as st
from PIL import Image

from agents.orchestrator_agent import OrchestratorAgent


st.set_page_config(
    page_title="Assistive Vision Agent",
    page_icon="🦮",
    layout="centered",
)


def save_uploaded_image_temporarily(uploaded_file) -> str:
    suffix = Path(uploaded_file.name).suffix or ".jpg"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        return temp_file.name


def main() -> None:
    st.title("🦮 Assistive Vision Agent")
    st.caption("A safe multi-agent assistant for visually impaired users.")

    st.markdown(
        """
        This demo can describe images, read visible text, and provide safety-aware,
        voice-friendly responses.
        """
    )

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Upload a scene, sign, label, receipt, or document image.",
    )

    prompt = st.text_area(
        "What would you like help with?",
        value="Describe this image",
        placeholder="Examples: Describe this image, Read this sign, Where is my phone?",
    )

    run_button = st.button("Analyze image", type="primary")

    if uploaded_file is not None:
        st.image(
            Image.open(uploaded_file),
            caption="Uploaded image preview",
            use_container_width=True,
        )

    if run_button:
        if not prompt.strip():
            st.error("Please enter a question.")
            return

        image_path = None

        if uploaded_file is not None:
            image_path = save_uploaded_image_temporarily(uploaded_file)

        agent = OrchestratorAgent()

        with st.spinner("Analyzing..."):
            response = agent.handle_text_request(
                prompt=prompt.strip(),
                image_path=image_path,
            )

        st.subheader("Assistant response")
        st.write(response.answer)

        st.subheader("Safety")
        st.write(f"Risk level: **{response.risk_level.value}**")

        if response.uncertainty:
            st.warning(response.uncertainty)

        st.caption(
            "Privacy note: uploaded images are used for this analysis session. "
            "The app logs metadata and final answers, but not image contents."
        )

    st.divider()

    st.markdown(
        """
        **Safety notice:** This assistant does not replace professional medical,
        legal, financial, emergency, or navigation support.
        """
    )


if __name__ == "__main__":
    main()