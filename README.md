# Evidence360

Time and time again, we've heard that one must have evidence to back up their claims in a performance request. During performance review season, we've all seen and experienced the scramble to grab relevant evidence for everything we're trying to say, in hopes that it'll be good enough. Well... what if their was a tool that could help you with this?

Introducing... Evidence360 - an AI-powered tool to assist you with your performance review cycle! Evidence360 will automatically find relevant pieces of evidence for claims that you make such as "Bob is a great problem-solver". It'll scour through your company's Slack workspace and pick up threads that it deems relevant for this claim. These threads are filtered using the magic of AI! (see our Tech section below for more details on the technical side)

### Diving into the Tech

Behind the scenes we're using Modal to host/deploy our backend endpoints, Vercel to deploy our frontend with Next.js (React app), MongoDB to persist all of our data and Anthropic's Claude LLM to do the heavy-lifting of processing Slack messages and figuring out what's relevant! Check it out https://evidence360.vercel.app/

### Future Updates

In the future, we plan to expand the functionality to include other sources of evidence such as Notion, Google Docs, Linear, etc. (unfortunately, within the scope of the hackathon, we didn't have time to extend to these platforms).
