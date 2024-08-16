base_prompt = """
    Output in the language of the location {location}.

    Write a promotional social media post for the product presented below the dashes. Include emojis.

    Target, specifically, the segment "{segment}".

    The market segments are as follows:
    - School: Grade school or high school students
    - University: University students
    - Work: People of working age
    - Retired: People who are retired

    Connect to the audience by using very strong references to {location}, but don't change its
     place of origin nor mention product features not present in the product description below.

    Use markdown syntax for the output.

    -----
    {product_description}
    """
