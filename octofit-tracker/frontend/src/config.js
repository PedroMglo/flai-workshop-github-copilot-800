// API Configuration
// Dynamically construct API URL based on environment (Codespaces or localhost)

function getAPIBaseURL() {
  const protocol = window.location.protocol;
  const hostname = window.location.hostname;
  
  if (hostname.includes('app.github.dev')) {
    // GitHub Codespaces: Replace port 3000 with port 8000 in hostname
    const apiHostname = hostname.replace('-3000.app.github.dev', '-8000.app.github.dev');
    return `${protocol}//${apiHostname}/api`;
  } else if (hostname === 'localhost' || hostname === '127.0.0.1') {
    // Localhost development
    return `${protocol}//localhost:8000/api`;
  } else {
    // Fallback
    return `${protocol}//${hostname}:8000/api`;
  }
}

const API_BASE_URL = getAPIBaseURL();
console.log('🔌 API Base URL configured:', API_BASE_URL);

export default API_BASE_URL;
