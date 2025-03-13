// Define an empty listener for proxy authentication
browser.webRequest.onAuthRequired.addListener(
  function (details) {
    // Credentials will be dynamically injected via Selenium
  },
  { urls: ["<all_urls>"] },
  ["blocking"]
);
