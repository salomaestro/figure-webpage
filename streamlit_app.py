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
    """Generator which yields the images filenames in the shared directory between the dates."""

    start = int(start_date.strftime("%s"))
    end = int(end_date.strftime("%s"))

    # Use st_mtime (modification time) for sorting and filtering
    sort_key = lambda x: Path(x).stat().st_mtime
    sort_date = lambda x: x.stat().st_mtime > start and x.stat().st_mtime < end

    for fname in sorted(shared_dir.glob("*.png"), key=sort_key, reverse=True):

        if not sort_date(fname):
            continue

        yield fname

col1, col2 = st.columns(2)

def load_images_from_redis():
    while r.llen('image_queue') > 0:
        image_path = r.rpop('image_queue').decode('utf-8')
        st.session_state.images.append(Path(image_path))

with col1:
    
    # Initialize
    st.header("Newest Images")

    # Initialize session state for images
    if 'images' not in st.session_state:
        st.session_state.images = []

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

    # Initialize
    st.header("Archived Images")

    if "archive_images" not in st.session_state:
        st.session_state.archive_images = []

    # Expander and time search logic
    with st.expander("Load previous images"):
        today = datetime.datetime.now()
        prev_week = datetime.datetime(today.year, today.month, today.day - 7)

        try:
            start_date, end_date = st.date_input(
                "Set time range",
                (prev_week, today),
                format="YYYY.MM.DD"
            )
        except:
            pass

        try:
            # Load images in selected time range
            if st.button("Load"):

                st.session_state.archive_images.clear()

                for archive_image_path in load_timerange(start_date, end_date):

                    st.session_state.archive_images.append(archive_image_path)
        except:
            # Quick check to see if start and end date is set
            if not 'start_date' in locals():
                st.warning("Start date is missing!", icon='⚠️')
            if not 'end_date' in locals():
                st.warning("End date is missing!", icon='⚠️')


    # Display each image in smaller columns
    n_cols = 3
    imcols = st.columns(n_cols)
    for i, img_path in enumerate(st.session_state.archive_images):
        col_num = i % n_cols

        with imcols[col_num]:
            img = Image.open(img_path)
            st.image(img, caption=img_path.name, use_column_width="auto")

