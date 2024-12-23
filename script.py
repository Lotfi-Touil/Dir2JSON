#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script permettant de scanner un dossier et d'en produire un JSON décrivant l'arborescence,
en utilisant SEULEMENT les règles d'exclusion (.d2jignore) et PAS de règles d'inclusion.
Le .d2jignore doit se trouver au même niveau que ce script.

Le résultat est enregistré dans un dossier "outputs" situé au même niveau que ce script.

Exemple d'utilisation :
    python script.py /chemin/vers/dossier [eventuel/chemin/output]
"""

import os
import json
import base64
import fnmatch
from datetime import datetime
from typing import Dict, List, Union

# Repère le dossier dans lequel se trouve ce script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def read_ignore_patterns() -> List[str]:
    """
    Lit un fichier .d2jignore situé au même niveau que ce script.
    Retourne la liste des patterns à ignorer.
    """
    ignore_file = os.path.join(SCRIPT_DIR, ".d2jignore")
    if not os.path.isfile(ignore_file):
        return []

    patterns = []
    with open(ignore_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                patterns.append(line)
    return patterns


def _process_file(file_path: str) -> Dict[str, Union[str, int, bool]]:
    """
    Lit le contenu d'un fichier et génère un dictionnaire
    contenant ses métadonnées et (optionnellement) son contenu.

    - Si on peut lire en UTF-8, on stocke le contenu tel quel dans 'content'.
    - Sinon, on encode en Base64 et 'is_binary' = True.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            is_binary = False
    except UnicodeDecodeError:
        with open(file_path, 'rb') as file:
            raw = file.read()
            content = base64.b64encode(raw).decode('utf-8')
            is_binary = True

    return {
        "name": os.path.basename(file_path),
        "type": "file",
        "path": file_path,
        "size": os.path.getsize(file_path),
        "is_binary": is_binary,
        "content": content
    }


def scan_directory(directory_path: str, ignore_patterns: List[str]) -> Dict[str, Union[str, List]]:
    """
    Scanne récursivement un répertoire et crée un dictionnaire décrivant
    son contenu, en ignorant tout fichier/dossier qui matche l'un des patterns
    définis dans .d2jignore.

    :param directory_path: Chemin du répertoire à scanner.
    :param ignore_patterns: Liste de patterns à ignorer.
    :return: Un dictionnaire représentant le contenu du dossier.
    """
    result = {
        "name": os.path.basename(os.path.normpath(directory_path)),
        "type": "directory",
        "path": directory_path,
        "children": []
    }

    try:
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)

            # Vérification : est-ce que le nom 'item' match un pattern à ignorer ?
            if any(fnmatch.fnmatch(item, pat) for pat in ignore_patterns):
                print(f"Ignored: {item_path}")
                continue

            if os.path.isdir(item_path):
                result["children"].append(
                    scan_directory(item_path, ignore_patterns)
                )
            elif os.path.isfile(item_path):
                result["children"].append(_process_file(item_path))

    except PermissionError as exc:
        print(f"Permission denied: {directory_path}")
        result["error"] = str(exc)
    except Exception as exc:
        print(f"Error scanning {directory_path}: {exc}")
        result["error"] = str(exc)

    return result


def scan_to_json(directory_path: str, output_dir: Union[str, None] = None) -> str:
    """
    Fonction principale : lit .d2jignore, scanne le répertoire
    et génère un fichier JSON dans un dossier "outputs" (ou un autre
    dossier spécifié en paramètre).

    :param directory_path: Chemin du répertoire à scanner.
    :param output_dir: Chemin du dossier de sortie (optionnel).
    :return: Un message indiquant où le JSON a été enregistré.
    """
    # Lecture des patterns d'ignore
    ignore_patterns = read_ignore_patterns()
    print(f"Ignore patterns: {ignore_patterns}")

    # Scan du répertoire
    result_data = scan_directory(directory_path, ignore_patterns)

    # Gère le dossier de sortie
    if output_dir is None:
        output_dir = os.path.join(SCRIPT_DIR, "outputs")
    os.makedirs(output_dir, exist_ok=True)

    # Génère un nom de fichier structuré
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    directory_name = os.path.basename(os.path.normpath(directory_path)) or "unknown"
    output_file = os.path.join(output_dir, f"{timestamp}_{directory_name}.json")

    # Écrit le JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)

    return f"Result saved to {output_file}"


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python script.py <directory_path> [output_directory]")
        sys.exit(1)

    dir_path = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result_message = scan_to_json(dir_path, out_dir)
        print(result_message)
    except Exception as e:
        print(f"Error: {e}")
