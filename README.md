# Dir2JSON

**Dir2JSON** is a lightweight Python utility that scans a directory and **exports its entire structure**—including file metadata and contents—into a **user-friendly JSON**. You can easily exclude noisy files or folders (like `node_modules`, log files, etc.) by adding them to a `.d2jignore` file. It’s perfect for creating a **portable snapshot** of any filesystem or project folder.

---

## ✨ Features

- **Recursive Directory Scan**  
  Automatically traverses subfolders to capture the complete directory tree.

- **Ignore Rules**  
  Skip unwanted items (e.g. `node_modules`, `.git`, `*.log`) via a simple `.d2jignore` file.

- **Human-Readable JSON**  
  The output is prettified (indented, UTF-8) with metadata like file size, path, and optional contents.

- **Base64 Fallback**  
  If a file is not UTF-8, it’s included as Base64—no risk of breaking JSON parsing.

- **Timestamped Filenames**  
  Outputs include a time-stamp, so you can keep multiple snapshots organized.

---

## 🏷️ Why Dir2JSON?

- **Documentation:** Provide a clear, navigable JSON overview of your repository structure.
- **Backup & Migration:** Quickly confirm or compare directory layouts across different environments.
- **Analysis & Indexing:** Feed the resulting JSON into other tools or pipelines to generate reports, do checksums, or process data.

---

## 🚀 Installation

1. Make sure you have **Python 3.6+** installed.
2. Clone (or download) this repository:
    ```bash
    ### HTTPS
    git clone https://github.com/Lotfi-Touil/Dir2JSON.git
    cd dir2json
    ```
    ```bash
    ### SSH
    git clone git@github.com:Lotfi-Touil/Dir2JSON.git
    cd dir2json
    ```
3. No extra dependencies are required—just plain Python!

---

## ⚙️ Usage

1. *(Optional)* Create a `.d2jignore` file (in the same folder as `script.py`) to list items you want to skip. For example:

    ```plaintext
    # Ignore node modules
    node_modules

    # Ignore Git
    .git

    # Ignore logs
    *.log
    *.tmp
    ```

2. Run the script:

    ```bash
    python script.py <directory_path> [output_directory]
    ```

    - `<directory_path>`: The folder to scan (required).
    - `[output_directory]`: Where to save the JSON. Defaults to an `outputs/` folder alongside the script.

3. **Example**:

    ```bash
    # Scans the "my-project" folder and writes the JSON into "./results".
    python script.py ./my-project ./results
    ```

    - If `./results` doesn’t exist, the script will create it.
    - The output JSON is named according to the timestamp and directory name (e.g. `20240101_123456_my-project.json`).

---

## 📝 Example Output

A typical JSON file might look like:

```json
{
  "name": "my-project",
  "type": "directory",
  "path": "./my-project",
  "children": [
    {
      "name": "index.js",
      "type": "file",
      "path": "./my-project/index.js",
      "size": 2345,
      "is_binary": false,
      "content": "// JavaScript content here..."
    },
    {
      "name": "docs",
      "type": "directory",
      "path": "./my-project/docs",
      "children": [
        {
          "name": "README.md",
          "type": "file",
          "path": "./my-project/docs/README.md",
          "size": 1234,
          "is_binary": false,
          "content": "# Project Documentation..."
        }
      ]
    }
  ]
}
```
**is_binary** is true if we had to store the content in Base64.  
**content** is the full file contents (or base64-encoded data) if it’s not ignored.

## 🔧 Customization

- **Skip large files:** Modify `_process_file()` in `script.py` to avoid or partially read big files.  
- **Ignore big directories:** Add them to `.d2jignore` to stop scanning them altogether (e.g. `node_modules`, `.git`, or large media folders).  
- **Exclude file contents:** If you don’t want to include file data, just remove the code that reads/encodes it. You’ll still get metadata like name, size, and path.

## 🤝 Contributing

All contributions are welcome—bug fixes, performance enhancements, or brand-new ideas!

1. Fork the repo.  
2. Create a new branch (`git checkout -b feature/awesome-improvement`).  
3. Commit your changes (`git commit -m "Add some feature"`).  
4. Push to the branch (`git push origin feature/awesome-improvement`).  
5. Create a Pull Request.

## License

This project is licensed under the MIT License.
This project is licensed under the [MIT License](LICENSE).

---

**Happy scanning!**
