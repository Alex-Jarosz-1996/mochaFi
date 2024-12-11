# Frontend Dockerfile
FROM node:16

WORKDIR /app
COPY package.json package.json
COPY package-lock.json package-lock.json

# Install dependencies using npm
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Start the React app
CMD ["npm", "start"]
