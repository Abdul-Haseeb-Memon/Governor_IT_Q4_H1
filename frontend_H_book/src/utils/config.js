// Configuration file for API endpoints
// This file is built with environment variables during the build process

// Default configuration
const config = {
  // In Docusaurus deployed to Vercel, the environment variables should be available during build
  // If not, fall back to the custom fields set in docusaurus.config.ts
  API_BASE_URL:
    // First check if build-time environment variable is available
    (typeof process !== 'undefined' && process.env && process.env.REACT_APP_API_BASE_URL)
    ? process.env.REACT_APP_API_BASE_URL
    // Then check for custom fields (runtime)
    : (typeof window !== 'undefined' && window.DOCUSAURUS_CUSTOM_FIELDS && window.DOCUSAURUS_CUSTOM_FIELDS.apiBaseUrl)
      ? window.DOCUSAURUS_CUSTOM_FIELDS.apiBaseUrl
      // Finally, fallback to default
      : 'https://governor-it-q4-h1.onrender.com' // Default production URL
};

export default config;