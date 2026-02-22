# Idea to Backlog

AI-powered tool to transform product ideas into sprint-ready user stories with acceptance criteria and effort estimates.

## 🎯 Overview

Idea to Backlog uses AI (Google Gemini) to help you:
1. **Generate PRDs** from product ideas
2. **Break down features** into categorized, sequenced user stories
3. **Create detailed backlogs** with acceptance criteria and effort estimates

All in a simple markdown-based workflow - no UI, just edit files and run commands.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key (get one at https://makersuite.google.com/app/apikey)

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your API key:
```bash
export GEMINI_API_KEY='your-api-key-here'
```

To make it permanent, add to your shell profile (~/.zshrc or ~/.bashrc):
```bash
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### Workflow

#### Step 1: Create a new project
```bash
python3 scripts/cli.py new my-project
```
This creates `projects/my-project/idea.md` with a template to fill in.

#### Step 2: Edit `idea.md`
Fill in your product overview, business goals, target users, constraints, etc.

Example: `projects/spotify-for-kids/idea.md`

#### Step 3: Generate PRD
```bash
python3 scripts/cli.py prd projects/my-project

# Overwrite without being prompted:
python3 scripts/cli.py prd projects/my-project --force   # or -f
```
Review and edit `prd.md` as needed.

#### Step 4: Generate User Stories
```bash
python3 scripts/cli.py stories projects/my-project

# Overwrite without being prompted:
python3 scripts/cli.py stories projects/my-project --force   # or -f
```
Review `user_stories.md` - stories are categorized into:
- 🏗️ Architecture & Non-Functional
- 💻 Frontend
- ⚙️ Backend
- 🤖 ML (if applicable)

Stories are sequenced in build order.

#### Step 5: Generate Backlog
```bash
python3 scripts/cli.py backlog projects/my-project

# Overwrite without being prompted:
python3 scripts/cli.py backlog projects/my-project --force   # or -f
```
Review `backlog.md` with:
- Detailed acceptance criteria
- Effort estimates (Story Points)
- Risk factors
- Sprint plan

#### Step 6: Export to Google Sheets *(optional)*
```bash
# Creates a new spreadsheet automatically
python3 scripts/cli.py export projects/my-project

# Push into an existing spreadsheet
python3 scripts/cli.py export projects/my-project --sheet-id <spreadsheet-id>

# Create new sheet inside a specific Drive folder
python3 scripts/cli.py export projects/my-project --folder-id <folder-id>
```
See [Google Sheets Export Setup](#-google-sheets-export-setup) below for one-time credential setup.

#### Step 7: Check project status at any time
```bash
python3 scripts/cli.py status projects/my-project
```

#### Step 8: Sprint Planning
Use `backlog.md` or your Google Sheet for sprint planning!

## 📁 Project Structure

```
pm_planner/
├── projects/
│   └── my-project/
│       ├── idea.md           # Your input
│       ├── prd.md            # Generated PRD
│       ├── user_stories.md   # Generated stories
│       └── backlog.md        # Generated backlog
│
├── scripts/
│   ├── cli.py               # Main CLI
│   ├── generate_prd.py
│   ├── generate_stories.py
│   ├── generate_backlog.py
│   └── export_to_sheets.py  # Google Sheets export
│
├── prompts/
│   ├── prd_prompt.txt
│   ├── stories_prompt.txt
│   └── backlog_prompt.txt
│
└── templates/
    └── idea-template.md
```

## 💡 Example: Spotify for Kids

See `projects/spotify-for-kids/` for a complete example:
- Audio streaming platform for kids ages 5-10
- Age-appropriate content with parental controls
- Full PRD → Stories → Backlog workflow

## 🎯 Key Features

### ✅ Modular Workflow
- Enter at any stage (already have a PRD? Start from there)
- Review and edit at each checkpoint
- Human validation before proceeding

### ✅ Transparent Assumptions
- AI surfaces all assumptions it's making
- Flags risks and uncertainties
- Shows confidence levels for estimates

### ✅ Realistic Estimates
- Story points with day conversion (1 SP = 1 day by default)
- Breakdown by area (FE/BE/ML/DevOps %)
- Chain-of-thought reasoning shown
- Risk factors identified

### ✅ Smart Sequencing
- Stories ordered by technical dependencies
- Build order clearly marked
- Sprint plans suggested

## 🛠️ CLI Commands

```bash
# Create a new project
python3 scripts/cli.py new <project-name>

# Generate PRD from idea.md
python3 scripts/cli.py prd projects/<project-name>
python3 scripts/cli.py prd projects/<project-name> --force   # or -f  – overwrite without prompt

# Generate user stories from prd.md
python3 scripts/cli.py stories projects/<project-name>
python3 scripts/cli.py stories projects/<project-name> --force   # or -f

# Generate backlog from user_stories.md
python3 scripts/cli.py backlog projects/<project-name>
python3 scripts/cli.py backlog projects/<project-name> --force   # or -f

# Export backlog to Google Sheets
python3 scripts/cli.py export projects/<project-name>                                 # creates a new sheet
python3 scripts/cli.py export projects/<project-name> --sheet-id <spreadsheet-id>    # update existing sheet
python3 scripts/cli.py export projects/<project-name> --folder-id <folder-id>        # new sheet in specific Drive folder (ignored when --sheet-id is set)

# Check project status
python3 scripts/cli.py status projects/<project-name>
```

## � Google Sheets Export Setup

The `export` command parses `backlog.md` and writes a formatted table to Google Sheets.
Each story becomes one row with these columns:

| Column | Example |
|---|---|
| Build Order | 1 |
| Story ID | AN1 |
| Category | Architecture & Non-Functional Stories |
| Story Title | Cloud Infrastructure Setup (MVP) |
| Description | As a/an Engineering Team, I want to set up foundational cloud infrastructure, so that we have a scalable and reliable environment. |
| Effort (SP) | 8 |
| Complexity | Medium (3★) |
| Breakdown | DevOps: 90%, Backend: 10% |
| Dependencies | None |
| Acceptance Criteria | • Core AWS VPC is provisioned… |
| Status | Not Started |

### One-time credential setup

1. **Enable the API** – in [Google Cloud Console](https://console.cloud.google.com/) enable:
   - *Google Sheets API* (Drive API is **not** required)

2. **Create a Service Account**
   - IAM & Admin → Service Accounts → Create
   - Download the JSON key file (e.g. `service-account.json`)

3. **Share your spreadsheet** with the service account email  
   (looks like `name@project.iam.gserviceaccount.com`) as **Editor**.

4. **Set the env var** (add to `~/.zshrc` to make it permanent):
   ```bash
   export GOOGLE_SERVICE_ACCOUNT_FILE=/path/to/service-account.json
   ```
   *Alternatively*, place the file as `credentials.json` in the project root — it is auto-detected.

> ⚠️ Never commit `service-account.json` or `credentials.json` to version control.  
> Add both patterns to `.gitignore`.

## �🔧 Customization

### Adjust Team Calibration
Edit estimates in `backlog.md` based on your team's velocity.

Default: 1 SP = 1 day for mid-level engineer

### Modify Prompts
Edit files in `prompts/` to customize AI behavior:
- `prd_prompt.txt` - How PRDs are generated
- `stories_prompt.txt` - How stories are created
- `backlog_prompt.txt` - How estimates are made

## 📊 Output Format

### PRD includes:
- Problem statement
- Proposed solution
- Functional & non-functional requirements
- User flows
- Success metrics
- Assumptions & risks
- Dependencies

### User Stories include:
- Standard format: "As a [user], I want [goal], so that [benefit]"
- Categorized by technical area
- Sequenced in build order
- Dependencies identified

### Backlog includes:
- Specific acceptance criteria
- Effort estimates with reasoning
- Confidence levels
- Risk factors
- Sprint plan
- Team composition needed

## 🚀 Roadmap

- [ ] Team calibration config file
- [ ] Retrospective mode (actual vs estimated effort)
- [x] Export to Google Sheets
- [ ] Export to Jira/Linear
- [ ] Template library
- [ ] Dependency graph visualization

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! This is a prototype - lots of room for improvement.

---

**Built with ❤️ using Google Gemini 2.5 Flash**
