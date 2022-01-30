FROM node:16-alpine AS builder
RUN apk add git
RUN git clone https://github.com/lycanru/za_record
WORKDIR /za_record
RUN yarn install --frozen-lockfile
# COPY . .
RUN npm run build
#RUN ./node_modules/next/dist/bin/next export
RUN npx next export

FROM python:3.8-slim-buster
WORKDIR /app
RUN mkdir uploads
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
COPY --from=builder /za_record/out ./pages
ENV FLASK_APP="main.py"
CMD ["flask", "run", "--host=0.0.0.0"]
