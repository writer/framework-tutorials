from datetime import datetime

import aiohttp
from Bio import Entrez, Medline
from writerai import AsyncWriter


async def _get_full_prescribing_info(drug_name: str, limit: int = 1) -> list:
    """
    Fetch full prescribing information from the OpenFDA API.

    Parameters:
    - drug_name: The name of the drug to search for.
    - limit: The maximum number of records to return (default is 1).

    Returns:
    - A list of dictionaries containing full prescribing information.
    """
    base_url = "https://api.fda.gov/drug/label.json"
    params = {"search": f'openfda.brand_name:"{drug_name}"', "limit": limit}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params, timeout=5) as response:
                response.raise_for_status()  # Raise an error for bad responses
                data = await response.json()

                # Extract and return the full prescribing information
                results = data.get("results", [{}])

                return results

    except Exception as e:
        print(f"An error occurred while prescribing info fetching: {e}")
        return [{}]


def _parse_prescribing_info(info: dict) -> str:
    return (
        "## Full Prescribing Information\n\n"
        f"**Product Data Elements:** {info.get('spl_product_data_elements', ['N/A'])[0]}\n\n"
        f"**Brand Name:** {info.get('openfda', {}).get('brand_name', ['N/A'])[0]}\n\n"
        f"**Generic Name:** {info.get('openfda', {}).get('generic_name', ['N/A'])[0]}\n\n"
        f"**Indications and Usage:** {info.get('indications_and_usage', ['N/A'])[0]}\n\n"
        f"**Dosage and Administration:** {info.get('dosage_and_administration', ['N/A'])[0]}\n\n"
        f"**Contraindications:** {info.get('contraindications', ['N/A'])[0]}\n\n"
        f"**Warnings and Precautions:** {info.get('warnings_and_cautions', ['N/A'])[0]}\n\n"
        f"**Adverse Reactions:** {info.get('adverse_reactions', ['N/A'])[0]}\n\n"
        f"**Use in Specific Populations:** {info.get('use_in_specific_populations', ['N/A'])[0]}\n\n"
        f"**Pharmacodynamics:** {info.get('pharmacodynamics', ['N/A'])[0]}\n\n"
        f"**Pharmacokinetics:** {info.get('pharmacokinetics', ['N/A'])[0]}\n\n"
        f"**Clinical Pharmacology:** {info.get('clinical_pharmacology', ['N/A'])[0]}\n\n"
        f"**Mechanism of Action:** {info.get('mechanism_of_action', ['N/A'])[0]}\n\n"
        f"**Information for Patients:** {info.get('information_for_patients', ['N/A'])[0]}\n\n"
        + "---"
    )


async def _get_drug_side_effects(drug_name: str) -> str:
    # Define the base URL for the OpenFDA API
    base_url = "https://api.fda.gov/drug/event.json"

    # Set up the query parameters
    params = {
        "search": f'patient.drug.medicinalproduct:"{drug_name}"',
        "limit": 5,  # Limit the number of results
    }
    try:
        # Make the request to the OpenFDA API
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params, timeout=5) as response:
                response.raise_for_status()  # Raise an error for bad responses

                # Parse the JSON response
                data = await response.json()

                # Extract and print the side effects
                result = data.get("results", [{}])[0]

                reactions = result.get("patient", {}).get("reaction", [])

                adverse_reactions = ""
                for reaction in reactions:
                    adverse_reactions += f"- {reaction.get('reactionmeddrapt')}\n"

                return adverse_reactions

    except Exception as e:
        print(f"An error occurred during fetching side effects: {e}")
        return ""


def _get_pubmed_sheets(drug_name: str) -> dict:
    Entrez.email = "your_email@example.com"

    # Search for articles related to a specific drug
    handle = Entrez.esearch(db="pubmed", term=drug_name, retmax=5)
    record = Entrez.read(handle)
    handle.close()

    # Fetch details of the articles
    id_list = record["IdList"]
    handle = Entrez.efetch(db="pubmed", id=id_list, rettype="medline", retmode="text")
    records = Medline.parse(handle)

    # Prepare data for state variable
    pubmed_articles_list = []
    for record in records:
        # Extract required fields
        title = record.get("TI", "N/A")
        abstract = record.get("AB", "N/A")
        place_of_publication = record.get("PL", "N/A")

        # Use a combination of fields for more accurate dating
        date_fields = ["EDAT", "CRDT", "DEP", "DP"]
        publication_date = next(
            (record.get(field) for field in date_fields if field in record), "N/A"
        )

        if publication_date != "N/A":
            try:
                # Parse the date string
                date_obj = datetime.strptime(publication_date, "%Y/%m/%d %H:%M")
                publication_date = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                # If parsing fails, keep the original string
                pass

        pmid = record.get("PMID", "N/A")
        article_link = (
            f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid != "N/A" else "N/A"
        )

        # Add to pubmed_articles_list
        pubmed_articles_list.append(
            {
                "Title": title,
                "Abstract": abstract,
                "Place of Publication": place_of_publication,
                "Publication Date": publication_date,
                "Article Link": article_link,
            }
        )

    handle.close()

    # Sort the list by publication date (newest first)
    pubmed_articles_list.sort(key=lambda x: x["Publication Date"], reverse=True)

    # Convert the sorted list back to a dictionary
    pubmed_articles = {
        f"Article {i}": article for i, article in enumerate(pubmed_articles_list, 1)
    }

    return pubmed_articles


async def _upload_file_and_add_to_graph(
    file_data: str, file_name: str, graph_id: str
) -> dict:
    try:
        client = AsyncWriter()
        file_id = await _upload_file(client, file_data, file_name)
        await _add_file_to_graph(client, graph_id, file_id)
        return {"file_id": file_id, "graph_id": graph_id}

    except Exception as e:
        print(f"An error while file uploading occurred: {str(e)}")
        return {}


async def _upload_file(client: AsyncWriter, file_data: str, file_name) -> str:
    uploaded_file = await client.files.upload(
        content=str.encode(file_data),
        content_disposition=f"attachment; filename='{file_name}'",
        content_type="text/plain",
    )
    return uploaded_file.id


async def _add_file_to_graph(client: AsyncWriter, graph_id: str, file_id: str) -> None:
    await client.graphs.add_file_to_graph(graph_id=graph_id, file_id=file_id)
