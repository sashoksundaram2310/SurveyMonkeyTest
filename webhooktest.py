import unittest
import requests
import json
from random import randint
import time

YOUR_ACCESS_TOKEN = "DBFO7wTXGJgnUjIVlznq.25b3UTEUBWh.S0McNpPp577NGubDa3vrNsF8EZn.mCj1fChydsP2p0DZYGY.Nzxg8Y9MPc3xLcDIZcB7-FiDUZoqcyXnKETOpfUBRA9nW34"

# this class contains all the web hook test cases
# NOTE:  everytime the test is run, we have to make the subscription_url unique
class TestWebhooks(unittest.TestCase):
	
	def setup_header(self):
		s = requests.Session()
		s.headers.update({
		  "Authorization": "Bearer %s" % YOUR_ACCESS_TOKEN,
		  "Content-Type": "application/json"
		})
		return s

	def setUp(self):
		print "--------------- Inside setup ---------------"
		time.sleep(3)
		global createdWebhookId
		s = self.setup_header()
		payload = {
		  "title": "Ashok Survey1" + str(randint(100, 999))
		}
		url = "https://api.surveymonkey.net/v3/surveys"
		r = s.post(url, json=payload)
		self.survey_id = json.loads(r.text)["id"]
		print "Survery created: " + self.survey_id

	def makeWebhookAndReturnResponse(self):
		print "------inside makeWebhookAndReturnResponse----------"
		s = self.setup_header()
		payload = {
		  	"name": "My Webhook" + str(randint(100, 999)),
		  	"event_type": "response_completed",
		  	"object_type": "survey",
		  	"object_ids": [str(self.survey_id)],#[self.survey_id],
		  	"subscription_url": "http://requestb.in/pw0jmppw"
		}
		url = "https://api.surveymonkey.net/v3/webhooks"
		# print "Before post"
		# print "url:\n"
		# print url
		# print "payload:\n"
		# print payload
		r = s.post(url, json=payload)
		response =  json.loads(r.text)
		# print response
		print "------after makeWebhookAndReturnResponse----------"
		return r
		
	# webhooks post call response assertions
	def test_create_webhook(self):
		print "test_01_create_webhook"
		r = self.makeWebhookAndReturnResponse()
		# print "After post"	
		# print "type of :" + str(type(r))
		print "response:\n"+ r.text
		# print "id" + r["id"]
		# self.createdEventType = json.loads(r.text)["event_type"]
		# print self.createdEventType
		# self.assertEquals("response_completed", self.createdEventType)
		# print "Asserted event type"
		# createdWebhookId =  json.loads(r.text)["id"]
		# print "Created webhook Id: " + createdWebhookId
		self.createdObjectId = json.loads(r.text)["object_ids"]
		# print self.createdObjectId
		self.assertEquals([self.survey_id], self.createdObjectId)
		print "Pass: Asserted object ids"
		self.createdEventType = json.loads(r.text)["event_type"]
		# print self.createdEventType
		self.assertEquals("response_completed", self.createdEventType)
		print "Pass: Asserted event type"
		# self.assertEquals(payload.subscription_url, r["subscription_url"])
		# print "Asserted subscrition_url"

	def test_02_list_of_webhooks(self):
		r = self.makeWebhookAndReturnResponse()
		createdWebhookId =  json.loads(r.text)["id"]
		s02 = self.setup_header()
		url = "https://api.surveymonkey.net/v3/webhooks"
		response = s02.get(url)
		dataArr = json.loads(response.text)["data"]
		# print dataArr
		ids=[]
		for element in dataArr:
			# print element
			kl = element["id"]
			ids.append(kl)
		# print "ids:\n"
		# print ids
		self.assertIn(createdWebhookId, ids)
		print "Pass: Asserted list of webhooks contain the created webhook"

		# lo = json.loads(ele)["total"]
		# print lo
		# self.assertEquals(lo,3)

	# def _02_status_check(self):
	# 	s = self.setup_header()
	# 	payload = {
	# 	  "name": "My Webhook",
	# 	  "event_type": "response_completed",
	# 	  "object_type": "survey",
	# 	  "object_ids": [self.survey_id],
	# 	  "subscription_url": "https://surveymonkey.com/webhooks"	
	# 	}
	# 	url = "https://api.surveymonkey.net/v3/surveys"
	# 	r = s.post(url, json=payload)
	# 	print r.text
	# 	print 'prem'
	# 	status_code = json.loads(r.text)["error"]["http_status_code"]
	# 	print status_code
	# 	self.assertEquals(status_code,"200")

	# def _03_list_of_webhooks(self):
	# 	s = self.setup_header()
	# 	url = "https://api.surveymonkey.net/v3/webhooks"
	# 	get_elements = s.get(url)
	# 	ele = get_elements.text
	# 	lo = json.loads(ele)["total"]
	# 	print lo
	# 	self.assertEquals(lo,3)

	def test_03_getwebhookid(self):
		# step1 create survey(setup)
		# step2 create webhook 
		r = self.makeWebhookAndReturnResponse()
		# step3 get created webhookid from the response of created webhook call
		createdWebhookId =  json.loads(r.text)["id"]
		createdWebhookName = json.loads(r.text)["name"]
		createdObjectId = json.loads(r.text)["object_ids"]
		s02 = self.setup_header()
		url = "https://api.surveymonkey.net/v3/webhooks/"+createdWebhookId
		callBack = s02.get(url)
		callBack_text = callBack.text
		print "callbacktext: \n"
		print callBack_text
		self.assertEquals(createdWebhookId, json.loads(callBack_text)["id"])
		print "pass: Asserted the created webhookid wih get/id response id"
		self.assertEquals(createdWebhookName, json.loads(callBack_text)["name"])
		print "pass: Asserted the created webhook name wih get/id response name"
		self.assertEquals(createdObjectId, json.loads(callBack_text)["object_ids"])
		print "pass: Asserted the created survey ID wih get/id response's Survey id"
	
	def test_06_putWebhook(self):
		# step1 create survey(setup)
		# step2 create webhook 
		r = self.makeWebhookAndReturnResponse()
		# step3 get created webhookid from the response of created webhook call
		createdWebhookId =  json.loads(r.text)["id"]
		createdWebhookName = json.loads(r.text)["name"]
		createdObjectId = json.loads(r.text)["object_ids"]
		s02 = self.setup_header()

		payload = {
		  	"name": "updatedName",
		  	"event_type": "response_completed",
		  	"object_type": "survey",
		  	"object_ids": [str(self.survey_id)],#[self.survey_id],
		  	"subscription_url": "http://requestb.in/1hldkrs1"
		  	# "subscription_url": "https://surveymonkey.com/webhook_reciever"
		}

		url = "https://api.surveymonkey.net/v3/webhooks/"+createdWebhookId

		r = s02.put(url, json=payload)
		response = json.loads(r.text)
		print response
		self.assertEquals("updatedName", json.loads(r.text)["name"])
		print "pass: Asserted the updated webhook name wih put/id response name"
		  	

	def test_head_webhookid(self):
		# step1 create survey(setup)
		# step2 create webhook 
		r = self.makeWebhookAndReturnResponse()
		# step3 get created webhookid from the response of created webhook call
		createdWebhookId =  json.loads(r.text)["id"]
		createdWebhookName = json.loads(r.text)["name"]
		createdObjectId = json.loads(r.text)["object_ids"]
		s02 = self.setup_header()
		url = "https://api.surveymonkey.net/v3/webhooks/"+createdWebhookId
		r = s02.head(url)
		# response = json.loads(r.text)
		# print r
		self.assertIn("204", str(r))
		print "Pass: Asserted response of head api call to be http 204"
		

	def test_delete(self):

		print "---------------Inside Delete ---------------"
		r = self.makeWebhookAndReturnResponse()
		s02 = self.setup_header()
		createdWebhookId =  json.loads(r.text)["id"]
		createdWebhookName = json.loads(r.text)["name"]
		# print "hi"
		print "Created webhook id: "+ createdWebhookId
		url = "https://api.surveymonkey.net/v3/webhooks/" + createdWebhookId
		# print url
		delete_response = s02.delete(url)
		# print delete_response.text
		self.assertEquals(createdWebhookId, json.loads(delete_response.text)["id"])
		print "asserted deleted WebhookId"
		self.assertEquals(createdWebhookName, json.loads(delete_response.text)["name"])
		print "asserted deleted WebhookName"


	

if __name__ == '__main__':
    unittest.main()		