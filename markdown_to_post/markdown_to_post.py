import markdown
import re

def add_custom_classes(html):
    # Adding classes to headings
    html = re.sub(r'<h1>(.*?)</h1>', r"<h1 class='main-heading'>\1</h1>", html)
    html = re.sub(r'<h2>(.*?)</h2>', r"<h2 class='sub-heading'>\1</h2>", html)
    html = re.sub(r'<h3>(.*?)</h3>', r"<h3 class='sub-sub-heading'>\1</h3>", html)

    # Adding class to paragraphs
    html = re.sub(r'<p>(.*?)</p>', r"<p class='blog-paragraph'>\1</p>", html)

    # Further customization can be added here

    return html

def markdown_to_html(markdown_text):
    # Convert Markdown to HTML
    html = markdown.markdown(markdown_text)
    
    # Add custom classes for styling
    html_with_classes = add_custom_classes(html)

    return html_with_classes

# Example Markdown text
markdown_text = """
##Lead Generation: It's Really About Sales

Struggling to get leads? Feel like no matter what you do, they just aren't coming in? You're not the only one. A lot of businesses have this problem. And here's a little secret: often, the trouble with getting leads is more about sales than marketing. Let's dive into why that is.

##When Marketing and Sales Don't Talk

**Different Goals**

A big reason why getting leads is tough is because marketing and sales teams don't always work together. Marketing tries to get leads, and sales tries to close deals. If they don't talk to each other, things get mixed up, and leads get lost.

##Leads That Don't Fit

Marketing can bring in lots of leads, but if they're not the right kind, they're not much use to sales. It's important for both teams to agree on what makes a good customer. This way, marketing brings in leads that sales can really use.

##Slow Follow-up

Sometimes, marketing does pass good leads to sales, but then nothing happens fast enough. If you don't reach out to a lead quickly, they might lose interest. This is where sales need to step up and make quick moves.

##How to Fix It: Get Marketing and Sales on the Same Page
**Shared Goals**

To fix the lead problem, marketing and sales need to have the same goals. When both teams know what they're working towards, they understand each other better and can work together more effectively.

**Talk to Each Other**

It's really important for marketing and sales to talk to each other. Regular meetings can help both sides understand what kind of leads are coming in and what the sales team needs.

**Score and Nurture Leads**

Using a system to score leads helps sales know which ones to focus on. Marketing can also help by keeping leads interested until they're ready to buy.

The Personal Touch in Getting Leads
Know What Your Customers Need

To get good leads, you need to really understand what your customers are looking for. What problems do they have? What do they need help with? If you can answer these questions, your lead efforts will be more successful.

**Build Real Relationships**

People buy from people they like and trust. So, it's important to build real relationships with your leads. Show them you care about their problems, not just about selling something. When leads feel valued, they're more likely to become customers.

##Finalizing
Getting leads isn't just about collecting contact info. It's about understanding your customers, guiding them, and helping them with their problems. By getting marketing and sales to work together, focusing on the right leads, and adding a personal touch, you can turn lead generation from a problem into a success.

Remember, it's not just about making a sale. It's about building a relationship that's good for both you and your customer. Let's work together to fix the lead generation problem and help your business grow.
"""

# Convert and print HTML
html_content = markdown_to_html(markdown_text)
print(html_content)
