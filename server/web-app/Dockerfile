FROM node:alpine

WORKDIR /app
COPY . .

# Install deps 
RUN cd /app &&  npm install 

# Build 
RUN npm run build

ENTRYPOINT [ "npm", "run", "start" ]