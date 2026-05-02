function extractContent() {
    // Try to find the main article content first using common class names
    let mainContent = document.querySelector('article') || 
                      document.querySelector('.article-content') ||
                      document.querySelector('.entry-content') || 
                      document.querySelector('main') ||
                      document.querySelector('#content');
    
    let text = "";
    if (mainContent) {
        text = mainContent.innerText;
    } else {
        // Fallback: Get all text from paragraphs
        text = Array.from(document.querySelectorAll('p'))
            .map(p => p.innerText)
            .filter(t => t.length > 20)
            .join(' ');
    }

    // If still too short, take the whole body text
    if (text.length < 200) {
        text = document.body.innerText;
    }

    // Clean up whitespace and limit length to avoid overwhelming the model
    return text.replace(/\s+/g, ' ').trim().substring(0, 6000);
}

// Listen for messages from popup.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "extract_text") {
        const extractedText = extractContent();
        sendResponse({ text: extractedText });
    }
    return true; // Keep connection open for async response
});
