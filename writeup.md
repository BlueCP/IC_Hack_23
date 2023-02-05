# Write-up

## Inspiration

It has become increasingly clear in recent years that people want to know how they can contribute to the global sustainability effort. One way of doing this is by leveraging the free market, buying from companies which have upheld their social responsibilities, and avoiding those that haven’t. However, it is time-consuming for the average consumer to conduct this research on their own, so we have developed a tool to help.

## What it does

Our web application scans a branded product, identifies the company, and displays information about that company’s social and environmental impact. We generate scores for a number of categories by matching those companies against datasets we have aggregated, as well as by scraping websites we consider to be reliable sources of information.

## Tools we used

- We decided to write the majority of this project in Python due to its ease of use and rich ecosystem.
- For coding the back-end web server, we used the Flask framework since it is lightweight and imposes a shallow learning curve, which was ideal for a proof-of-concept.
- For the front-end, we decided to program in bare HTML, CSS and Javascript. Although using a framework such as React or Node.js is usually recommended, the simplicity of our application at this stage (having just a single webpage) made this seem unnecessary.
- We used the Beautiful Soup package for Python to parse HTML webpages as part of the web scraping process.
- To recognise logos, we used a freely available logo detection API, which itself uses Keras, a high-level API for TensorFlow.


## How it works

We have a live video feed from the webcam where we periodically take a screenshot and asynchronously send this to a backend computer vision model which does object detection and matches the recognised objects against well-known corporate brands. The brand name is then fed to three different data extractors, one web scraping Wikipedia to lookg for controversies, transparencies, etc., another for checking a database with results from the [transparency index study](https://crni.ie/content/uploads/2020/04/FR_FashionTransparencyIndex2020.pdf), [human rights friendliness scores](https://www.worldbenchmarkingalliance.org/publication/chrb/rankings/type/ungp/industry-apparel/) (To be added to the project), and https://data.cdp.net/ . This data is then summarised in a report that is presented to the user.


## Challenges
1. Figure out a way to compute the controversy index of a brand (if a company has more and more "bad" keywords associated to it, the lower the controversy index).
2. Summarize controversies into 1 or 2 sentences highlighting the controversies of the brand.
3. Adapting the computer vision model to recognising brand logos


## Accomplishments
Build a web application from front end to back end gathering critical information about the brand while detecting the brand live on the camera.

## What's next

Although we decided to implement this idea as a web application rather than a mobile app since we thought it would be easier, a mobile app would be significantly better suited for this task. Consumers are more likely to check their purchases if it is convenient to do so. Since this tool was originally intended to be used by shoppers, a smartphone is the natural target platform.
