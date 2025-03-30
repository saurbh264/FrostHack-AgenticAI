# **Autonomous Agents with Heurist.ai**

This is the project for **FrostHack 2025**. We’re building **autonomous AI agents** using the **Heurist Agent Framework**, and our agents need to be capable of a few core tasks, like processing natural language, generating images, and handling voice interactions, all across platforms like **Telegram**, **Discord**, or **Twitter**.

## What We’re Building

We’re creating agents that can:
- **Deploy on platforms**: Make your agent work on Telegram, Discord, or Twitter.
- **Process natural language**: Use large language models (LLMs) to understand and generate human language.
- **Generate images**: Use AI models to create high-quality images.

### The Only Rule:
You *must* use the **Heurist Agent Framework** to build everything. Other than that, it’s up to you how you choose to approach the problem. 

## Project Structure

- `agents/`: Contains the implementation of various autonomous agents.
- `bots/`: Includes bot-specific code for different platforms.
- `clients/`: Houses client-side applications and interfaces.
- `config/`: Configuration files for setting up the environment and parameters.
- `core/`: Core functionalities and utilities shared across the project.
- `interfaces/`: Defines interfaces for interaction between different modules.
- `media/`: Assets and media files used within the project.
- `video_generator/`: Module dedicated to generating videos using AI models.
- `.envexample`: Example environment configuration file.
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `README.md`: This documentation file.
- `embeddings.db`: Database file containing embeddings for various models.
- `main_app.py`: Main application script to run the project.
- `main_script.py`: Primary script executing core functionalities.
- `main_telegram.py`: Telegram-specific main script for deploying the agent.
- `requirements.txt`: Lists the dependencies required for the project.

### 📽 **Demo Video**  
Experience WanderWise in action! Watch our demo to see how it makes travel planning smarter and easier:  

[Watch the Demo Here](https://youtu.be/xinmGBPTWmU)  

## Getting Started

To set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/saurbh264/FrostHack-AgenticAI.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd FrostHack-AgenticAI
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables**:
   - Rename `.envexample` to `.env`.
   - Update the `.env` file with appropriate configuration values.
5. **Run the Application**:
   ```bash
   python main_app.py
   ```
6. **(Optional) Google Colab**
   If you're facing issue in seting up locally, you can setup it on Google Colab using:
   ```bash
      !git clone https://github.com/saurbh264/FrostHack-AgenticAI.git
      %cd FrostHack-AgenticAI/
      !pip install -r requirements.txt
      !python main_script.py
   ```


## Acknowledgments

We extend our gratitude to the organizers of FrostHack 2025 and the developers of the Heurist Agent Framework for their support and tools that made this project possible.
Repo Link Mainly Used For Integrating HeuristAI - https://github.com/heurist-network/heurist-agent-framework.git

## Contributing

We welcome contributions from the community. To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Open a pull request detailing your changes.

## HAPPY HACKING !!

---
