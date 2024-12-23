import os
import subprocess
import argparse
from datetime import datetime
import re
import zlib

def decode(data):
    return zlib.decompress(data).decode('latin-1', errors='ignore')

def unpack_objects(repo_path):
    pack_dir = os.path.join(repo_path, '.git', 'objects', 'pack')
    pack_files = [f for f in os.listdir(pack_dir) if f.endswith('.pack')]
    for pack_file in pack_files:
        pack_file_path = os.path.join(pack_dir, pack_file)
        print(f"Unpacking objects from {pack_file_path}")
        subprocess.run(['git', 'unpack-objects', '<', pack_file_path], cwd=repo_path, shell=True)

def get_commit_hashes(repo_path):
    if not os.path.isdir(repo_path):
        raise FileNotFoundError(f"Repository path not found: {repo_path}")

    unpack_objects(repo_path)

    commit_hashes = []
    objects_path = os.path.join(repo_path, '.git', 'objects')
    for root, _, files in os.walk(objects_path):
        for file in files:
            if len(file) == 38:
                commit_hash = root[-2:] + file
                commit_path = os.path.join(root, file)
                with open(commit_path, 'rb') as f:
                    commit_data = f.read()
                commit_data = decode(commit_data)
                if commit_data.startswith('commit'):
                    commit_hashes.append(commit_hash)
                    print(f"Found commit hash: {commit_hash}")

    if not commit_hashes:
        raise ValueError("No commit hashes found in the repository.")

    return commit_hashes

def get_commit_info(repo_path, commit_hash):
    commit_path = os.path.join(repo_path, '.git', 'objects', commit_hash[:2], commit_hash[2:])
    print(f"Looking for commit file: {commit_path}")
    if not os.path.isfile(commit_path):
        print(f"Commit file not found: {commit_path}")
        raise FileNotFoundError(f"Commit file not found: {commit_path}")

    with open(commit_path, 'rb') as f:
        commit_data = f.read()

    commit_data = decode(commit_data)
    print(f"Commit data: {commit_data}")  # Добавляем отладочную информацию
    
    commit_info = {}
    commit_info['hash'] = commit_hash
    
    author_match = re.search(r'author (.+?) <', commit_data)
    if author_match:
        commit_info['author'] = author_match.group(1)
    else:
        print(f"Author not found in commit data: {commit_data}")
        commit_info['author'] = 'Unknown'
    
    date_match = re.search(r'date (\d+)', commit_data)
    if date_match:
        commit_info['date'] = datetime.fromtimestamp(int(date_match.group(1)))
    else:
        print(f"Date not found in commit data: {commit_data}")
        commit_info['date'] = 'Unknown'
    
    tree_match = re.search(r'tree ([0-9a-f]{40})', commit_data)
    if tree_match:
        commit_info['tree'] = tree_match.group(1)
    else:
        print(f"Tree not found in commit data: {commit_data}")
        commit_info['tree'] = None
    
    return commit_info

def get_tree_objects(repo_path, tree_hash):
    tree_path = os.path.join(repo_path, '.git', 'objects', tree_hash[:2], tree_hash[2:])
    if not os.path.isfile(tree_path):
        print(f"Tree file not found: {tree_path}")
        raise FileNotFoundError(f"Tree file not found: {tree_path}")

    with open(tree_path, 'rb') as f:
        tree_data = f.read()

    return zlib.decompress(tree_data)

def parse_tree(tree_data):
    objects = []
    i = 0
    while i < len(tree_data):
        space_index = tree_data.find(b' ', i)
        null_index = tree_data.find(b'\x00', space_index)
        obj_hash = tree_data[null_index + 1:null_index + 21].hex()
        objects.append(obj_hash)
        i = null_index + 21
    return objects

def build_dependency_graph(repo_path, file_hash):
    commit_hashes = get_commit_hashes(repo_path)
    dependencies = []

    for commit_hash in commit_hashes:
        commit_info = get_commit_info(repo_path, commit_hash)

        if commit_info['tree']:
            tree_data = get_tree_objects(repo_path, commit_info['tree'])
            tree_objects = parse_tree(tree_data)

            if file_hash in tree_objects:
                dependencies.append(commit_info)
            else:
                print(f"File hash {file_hash} not found in tree {commit_info['tree']}")

    if not dependencies:
        raise ValueError("No dependencies found for the given file hash.")

    return dependencies

def visualize_graph(dependencies, visualizer_path):
    mermaid_graph = 'graph TD\n'
    for dep in dependencies:
        mermaid_graph += f"{dep['hash']}[\"{dep['author']} {dep['date']}\"]\n"

    with open('graph.mmd', 'w') as f:
        f.write(mermaid_graph)

    if not os.path.isfile(visualizer_path):
        raise FileNotFoundError(f"Visualizer program not found at {visualizer_path}")

    print("Generating single mermaid chart")
    subprocess.run([visualizer_path, '-i', 'graph.mmd'])

def main():
    parser = argparse.ArgumentParser(description='Visualize git commit dependencies.')
    parser.add_argument('--visualizer', type=str, help='Path to the graph visualizer program.')
    parser.add_argument('--repo', type=str, help='Path to the git repository.')
    parser.add_argument('--file_hash', type=str, help='Path to the file containing the hash value to analyze.')
    args = parser.parse_args()

    if not os.path.isfile(args.file_hash):
        raise FileNotFoundError(f"File containing hash value not found: {args.file_hash}")
    
    with open(args.file_hash, 'r') as f:
        file_hash = f.read().strip()

    print(f"File hash to analyze: {file_hash}")
    print(f"Repository path: {args.repo}")

    dependencies = build_dependency_graph(args.repo, file_hash)
    print(f"Found {len(dependencies)} dependencies")
    visualize_graph(dependencies, args.visualizer)

if __name__ == '__main__':
    main()
