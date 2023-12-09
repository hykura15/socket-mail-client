for path, contents in zip(filePaths, fileContents):
            file_name = os.path.basename(path)

            save_path = os.path.join(save_folder, file_name)
            with open(save_path, 'wb') as file:
                    content = '\r\n'.join(contents)
                    content = base64.b64decode(content)
                    file.write(content)