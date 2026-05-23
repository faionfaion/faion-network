<!-- purpose: Archetype-keyed annotation library covering 8 ARIA APG patterns -->
<!-- consumes: designer/dev request for an archetype -->
<!-- produces: ready-to-paste annotation snippet -->
<!-- depends-on: WCAG 2.2 + ARIA APG -->
<!-- token-budget-impact: ~1500 when loaded -->


# Annotation Snippet Library

## button
role: button
name: <imperative verb phrase, e.g. "Save changes">
states: default | hover | active | disabled
keyboard: Enter, Space → activate
focus_behaviour: visible 2px outline at >=3:1 contrast

## link
role: link
name: <destination noun phrase, e.g. "Pricing page">
states: default | visited | focus
keyboard: Enter → activate
focus_behaviour: underline + outline

## dialog
role: dialog (aria-modal=true)
name: <modal title>
states: open | closed
keyboard: Esc → close; Tab → trap; Shift+Tab → cycle back
focus_behaviour: focus first focusable on open; restore to trigger on close

## menu
role: menu (or menubar)
name: <menu purpose>
states: collapsed | expanded
keyboard: ArrowDown next item; ArrowUp previous; Esc close
focus_behaviour: roving tabindex on items

## tabs
role: tablist (children role=tab; panels role=tabpanel)
name: <tab group label>
states: selected | unselected
keyboard: ArrowRight/Left between tabs; Home/End first/last
focus_behaviour: manual activation (Space/Enter) OR automatic on focus

## combobox
role: combobox (with listbox)
name: <field purpose>
states: closed | open | filtering | has-selection
keyboard: ArrowDown opens; Enter selects; Esc closes & restores
focus_behaviour: aria-activedescendant on focused option

## form_field
role: textbox | spinbutton | switch | radio | etc
name: <field label>
states: empty | filled | error | disabled
keyboard: Tab next field
focus_behaviour: visible outline; aria-describedby for error/help text

## data_table
role: table (children rowgroup, row, columnheader, cell)
name: <table caption>
states: sortable | sorted-asc | sorted-desc
keyboard: ArrowKeys cell navigation (if interactive cells)
focus_behaviour: cell-by-cell focus; optional row activation
