import streamlit as st

# Default cover image to use when a book cover is missing
DEFAULT_COVER_IMAGE_URL = "https://cdn.pixabay.com/photo/2018/01/17/18/43/book-3088775_960_720.jpg"

def format_book_card(book):
    """Format a book as a card in the Streamlit interface"""
    # Use the provided cover URL or default image
    cover_url = book['cover_url'] if book['cover_url'] else DEFAULT_COVER_IMAGE_URL
    
    # Handle potential image loading issues
    try:
        # Create a container for the book card with border and padding
        with st.container():
            # Adding some spacing and border with consistent height for better alignment
            st.markdown(f"""
            <div style="padding: 15px; margin-bottom: 20px; border-radius: 8px; 
                        border: 1px solid #e0e0e0; background-color: white; 
                        box-shadow: 0 2px 5px rgba(0,0,0,0.05); height: 100%;">
            """, unsafe_allow_html=True)
            
            # Show cover image with fixed height to maintain alignment
            st.image(
                cover_url, 
                width=180, 
                use_container_width=True,  # Updated from deprecated use_column_width
                output_format="JPEG"  # Specify format for better compatibility
            )
            
            # Book title with consistent styling
            st.markdown(f"""
            <h3 style="margin-top: 10px; margin-bottom: 5px; font-size: 1.2rem; 
                        height: 40px; overflow: hidden; text-overflow: ellipsis;">
                {book['title']}
            </h3>
            """, unsafe_allow_html=True)
            
            # Author
            st.markdown(f"**Author:** {book['author']}")
            
            # Metadata (genre, age group, popularity) in a more compact format
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Genre:** {book['genre']}")
            with col2:
                st.markdown(f"**Age Group:** {book['age_group']}")
            
            # Popularity indicator (stars)
            popularity = min(max(book['popularity'], 1), 5)  # Ensure between 1-5
            stars = "⭐" * popularity
            st.markdown(f"**Popularity:** {stars}")
            
            # Description (with truncation if too long)
            description = book['description']
            if len(description) > 150:  # Shortened a bit for better card layout
                description = description[:150] + "..."
            st.markdown(f"""
            <div style="height: 100px; overflow: hidden;">
                <strong>Description:</strong> {description}
            </div>
            """, unsafe_allow_html=True)
            
            # Close the container div
            st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        # If there's an error loading an image, use the default image
        st.warning(f"Could not display book: {book['title']}. Using default image.")
        st.error(str(e))
