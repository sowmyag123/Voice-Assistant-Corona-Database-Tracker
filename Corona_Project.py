import requests
import json
import pyttsx3
import speech_recognition as sr
import re

API_KEY="twuNoQWXK8vs"
PROJECT_TOKEN="tKObvN47XHA9"
RUN_TOKEN="t_pamckgu1AK"

class Data:
	def __init__(self, api_key, project_token):
		self.api_key = api_key
		self.project_token = project_token
		self.params = {
			"api_key": self.api_key
		}
		self.data = self.get_data()

	def get_data(self):
		response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params={"api_key":API_KEY})
		data = json.loads(response.text)
		return data

	def get_total_cases(self):
		data= self.data['total']

		for content in data:
			if content['name']=="Total Cases":
				return content['value']

	def get_total_deaths(self):
		data= self.data['total']

		for content in data:
			if content['name']=="Deaths\n(1.33%)":
				return content['value']

	def get_state_data(self,state):
		data=self.data["state"]

		for content in data:
			if content['name'].lower()== state.lower():
				return content

	def get_list_of_states(self):
		states = []
		for state in self.data['state']:
			states.append(state['name'].lower())

		return states

		


def speak(text):
	engine= pyttsx3.init()
	engine.say(text)
	engine.runAndWait()

def get_audio():
	r= sr.Recognizer()
	with sr.Microphone() as source:
		audio = r.listen(source)
		said = ""

		try:
			said = r.recognize_google(audio)
		except Exception as e:
			print("Exception", str(e))

	return said.lower()

def main():
	print("Start Program")
	data= Data(API_KEY,PROJECT_TOKEN)


	while True:
		print("Listening...")
		print("Select your options: a.Total number of cases b.Total number of deaths c.Statewise information")
		text = get_audio()
		print(text)
		
		if text.lower() == "a":
			print( "Total number cases in India: "+data.get_total_cases())
			return speak( "Total number cases in India: "+data.get_total_cases())
			break
		elif text.lower() == "b":
			print("Total number of deaths in India: "+data.get_total_deaths())
			return speak("Total number of deaths in India: "+data.get_total_deaths())
			break
		
		elif text.lower() == "c":
			speak("Which state information would you want to know")
			state = get_audio()
			print(data.get_state_data(state))
			return speak(data.get_state_data(state))
			break
		
		else :
			speak("Please tell the right alphabet option")
			break
		
			

main()
