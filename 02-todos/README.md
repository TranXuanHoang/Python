# TODOs

This project creates both a desktop and a web application from a single code base.

The desktop application's GUI is built using [FreeSimpleGUI](https://github.com/spyoungtech/FreeSimpleGUI), while [Streamlit](https://streamlit.io/) is used for the web application. The backend processing logic is written in standard Python.

## Creating Virtual Environment and Install 3rd Dependencies

To create a virtual Python environment called `.venv` and install the dependencies from a `requirements.txt` file, follow these steps:

### Step 1: Create the virtual environment

1. Open a terminal (Command Prompt, PowerShell, or any terminal on macOS/Linux).
2. Navigate to the directory where you want to create the virtual environment.

   ```bash
   cd /path/to/your/project
   ```

3. Run the following command to create a virtual environment named `.venv`:

   ```bash
   # Windows
   python -m venv .venv

   # macOS/Linux
   python3 -m venv .venv
   ```

   This will create a `.venv` folder in your project directory containing a new virtual environment.

### Step 2: Activate the virtual environment

- **On Windows**:

  ```bash
  .venv\Scripts\activate
  ```

- **On macOS/Linux**:

  ```bash
  source .venv/bin/activate
  ```

   Once activated, your terminal prompt should change to show the name of the virtual environment, like `(.venv)`.

### Step 3: Create or check the `requirements.txt` file

1. If you don't already have a `requirements.txt` file, create one in the same directory as your `.venv` folder.
2. Inside the `requirements.txt` file, add the following dependencies:

   ```txt
   FreeSimpleGUI
   streamlit
   ```

### Step 4: Install dependencies from `requirements.txt`

1. With the virtual environment still activated, run the following command to install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   This will install both `FreeSimpleGUI` and `streamlit` (and any additional dependencies specified in `requirements.txt`).

### Step 5: Verify the installation

1. To verify that the packages are installed, you can run:

   ```bash
   pip list
   ```

   This will show you a list of installed packages, including `FreeSimpleGUI` and `streamlit`.

### Step 6: Deactivate the virtual environment (when you're done)

1. When you're finished working, you can deactivate the virtual environment by running:

   ```bash
   deactivate
   ```
