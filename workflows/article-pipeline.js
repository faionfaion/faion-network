// article-pipeline — universal longform article production workflow.
// Content only: agents write and edit article files, never code; the only
// shell it runs are the validation commands supplied via args.gates.
//
// args contract (all paths relative to the session cwd unless absolute):
//   brief      REQUIRED  path to the editorial brief / seed file
//   article    REQUIRED  target path of the finished source-language article
//   workdir    REQUIRED  scratch dir for section drafts and per-lang files
//   languages  optional  target language codes, e.g. ["uk","pl"]; default []
//   rulesDir   optional  dir with per-language rule files <code>.md
//   styleGuide optional  path to the project style guide
//   glossaryDir optional dir of existing glossary term files (dedup source)
//   gates      optional  shell command templates; {file} {lang} {article_dir}
//                        are substituted per run. Empty = no gate stage.
//   prompts    optional  per-stage override files layered on top of the
//                        universal role prompts: {outline, write, review,
//                        translate, langReview}
//   maxFixRounds optional gate-fix iterations per file (default 2)

export const meta = {
  name: 'article-pipeline',
  description: 'Longform article production: outline → sectioned draft → editor review → quality gates → per-language translation, review and gates. Content only — never touches code.',
  whenToUse: 'Writing or translating a longform article/guide from an editorial brief; multilingual content production. Not for code, docs-in-repo, or build/deploy work.',
  phases: [
    { title: 'Outline', detail: 'brief → sectioned outline (JSON)' },
    { title: 'Write', detail: 'parallel section drafts → assembled article' },
    { title: 'Review', detail: 'editor pass in place' },
    { title: 'Gates', detail: 'validation commands → targeted fixes' },
    { title: 'Translate', detail: 'per-language translate → review → gates, no barriers' },
  ],
}

const A = args || {}
if (!A.brief || !A.article || !A.workdir) {
  throw new Error('article-pipeline requires args.brief, args.article, args.workdir')
}
const LANGS = A.languages || []
const FIX_ROUNDS = A.maxFixRounds ?? 2
const P = A.prompts || {}

const overlay = (stage) => P[stage]
  ? `\nAdditionally read and follow the project stage instructions at ${P[stage]} — they override these defaults where they conflict.`
  : ''
const styleRef = A.styleGuide ? `Read the style guide at ${A.styleGuide} first and follow it.` : ''
const CONTENT_ONLY = 'Hard boundary: you write and edit ARTICLE FILES only. Never modify code, configs, or anything outside the article/workdir paths given; never run build, deploy, or git commands.'

const OUTLINE_SCHEMA = {
  type: 'object', required: ['title', 'description', 'sections'],
  properties: {
    title: { type: 'string' },
    description: { type: 'string', maxLength: 160 },
    sections: {
      type: 'array', minItems: 6, maxItems: 14,
      items: {
        type: 'object', required: ['n', 'heading', 'target_words', 'key_points'],
        properties: {
          n: { type: 'integer' }, heading: { type: 'string' },
          target_words: { type: 'integer' },
          key_points: { type: 'array', items: { type: 'string' } },
        },
      },
    },
  },
}

const GATE_SCHEMA = {
  type: 'object', required: ['clean', 'findings'],
  properties: {
    clean: { type: 'boolean' },
    findings: { type: 'array', items: { type: 'string' } },
  },
}

phase('Outline')
const outline = await agent(
  `You are an article outliner. Read the editorial brief at ${A.brief}. ${styleRef} ` +
  `Produce the outline as your structured output: a working title, a description of AT MOST 160 characters (hard cap — it ships as metadata), and 6-14 sections with heading, target word count and 2-5 key points each. ${CONTENT_ONLY}${overlay('outline')}`,
  { label: 'outline', schema: OUTLINE_SCHEMA },
)
if (!outline) throw new Error('outliner returned nothing')
log(`outline: ${outline.sections.length} sections — ${outline.title}`)

phase('Write')
await parallel(outline.sections.map((s) => () => agent(
  `You are a section writer for the article "${outline.title}". Write ONLY section ${s.n}: "${s.heading}" (~${s.target_words} words) covering: ${s.key_points.join('; ')}. ` +
  `Read the brief at ${A.brief} for grounding — never invent facts, numbers or sources absent from it. ${styleRef} ` +
  `Save to ${A.workdir}/section-${String(s.n).padStart(2, '0')}.md as ONE complete Write call — write the whole file in a single call, no incremental appends. Return one line: DONE section ${s.n}. ${CONTENT_ONLY}${overlay('write')}`,
  { label: `write:${s.n}`, phase: 'Write' },
)))
const assembled = await agent(
  `Assemble the article. Read every ${A.workdir}/section-NN.md in order plus the brief at ${A.brief}. ` +
  `Write the COMPLETE article to ${A.article} in one Write call: frontmatter (title: ${JSON.stringify(outline.title)}, description under 160 chars, any fields the brief's format requires), then the section bodies joined with proper heading levels. ` +
  `Before finishing, re-read the LAST 20 lines of ${A.article} and confirm no tool-wrapper artifacts, XML tags or truncation at the tail; fix if found. Return one line: DONE <total word count>. ${CONTENT_ONLY}`,
  { label: 'assemble', phase: 'Write' },
)
log(`assembled: ${assembled}`)

phase('Review')
await agent(
  `You are the editor. Review ${A.article} in place with the Edit tool: voice and flow, structure against the outline, factual claims traceable to the brief at ${A.brief} (delete or soften what is not), heading hierarchy, description still under 160 chars. ${styleRef} ` +
  `Make the edits yourself — do not produce a report. Return one line: DONE <number of edits>. ${CONTENT_ONLY}${overlay('review')}`,
  { label: 'review' },
)

const runGates = async (file, lang, label) => {
  if (!(A.gates || []).length) return { clean: true, findings: [] }
  const cmds = A.gates.map((g) => g
    .replaceAll('{file}', file)
    .replaceAll('{lang}', lang)
    .replaceAll('{article_dir}', file.slice(0, file.lastIndexOf('/'))))
  for (let round = 0; round <= FIX_ROUNDS; round++) {
    const res = await agent(
      `Run these validation commands with Bash, one by one, and parse their output:\n${cmds.join('\n')}\n` +
      `Report structured output: clean=true only if every command passed with zero findings; otherwise clean=false and findings as short "file:issue" strings. Do not fix anything yourself. ${CONTENT_ONLY}`,
      { label: `gate:${label}:r${round}`, phase: 'Gates', schema: GATE_SCHEMA },
    )
    if (!res || res.clean) return res || { clean: true, findings: [] }
    if (round === FIX_ROUNDS) return res
    await agent(
      `You are the quality-gate fixer for ${file}. Fix EXACTLY these findings with the Edit tool, changing article text only:\n- ${res.findings.join('\n- ')}\n` +
      `Return one line: DONE. ${CONTENT_ONLY}`,
      { label: `fix:${label}:r${round}`, phase: 'Gates' },
    )
  }
}

phase('Gates')
const enGate = await runGates(A.article, 'en', 'en')
log(`en gates: ${enGate.clean ? 'clean' : `${enGate.findings.length} findings left`}`)

phase('Translate')
const langFile = (code) => `${A.workdir}/${code}.mdx`
const perLang = await pipeline(
  LANGS,
  (code) => agent(
    `You are a translator into "${code}". Read the finished article at ${A.article}. Translate the FULL article into ${code} and save to ${langFile(code)}. Rules:\n` +
    `- Default: ONE complete Write call for the whole file. Exception for very long articles: a SMALL first Write (frontmatter + first section), then Edit-appends section by section until the tail matches the source's structure. Never stop mid-file either way.\n` +
    `- Frontmatter: translate title and description; description stays UNDER 160 characters even if a literal translation runs longer — compress, do not overflow.\n` +
    `- Copy every non-translatable frontmatter field (slugs, refs, lists, dates) VERBATIM — dropping or altering them is a defect.\n` +
    `- Translate meaning, not words; keep code blocks, product names and citations untouched.\n` +
    (A.rulesDir ? `- Read and apply the language rules at ${A.rulesDir}/${code}.md.\n` : '') +
    `Return one line: DONE ${code}. ${CONTENT_ONLY}${overlay('translate')}`,
    { label: `translate:${code}`, phase: 'Translate' },
  ),
  (_r, code) => agent(
    `You are the ${code} language reviewer. Compare ${langFile(code)} against the source ${A.article} and fix in place with Edit: mistranslations, calques and source-language interference, tone drift, broken frontmatter (missing verbatim fields, description over 160 chars), any tool-wrapper artifacts at the file tail. ` +
    (A.rulesDir ? `Apply the defect list at ${A.rulesDir}/${code}.md. ` : '') +
    `Make the edits yourself. Return one line: DONE ${code} <number of edits>. ${CONTENT_ONLY}${overlay('langReview')}`,
    { label: `langReview:${code}`, phase: 'Translate' },
  ),
  (_r, code) => runGates(langFile(code), code, code).then((g) => ({ code, gate: g })),
)

const langResults = perLang.filter(Boolean)
return {
  article: A.article,
  outline: { title: outline.title, sections: outline.sections.length },
  en_gate: enGate,
  languages: langResults.map((r) => ({
    code: r.code, file: langFile(r.code),
    clean: r.gate?.clean ?? null, findings: r.gate?.findings?.length ?? 0,
  })),
}
