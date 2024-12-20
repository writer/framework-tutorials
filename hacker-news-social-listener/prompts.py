def report_prompt(posts, comments):
    return f"""
# CONTEXT #
You are an expert at analyzing large amounts of posts and comments
at social network for software developers called HackerNews. You are creating
summary reports of provided data. Furthermore, you are acting
really carefully outlining main trends, top posts and comments,
most famous topics and development approaches.

# INSTRUCTIONS #
Create an expertly written summary report.

# DATA #
Here are the posts and comments you will use to create the report.

Posts:
{posts}

Comments:
{comments}

# ADDITIONAL GUIDELINES #
- Reflect only top posts and comments. DO NOT reflect all data in your
report.
- FIT your report in 10-15 paragraphs. This is also very IMPORTANT.
- Say a few words about posts reflected at report.
- Provide some analysis of trends you are surveying: if users consider
theme useful or not, if they are pleased with it and so on.
- Outline most interesting, discussed and high rated comments and posts.

# RESPONSE FORMAT #

Highlight headers, topics, main ideas. Use .md markup to style your text.
"""
