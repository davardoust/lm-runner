<<<<<<< HEAD
# lm-runner



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/topics/git/add_files/#add-files-to-a-git-repository) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://cr.si24.ir/innovation-hub/idp/modules/lm-runner.git
git branch -M develop
git push -uf origin develop
```

## Integrate with your tools

- [ ] [Set up project integrations](https://cr.si24.ir/innovation-hub/idp/modules/lm-runner/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/user/project/merge_requests/auto_merge/)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
=======
# Medical Lab VLM Pipeline

A robust, production-grade Python pipeline for extracting structured data from Persian/English medical lab reports. This system uses **Ollama (DeepSeek-OCR/LLaVA)** for vision-language inference, **LangChain** for orchestration, and **Opik** for full-stack observability.





## 🚀 Key Features

*   **Multimodal Extraction**: Handles both header metadata (Persian/English names, dates) and complex tabulated test results (Hematology, Hormones).
*   **Prompt-Based Anchoring**: Uses semantic "visual anchors" to accurately locate Persian fields like National Code (`کد ملی`) and Patient Name (`نام بیمار`).
*   **Batch Processing**: Multi-threaded processing optimized for local GPUs.
*   **Resilient Architecture**:
    *   **Client-Side Parsing**: Bypasses server-side JSON limitations in smaller VLMs by handling parsing in Python.
    *   **Context Flushing**: Fixes common Ollama KV-cache corruption bugs in batch processing.
*   **Observability**: Integrated with **Opik (by Comet)** for tracking traces, latency, and inputs/outputs.

## 🛠️ Tech Stack

*   **Core**: Python 3.11+, Pydantic V2
*   **AI Engine**: [Ollama](https://ollama.com/) (running `deepseek-ocr` or `llama3.2-vision`)
*   **Orchestration**: LangChain, LCEL
*   **Observability**: Opik (Comet ML)
*   **Utilities**: Pillow, HTTPX, ThreadPoolExecutor

## 📂 Project Structure

```text
medical-lab-vlm-pipeline/
├── data/
│   ├── images/              # Input images (.jpg, .png)
│   └── prompts.json         # Configurable prompts for extraction
├── outputs/
│   ├── logs/                # Execution logs
│   ├── results/             # Structured JSON outputs per prompt ID
│   └── summary_report.csv   # Batch processing stats
├── src/
│   ├── agent_factory.py     # Ollama client with timeouts & parsing logic
│   ├── pipeline.py          # Main batch orchestrator & thread pool
│   ├── preprocessor.py      # Image resizing & base64 conversion
│   ├── logger.py            # Thread-safe logging setup
│   └── schemas.py           # Pydantic models for data validation
├── config.yaml              # Global configuration (model, timeouts, paths)
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
└── README.md
```

## ⚙️ Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/medical-lab-vlm-pipeline.git
    cd medical-lab-vlm-pipeline
    ```

2.  **Set up Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install & Serve Ollama**
    *   Download [Ollama](https://ollama.com/).
    *   Pull the vision model:
        ```bash
        ollama pull deepseek-ocr
        ```
    *   Start the server:
        ```bash
        ollama serve
        ```

## 🔧 Configuration

### 1. `config.yaml`
Control global settings like batch size (keep low for vision models) and timeouts.

```yaml
system:
  input_dir: "./data/images"
  output_dir: "./outputs"
  prompts_file: "./data/prompts.json"
  batch_size: 1               # Keep to 1-2 for local GPUs
  log_level: "INFO"

model:
  name: "deepseek-ocr"
  timeout: 300                # Seconds
  base_url: "http://localhost:11434"
```

### 2. Environment Variables (`.env`)
Create a `.env` file for your Opik observability keys (optional).

```env
# If using Cloud Opik
OPIK_API_KEY=your_key_here
OPIK_WORKSPACE=default
OPIK_PROJECT_NAME=medical-ocr-extraction

# If using Self-Hosted Opik (Local Docker)
# OPIK_URL_OVERRIDE=http://localhost:5173/api
```

## 🏃 Usage

**Run the pipeline:**
```bash
python main.py
```

The script will:
1.  Load images from `data/images`.
2.  Preprocess them (resize/convert).
3.  Send them to Ollama using the prompt strategies defined in `data/prompts.json`.
4.  Validate output against `src/schemas.py`.
5.  Save individual JSON results to `outputs/results/<prompt_id>/`.
6.  Generate a summary CSV in `outputs/`.

## 📊 Observability (Opik)

This project uses **Opik** to visualize execution traces.
*   **Cloud Dashboard**: Log in to [Comet Opik](https://www.comet.com/opik).
*   **Local Dashboard**: If running locally, visit `http://localhost:5173`.

You will see full traces including:
*   The exact prompt sent to the LLM.
*   The raw JSON string returned.
*   Validation errors (if any).
*   Latency metrics per image.

## 🐛 Troubleshooting

| Error | Solution |
| :--- | :--- |
| `Status Code 500` | Restart Ollama (`ollama serve`). The KV cache might be corrupted. |
| `SameBatch may not be specified...` | Update `src/agent_factory.py` to ensure `num_keep=0` is set in the model config. |
| `Validation Error` | Check `src/schemas.py`. Ensure field types (like `int` vs `str`) match the model's output capability. |
| `ConnectionRefused` | Ensure Ollama is running on port 11434. |

## 📜 License
MIT License. See `LICENSE` for details.

***

### **Citations**
*   **Ollama**: [https://ollama.com](https://ollama.com)
*   **LangChain**: [https://python.langchain.com](https://python.langchain.com)
*   **Opik**: [https://www.comet.com/opik](https://www.comet.com/opik)

[1](https://github.com/rochacbruno/python-project-template/blob/main/README.md)
[2](https://realpython.com/readme-python-project/)
[3](https://github.com/othneildrew/Best-README-Template)
[4](https://github.com/azavea/python-project-template/blob/master/README.md)
[5](https://www.makeareadme.com)
[6](https://github.com/allenai/python-package-template/blob/main/README.md)
[7](https://github.com/catiaspsilva/README-template)
[8](https://www.youtube.com/watch?v=12trn2NKw5I)
[9](https://www.reddit.com/r/Python/comments/u7081n/i_developed_a_template_for_starting_new_python/)
[10](https://git.ifas.rwth-aachen.de/templates/ifas-python-template/-/blob/master/README.md)
>>>>>>> 1e0629e (first commit)
