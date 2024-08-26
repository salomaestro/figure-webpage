import streamlit as st
from PIL import Image
import redis
from pathlib import Path
import datetime

# Initialize Redis connection
r = redis.Redis(host='redis', port=6379, db=0)
shared_dir = Path("data")

st.set_page_config(layout="wide")

def load_timerange(start_date, end_date):
    """Loads the images in the shared directory between the dates."""

    start = int(start_date.strftime("%s"))
    end = int(end_date.strftime("%s"))

    files = list(
        filter(
            lambda x: x.stat().st_mtime > start and x.stat().st_mtime < end,
            sorted(shared_dir.glob("*.png"), key=lambda x: Path(x).stat().st_mtime, reverse=True)
        )
    )

    return files

col1, col2 = st.columns(2)


# Initialize session state for images
if 'images' not in st.session_state:
    st.session_state.images = []

def load_images_from_redis():
    while r.llen('image_queue') > 0:
        image_path = r.rpop('image_queue').decode('utf-8')
        st.session_state.images.append(Path(image_path))

with col1:
    st.header("Newest Images")

    # Load new images
    load_images_from_redis()

    # Manual refresh button
    if st.button("Refresh Images"):
        load_images_from_redis()

    # Display the images
    for img_path in st.session_state.images:
        img = Image.open(img_path)
        st.image(img, caption=img_path.name, use_column_width="auto")

with col2:
    st.header("Archived Images")

    if "archive_images" not in st.session_state:
        st.session_state.archive_images = []

    with st.expander("Load previous images"):
        today = datetime.datetime.now()
        prev_week = datetime.datetime(today.year, today.month, today.day - 7)

        start_date, end_date = st.date_input(
            "Set time range",
            (prev_week, today),
            format="YYYY.MM.DD"
        )

        if st.button("Load"):
            st.session_state.archive_images.clear()

            for archive_image_path in load_timerange(start_date, end_date):

                st.session_state.archive_images.append(archive_image_path)

    imcols = st.columns(3)
    for i, img_path in enumerate(st.session_state.archive_images):
        col_num = i % 3

        with imcols[col_num]:
            img = Image.open(img_path)
            st.image(img, caption=img_path.name, use_column_width="auto")

