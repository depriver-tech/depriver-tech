"""Rebuild the searchable, notebook-style Git lesson. Requires reportlab."""
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'public/archive/git-the-practical-notebook.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
for name,file in [('Hand','PatrickHand-Regular.ttf'),('Body','Poppins-Regular.ttf'),('Bold','Poppins-SemiBold.ttf'),('Code','LiberationMono-Regular.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(ROOT/'studio/fonts'/file)))
INK='#152E56'; BLUE='#244E9A'; PAPER='#FBF7ED'; YELLOW='#F8DD72'
W,H=595.28,841.89
c=canvas.Canvas(str(OUT),pagesize=(W,H)); c.setTitle('Git: The Practical Notebook');c.setAuthor('depriver.tech');c.setSubject('A hands-on Git course, from first commit to team collaboration')
page=0;y=0
plain=[]

def para(text,size=11,font='Body',color=INK,gap=14):
    global y
    p=Paragraph(escape(text),ParagraphStyle('p',fontName=font,fontSize=size,leading=19,textColor=HexColor(color)))
    _,h=p.wrap(455,700)
    if y-h<82: raise ValueError(f'Page {page} overflow: {text[:35]} at {y}')
    p.drawOn(c,86,y-h);y-=h+gap;plain.append(text+'\n')

def head(text):
    global y
    para(text,22,'Hand',BLUE,8)

def code(text):
    global y
    lines=text.split('\n');h=18*len(lines)+24
    if y-h<82: raise ValueError(f'Code overflow page {page}')
    c.setFillColor(HexColor('#EFF3F8')); c.roundRect(80,y-h,462,h,7,fill=1,stroke=0)
    c.setFillColor(HexColor(INK));c.setFont('Code',9.3)
    for i,line in enumerate(lines):
        if pdfmetrics.stringWidth(line,'Code',9.3)>440: raise ValueError('Code too wide: '+line)
        c.drawString(92,y-19-i*18,line)
    y-=h+16;plain.append('```bash\n'+text+'\n```\n')

def note(text):
    global y
    p=Paragraph(escape(text),ParagraphStyle('n',fontName='Hand',fontSize=17,leading=21,textColor=HexColor(INK)))
    _,h=p.wrap(425,700)
    if y-h-24<74: raise ValueError(f'Note overflow {page}')
    c.setFillColor(HexColor('#FAEBA7'));c.roundRect(80,y-h-20,462,h+20,3,stroke=0,fill=1)
    p.drawOn(c,96,y-h-10);y-=h+38;plain.append('Note: '+text+'\n')

def new(title,subtitle,ref=''):
    global page,y
    if page:c.showPage()
    page+=1
    c.setFillColor(HexColor(PAPER));c.rect(0,0,W,H,fill=1,stroke=0)
    c.setStrokeColor(HexColor('#D4E1E9'));c.setLineWidth(.4)
    for line in range(102,760,22):c.line(34,line,W-30,line)
    c.setStrokeColor(HexColor('#DB8D89'));c.line(65,75,65,H-43);c.line(68,75,68,H-43)
    c.setFillColor(HexColor(INK));c.setFont('Code',9);c.drawString(85,H-40,'depriver.tech  /  FIELD NOTES');c.drawRightString(W-35,H-40,'GIT / 2026')
    c.setFillColor(HexColor(YELLOW));c.rect(83,H-113,min(440,pdfmetrics.stringWidth(title,'Hand',33)),9,fill=1,stroke=0)
    c.setFillColor(HexColor(INK));c.setFont('Hand',33);c.drawString(84,H-110,title)
    c.setFont('Body',9);c.drawString(85,H-135,subtitle)
    c.setFont('Code',8);c.drawString(85,43,'LEARN IT. TRY IT. KEEP THE NOTES.');c.drawRightString(W-35,43,f'{page:02}')
    if ref:
        c.setFont('Body',6.8);c.drawString(85,62,ref)
        if ref.startswith('git-scm.com'):c.linkURL('https://'+ref,(85,59,540,70),relative=0)
    c.bookmarkPage(f'p{page}');c.addOutlineEntry(title,f'p{page}',0)
    plain.append('\n# '+title+'\n'+subtitle+'\n');y=H-167

new('Git: the practical notebook','A complete practical course for beginners and everyday collaborators')
para('Keep your work. Understand your history. Build with others.',27,'Hand',gap=28)
para('A guided lesson in the confident notebook style: warm paper, blue ink, clear rules and highlights that help you remember.')
head('What you will learn')
para('Create a repository, make meaningful commits, work on branches, share through GitHub, resolve conflicts and recover from common mistakes.')
head('How to use this notebook')
para('Read one lesson, type the commands in a disposable practice folder, then answer the checkpoint. Commands use Bash: Linux, macOS or Git Bash on Windows. Replace YOUR-NAME and repository URLs with your own values.')
note('The handwriting is for learning. Commands stay in a precise monospace font so you can copy them safely.')
para('Edition 1.0  /  19 October 2026  /  By depriver.tech',10)
# A small branch sketch makes the cover feel like a real working notebook.
c.setStrokeColor(HexColor(BLUE));c.setLineWidth(1.7)
c.line(108,180,490,180);c.line(210,180,290,240);c.line(290,240,380,240);c.line(380,240,460,180)
for px,py in [(110,180),(210,180),(290,240),(380,240),(460,180)]:
    c.setFillColor(HexColor(PAPER));c.circle(px,py,5,fill=1,stroke=1)
c.setFillColor(HexColor(BLUE));c.setFont('Hand',18)
c.drawString(90,150,'start');c.drawString(286,261,'try an idea');c.drawString(420,150,'bring it back')


new('Your learning route','A course you can follow in short sessions')
for title,desc in [('01 / Build the foundation - pages 3-6','Understand Git, configure your identity, create a repository and read changes.'),('02 / Work with others - pages 7-10','Branches, remotes, a pull-request workflow and conflict resolution.'),('03 / Stay in control - pages 11-17','Ignore rules, undo choices, stashes, history tools, releases and advanced workflows.'),('04 / Put it into practice - pages 18-21','A complete exercise, answer checks, troubleshooting and command reference.'),('05 / Keep learning - page 22','Official references and a glossary you can return to.')]:
    head(title);para(desc)
note('Use a practice repository first. A clean git status is your checkpoint before merging, rebasing or switching tasks.')

new('01 / Think in snapshots','Understand what Git is protecting','git-scm.com/docs/gittutorial')
para('Git records versions of a project on your computer. A commit identifies a snapshot plus information such as its parent, author and message. You can inspect earlier work without keeping folders named final-final-v3.')
head('Four places to understand')
para('Working tree: the files you edit.\nStaging area: the exact changes selected for the next commit.\nLocal repository: the history stored in .git.\nRemote: another repository you exchange commits with.')
code('edit files  ->  git add  ->  git commit  ->  git push\nworking tree   staging      local history   remote')
para('A branch is a movable name pointing at a commit. HEAD normally refers to the branch you have checked out. A commit hash identifies a particular commit; branch names can move as you work.')
head('Git and GitHub')
para('Git is the version-control tool. GitHub is one hosting and collaboration service. Local commits work offline; sharing with a remote usually needs a connection and authentication.')
note('Checkpoint: saving a file is not committing it, and committing it is not uploading it.')

new('02 / Set up once','Install Git, then choose your commit identity','git-scm.com/docs/git-config')
para('Install Git using the instructions for your operating system at git-scm.com/install. On Windows, open Git Bash for this course. On macOS or Linux, open your terminal.')
code('git --version\ngit config --global user.name "Your Name"\ngit config --global user.email "you@example.com"\ngit config --global init.defaultBranch main\ngit config --get user.name\ngit config --get user.email')
para('Replace the example identity. Your name and email become part of future commits. If you use GitHub and prefer email privacy, use the exact no-reply address shown in your account settings.')
head('Project-specific identity')
para('Run the next command inside a repository to override the global email for that project. This does not change old commits.')
code('git config user.email "work@example.com"\ngit help commit')
note('Commit identity is not a login. HTTPS credentials or SSH keys authenticate you to your remote host.')

new('03 / Your first repository','Create a small notebook project','git-scm.com/docs/git-init')
code('mkdir git-notebook\ncd git-notebook\ngit init -b main\nprintf "# My Git notebook\\n" > README.md\ngit status\ngit add README.md\ngit diff --staged\ngit commit -m "Add notebook introduction"\ngit status')
para('Before git add, README.md is untracked. After git add, it is staged. After the commit, git status should report a clean working tree. The first commit is now your starting point.')
head('Make the second snapshot')
code('printf "\\nI am learning Git.\\n" >> README.md\ngit diff\ngit add README.md\ngit commit -m "Describe notebook purpose"\ngit log --oneline')
note('Expected result: two commits, newest first. Their hashes will differ from anyone else\'s example.')

new('04 / Read before you commit','See the exact change, then save one clear idea','git-scm.com/docs/git-diff')
code('git status --short\ngit diff\ngit diff --staged\ngit diff HEAD\ngit log --oneline --graph --decorate --all')
para('git diff compares working files with the staging area. --staged compares the staging area with the last commit. git diff HEAD shows tracked changes relative to the last commit. New untracked file content is not included until staged.')
head('Stage deliberately')
code('git add README.md\ngit add -p\ngit restore --staged README.md')
para('git add -p lets you choose individual change sections. Unstaging keeps the file edits. If you edit a file after staging it, add it again to include the latest content.')
head('Write useful messages')
para('Prefer "Fix broken guide download link" over "updates". Keep unrelated fixes in separate commits. Check for private keys, passwords and generated files before committing.')
note('Checkpoint: staged and unstaged changes can exist in the same file at the same time.')

new('05 / Branch without fear','Work on one idea without changing main','git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging')
code('git switch -c feature/checklist\nprintf "%s\\n" "- Review before committing" > checklist.md\ngit add checklist.md\ngit commit -m "Add review checklist"\ngit switch main\ngit merge feature/checklist\ngit branch -d feature/checklist')
para('The feature branch moves when you commit. Switching back to main restores its snapshot. Merging brings the feature history into the current branch. Use git branch to confirm the current branch before a merge.')
head('Two ordinary merge outcomes')
para('Fast-forward: main has no separate new work, so Git moves its pointer forward. A merge commit: both branches advanced, so Git joins the histories with a commit that has two parents.')
code('git log --oneline --graph --all\ngit branch')
note('A branch is cheap. Use clear names such as feature/docs-archive or fix/download-link.')

new('06 / Connect to a remote','Publish your local history or clone existing work','git-scm.com/docs/git-push')
para('Create an empty repository on your hosting service before connecting this existing project. Do not initialise it with a README for this exercise. Replace YOUR-NAME below.')
code('git remote add origin https://github.com/YOUR-NAME/git-notebook.git\ngit remote -v\ngit push -u origin main')
para('origin is a conventional remote name. -u records an upstream relationship so later git push and git pull know the usual destination for this branch. Follow your host\'s HTTPS credential-manager or SSH setup instructions; do not put tokens in a remote URL.')
head('Starting from an existing repository')
code('git clone https://github.com/YOUR-NAME/git-notebook.git\ncd git-notebook\ngit remote -v')
para('Clone creates a new folder containing the project and its history. Use clone instead of init when joining a repository that already exists.')
note('Never commit credentials. If authentication fails, check the remote URL, your account access and your host\'s credential setup.')

new('07 / A team workflow','Fetch, review, integrate, then share','git-scm.com/docs/git-fetch')
code('git switch main\ngit status\ngit fetch origin\ngit log --oneline main..origin/main\ngit pull --ff-only\ngit switch -c feature/lesson-notes')
para('Fetch updates your local view of the remote without merging into your working branch. origin/main is that last fetched view. Pull fetches and then integrates. --ff-only refuses to combine diverged histories automatically.')
head('Open a pull request')
para('Edit and test your files, stage only the intended changes, commit, then push the feature branch. On your host, open a pull request into main. Explain the problem, the change and how you tested it.')
code('git add README.md\ngit commit -m "Add lesson notes"\ngit push -u origin feature/lesson-notes')
para('Respond to feedback with additional commits. After the reviewed change is merged on the host, switch to main and run git pull --ff-only. A squash merge may leave a different commit history from a normal merge.')
note('A pull request is a hosting-service workflow. It is not a command built into Git.')

new('08 / Resolve a conflict','A conflict asks you to choose the right final content','git-scm.com/docs/git-merge')
para('When branches change the same lines differently, Git may pause the merge. Start from clean work so it is easier to recover. Read git status and open every file listed as unmerged.')
code('<<<<<<< HEAD\nTitle from your current branch\n=======\nTitle from the incoming branch\n>>>>>>> feature/lesson-notes')
para('Edit this region into the final text you want. Keep one version, combine them, or write a better version. Remove all marker lines, then test the result.')
code('git add README.md\ngit diff --staged\ngit merge --continue\ngit status')
head('Need to stop?')
code('git merge --abort')
para('Use --abort during an unresolved merge. For a rebase conflict, use git rebase --continue or git rebase --abort instead. Resolving a conflict is a content decision, not simply clicking "accept both".')

new('09 / Keep your repository clean','Ignore generated files and keep secrets out','git-scm.com/docs/gitignore')
para('Create .gitignore in the project root. These example patterns suit many web projects; adjust them to your stack.')
code('# .gitignore\nnode_modules/\ndist/\n.env\n.env.*\n!.env.example\n*.log\n.DS_Store')
para('Ignore rules affect untracked files. If .env was already tracked, adding it to .gitignore does not remove it from Git history.')
code('git rm --cached .env\ngit add .gitignore\ngit commit -m "Stop tracking local environment file"')
para('Run that removal only if .env is tracked. It keeps the local file while removing it from the next snapshot. If a secret was exposed, revoke or rotate it promptly; deleting the latest copy does not erase previous commits.')
note('For large applications and ZIP downloads, use release assets or object storage. Keep source and metadata in Git; use Git LFS only when it fits your hosting workflow.')

new('10 / Undo the right thing','Choose the scope before choosing the command','git-scm.com/docs/git-restore')
head('Unstage, but keep your edits')
code('git restore --staged README.md')
para('This changes the staging area, not the working copy. It is useful when you selected too much for a commit.')
head('Discard unstaged edits to one file')
code('git diff -- README.md\ngit restore -- README.md')
para('The second command replaces the working copy from the index by default. Unstaged edits are lost. Review or copy them elsewhere first if you might need them.')
head('Bring back a version from a commit')
code('git restore --source=COMMIT_HASH -- README.md\ngit diff -- README.md')
para('Replace COMMIT_HASH with an actual hash. This restores the working file from that snapshot; inspect it, then stage and commit if you want to keep it.')
note('restore changes file content or staging. revert records an inverse commit. reset can move the current branch. They solve different problems.')

new('11 / Repair committed work','Prefer a new correction when history is shared','git-scm.com/docs/git-revert')
head('Reverse an ordinary shared commit')
code('git status\ngit revert COMMIT_HASH\ngit push')
para('Use a clean working tree and a real commit hash. Revert records a new inverse change and preserves the original history. It can conflict; resolve and use git revert --continue, or git revert --abort. Reverting a merge needs special care with its mainline parent.')
head('Fix your latest unpushed commit')
code('git add README.md\ngit commit --amend --no-edit')
para('Amend replaces the latest commit with a new one, including staged changes. Omit --no-edit to revise the message. Do this only when rewriting that commit will not disrupt collaborators.')
head('Reset: know the difference')
para('--soft moves the branch while keeping staging and files. The default --mixed also resets staging but keeps working edits. --hard resets tracked files too and can destroy uncommitted work. Do not use it as a routine fix.')
note('Avoid force-pushing shared main. Rewriting published history needs an agreed team process.')

new('12 / Pause and recover','Use a stash for interruptions and reflog for lost pointers','git-scm.com/docs/git-stash')
code('git stash push -u -m "Draft lesson edits"\ngit stash list\ngit stash show -p "stash@{0}"\ngit stash apply "stash@{0}"')
para('-u includes untracked files, but not ignored files. apply restores the changes and keeps the stash entry. After checking the result, remove it with git stash drop "stash@{0}". Applying a stash can produce conflicts.')
head('Find a commit you lost track of')
code('git reflog\ngit show COMMIT_HASH\ngit branch rescue/lesson COMMIT_HASH')
para('Reflog records recent local reference movements. If the commit still exists, creating a branch gives it a lasting name. Reflog is local and entries expire; it is not a backup of every unsaved edit.')
note('For important unfinished work, a commit on a temporary branch is easier to explain and back up than a forgotten stash.')

new('13 / Read the project history','Find what changed and why','git-scm.com/docs/git-bisect')
code('git log --oneline --graph --decorate --all\ngit log -p -- README.md\ngit show COMMIT_HASH\ngit blame README.md\ngit log --grep="download" --oneline')
para('Log shows history; show inspects a commit; blame associates current lines with the last changes that touched them. Use blame to find context, not to assign fault.')
head('Find the first bad commit')
code('git bisect start\ngit bisect bad\ngit bisect good GOOD_COMMIT_HASH\n# Test the checked-out version, then mark it:\ngit bisect good\n# Or: git bisect bad\n# Repeat until Git identifies the change.\ngit bisect reset')
para('Begin with clean work, one known bad revision and one known good revision. Bisect tests intermediate history to narrow the search. Use git bisect skip if a revision cannot be tested.')
note('A reproducible test makes history useful. Record the symptom before starting your search.')

new('14 / Release a known version','Tag a commit so you can find the shipped code','git-scm.com/docs/git-tag')
code('git switch main\ngit pull --ff-only\n# Run your project checks first.\ngit tag -a v1.0.0 -m "First notebook release"\ngit push origin v1.0.0\ngit show v1.0.0')
para('An annotated tag gives a release a stable name and message. Pushing a branch does not automatically push all tags. Publish the specific tag you intend to release.')
head('Source versus download files')
para('The Git tag identifies source history. A hosting-service release can attach built applications or ZIP files. Record the version, target platform, changes and installation steps alongside those files.')
head('Make a source-only ZIP')
code('git archive --format=zip --output=source-v1.zip v1.0.0')
para('This exports tracked files from the tag. It does not include the .git history, ignored build files or a compiled application unless those files were tracked.')
note('For your Docs Archive, keep a title, version, file type, size and short description with every download.')

new('15 / Beyond the basics','Understand these tools before adding them to daily work','git-scm.com/docs/git-rebase')
head('Rebase a private feature branch')
code('git fetch origin\ngit switch feature/lesson-notes\ngit rebase origin/main')
para('Rebase replays your branch commits on a new base and creates new commit identities. Use it for your own unshared work unless your team has agreed otherwise. Conflicts pause the replay; stage resolutions and use git rebase --continue, or --abort.')
head('Copy one change')
code('git cherry-pick COMMIT_HASH')
para('Cherry-pick applies the selected commit\'s change to your current branch as a new commit. Confirm the destination branch and test it; copying a change can introduce dependencies or conflicts.')
head('Work on another branch in another folder')
code('git worktree add ../notebook-review main\ngit worktree list')
para('Worktrees share repository objects while keeping separate working directories. The branch must not already be checked out in another worktree. Remove a finished, clean worktree with git worktree remove ../notebook-review.')

new('16 / Practice lab: build it','A fresh local exercise; no GitHub account required')
para('Run these commands in a new parent directory. This lab creates its own folder and sets an example identity only inside it. Do not use an existing project folder.')
code('mkdir git-notebook-lab\ncd git-notebook-lab\ngit init -b main\ngit config user.name "Git Learner"\ngit config user.email "learner@example.invalid"\nprintf "# Git lab\\n" > README.md\ngit add README.md\ngit commit -m "Start Git lab"\ngit switch -c feature/notes\nprintf "One idea per commit.\\n" > notes.txt\ngit add notes.txt\ngit commit -m "Add commit reminder"\ngit switch main\ngit merge feature/notes\ngit log --oneline --graph --all')
head('What should you see?')
para('Two commits, a clean working tree and notes.txt on main. Because main did not diverge, this merge fast-forwards. Keep this folder for the next page.')
note('Extra task: edit notes.txt, stage it, then unstage it without losing the edit. Inspect status at every step; restore the edit before continuing.')

new('17 / Practice lab: resolve it','Create a deliberate conflict, then fix it')
code('git switch -c feature/title\nprintf "# Team notebook\\n" > README.md\ngit add README.md\ngit commit -m "Use team title"\ngit switch main\nprintf "# Personal notebook\\n" > README.md\ngit add README.md\ngit commit -m "Use personal title"\ngit merge feature/title')
para('Expected: a content conflict in README.md. Open it and inspect the markers. For this exercise, choose a combined title, then complete the merge:')
code('printf "# Shared Git notebook\\n" > README.md\ngit add README.md\ngit commit -m "Resolve notebook title"\ngit status\ngit log --oneline --graph --all')
head('Answer checks')
para('The final README contains the combined title, status is clean, and the graph shows a merge commit joining the two histories. Try git show HEAD to inspect it.')

new('18 / When something goes wrong','Read the message, then choose the smallest fix')
for title,desc in [('Not a Git repository','Check your current folder with pwd and ls -a. Use cd to enter the project. Do not initialise random parent folders to silence the message.'),('Nothing to commit','The files may be unchanged, ignored or outside this repository. Inspect git status --short and git check-ignore -v FILE.'),('Push rejected / non-fast-forward','Fetch and inspect remote changes. Integrate using your team\'s merge or rebase policy, test, then push. Do not blindly force-push.'),('Local changes would be overwritten','Commit, stash or deliberately discard those changes before switching or merging. Git is protecting your working files.'),('Detached HEAD','You checked out a commit rather than a branch. Keep new work with git switch -c rescue/my-work before leaving it.'),('An editor opened unexpectedly','Git may be asking for a commit message. Save and close the editor to continue, or cancel intentionally. Use -m for simple commit messages.')]:
    head(title);para(desc,10.5,gap=9)

new('19 / Your desk reference','The everyday loop: inspect, change, review, commit, share')
rows=[('Start','git init -b main  /  git clone URL'),('Inspect','git status  /  git diff  /  git diff --staged'),('Stage','git add FILE  /  git add -p'),('Save','git commit -m "Describe the change"'),('History','git log --oneline --graph --all'),('Branch','git switch -c feature/name'),('Combine','git switch main  /  git merge feature/name'),('Remote','git fetch origin  /  git pull --ff-only'),('Share','git push -u origin BRANCH'),('Unstage','git restore --staged FILE'),('Undo shared','git revert COMMIT_HASH'),('Pause','git stash push -u -m "Draft"'),('Recover','git reflog  /  git branch rescue HASH'),('Release','git tag -a v1.0.0 -m "Release"')]
for label,cmd in rows:
    para(label,14,'Hand',gap=0);para(cmd,8.5,'Code',gap=0)
note('Before pushing: correct branch, reviewed diff, no secrets, checks passed, clear commit message.')

new('20 / Keep this page nearby','Glossary, official references and next steps')
para('Repository: project history. Commit: a recorded snapshot. Index: staging area. Branch: a movable commit reference. HEAD: your current position. Remote: another repository. Upstream: the branch used for usual tracking. Conflict: a change Git needs you to resolve.',11)
head('Official references')
refs=[('Install and configuration','https://git-scm.com/install'),('Git tutorial','https://git-scm.com/docs/gittutorial'),('Branching and merging','https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging'),('Restore, revert and reset','https://git-scm.com/docs/git-restore'),('Remote workflow','https://git-scm.com/docs/git-fetch'),('Stash and recovery','https://git-scm.com/docs/git-reflog'),('Advanced workflow','https://git-scm.com/docs/git-rebase'),('Command reference','https://git-scm.com/docs')]
for label,url in refs:
    start=y;para(label,15,'Hand',gap=1);para(url,7.5,'Body',gap=6);c.linkURL(url,(82,y,544,start),relative=0)
para('Command documentation reviewed 19 October 2026. This practical course covers everyday Git plus selected advanced tools; it is not a replacement for the full command reference.',9)
note('Your next step: use a feature branch and a reviewed pull request for one real improvement.')
c.save()
(ROOT/'studio/git-notebook/lesson.md').write_text('\n'.join(plain))
print(f'{OUT}\n{page} pages')
