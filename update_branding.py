# update_branding.py
# Run from D:\college_chatbot\: python update_branding.py
# Changes: Title -> AskCampus, Color -> Sky Blue

import os

# ── 1. Update CSS colors to Sky Blue ──────
css_path = 'frontend/static/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Light theme sky blue
css = css.replace('--accent:      #f97316;', '--accent:      #0ea5e9;')
css = css.replace('--accent2:     #ea580c;', '--accent2:     #0284c7;')
css = css.replace('rgba(249,115,22,0.15)',    'rgba(14,165,233,0.15)')
css = css.replace('linear-gradient(135deg,#f97316,#ea580c)', 'linear-gradient(135deg,#0ea5e9,#0284c7)')

# Dark theme sky blue
css = css.replace('--accent:      #fb923c;', '--accent:      #38bdf8;')
css = css.replace('--accent2:     #f97316;', '--accent2:     #0ea5e9;')
css = css.replace('rgba(249,115,22,0.2)',     'rgba(14,165,233,0.2)')

# Background sky blue tint
css = css.replace('--bg:          #f0f4ff;', '--bg:          #f0f9ff;')
css = css.replace('--surface2:    #f7f9ff;', '--surface2:    #f0f9ff;')
css = css.replace('--border:      #e2e8f8;', '--border:      #bae6fd;')

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)
print("CSS updated to sky blue!")

# ── 2. Update HTML title and branding ─────
html_path = 'frontend/templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('<title>College AI Assistant</title>', '<title>AskCampus - Excel Group Institutions</title>')
html = html.replace('College AI Assistant</h1>', 'AskCampus</h1>')
html = html.replace('>College AI Assistant<', '>AskCampus<')
html = html.replace("I'm your <strong>College AI Assistant</strong>", "I'm your <strong>AskCampus AI</strong>")
html = html.replace('College AI Assistant.', 'AskCampus AI.')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML updated to AskCampus!")

# ── 3. Update admin HTML ───────────────────
admin_path = 'frontend/templates/admin.html'
if os.path.exists(admin_path):
    with open(admin_path, 'r', encoding='utf-8') as f:
        admin = f.read()
    admin = admin.replace('<title>Admin Panel – College AI Assistant</title>', '<title>Admin Panel – AskCampus</title>')
    admin = admin.replace('College AI Assistant', 'AskCampus')
    # Sky blue colors in admin CSS too
    admin = admin.replace('#4361ee', '#0ea5e9')
    admin = admin.replace('#7b5ea7', '#0284c7')
    admin = admin.replace('rgba(67,97,238', 'rgba(14,165,233')
    with open(admin_path, 'w', encoding='utf-8') as f:
        f.write(admin)
    print("Admin HTML updated!")

print("\nAll done! Now run: python run.py")
print("Then Ctrl+Shift+R in browser")
