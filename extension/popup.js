document.addEventListener('DOMContentLoaded', () => {
    const currentTabBtn = document.getElementById('currentTabBtn');
    const combinedBtn = document.getElementById('combinedBtn');
    const resultsDiv = document.getElementById('results');
    const loader = document.getElementById('loader');

    const API_URL = "http://localhost:8000";

    async function getActiveTab() {
        return new Promise((resolve) => {
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                resolve(tabs[0]);
            });
        });
    }

    async function getAllTabs() {
        return new Promise((resolve) => {
            chrome.tabs.query({}, (tabs) => {
                const webTabs = tabs.filter(t => t.url.startsWith('http'));
                resolve(webTabs);
            });
        });
    }

    async function extractTextFromTab(tabId) {
        return new Promise((resolve) => {
            chrome.tabs.sendMessage(tabId, { action: "extract_text" }, (response) => {
                if (chrome.runtime.lastError || !response) {
                    resolve("");
                } else {
                    resolve(response.text);
                }
            });
        });
    }

    function displayResult(title, text) {
        resultsDiv.innerHTML = "";
        const item = document.createElement('div');
        item.className = 'summary-item';
        item.innerHTML = `
            <span class="summary-title">${title} <span class="badge">AI</span></span>
            <p class="summary-text">${text}</p>
        `;
        resultsDiv.appendChild(item);
    }

    function displayCombinedResults(data) {
        resultsDiv.innerHTML = "";
        
        // 1. Show individual summaries first
        data.individual_summaries.forEach((summary, index) => {
            const item = document.createElement('div');
            item.className = 'summary-item';
            item.style.borderLeft = "4px solid #3498db";
            item.innerHTML = `
                <span class="summary-title">Tab ${index + 1} Individual Summary</span>
                <p class="summary-text" style="font-size: 0.8rem; color: #666;">${summary}</p>
            `;
            resultsDiv.appendChild(item);
        });

        // 2. Show final combined summary
        const finalItem = document.createElement('div');
        finalItem.className = 'summary-item';
        finalItem.style.backgroundColor = "#e8f4fd";
        finalItem.style.border = "1px solid #3498db";
        finalItem.innerHTML = `
            <span class="summary-title" style="color: #2980b9;">FINAL COMBINED SUMMARY <span class="badge" style="background: #2980b9;">PRO</span></span>
            <p class="summary-text" style="font-weight: 500;">${data.combined_summary}</p>
        `;
        resultsDiv.appendChild(finalItem);
    }

    async function summarizeCurrent() {
        loader.style.display = "block";
        resultsDiv.innerHTML = "";
        currentTabBtn.disabled = true;
        combinedBtn.disabled = true;

        try {
            const tab = await getActiveTab();
            const text = await extractTextFromTab(tab.id);

            if (!text || text.length < 100) {
                resultsDiv.innerHTML = "<p>Current tab has no readable content. Please refresh the page.</p>";
                return;
            }

            const response = await fetch(`${API_URL}/summarize_single`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();
            displayResult("Current Tab Summary", data.summary);

        } catch (error) {
            resultsDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        } finally {
            loader.style.display = "none";
            currentTabBtn.disabled = false;
            combinedBtn.disabled = false;
        }
    }

    async function summarizeCombined() {
        loader.style.display = "block";
        resultsDiv.innerHTML = "";
        currentTabBtn.disabled = true;
        combinedBtn.disabled = true;

        try {
            const tabs = await getAllTabs();
            const texts = [];

            for (const tab of tabs) {
                const text = await extractTextFromTab(tab.id);
                if (text && text.length > 100) {
                    texts.push(text);
                }
            }

            if (texts.length === 0) {
                resultsDiv.innerHTML = "<p>No readable content found in any open tabs.</p>";
                return;
            }

            const response = await fetch(`${API_URL}/summarize_batch`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ texts: texts })
            });

            const data = await response.json();
            displayCombinedResults(data);

        } catch (error) {
            resultsDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        } finally {
            loader.style.display = "none";
            currentTabBtn.disabled = false;
            combinedBtn.disabled = false;
        }
    }

    currentTabBtn.addEventListener('click', summarizeCurrent);
    combinedBtn.addEventListener('click', summarizeCombined);
});
