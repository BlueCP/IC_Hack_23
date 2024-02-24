# IC_Hack_23

The source code for our team's submission to IC Hack 23. A web app that can scan an image of a product, identify brand logos, and look up the brands in a database to return 'ethics scores'. The aim is to help consumers make more conscientious decisions when shopping. Uses Flask for the backend, Keras for computer vision (brand logo recognition), and other libraries such as Pandas and Beautiful Soup for web scraping to generate ethics scores.


## Getting the static data



Three data sources:

* Data source 1:
  * https://www.worldbenchmarkingalliance.org/publication/chrb/rankings/type/ungp/industry-apparel/
  * Webscrape the above data (also click onto each site and record the scores in the different metric such as "remedies and griance mechanisms"), e.g. https://www.worldbenchmarkingalliance.org/publication/chrb/2020/companies/tesco-2/
* Data source 2:
  * https://drive.google.com/file/d/1Nc75LmR2oKUsIwvP5ycG6ZbpPvuowJDR/view
  * Put this above in a CSV
  * Find a way of aggregating this to produce a transparency score
* Data source 3:
  * https://www.cdp.net/en/responses?queries%5Bname%5D=nestle
  * Does a dynamic search on this website based on input brand name
  * Looks up the climate change report and returns the letter score


## Running the code

Run the following script to download the weights for the brand logo recogniser `brand_recogniser_model/build/build.sh`.

Install necessary python modules (or use `pip`):
```
conda install matplotlib keras=2.2.4 pillow scikit-learn
conda install tensorflow-gpu
conda install opencv=3.4.4`
```
