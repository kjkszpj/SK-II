# SK-II
SIMPLE socket programming, for network project.

---
### todo
-   combine socket + pyaudio
-   control of audio
    -   relocation
    -   select
    -   play
    -   stop
-   other than audio
    -   user login
    -   share
-   ...
-   UI

### done
-   try socket
-   try pyaudio

###	scheme:
-   let's do a simple audio player
-	Should separate server and client when design & programming.

###	question
1.	return value of socket method?
-	socket.socket()		--->	new instance of socket(socket fd in LINUX)
-	socket.bind()		--->	?
-	socket.listen()		--->	?
-	socket.accept()		--->	new socket object and addr of client
-	socket.send(buff)	--->	?
-	socket.recv(bufsz)	--->	?
-	socket.close()		--->	?

2.	SOCK\_STREAM or SOCK\_PACKET
3.	backlog, what happen?
4.	time out issue, have it or implement it?

---

by Piji You

Mail: you.piji@gmail.com

---

### License
MIT License