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
            <div style="padding: 18px; margin-bottom: 25px; border-radius: 12px; 
                        border: 1px solid #e0e0e0; background-color: white; 
                        box-shadow: 0 3px 10px rgba(0,0,0,0.08); height: 450px; overflow: hidden;">
            """, unsafe_allow_html=True)
            
            # Show cover image with fixed height to maintain alignment
            st.image(
                cover_url, 
                width=180, 
                use_container_width=True,
                output_format="JPEG"  # Specify format for better compatibility
            )
            
            # Book title with consistent styling and Al Khor branding color
            st.markdown(f"""
            <h3 style="margin-top: 15px; margin-bottom: 8px; font-size: 1.25rem; color: #873600;
                      height: 48px; overflow: hidden; text-overflow: ellipsis; font-weight: 600;">
                {book['title']}
            </h3>
            """, unsafe_allow_html=True)
            
            # Author with better styling
            st.markdown(f"""
            <p style="margin-bottom: 12px; font-size: 1rem; color: #555;">
                <strong>Author:</strong> {book['author']}
            </p>
            """, unsafe_allow_html=True)
            
            # Metadata (genre, age group) with better styling
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <div>
                    <span style="font-weight: 600; color: #444;">Genre:</span> 
                    <span style="color: #555;">{book['genre']}</span>
                </div>
                <div>
                    <span style="font-weight: 600; color: #444;">Age Group:</span> 
                    <span style="color: #555;">{book['age_group']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Popularity indicator (stars)
            popularity = min(max(book['popularity'], 1), 5)  # Ensure between 1-5
            stars = "⭐" * popularity
            st.markdown(f"""
            <p style="margin-bottom: 12px;">
                <strong style="color: #444;">Rating:</strong> <span>{stars}</span>
            </p>
            """, unsafe_allow_html=True)
            
            # Description (with truncation if too long)
            description = book['description']
            if len(description) > 180:  # Slightly longer for better readability
                description = description[:180] + "..."
            
            st.markdown(f"""
            <div style="height: 130px; overflow: hidden; margin-top: 5px; border-top: 1px solid #eee; padding-top: 12px;">
                <strong style="color: #444;">Description:</strong>
                <p style="color: #555; font-size: 0.95rem; line-height: 1.4; margin-top: 5px;">{description}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Close the container div
            st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        # If there's an error loading an image, use the default image
        st.warning(f"Could not display book: {book['title']}. Using default image.")
        st.error(str(e))
