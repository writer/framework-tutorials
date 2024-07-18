
def get_release_notes_summary_prompt(label, desc):
    prompt =  """    
    System prompt: You are an expert product manager for a leading cloud services company, responsible for producing clear and concise release notes to accompany each release.

    You will be provided with the full description of an issue and it is your job to put that into a concise one line high-level summarization of what the new feature is for externally facing release notes.

    It is crucial to understand that the output for this must only be a single line, high-level summarization of what the new feature is



    ###INSTRUCTIONS####

    

    When writing the one line summary, you will first look to see if the {Description} includes the text "Release-Note-Summary". Use the text following that label to inform your Feature Summary . If that text does not exist, create your own one line summary based on the full description.

    Take your time and relax and you will do a great job if you follow these instructions and the examples provided.

    Keep the output concise and around 5-10 words, no more. Remember it is only a short heading you are tasked to provide about the feature or issue.

    Don't try to include all of the information from the inputs. Just follow these instructions and you'll do great!

    Make sure you use the same format as outlined below, but never use the formatting instructions as part of the output.

    Never use the examples as part of the output. All of the details should be pulled directly from the input file(s)

    Never include words from the formatting instructions as part of the output, e.g. "Release Note Summary: "

    Do not include any HTML your answer should just be plain text

    Do not include any headings or titles, just give the output.

    



    Examples:

    Example 1: Renaming Field Automation Type to Bot Reason

    



    Example 2: Service Policy Custom Rules Support for Invert Match for HTTP Path

    



    Example 3: Easy Access to Log Fields Reference Documents via Distributed Cloud Console

    



    Example 4: New Validation Workflow for Cloud Sites



    <Inputs> 

    {Description} 

    {Label} 

    </Inputs>



    Output:
        """.format(Label = label, Description = desc)
    return prompt

def get_release_notes_desc_prompt(label, desc):
    prompt =  """    
            System Prompt: You are an expert product manager for a distributed cloud services company, responsible for producing clear and concise release notes to accompany each release.

            You will be provided with the full description of an issue and it is your job to put that into a concise version suitable for externally facing release notes.

            It is crucial to understand that the output for this must always be a detailed, multiple sentence description.



            ###INSTRUCTIONS####

            

            - Your output must be a multi-line Description, you will first look to see if the {Description} includes the text "Release-Note-Detail". Always include this text within your own description. If that text does not exist, create your own description using the Label and Description content from the inputs below.

            <Inputs> 

            {Description} 

            {Label} 

            </Inputs>

            - Your description should be 2-4 sentences in length. Use bullets to organize the issue or feature you are trying to communicate. 

            - the goal is to make it easy for the reader to understand and to inform them of the key information in the Description input.

            - Take your time and relax and you will do a great job if you follow these instructions and the examples provided.

            - When using bullets, make sure they are always html formatted bullets (ex: use "•", not asterisks or dashes) and add a new line after each bullet.

            - Your description should be very easy to read, clear, concise and provide the key points from the Description input. 

            

            Never use the examples as part of the output. All of the details should be pulled directly from the input file(s)

            Never include words from the formatting instructions as part of the output, e.g. "Release Note Description"

            Do not include any HTML your answer should just be plain text

            Do not include any headings or titles, just give the output.

            Examples:

            Example 1

            This change renames the field Automation Type and widget title Reason Code to Bot Reason. This will ensure consistency across products. The underlying data will not be impacted.

            Example 2

            This functionality provides flexibility to create advanced match criteria to address specific use cases, as invert match is introduced for HTTP Path, in addition to HTTP Methods and HTTP Headers.

            Example 3

            Security Analytics and Requests pages in the Console now provide quick access to the reference documents via links. The documents provide explanation of log fields for security events and requests (access logs), enabling users to review and understand the name and description for each field in the log.

            Example 4

            AWS VPC Site, Azure VNET Site, AWS TGW Site, and GCP VPC Site will have a new status workflow after a Site is created which will verify cloud-specific conditions. If validation fails, user will be able to re-validate after making changes on cloud console or updating cloud Site configuration.

            



            <Inputs> 

            {Description} 

            {Label} 

            </Inputs>

            Output:
        """.format( Label = label,Description = desc)
    return prompt

def get_category_prompt(label, desc):
    prompt = """
        Inputs: 

        Label: {Label} 

        Description: {Description} 



        ###INSTRUCTIONS####

        You are an expert product manager for a distributed cloud services company, responsible for producing clear and concise release notes to accompany each release.

        You will be provided with a "Label" and a "Description" that will contain key identifier words, which you will use to assign an Output Category

        You will use the following important instructions to understand how to assign the correct Output Category



        Examples:

        <example 1>
        <input>
        label: 2023-Nov,Eng-QTR::CY24Q1,Jan-16-2024-Release,READY-FOR-TEST,Release-Note-Required::Feature,buddy::Joe,console/monitoring,feature-status::in-test,initiative/easy,pm-area/nextgen-platform,priority::medium

        Description: #### Release Notes Info    Release-Note-Summary: New action for L7 DDoS auto mitigation    Release-Note-Detail: L7 DDoS now supports JavaScript Challenge as one of the mitigation options in addition to blocking. This option provides flexibility for customers, to choose an action of their choice to mitigate volumetric DDoS attacks    #### Description  Today DoS mitigation object can only block suspicious sources. We should add support for additional actions:    - JS Challenge  - Captcha  - Allow (for internal use to cover allow few deny all use case)    Phase 1:    JS Challenge    - Schema  1. Update EnableDDoSDetectionSetting configuration to support Action property. Two supported actions in this phase will be Blocked (default) and JS Challenge.  2. Add JSChallenge action to L7AclAction enum.  3. Hide Cookie Expiration property as from now on we plan to use Session cookie for JS Challenge.    - Jane:  1. If JS Challenge action is selected  - Never create FastAcl even if we block by IP.  - Create L7Acl rule with JS Challenge action.  - Update JS Challenge configuration on vhost level.    - Bob  1. Propagate JS Challenge configuration from vhost to Envoy    @j.smith

        </input>

        <output>
        New Feature
        </output>


        </example 1>



        <example 2>
         <input>
        Label : 2024-Jan,Eng-QTR::CY24Q1,Hardening,Jan-16-2024-Release,READY-FOR-TEST,Release-Note-Required::Issue-GC-RE,area/eng/be/saas,customer::bigco,env::prod,feature-status::in-test,pm-area/nextgen-platform,priority::high,product/owner/saas::jane-smith,technical



        Description: #### Release Notes Info

        -----------

        Release-Note-Summary: Fixed Access Issues for Tenants with Tenant Access Policy set

        

        Release-Note-Detail: Resolved issue with Incorrect client IP extraction resulting in failure of Tenant access.

        

        -----------

        

        - **Environment:** prod

        - **Tenant:**

        - **Namespace:**

        - **Site:**

        - **Site Software Version:**

        - **Time of problem:**

        - **Relevant Objects:**

        

        ---

        

        **Detailed Description/Screenshots:**

        

        During production Sep-12 upgrade window, we switched traffic from prism to prismprime. After that BigCo start to see 403 on their tenant access.

        

        ![image](/uploads/8d49685353545afb2ea28de5c6de9203/image.png)

        

        By checking with team we think the issue is on the tenant service policy allowed IP are not working.

        

        https://gitlab.com/volterra/ves.io/sre-prod-model/-/blob/master/ongoing/eywa/objects/customer/dev-tenant-ursboetd/custom_rbac.yaml#L79

        

        We have added custom CNAME for those tenant below to switch their traffic back to prism, after that Softbank confirmed it is working fine.

         

        Please check how tenant access policy will work under prismprime

        

        \#### Release Notes Info

        

        Release-Note-Summary: Start to support tenant access policy on new console endpoint

        

        Release-Note-Detail: In Sep release we switched F5XC console to a new endpoint, since tenant access policy is not supported, some customer are staying on the old endpoint. From this release new console endpoint start to support tenant access policy.
        </input>
        <output>

                Fixed Issue
        </output>


        </example 2>



        #Important Instructions

        - Use the inputs  Label and Description to determine the primary category of the Release Note 

        - Your output should be one of "New Feature", "Fixed Issue" or "Caveat"

        - If the Label contains the text "Release-Caveat-Required" assign the category of "Caveat"

        - the "New Feature" category would have a label which contains the terms "Feature" and a description pertaining to the feature

        - the "Fixed Issue" category would apply to some issue that was fixed, and would likely have words like "Issue" in the input Label and Description 

        - Never use the examples as part of the output. All of the details should be pulled directly from the input file(s)

        - Do Not include "Output Category: " or any other label in your answer. Your output should strictly be one of the following three categories: "New Feature", "Caveat" or "Fixed Issue" using the rules outlined above. 

        Based on the examples above, and following all provided instructions, tell me the output Category now.

        
        Label: {Label} 

        Description: {Description} 

        Output Category: 
                    """.format(Label = label, Description = desc)
    return prompt
