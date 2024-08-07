def soap_notes_prompt(history):
    return f'''
    System: You are an expert at reviewing medical conversations and generating SOAP format medical notes summarizing those conversations. You will be given a conversation between a doctor and their patient. Review the conversation and create SOAP notes summarizing the encounter.
    
    Here are examples of SOAP notes. Your SOAP notes must be in the same exact format as these examples:
    
    <example>
    ### Lower back pain
    Patient experiencing severe lower back pain, which occasionally radiates down the left leg, indicative of possible sciatica. The symptoms have been present for a few days. The pain intensifies when sitting for prolonged periods or when attempting to stand. Home remedies such as a heating pad and ibuprofen have been tried, providing only temporary relief.\n\n
    
    Home care reviewed including continuing the use of a heating pad and over-the-counter ibuprofen for pain management. Advised to maintain moderate physical activity as tolerated and avoid prolonged sitting or standing in one position.\n\n\n
    
    #### Prescription sent \n
    Gabapentin \n
    Take 1 capsule three times a day \n 
    Disp: #90 capsules \n
    Refills: 1 \n\n
    
    Patient is advised to monitor symptoms and report any increase in pain or new symptoms. A follow-up visit is recommended to assess the effectiveness of the treatment and make any necessary adjustments.
    </example>

    <example>
    ### Adult Sinus
    Patient experiencing worsening sinus congestion, drainage, and headache for the past 5 days. The patient reports pain around the forehead and cheeks, particularly when bending over, but no fever is present. Home remedies including saline nasal spray and over-the-counter decongestants have been tried with minimal relief.\n\n

    Home care reviewed including continuing the use of saline nasal spray and maintaining hydration. Advised to avoid allergens and pollutants where possible and to use steam inhalation to help alleviate congestion.\n\n\n

    #### Prescriptions sent \n\n
    Amoxicillin 500 mg \n
    Take 1 capsule three times a day \n
    Disp: #30 capsules \n
    Refills: 0\n\n

    Fluticasone Propionate Nasal Spray \n
    Use two sprays in each nostril once a day \n
    Disp: #1 bottle \n
    Refills: 1\n\n

    Patient is advised to complete the full course of antibiotics and to monitor symptoms closely. A follow-up is recommended if symptoms persist beyond the treatment period or worsen.
    </example>

    Here is the conversation you need to review:

    <conversation>
    {history} 
    </conversation>

    Only give me the notes. Do not give me a title nor start your notes with "SOAP Notes". Do use Markdown formatting for your notes, including line breaks and an empty line between each paragraph.

    You must only use information from the conversation to write your SOAP notes. Do not make up any information. Use the same exact format as the examples provided for your SOAP notes, starting with a category as a Markdown header (e.g. "### Lower back pain" or "### Adult Sinus"). If the doctor orders medication(s) within the conversation, list that at the end of the SOAP notes, exactly like the examples. ONLY INCLUDE A MEDICATION IF IT WAS ORDERED - JUST BECAUSE A MEDICATION IS MENTIONED DOES NOT MEAN IT WAS ORDERED.

    If the patient's age is not mentioned in the conversation, then do not mention their age in your SOAP notes.

    Give me the SOAP notes now:
    '''

def icd_codes_prompt(history, notes):
    return f'''
    System: You are an expert at extracting ICD-10 codes from SOAP format medical notes. You will be given a conversation between a doctor and their patient, the resulting SOAP notes, and asked to extract all relevant ICD-10 codes.

    Here is the conversation you need to review:
    {history}

    Here are the SOAP notes you need to review:
    {notes}

    Extract all relevant ICD-10 codes from the conversation and SOAP notes.
    '''