import ControlPanel

def main():
	CP=ControlPanel.ControlPanel(source="http://feeds.reuters.com/news/artsculture")
	CP.jobOn()

if __name__=="__main__":
	main()