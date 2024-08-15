def _format_output(name, desc, product_num, features, specifications):
    html = f"""
    <div>
        <br>
            <h2>{name}</h2>
        <br>
            <p class="description"><b>Description</b>: {desc}</p>
        <br>
            <p class="description"><b>Product #</b>: {product_num}</p>
        <br>
            <h3> Features </h3>
            <p>{features}</p>
        <br>
            <h3> Specifications </h3>
            <p>{specifications}</p>
        <br>
    <div>

    """
    return html
