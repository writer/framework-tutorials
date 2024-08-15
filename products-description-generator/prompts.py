def _get_features_prompt(features):
    prompt = f"""
You are a Product description page writer and formatter. Take in the following inputs which describe the product's
features and output a HTML bulleted list of the features.

Instructions:

- Do not output any Headings for anything else other than the bulleted list of features.
- Do not make up anything. Just reformat the contents of the input into the feature list.
- The Output MUST be formatted as a bulleted list. You will be penalized if you do not include bullets.
- If any of the features are "nan" ignore those lines and do not include them in the output.

Input: {features}

Look at the example below to understand the required format of the output

Example Output :

- Simplifies the running experience with lightweight, easy-to-use design.
- Enhances performance with features optimized for better energy return and cushioning.
- Adapts to a wide variety of running conditions, providing versatility and comfort on different terrains.

Output: 

    Output:
        """.format(
        features=features
    )
    return prompt


def _get_specifications_prompt(specifications):
    prompt = f"""
You are a Product description page writer and formatter. Take in the following inputs which describe the product's
specifications and output a List of the specifications with the Specification title wrapped in HTML bold tags <b> </b>
and the specification value next to it. Do not output any Headings for anything else other than
the list of specifications. Do not make up anything. Just reformat the contents of the input into the specification 
list.

Input: {specifications}

Look at the example below to understand the required format of the output. Notice that the format is "Label:
specification value". Ensure there is a colon between the label and the value. There must be a new line space
 "\n" between each item.

You can format the output as a bulleted list.

Example output:

- Suitable for a variety of conditions: Road running, trail running, treadmill \n
- Shoe Type: Neutral, Stability, Motion Control \n
- Size Range: US 7-14 \n
- Available in multiple widths: Narrow, Regular, Wide, Extra Wide \n
- Ideal for: Long-distance running, daily training, competitive racing

Output: 
        """.format(
        specifications=specifications
    )
    return prompt


def _get_description_prompt(desc):
    prompt = f"""
You are a Product description page writer and formatter. Take in the following long description for a product and
slightly rewrite it to sound more like the examples below.

Instructions:

- Do not output any Headings for anything else other than the modified product description
- Do not make up anything. Make sure none of the facts about the product are changed
- The output length should be less than 150 characters
- Learn the voice and structure from the examples below but do not copy any of the content into your output.
Only reference the voice and structure of the examples.

Examples:

1. Elevate your running game with the StrideMax Pro. Designed for seamless comfort and performance, 
these shoes make every run feel effortless. With adaptive cushioning, you’ll feel the difference 
from the very first step.

2. Take your daily jogs to the next level with SwiftRun 360. Engineered for both beginners and pros, these shoes offer
a perfect blend of support and flexibility. Slip them on, and experience a smooth ride right out of the box.

3. Transform your training with the SpeedFlex Elite. Built for endurance and speed, these shoes provide optimal support 
in every stride. Easy to break in, they’ll have you hitting your personal bests in no time.

Input: {desc}

Output: 

    Output:
        """.format(
        desc=desc
    )
    return prompt


def _get_translation_prompt(text, language):
    prompt = f"""
<context> You are a translation service that translates materials for multiple global markets.
You translate text exactly as is, word for word. You do not paraphrase or rewrite anything
with your translation. </context>

Translate the source provided to language without altering any of the formatting, including hyperlinks,
 lists, italicized text, and section headers.

<instructions>
1. DO NOT skip any sections and DO NOT paraphrase anything.
2. Make sure to retain the spacing formatting of the output and use the same headers and paragraphs in the output.
If bullets, headers, section titles or specific spacing is used you MUST retain the same formatting in the output
including line spaces and bullet points. Do not retain the Bold formatting.
3. DO NOT make up any information in the output. You will be heavily penalized for including details in your output
that are not present in the original text.
4. DO not output instructions, only give the translated output of the source text from the input below.
5. For short pieces of text such as Names of devices, do not include any additional text aside from the Name
of the device. You will get a $200 tip if you follow this rule.

<inputs>
source: {text}
language: {language}
</inputs>

Output:
""".format(
        text=text, language=language
    )
    return prompt
