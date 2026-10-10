# Google Drive archive

Every finished package goes to Google Drive, in
**Development (Vibe Code) / martinmotlik.com web / Insights**
(folder id `1_ymTfOKEwWlDeFK7waE6PIfGGKbs88II`). Git keeps the sources;
Drive keeps the finished deliverables in one place to share and reuse.

## Layout

```
Insights/
  01 ai-visibility-for-aec · Be the source/
    1 Article/     Article EN (Google Doc), hero original, OG image
    2 Podcast/     EP NN Transcript (Google Doc), episode MP3, cover 3000 px, .vtt, chapters .json
    3 Social/      Social posts (Google Doc)
    4 Instagram/   story MP4(s)
```

Folder name: `<NN> <slug> · <short name>`, NN = episode number, two digits.
Record the folder URL, its id and the four subfolder ids in
`_insights/<slug>/package.json` → `drive` the moment you create them.

## Procedure

1. **Folders**: Google Drive connector, `create_file` with
   `contentMimeType: application/vnd.google-apps.folder` and `parentId`
   (Insights folder, then the package folder).
2. **Text → Google Docs** through the connector: `create_file` with
   `textContent`, `contentMimeType: text/markdown` (converted to a Doc):
   - `1 Article/Article EN · <title>`: `python3 tools/insights/export-article.py insights/<slug>/index.html`
     (add the CS/DE URLs and the publish date under the source line)
   - `2 Podcast/EP NN Transcript · <short name>`: the transcript from
     `podcast/episodes/`, with the listen links and the disclosure on top
   - `3 Social/Social posts · <short name> (EP NN)`: `_insights/<slug>/social.md`
   Read one back with `read_file_content` to confirm the conversion.
3. **Binary files** (hero, OG image, MP3, cover, VTT, chapters, story
   MP4s): `python3 tools/insights/drive-stage.py <slug>`. It stages them in
   `Sources/exports/drive/<folder>/`, uploads them with **rclone**
   (`rclone copy --checksum`, so a rerun only sends what changed) and records
   every file with its link in `package.json` → `drive.uploaded`. The
   connector cannot carry files this size (it sends the whole file inside one
   request); never base64 a large file into a tool call.
4. **Verify**: the script lists what is on Drive after the upload; for the
   Docs use `search_files` (`parentId = '<subfolder id>'`) and record them
   in `drive.uploaded` as `"<subfolder>/<title>": "<url>"`.
5. `python3 tools/insights/check-package.py <slug>`: the Drive group is all ✓.
6. Put the Drive link in the package README and commit.

Never overwrite or delete anything on Drive without asking. When a
deliverable changes after archiving (e.g. a new teaser), upload the new file
next to the old one with a clear name and tell the user.

## rclone

- Binary: `~/.local/bin/rclone` (official build from downloads.rclone.org,
  checksum verified). Remote **`gdrive`**, `scope = drive`,
  `root_folder_id` = the Insights folder, so `gdrive:` *is* Insights and
  rclone cannot touch anything outside it. Config with the OAuth token:
  `~/.config/rclone/rclone.conf` (mode 600, never in git, never printed).
- Useful: `rclone lsf -R "gdrive:<folder>"`, `rclone size "gdrive:<folder>"`.
  Add `--log-level ERROR` to hide notices.
- If the remote is missing or the token expired: `rclone config reconnect gdrive:`
  (or create it again with
  `rclone config create gdrive drive scope=drive root_folder_id=1_ymTfOKEwWlDeFK7waE6PIfGGKbs88II`).
  It opens Google sign-in in the browser: the **user** signs in and allows
  access. The command echoes the token; delete any log that captured it.
- **To do**: the remote uses rclone's shared Google client ID, which Google
  retires during 2026. Before it stops, the user creates their own OAuth
  client (Google Cloud Console → APIs & Services → Credentials → OAuth
  client ID, type Desktop app, Drive API enabled) and we set it with
  `rclone config update gdrive client_id=… client_secret=…` +
  `rclone config reconnect gdrive:`. See
  https://rclone.org/drive/#making-your-own-client-id.
- Fallbacks when rclone is unavailable: Google Drive for desktop (the script
  copies into `~/Library/CloudStorage/GoogleDrive-*/My Drive/…`), or the user
  drags the staged files into the Drive folder.
