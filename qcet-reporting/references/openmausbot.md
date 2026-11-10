# OpenMausBot import compatibility

Verified against OpenMausBot main branch inspection in the previous qcet-work-planning build (2026-11-09). Recheck on new releases.

- App Bot Settings -> Skills accepts GitHub repository/folder/SKILL.md or skills.sh URL, not a local ZIP in the GitHub source box.
- Imported skills are initially disabled for user review. Review SKILL.md and attached files, then enable.
- GitHub import fetches supporting files from the same skill folder, subject to limits. Push the `qcet-reporting/` folder as a directory into a repository you control, then provide its URL.
- Avoid committing operational school data. The sample report is entirely synthetic.
- Skill text is guidance, not an automatic permission gate. Use bot approval mode Ask and restrict computer/connector permissions separately. Connected services are not assumed available.
- Windows native skills are possible through the chosen Claude/Codex agent's configured local directories, but exact discovery depends on OpenMausBot runtime configuration.

Core project references:
- https://github.com/milind-soni/OpenMausBot/blob/main/server/routes/bot-skills.ts
- https://github.com/milind-soni/OpenMausBot/blob/main/server/skill-folder.ts
- https://github.com/milind-soni/OpenMausBot/blob/main/src/components/bot-settings/SkillsSection.tsx
- https://github.com/milind-soni/OpenMausBot/blob/main/docs/headless-cli.md
