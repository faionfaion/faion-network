---
name: javascript-first-project
description: Create index.html and app.js, open the page in a browser, read console.log output in DevTools, and change the DOM with a button click.
tier: free
group: dev-fundamentals
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working `index.html` + `app.js` project that runs in your browser, shows a log message in the DevTools Console tab, and changes the page heading when you click a button — no build tools, no Node.js required.

## Prerequisites

- A text editor (VS Code from https://code.visualstudio.com is recommended, but Notepad works too).
- Any modern browser (Chrome, Firefox, Edge, or Safari — version from 2020 or later).
- No prior JavaScript knowledge required.

## Steps

1. Create a project folder on your machine:

   ```bash
   mkdir ~/projects/my-first-js
   ```

   If you are on Windows and prefer not to use a terminal, create the folder in Explorer: right-click the Desktop → "New → Folder" → name it `my-first-js`.

2. Inside that folder, create a file named `index.html` and save the following content:

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
     <meta charset="UTF-8">
     <title>My First JS Project</title>
   </head>
   <body>
     <h1 id="heading">Hello from HTML</h1>
     <button id="change-btn">Change heading</button>
     <script src="app.js"></script>
   </body>
   </html>
   ```

3. In the same folder, create a second file named `app.js` and save the following content:

   ```javascript
   console.log('app.js loaded successfully');

   const heading = document.getElementById('heading');
   const button = document.getElementById('change-btn');

   button.addEventListener('click', function () {
     heading.textContent = 'JavaScript changed this!';
     console.log('Button clicked — heading updated');
   });
   ```

4. Open the project in your browser by double-clicking `index.html` in your file manager. The URL field will show something like `file:///Users/yourname/projects/my-first-js/index.html`.

5. Open the browser DevTools Console:
   - **Chrome / Edge:** Press `F12` (Windows/Linux) or `Cmd+Option+J` (macOS).
   - **Firefox:** Press `F12` or `Cmd+Option+K` (macOS).
   - **Safari:** Enable Developer menu under Safari → Settings → Advanced → "Show features for web developers", then press `Cmd+Option+C`.

6. Confirm the console shows `app.js loaded successfully` — this means the browser loaded your script.

7. Click the "Change heading" button on the page. The heading text changes to `JavaScript changed this!` and a second log line appears in the Console.

## Verify

With the page open, run the following check in the DevTools Console (click the Console tab and type this, then press Enter):

```javascript
document.getElementById('heading').textContent
```

Expected output after clicking the button:

```
'JavaScript changed this!'
```

If the return value is `'Hello from HTML'` instead, the button was not yet clicked — click it, then re-run the command.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Console shows `Cannot read properties of null (reading 'addEventListener')` | `app.js` is loaded before the DOM elements exist — the `<script>` tag is in `<head>` instead of just before `</body>` | Move `<script src="app.js"></script>` to the bottom of `<body>`, just before `</body>` |
| Console shows no output at all | The browser cached an old version of `app.js` | Press `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (macOS) to hard-reload without cache |
| Page shows the HTML source as plain text, not a rendered page | The file was opened as a text file, not as an HTML page | Open the file manager, right-click `index.html` → "Open with" → choose your browser |
| `app.js` returns 404 in the Network tab | The file name is wrong or in a different folder | Verify both files are in the same folder; check for typos in `<script src="app.js">` |
| Heading does not change on click but no error appears | `id` attribute in HTML does not match `getElementById` argument in JS | Ensure the button has `id="change-btn"` and the heading has `id="heading"` — IDs are case-sensitive |

## Next

- [vscode-first-project-setup](../../tech-setup/vscode-first-project-setup) — configure VS Code with syntax highlighting, auto-format, and the Live Server extension so you stop manually refreshing the browser.
- [deploy-static-site-github-pages](../../hosting-infra/deploy-static-site-github-pages) — push your `index.html` + `app.js` to GitHub Pages and share a real URL with others.
- [javascript-add-fetch-api](../javascript-add-fetch-api) — extend this project to load data from a public API and render it on the page.

## References

- [knowledge/free/dev/javascript-developer/javascript-modern](../../../knowledge/free/dev/javascript-developer/javascript-modern) — the `javascript-modern` methodology's code-placement rule (browser ES2022+, no build step) directly informs Steps 2–3: plain `.js` file with `addEventListener`, no TypeScript or bundler, matching the methodology's "bootstrapping any browser project" entry condition.
