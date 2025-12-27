// Configuration file for API endpoints
// This file is built with environment variables during the build process

// Default configuration
const config = {
  // This will be replaced during the build process with the actual environment variable value
  API_BASE_URL: typeof process !== 'undefined' && process.env && process.env.REACT_APP_API_BASE_URL
    ? process.env.REACT_APP_API_BASE_URL
    : typeof process !== 'undefined' && process.env && process.env.API_BASE_URL
      ? process.env.API_BASE_URL
      : 'https://governor-it-q4-h1.onrender.com' // Default production URL
};

export default config;