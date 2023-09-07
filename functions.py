# In your Flask route function or context processor
navigation_items = [
    {"label": "Home", "url_for": "home", "sub_items": None},
    {
        "label": "Pages",
        "url_for": None,  # No direct link for the parent item
        "sub_items": [
            {"label": "About Us", "url_for": "about"},
            {"label": "Pricing", "url_for": "pricing"},
            {"label": "Testimonials", "url_for": "testimonials"},
            {"label": "Our Team", "url_for": "team"},
            # Add more sub-items as needed
        ],
    },
    {
        "label": "Shop",
        "url_for": None,  # No direct link for the parent item
        "sub_items": [
            {"label": "Products", "url_for": "products"},
            {"label": "Cart", "url_for": "cart"},
            {"label": "Checkout", "url_for": "checkout"},
            {"label": "Product Details", "url_for": "product_details"},
            {"label": "Global Location", "url_for": "global_location"},
            {"label": "FAQ", "url_for": "faq"},
            {"label": "Privacy Policy", "url_for": "privacy_policy"},
            {"label": "Terms and Conditions", "url_for": "terms_and_conditions"},
            # Add more sub-items as needed
        ],
    },
    {"label": "Services", "url_for": "services", "sub_items": None},
    {"label": "Blog", "url_for": "blog", "sub_items": None},
    {"label": "Company", "url_for": "company", "sub_items": None},
    {"label": "Contact Us", "url_for": "contact_us", "sub_items": None},
    # {
    #     "label": "User",
    #     "url_for": None,  # No direct link for the parent item
    #     "sub_items": [
    #         {"label": "My Account", "url_for": "my_account"},
    #         {"label": "Log In", "url_for": "login"},
    #         {"label": "Register", "url_for": "register"},
    #         {"label": "Forgot Password", "url_for": "recover_password"},
    #         # Add more sub-items as needed
    #     ],
    # },
    # Add more navigation items as needed
]