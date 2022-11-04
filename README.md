# pascalgt-modified-version

Original script credit to:
https://github.com/DaikiTanak/pascalgt

# What have been modified in this script

I added this line of code in the run() function, which will search all the xml files under the hierachy/folder.

```
files = path_source_xml_dir.glob('**/*.xml')
```

I also added another feature which the script read the list of label classes from a .yaml file.

```
pascal2gt.run(
    path_target_manifest = "./221026-example-images/output.manifest", 
    path_source_xml_dir = "./221026-example-images",
    path_project_yaml_file = "./project-files/project01.yaml"
)
```
