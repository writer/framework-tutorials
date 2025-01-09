prescribing_summary_prompt = """

Variables:

{prescribing_details}

************************

Prompt:
Here is the prescribing details text to summarize:

<text>
{prescribing_details}
</text>

Please summarize the prescribing details text.

"""
