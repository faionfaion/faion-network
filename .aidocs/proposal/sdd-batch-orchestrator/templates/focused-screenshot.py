"""Element-focused screenshot with CSS outline injection.

Locates an element by text-content regex, walks up to the nearest meaningful
container, injects a coloured outline, scrolls it into view, and clips the
screenshot to the element's neighbourhood (~220 px above and below).

Inputs:
    html_path          absolute file system path to the rendered HTML
    find_text_regex    regex matched against text nodes
    container_selector comma-separated CSS tag list to walk up to
    outline_color      e.g. "#d50000" (before) or "#1b8a3a" (after)
    output_path        where to write the PNG

Output: PNG file at output_path. Width 1400 px, height auto, capped near 1500 px.
"""

from playwright.sync_api import sync_playwright


def screenshot_focused(html_path, find_text_regex, container_selector,
                       outline_color, output_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1400, "height": 900})
        page = ctx.new_page()
        page.goto(f"file://{html_path}", timeout=60000)
        page.add_style_tag(content=f"""
          .__bug_highlight {{
            outline: 6px solid {outline_color} !important;
            outline-offset: -3px;
            box-shadow: 0 0 16px {outline_color}80 !important;
            background: {outline_color}10 !important;
          }}
        """)
        bbox = page.evaluate("""
            ({findText, containerSelector}) => {
              const re = new RegExp(findText);
              const walker = document.createTreeWalker(
                document.body, NodeFilter.SHOW_TEXT);
              let node;
              while (node = walker.nextNode()) {
                if (re.test(node.textContent)) {
                  let el = node.parentElement;
                  const tags = containerSelector.split(',')
                    .map(s => s.trim().toLowerCase());
                  while (el && el !== document.body) {
                    if (tags.some(t => el.matches(t))) break;
                    el = el.parentElement;
                  }
                  if (el && el !== document.body) {
                    el.classList.add('__bug_highlight');
                    el.scrollIntoView({block: 'center'});
                    const r = el.getBoundingClientRect();
                    return {x: r.left, y: r.top,
                            width: r.width, height: r.height,
                            scrollY: window.scrollY};
                  }
                }
              }
              return null;
            }
        """, {"findText": find_text_regex,
              "containerSelector": container_selector})

        if not bbox:
            page.screenshot(path=output_path, full_page=False)
        else:
            doc_height = page.evaluate("document.body.scrollHeight")
            scroll_y = bbox["scrollY"]
            abs_y = bbox["y"] + scroll_y
            clip_y = max(0, abs_y - 220)
            clip_h = min(doc_height - clip_y, bbox["height"] + 440)
            clip_h = max(clip_h, 600)
            page.screenshot(path=output_path, full_page=True,
                            clip={"x": 0, "y": clip_y,
                                  "width": 1400, "height": clip_h})
        browser.close()
