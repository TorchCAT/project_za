# projectza

Converts text to speech using the synchronous Yandex SpeechKit API.

### How to run:
Create a Yandex service account with `ai.speechkit-stt.user` role.

Get a service account key pair and save the private part to  `private.pem`.

Fill in the `.env.` file with your folder and account ids.

Start with `docker-compose up`

### TODO:
- [ ] add authorization
- [ ] support concurrent user requests
- [x] add frontend
