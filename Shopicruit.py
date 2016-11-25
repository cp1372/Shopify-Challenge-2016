'''
Getting shit done requires solid time management, so you’ve decided you need to
stock up on clocks and watches. You head to your favourite
Shopify store ‘Shopicruit’,which sells all kinds of wacky products.
Write a program that calculates how much it will cost you to buy all the
clocks and watches in the store. Attach your answer (in dollars),
as well as your program (any language) below. You can find the endpoint for
Shopicruit's products at: shopicruit.myshopify.com/products.json?page=1
(Keep in mind there are multiple pages of results).
'''
import sys
import urllib.request
import json

taxableSubtotal, untaxableSubtotal = 0, 0
variantCount, productCount = 0, 0
PST, GST  = 0.08, 0.05

pageCount = 1
pageSafetyThreshold = 50;

while (pageCount <= pageSafetyThreshold):
	URL = 'http://shopicruit.myshopify.com/products.json?page='
	URL += str(pageCount)
	
	#Get JSON data from a Shopicruit product page
	try:
		results = urllib.request.urlopen(URL).read().decode('UTF-8')
		productData = json.loads(results)
		
	except BaseException as e:
		print("Error: {}".format(str(e)))
		exit(1)
		
	products = productData["products"]	
	#Products will be a null list when we are past the last valid page
	if (products == []):
		print ("Final product page:", pageCount-1)
		break
		
	#Compute the price of buying 1 of each product and its variants on the product page
	for product in products:
		if (product["product_type"] == "Clock") or (product["product_type"] == "Watch"):
			productCount += 1
			#Products can have variants with different prices
			for item in product["variants"]:
				variantCount += 1
				
				if (item["taxable"] == True):
					taxableSubtotal += float( item["price"] )
				else:
					untaxableSubtotal += float( item["price"] )
	pageCount += 1

cost = untaxableSubtotal + taxableSubtotal*(1+PST+GST)

print("Number of Products:", productCount)
print("Number of Variants:", variantCount)
print("Total cost of all clocks and watches: ${:.2f}".format(cost))
print("Shipping and handling not included. Ontario tax rate applied.")
