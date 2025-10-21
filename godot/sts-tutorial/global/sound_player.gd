extends Node


func play(audio: AudioStream, single=false):
	if not audio:
		return
	
	if single:
		stop()
	
	for player in get_children():
		player = player as AudioStreamPlayer
		
		if not player.playing:
			player.stream = audio
			player.play()
			break


func stop():
	for player in get_children():
		player = player as AudioStreamPlayer
		player.stop()
